import streamlit as st
import tracker
from career_expert import CareerSession
from knowledge import (CAREERS, CAREER_META, SKILL_META, FIELDS, FIELD_EMOJI, CATEGORY_ORDER,
                       careers_in_fields, skills_for_careers, find_careers)

st.set_page_config(page_title="CS Career Coach", page_icon="🧭", layout="centered")

LEVELS = {0: "Never tried", 1: "Beginner", 2: "Learning", 3: "Comfortable", 4: "Strong", 5: "Expert"}
EVIDENCE_OPTIONS = {"project": "Built a project", "work": "Used it at work/internship",
                    "certification": "Certification", "course": "Finished a course"}
sname = lambda s: SKILL_META[s]["name"]

# ---------- state (plain values: Streamlit drops widget state for hidden widgets) ----------
ss = st.session_state
for k, v in {"step": 1, "session": None, "result": None, "fit_history": [], "levels": {},
             "evid": {}, "fields": [], "dream": [], "name": "", "hours": 10, "months": 9}.items():
    ss.setdefault(k, v)


if "admin" in st.query_params:
    tracker.render_admin()
    st.stop()
tracker.log_visit()          


def go(step):
    ss.step = step


def candidate_careers():
    return list(dict.fromkeys(careers_in_fields(ss.fields) + ss.dream))


# ---------- header ----------
st.title("🧭 CS Career Coach")
st.caption("Tell us where you are. We'll suggest careers, find your skill gaps, and build a step-by-step plan.")
labels = ["Step 1 of 3 · About you", "Step 2 of 3 · Your skills", "Step 3 of 3 · Proof of skills", "Your plan"]
st.progress((ss.step - 1) / 3, text=labels[ss.step - 1])

# ================= STEP 1: PROFILE =================
if ss.step == 1:
    st.subheader("👋 Let's start with you")
    ss.name = st.text_input("Your name (optional)", ss.name)
    ss.hours = st.slider("Hours per week you can study", 2, 40, ss.hours)
    ss.months = st.slider("Months until you want to be job-ready", 3, 24, ss.months)

    ss.fields = st.multiselect("Which areas excite you? (pick 1–3)", FIELDS, default=ss.fields,
                               format_func=lambda f: f"{FIELD_EMOJI.get(f, '•')} {f}")

    st.markdown("**Got a specific job in mind?** (optional)")
    q = st.text_input("Type a job title, e.g. “sre”, “ux designer”, “react developer”", key="dream_q")
    options = list(dict.fromkeys(ss.dream + find_careers(q)))
    ss.dream = st.multiselect("Matching roles", options, default=ss.dream,
                              help="Pick the roles you'd love. They'll always be part of your plan.")
    if q and not options:
        st.caption("No match. Try a simpler word like 'data', 'security' or 'mobile'.")

    ok = bool(ss.fields or ss.dream)
    if len(ss.fields) > 3:
        st.warning("That's a lot of areas. Fewer areas = fewer questions and a sharper plan.")
    st.button("Next →", type="primary", on_click=go, args=(2,), disabled=not ok)
    if not ok:
        st.caption("Pick at least one area or one role to continue.")
    

# ================= STEP 2: SKILLS =================
elif ss.step == 2:
    st.subheader("🛠️ Rate your skills honestly")
    skills = skills_for_careers(candidate_careers())
    st.info(f"We only ask about the **{len(skills)} skills** relevant to your choices. "
            "Everything starts at *Never tried*. Just change the ones you know.")
    by_cat = {}
    for sk, m in SKILL_META.items():           # data order is roughly beginner -> advanced
        if sk in skills:
            by_cat.setdefault(m["category"], []).append(sk)
    first = True
    for cat in [c for c in CATEGORY_ORDER if c in by_cat]:
        # IMPORTANT: keep the expander label constant. A changing label (like a live counter)
        # makes Streamlit rebuild the expander, which collapses it after every selection.
        with st.expander(f"{cat} ({len(by_cat[cat])} skills)", expanded=first):
            first = False
            rated = sum(1 for s in by_cat[cat] if ss.levels.get(s, 0) > 0)
            st.caption(f"✅ {rated} of {len(by_cat[cat])} rated")
            for sk in by_cat[cat]:
                ss.levels[sk] = st.select_slider(sname(sk), options=list(LEVELS),
                                                 value=ss.levels.get(sk, 0), format_func=LEVELS.get)
    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go, args=(1,))
    c2.button("Next →", type="primary", on_click=go, args=(3,))

# ================= STEP 3: EVIDENCE =================
elif ss.step == 3:
    st.subheader("📎 Show your proof")
    skills = skills_for_careers(candidate_careers())
    strong = [s for s in SKILL_META if s in skills and ss.levels.get(s, 0) >= 4]
    if strong:
        st.write("For skills you rated **Strong** or higher, tell us how you've shown them. "
                 "Skills without proof are counted as *Comfortable* at most.")
        for sk in strong:
            ss.evid[sk] = st.multiselect(sname(sk), list(EVIDENCE_OPTIONS),
                                         default=ss.evid.get(sk, []), format_func=EVIDENCE_OPTIONS.get)
    else:
        st.success("You didn't rate anything as Strong, so no proof is needed. 🎉")
    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go, args=(2,))
    if c2.button("Build my plan ✨", type="primary"):
        profile = {"name": ss.name, "hours_per_week": ss.hours, "target_months": ss.months,
                   "fields": ss.fields}
        assess = {s: (ss.levels.get(s, 0), 0.7) for s in skills}
        evidence = [(s, k, "self-reported") for s in skills if ss.levels.get(s, 0) >= 4
                    for k in ss.evid.get(s, [])]
        ss.session = CareerSession(profile, assess, evidence, careers_in_fields(ss.fields), ss.dream)
        ss.result = ss.session.run()
        ss.fit_history = [dict(ss.result["ranking"])]
        tracker.log_event("plan_built", ss.fields, ss.dream, ss.result["ranking"][0][0])   # no name
        go(4)
        st.rerun()

