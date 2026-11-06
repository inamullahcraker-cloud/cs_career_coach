
import os, sqlite3, tempfile, threading, uuid, json
from datetime import datetime, timezone
import streamlit as st

COLUMNS = ["ts", "session", "event", "fields", "dream", "top"]


def _secret(name):
    try:
        return st.secrets.get(name)
    except Exception:          
        return None


def _db_path():
    if os.environ.get("CAREER_DB"):
        return os.environ["CAREER_DB"]
    here = os.path.dirname(os.path.abspath(__file__))
    for base in (os.path.join(here, "data"), tempfile.gettempdir()):
        try:
            os.makedirs(base, exist_ok=True)
            if os.access(base, os.W_OK):
                return os.path.join(base, "usage.db")
        except OSError:
            continue
    return ":memory:"


def _conn():
    c = sqlite3.connect(_db_path(), timeout=5)
    c.execute("CREATE TABLE IF NOT EXISTS events (ts TEXT, session TEXT, event TEXT, "
              "fields TEXT, dream TEXT, top TEXT)")
    return c


def _post_webhook(url, row):
    try:
        import requests
        requests.post(url, data=json.dumps(dict(zip(COLUMNS, row))), timeout=5,
                      headers={"Content-Type": "text/plain"})
    except Exception:
        pass                   


def log_event(event, fields=None, dream=None, top=""):
    """Record one anonymous event. Never pass a name here."""
    ss = st.session_state
    ss.setdefault("_sid", uuid.uuid4().hex[:12])
    row = (datetime.now(timezone.utc).isoformat(timespec="seconds"), ss["_sid"], event,
           " | ".join(fields or []), " | ".join(dream or []), top or "")
    try:
        with _conn() as c:
            c.execute("INSERT INTO events VALUES (?,?,?,?,?,?)", row)
    except Exception:
        pass
    url = _secret("TRACKER_WEBHOOK")
    if url:
        threading.Thread(target=_post_webhook, args=(url, row), daemon=True).start()


def log_visit():
    """Count one visit per browser session."""
    if not st.session_state.get("_visit_logged"):
        st.session_state["_visit_logged"] = True
        log_event("visit")


def load_events():
    """Return a DataFrame of all events (from the Google Sheet if configured, else local DB)."""
    import pandas as pd
    url, key = _secret("TRACKER_WEBHOOK"), _secret("TRACKER_KEY")
    if url:
        try:
            import requests
            rows = requests.get(url, params={"key": key or ""}, timeout=10).json()
            rows = [r[:6] for r in rows if r and str(r[0]) != "ts"]
            return pd.DataFrame(rows, columns=COLUMNS)
        except Exception as e:
            st.warning(f"Couldn't reach the Google Sheet ({e}). Showing local data instead.")
    with _conn() as c:
        return pd.read_sql_query("SELECT * FROM events", c)


def _explode(df, col):
    s = df[col].astype(str).str.split(" | ", regex=False).explode().str.strip()
    return s[s.ne("") & s.ne("nan")]


def render_admin():
    """Password-protected anonymous stats page: open the app with ?admin=1"""
    import pandas as pd
    st.title("📊 Usage stats")
    st.caption("Anonymous counts only. No names or personal data are stored.")
    pw = _secret("ADMIN_PASSWORD")
    if not pw:
        st.error("No admin password set. Add `ADMIN_PASSWORD = \"your-password\"` in the app's "
                 "Secrets (see README), then reload.")
        return
    if st.text_input("Password", type="password") != pw:
        st.info("Enter the admin password to view stats.")
        return

    df = load_events()
    if df.empty:
        st.info("No visits recorded yet.")
        return
    df["day"] = pd.to_datetime(df["ts"], errors="coerce").dt.date
    visitors = df.loc[df.event == "visit", "session"].nunique()
    built = df.loc[df.event == "plan_built", "session"].nunique()
    updated = df.loc[df.event == "plan_updated", "session"].nunique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Visitors (sessions)", visitors)
    c2.metric("Plans built", built, f"{built / visitors:.0%} of visitors" if visitors else None)
    c3.metric("Came back to update", updated)

    st.markdown("**Visitors per day**")
    per_day = df[df.event == "visit"].groupby("day")["session"].nunique()
    st.line_chart(per_day)

    left, right = st.columns(2)
    with left:
        st.markdown("**Popular areas**")
        f = _explode(df[df.event == "plan_built"], "fields").value_counts()
        st.bar_chart(f) if not f.empty else st.caption("No data yet")
    with right:
        st.markdown("**Dream roles searched**")
        d = _explode(df[df.event == "plan_built"], "dream").value_counts().head(10)
        st.bar_chart(d) if not d.empty else st.caption("No data yet")

    st.markdown("**Most recommended career**")
    t = df.loc[df.event == "plan_built", "top"].value_counts().head(10)
    st.bar_chart(t) if not t.empty else st.caption("No data yet")

    st.download_button("⬇️ Download raw anonymous data (CSV)", df.drop(columns="day").to_csv(index=False),
                       "usage.csv", "text/csv")
    st.caption("A 'visitor' is one browser session, so one person visiting twice (or refreshing "
               "after a long break) can count twice. That's the trade-off of not using cookies or accounts.")
