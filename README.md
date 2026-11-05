# GoldenHour AI

Emergency guidance for families during a suspected stroke or heart attack. Built for **Build The AI For YOU 2026** by team **SD CODES** (Sai Deeksha S, solo).

> Prototype for a student hackathon. **Not a medical device.** It does not diagnose and cannot rule out an emergency. In an emergency, call 108 or 112.

## The problem
Families often miss or doubt stroke and heart attack signs, delay calling, and cannot give clear details to responders. GoldenHour AI helps the family act fast: call 108, get guidance in their own language, and hand over clear information.

## What it does
- One-tap emergency mode with a Call 108 button always visible
- Describe the situation by text or voice in English, Tamil or Hindi
- An LLM extracts symptoms from the description (backend `/extract`); plain-code safety rules decide the level (emergency / not clear / no signs reported). The rules never say "safe".
- Spoken waiting steps, onset-time timer, ambulance details card (typed or pasted from the 108 operator, with tap-to-call and ETA countdown)
- One-page hospital handoff, shareable only after consent

## Status (be honest, edit before submitting)
| Feature | Status |
|---|---|
| Web page, safety rules, quick-tap, handoff | Built |
| Ambulance details card and tap-to-call | Built |
| LLM symptom extraction backend | [Built and tested / Not working: edit] |
| Hospital list | **Sample data only**, replace with verified hospitals |
| Risk model (Kaggle stroke dataset) | Not built |
| Live ambulance tracking, live hospital data | Not built (future scope) |

## Development note
A first version of the web page was prepared during the Round 1 phase. During the Round 2 sprint (1 to 5 November 2026) I added: [list what you actually did, for example: backend, LLM integration, deployment, testing, fixes].

## AI assistance and third-party tools (acknowledgement)
- **AI assistant:** Claude (Anthropic) helped draft code and text. I reviewed, tested and edited it.
- **Runtime AI:** [Groq Cloud API, free tier, model: write the exact model name you use] for symptom extraction (edit to match what you really use).
- **Hosting:** Render [and GitHub Pages].
- **Browser features:** Web Speech API, Geolocation API.
- **References:** Lancet Global Health 2021 India neurological burden study; stroke in India systematic review (https://clok.uclan.ac.uk/38139). The Kaggle stroke dataset is [not used in this version].

## Run locally
```
cd backend
pip install -r requirements.txt
set GROQ_API_KEY=your-key      (Mac/Linux: export GROQ_API_KEY=your-key)
set LLM_MODEL=exact-model-name-from-the-Groq-console
uvicorn main:app --reload
```
Open `index.html` with VS Code Live Server and set `API_URL` in it to `http://127.0.0.1:8000/extract`.

## Limits
Keyword fallback is used if the LLM is unavailable. Tamil and Hindi text needs review by native speakers. Hospital data and symptom rules have not been reviewed by clinicians.
