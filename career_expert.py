"""
CS CAREER EXPERT SYSTEM  (Experta rule engine)

Pipeline:
 USER PROFILE -> SKILL ASSESSMENT -> EXPERTA ENGINE
   -> Career Ranking | Skill Gaps | Evidence
   -> DEPENDENCIES -> PRIORITY -> ROADMAP -> PROJECTS -> PROGRESS -> REASSESS (loop)
"""
# --- Compatibility shim: Experta/frozendict need collections.Mapping (removed in 3.10)
import collections, collections.abc
for _n in ("Mapping", "MutableMapping", "Sequence", "Iterable"):
    if not hasattr(collections, _n):
        setattr(collections, _n, getattr(collections.abc, _n))

import json, sys
from experta import KnowledgeEngine, Fact, Rule, Field, MATCH, TEST, AS, W

# ======================================================================
# 1. KNOWLEDGE BASE  (lives in knowledge_data.py, parsed by knowledge.py)
# ======================================================================
from knowledge import (PREREQS, CAREERS, PROJECTS, CAREER_META, skills_for_careers)

EVIDENCE_VALUE = {"project": 1.0, "certification": 0.6, "course": 0.3, "work": 1.5}
INTEREST_BONUS = 0.10   # fit bonus when a career belongs to a field the user picked


# ======================================================================
# 2. FACT TEMPLATES (working memory)
# ======================================================================
class Profile(Fact):
    """name, hours_per_week, fields(list), target_months"""

class SkillLevel(Fact):
    """skill, level(0-5), confidence(0-1)"""

class Requirement(Fact):
    """career, skill, required, weight"""

class Gap(Fact):
    """career, skill, size, weight"""

class Match(Fact):
    """career, score"""

class Prereq(Fact):
    """skill, needs"""

class Blocked(Fact):
    """skill, by"""

class Priority(Fact):
    """skill, score, careers(list)"""

class Evidence(Fact):
    """skill, kind, ref"""

class Target(Fact):
    """career"""


