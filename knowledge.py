"""Loads knowledge_data.py into structures the engine and UI use, and validates them."""
import re
from knowledge_data import SKILLS as _SKILLS, CAREERS as _CAREERS, ALIASES

SKILL_META = {}   # id -> {name, category, prereqs[list], project}
PREREQS = {}      # id -> [prereq ids]
PROJECTS = {}     # id -> [project]
CAREERS = {}      # name -> {skill: (required_level, weight)}
CAREER_META = {}  # name -> {field, track}


def _rows(text):
    return [ln.strip() for ln in text.strip().splitlines() if ln.strip()]


for line in _rows(_SKILLS):
    sid, name, cat, pre, proj = line.split("|")
    if sid in SKILL_META:
        raise ValueError(f"duplicate skill id: {sid}")
    pre_list = [p for p in pre.split(",") if p]
    SKILL_META[sid] = {"name": name, "category": cat, "prereqs": pre_list, "project": proj}
    PREREQS[sid] = pre_list
    PROJECTS[sid] = [proj]

for line in _rows(_CAREERS):
    name, field, track, reqs = line.split("|")
    if name in CAREERS:
        raise ValueError(f"duplicate career: {name}")
    CAREERS[name] = {}
    for item in reqs.split(","):
        sk, lvl, w = item.split(":")
        CAREERS[name][sk] = (int(lvl), int(w))
    CAREER_META[name] = {"field": field, "track": track}


def validate():
    """Return a list of problems (empty list = knowledge base is healthy)."""
    problems = []
    for sid, pres in PREREQS.items():
        for p in pres:
            if p not in SKILL_META:
                problems.append(f"skill {sid}: unknown prerequisite '{p}'")
    for c, reqs in CAREERS.items():
        for sk, (lvl, w) in reqs.items():
            if sk not in SKILL_META:
                problems.append(f"career {c}: unknown skill '{sk}'")
            if not (1 <= lvl <= 5 and 1 <= w <= 5):
                problems.append(f"career {c}: bad level/weight for {sk}")
    for c in ALIASES:
        if c not in CAREERS:
            problems.append(f"alias target '{c}' is not a career")
    # cycle check (DFS)
    state = {}
    def visit(n, path):
        if state.get(n) == 1:
            problems.append("cycle: " + " -> ".join(path + [n])); return
        if state.get(n) == 2:
            return
        state[n] = 1
        for p in PREREQS.get(n, []):
            if p in PREREQS:
                visit(p, path + [n])
        state[n] = 2
    for s in PREREQS:
        visit(s, [])
    used = {sk for r in CAREERS.values() for sk in r}
    for s in PREREQS:
        if s not in used and not any(s in PREREQS[o] for o in PREREQS):
            problems.append(f"note: skill '{s}' is not used by any career or prerequisite")
    return problems


FIELDS = sorted({m["field"] for m in CAREER_META.values()})
FIELD_EMOJI = {
    "Software Engineering": "💻", "Data & AI": "🤖", "Infrastructure & Cloud": "☁️",
    "Security": "🔐", "Game & Graphics": "🎮", "Embedded & IoT": "🔌",
    "Quality Engineering": "🧪", "Emerging Tech": "⛓️", "Design & Product": "🎨",
}
CATEGORY_ORDER = ["Foundations", "Languages", "Web", "Mobile", "Design", "Infrastructure",
                  "Security", "Data & AI", "Game & Graphics", "Embedded & IoT", "Quality",
                  "Emerging", "Professional"]


def careers_in_fields(fields):
    return [c for c, m in CAREER_META.items() if m["field"] in fields]


def closure(skills):
    """Skills plus all their transitive prerequisites."""
    out, stack = set(), list(skills)
    while stack:
        s = stack.pop()
        if s in out:
            continue
        out.add(s)
        stack.extend(PREREQS.get(s, []))
    return out


def skills_for_careers(careers):
    needed = {sk for c in careers for sk in CAREERS[c]}
    return closure(needed)


# ---------------- job-title search (names + aliases) ----------------
def _norm(t):
    return re.sub(r"[^a-z0-9 ]+", " ", t.lower().replace("-", " ")).strip()


def find_careers(query, limit=8):
    q = _norm(query)
    if len(q) < 2:
        return []
    qtok = set(q.split())
    scores = {}
    for career in CAREERS:
        names = [_norm(career)] + [_norm(a) for a in ALIASES.get(career, [])]
        best = 0
        for n in names:
            if q == n:
                best = max(best, 100)
            elif q in n or n in q:
                best = max(best, 70 if len(q) >= 3 else 40)
            else:
                overlap = qtok & set(n.split())
                if overlap:
                    best = max(best, 20 + 15 * len(overlap))
        meta = CAREER_META[career]
        if q in _norm(meta["track"]) or q in _norm(meta["field"]):
            best = max(best, 30)
        if best:
            scores[career] = best
    return [c for c, _ in sorted(scores.items(), key=lambda t: (-t[1], t[0]))][:limit]


if __name__ == "__main__":
    probs = validate()
    print(f"{len(SKILL_META)} skills, {len(CAREERS)} careers, {len(FIELDS)} fields")
    print("\n".join(probs) if probs else "knowledge base OK")