# ================= STEP 4: RESULTS =================
else:
    res, sess = ss.result, ss.session
    st.subheader(f"🎯 Your plan{', ' + ss.name if ss.name else ''}")
    goal_weeks = round(ss.months * 4.3)
    tab1, tab2, tab3 = st.tabs(["Best-fit careers", "Roadmap & projects", "Skill snapshot"])

    # ---- careers ----
    with tab1:
        for i, (career, score) in enumerate(res["ranking"][:5]):
            meta = CAREER_META[career]
            with st.container(border=True):
                star = " ⭐ your pick" if career in sess.dream else ""
                st.markdown(f"**{career}**{star}")
                st.caption(f"{FIELD_EMOJI.get(meta['field'], '')} {meta['field']} · {meta['track']}")
                st.progress(min(score, 1.0), text=f"{score:.0%} match")
                gaps = [s for s, (req, _) in CAREERS[career].items() if res["levels"].get(s, 0) < req]
                if gaps:
                    st.caption("To improve: " + ", ".join(sname(g) for g in gaps))
                else:
                    st.caption("✅ You meet every requirement!")
        if len(res["ranking"]) > 5:
            with st.expander(f"See all {len(res['ranking'])} careers"):
                for career, score in res["ranking"][5:]:
                    st.write(f"{career}: {score:.0%}")
        if len(ss.fit_history) > 1:
            st.markdown("**Progress since your first assessment**")
            first, last = ss.fit_history[0], ss.fit_history[-1]
            cols = st.columns(len(res["targets"]))
            for col, c in zip(cols, res["targets"]):
                col.metric(c, f"{last[c]:.0%}", f"{(last[c]-first[c])*100:+.0f} pts")

    # ---- roadmap ----
    with tab2:
        road = res["roadmap"]
        if not road:
            st.balloons()
            st.success("No gaps for your top careers. Start applying! 🚀")
        else:
            targets = ", ".join(res["targets"])
            st.write(f"Built for: **{targets}**. Work top to bottom. Each step ends with a project to show employers.")
            done_now = []
            later = None
            for i, r in enumerate(road):
                fits = r["end_week"] <= goal_weeks
                if i == 6:
                    later = st.expander(f"Later steps ({len(road) - 6} more)")
                box = st if i < 6 else later
                with box.container(border=True):
                    st.markdown(f"**Weeks {r['start_week']}–{r['end_week']} · {sname(r['skill'])}** "
                                f"{'✅ in goal' if fits else '🕒 beyond goal'}")
                    st.write(f"🔨 Project: {r['project']}")
                    st.caption("Helps with: " + ", ".join(r["serves"]))
                    if st.checkbox("I finished this project", key=f"done_{r['skill']}_{len(ss.fit_history)}"):
                        done_now.append(r["skill"])
            if st.button("🔄 Update my plan", type="primary", disabled=not done_now):
                for sk in done_now:
                    cur = sess.assessments.get(sk, (0, 0.5))[0]
                    sess.complete_project(sk, "finished roadmap project", min(5, cur + 1))
                ss.result = sess.reassess()
                ss.fit_history.append(dict(ss.result["ranking"]))
                tracker.log_event("plan_updated", ss.fields, ss.dream, ss.result["ranking"][0][0])
                st.rerun()
            total = road[-1]["end_week"]
            fit_n = sum(1 for r in road if r["end_week"] <= goal_weeks)
            st.caption(f"⏱️ Full plan: ~{total} weeks at {ss.hours} hrs/week. "
                       f"Your goal ({ss.months} months ≈ {goal_weeks} weeks) covers the first {fit_n} of {len(road)} steps.")
            md = [f"# Career plan for {ss.name or 'me'}", f"Targets: {targets}", ""]
            for r in road:
                md.append(f"- Weeks {r['start_week']}-{r['end_week']}: **{sname(r['skill'])}** → {r['project']}")
            st.download_button("⬇️ Download my plan", "\n".join(md), "career_plan.md", "text/markdown")

    # ---- skills ----
    with tab3:
        for sk, lvl in sorted(res["levels"].items(), key=lambda t: -t[1]):
            if lvl > 0:
                st.progress(lvl / 5, text=f"{sname(sk)} · {LEVELS[int(round(lvl))]}")
        if not any(v > 0 for v in res["levels"].values()):
            st.caption("You're starting from zero, and that's a perfectly good place to begin. 🌱")
        in_plan = {r["skill"] for r in res["roadmap"]}
        notes = [e for e in res["explanations"] if e.startswith("[evidence]")
                 or (e.startswith("[dependency]") and any(e.startswith(f"[dependency] {s} ") for s in in_plan))]
        if notes:
            with st.expander("Why we scored things this way"):
                for n in notes:
                    st.write("•", n)

    st.divider()
    if st.button("↩ Start over"):
        for k in list(ss.keys()):
            del ss[k]
        st.rerun()