# ======================================================================
# 3. THE EXPERTA ENGINE
# ======================================================================
class CareerEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.explanations = []   # audit trail: why each conclusion was reached

    def log(self, msg):
        self.explanations.append(msg)

    # ---- Load static knowledge into working memory ------------------
    def load_knowledge(self, careers, skills):
        self.careers = list(careers)
        for career in self.careers:
            for skill, (lvl, w) in CAREERS[career].items():
                self.declare(Requirement(career=career, skill=skill, required=lvl, weight=w))
        for skill in skills:
            for n in PREREQS[skill]:
                self.declare(Prereq(skill=skill, needs=n))

    # ---- RULE GROUP A: Evidence adjusts self-assessed level ---------
    # Self-ratings are untrusted. Without evidence, claimed levels > 3 are capped.
    @Rule(AS.s << SkillLevel(skill=MATCH.sk, level=MATCH.lv, confidence=MATCH.c, adjusted=False),
          TEST(lambda lv: lv > 3),
          salience=100)
    def cap_unverified_claims(self, s, sk, lv, c):
        has_ev = any(isinstance(f, Evidence) and f["skill"] == sk
                     for f in self.facts.values())
        if has_ev:
            bonus = sum(EVIDENCE_VALUE[f["kind"]] for f in self.facts.values()
                        if isinstance(f, Evidence) and f["skill"] == sk)
            new = min(lv, 3 + bonus)   # evidence unlocks levels above 3
            tag = "supported by evidence"
        else:
            new, tag = 3, "capped at 3 (no evidence)"
        self.modify(s, level=round(new, 1), adjusted=True)
        self.log(f"[evidence] {sk}: claimed {lv} -> {round(new,1)} ({tag})")

    @Rule(AS.s << SkillLevel(adjusted=False, level=MATCH.lv), TEST(lambda lv: lv <= 3), salience=99)
    def accept_low_claims(self, s):
        self.modify(s, adjusted=True)

    # ---- RULE GROUP B: Skill gaps -----------------------------------
    @Rule(Requirement(career=MATCH.car, skill=MATCH.sk, required=MATCH.req, weight=MATCH.w),
          SkillLevel(skill=MATCH.sk, level=MATCH.lv, adjusted=True),
          TEST(lambda req, lv: lv < req),
          salience=50)
    def detect_gap(self, car, sk, req, w, lv):
        self.declare(Gap(career=car, skill=sk, size=round(req - lv, 1), weight=w))

    # ---- RULE GROUP C: Dependency blocking --------------------------
    # A skill is blocked if a prerequisite is below level 2.
    @Rule(Prereq(skill=MATCH.sk, needs=MATCH.n),
          SkillLevel(skill=MATCH.n, level=MATCH.lv, adjusted=True),
          TEST(lambda lv: lv < 2),
          salience=40)
    def detect_blocked(self, sk, n):
        self.declare(Blocked(skill=sk, by=n))
        self.log(f"[dependency] {sk} is blocked by weak prerequisite {n}")

    # ---- RULE GROUP D: Hard constraints on careers ------------------
    @Rule(Profile(hours_per_week=MATCH.h, target_months=MATCH.m),
          TEST(lambda h, m: h * m * 4.3 < 150))
    def timeline_warning(self, h, m):
        self.log(f"[constraint] only ~{int(h*m*4.3)} study hours available: expect a partial roadmap")

    # ---- Aggregation (after fixed-point of rules above) -------------
    def compute_rankings(self, profile):
        levels = {f["skill"]: f["level"] for f in self.facts.values() if isinstance(f, SkillLevel)}
        ranking = []
        for career in self.careers:
            reqs = CAREERS[career]
            total_w = sum(w for _, w in reqs.values())
            got = sum(w * min(levels.get(s, 0) / req, 1.0) for s, (req, w) in reqs.items())
            score = got / total_w
            if CAREER_META[career]["field"] in profile.get("fields", []):
                score += INTEREST_BONUS
            ranking.append((career, round(min(score, 1.0), 3)))
        ranking.sort(key=lambda t: -t[1])
        for c, s in ranking:
            self.declare(Match(career=c, score=s))
        return ranking

    def compute_priorities(self, targets):
        """priority = sum(weight*gap) over target careers + unlock bonus + low-hanging-fruit bonus."""
        gaps = [f for f in self.facts.values() if isinstance(f, Gap) and f["career"] in targets]
        unlocks = {}
        for f in self.facts.values():
            if isinstance(f, Prereq):
                unlocks[f["needs"]] = unlocks.get(f["needs"], 0) + 1
        agg = {}
        for g in gaps:
            e = agg.setdefault(g["skill"], {"score": 0.0, "careers": set(), "size": 0})
            e["score"] += g["weight"] * g["size"]
            e["careers"].add(g["career"])
            e["size"] = max(e["size"], g["size"])
        blocked = {f["skill"] for f in self.facts.values() if isinstance(f, Blocked)}
        out = {}
        for sk, e in agg.items():
            s = e["score"] + 1.5 * unlocks.get(sk, 0) + (1.0 if e["size"] <= 1 else 0)
            if sk in blocked:
                s *= 0.5   # still needed, but can't be started yet
            out[sk] = {"score": round(s, 2), "careers": sorted(e["careers"]), "size": e["size"]}
        return out


# ======================================================================
# 4. ROADMAP BUILDER (dependency-aware topological ordering)
# ======================================================================
WEEKS_PER_LEVEL = 3  # weeks of focused study per level of gap at 10 h/week

def build_roadmap(priorities, levels, hours):
    needed = set(priorities)
    # pull in prerequisite chain when prerequisite is weak
    changed = True
    while changed:
        changed = False
        for sk in list(needed):
            for p in PREREQS[sk]:
                if levels.get(p, 0) < 2 and p not in needed:
                    needed.add(p)
                    priorities[p] = {"score": 0.5, "careers": ["(prerequisite)"], "size": 2 - levels.get(p, 0)}
                    changed = True
    done, order = set(), []
    while len(order) < len(needed):
        ready = [s for s in needed - done
                 if all(p in done or levels.get(p, 0) >= 2 or p not in needed for p in PREREQS[s])]
        if not ready:
            raise RuntimeError("cyclic dependency in knowledge base")
        ready.sort(key=lambda s: -priorities[s]["score"])
        pick = ready[0]
        order.append(pick); done.add(pick)
    scale = 10.0 / max(hours, 1)
    plan, week = [], 0
    for sk in order:
        dur = max(1, round(priorities[sk]["size"] * WEEKS_PER_LEVEL * scale))
        plan.append({"skill": sk, "start_week": week + 1, "end_week": week + dur,
                     "priority": priorities[sk]["score"],
                     "serves": priorities[sk]["careers"],
                     "project": PROJECTS[sk][0]})
        week += dur
    return plan


