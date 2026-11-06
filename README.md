# 🧭 CS Career Coach

A friendly rule-based career advisor (Experta expert system + Streamlit UI).

## Run locally
    pip install -r requirements.txt
    streamlit run app.py

## Deploy FREE on Streamlit Community Cloud (about 5 minutes)
1. Create a free GitHub account and a new **public** repo.
2. Upload these files to the repo root: `app.py`, `career_expert.py`, `knowledge.py`,
   `knowledge_data.py`, `requirements.txt`, and the `.streamlit/` folder.
3. Go to https://share.streamlit.io and sign in with GitHub.
4. Click **Create app** -> pick your repo -> main file: `app.py` -> **Deploy**.
5. You get a public link like `https://your-name-career-coach.streamlit.app`.

## Alternative: Hugging Face Spaces (free)
New Space -> SDK: Streamlit -> upload the same files.

## Customise
All career knowledge lives in `knowledge_data.py` (84 skills, 59 careers, job-title aliases):
- `SKILLS`: `id|Name|Category|prerequisites|portfolio project`
- `CAREERS`: `Name|Field|Track|skill:required_level:weight,...`
- `ALIASES`: alternative job titles used by the search box

Add a skill or career by adding a line. No rule changes needed.
Check your edits with:

    python knowledge.py     # validates unknown skills, bad levels, dependency cycles

## Count visitors (anonymous, no names)
The app counts anonymous sessions: a random ID per visit, never a name, IP or cookie.
View the stats by opening your app link with `?admin=1` on the end
(e.g. `https://your-app.streamlit.app/?admin=1`), then enter your password.

**Step 1: set the admin password.** In Streamlit Cloud: your app -> Settings -> Secrets, paste:

    ADMIN_PASSWORD = "choose-a-strong-password"

That is enough to start. Counts are kept in a small local file, but the free host
resets it when the app restarts or redeploys.

**Step 2 (recommended): make counts permanent with a free Google Sheet.**
1. Create a new Google Sheet. Extensions -> Apps Script -> paste `google_sheets_counter.gs`.
   Change `SECRET` to a long random word.
2. Deploy -> New deployment -> type **Web app** -> Execute as **Me**, access **Anyone** -> Deploy.
   Authorise when asked, then copy the Web app URL.
3. Add to the app's Secrets:

       TRACKER_WEBHOOK = "https://script.google.com/macros/s/XXXX/exec"
       TRACKER_KEY = "the same SECRET word"

Every visit is now a row in your sheet (you can also open it directly), and the `?admin=1`
page reads from it.

**What is counted:** visit, plan built, plan updated, plus chosen areas, dream roles and top
recommended career. **Not stored:** name, answers to skill questions, IP address.
A "visitor" is one browser session, so someone returning on another day can count twice.