# ======================================================================
# 5. SESSION: assessment -> inference -> roadmap -> progress -> reassess
# ======================================================================
class CareerSession:
    def __init__(self, profile, assessments, evidence=None, careers=None, dream=None):
        self.profile = profile
        self.assessments = dict(assessments)   # skill -> (level, confidence)
        self.evidence = list(evidence or [])   # (skill, kind, ref)
        self.dream = [c for c in (dream or []) if c in CAREERS]
        pool = list(careers) if careers else list(CAREERS)
        self.careers = list(dict.fromkeys(pool + self.dream))   # dream roles always included
        self.skills = skills_for_careers(self.careers)
        self.history = []

    def run(self, top_n=3):
        eng = CareerEngine()
        eng.reset()
        eng.load_knowledge(self.careers, self.skills)
        eng.declare(Profile(**self.profile))
        for sk in self.skills:
            lvl, conf = self.assessments.get(sk, (0, 0.5))
            eng.declare(SkillLevel(skill=sk, level=lvl, confidence=conf, adjusted=False))
        for sk, kind, ref in self.evidence:
            if sk in self.skills:
                eng.declare(Evidence(skill=sk, kind=kind, ref=ref))
        eng.run()                                     # forward chaining to fixed point
        ranking = eng.compute_rankings(self.profile)
        # dream roles come first, the best-fitting others fill the remaining slots
        targets = list(self.dream[:top_n])
        for c, _ in ranking:
            if len(targets) >= top_n:
                break
            if c not in targets:
                targets.append(c)
        prio = eng.compute_priorities(targets)
        levels = {f["skill"]: f["level"] for f in eng.facts.values() if isinstance(f, SkillLevel)}
        roadmap = build_roadmap(prio, levels, self.profile["hours_per_week"])
        result = {"ranking": ranking, "targets": targets, "levels": levels,
                  "priorities": prio, "roadmap": roadmap, "explanations": eng.explanations}
        self.history.append(result)
        return result

    # PROGRESS: record a completed project -> becomes evidence + raises level
    def complete_project(self, skill, ref, new_level):
        self.evidence.append((skill, "project", ref))
        old = self.assessments.get(skill, (0, 0.5))[0]
        self.assessments[skill] = (max(old, new_level), 0.9)

    # REASSESS: rerun the full pipeline; the loop closes here
    def reassess(self):
        return self.run()


def report(res, title):
    print(f"\n{'='*66}\n{title}\n{'='*66}")
    print("CAREER RANKING")
    for i, (c, s) in enumerate(res["ranking"], 1):
        print(f"  {i}. {c:<24} fit {s:.0%}")
    print(f"\nTARGETS: {', '.join(res['targets'])}")
    print("\nEVIDENCE / DEPENDENCY NOTES")
    for e in res["explanations"]:
        print("  -", e)
    print("\nROADMAP")
    for r in res["roadmap"]:
        print(f"  wk {r['start_week']:>2}-{r['end_week']:<2} {r['skill']:<17} "
              f"(prio {r['priority']:>5}) -> project: {r['project']}")


if __name__ == "__main__":
    from knowledge import careers_in_fields
    profile = {"name": "Aisha", "hours_per_week": 12, "target_months": 9,
               "fields": ["Software Engineering"]}
    assessments = {"programming": (4, .8), "git": (3, .7), "data_structures": (3, .6),
                   "databases": (2, .6), "javascript": (3, .6), "html_css": (4, .7)}
    s = CareerSession(profile, assessments, [("html_css", "project", "portfolio")],
                      careers_in_fields(profile["fields"]), dream=["Frontend Engineer"])
    report(s.run(), "DEMO")
