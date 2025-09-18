# 🦅 Social Eagle – Python Challenge Day 10

Day 10 Task :  

Event Registration System 🎉

> Registration form: Name, Email, Event Choice.

> Save all responses in st.session_state (or CSV).

> Show live count of total registrations.

> Allow CSV export for organizer

# Hyperlane Events — Streamlit Event Registration System

A complete Streamlit app to run events end to end: registrations, QR tickets, voice guidance, multi-currency pricing, waitlists, social sharing, live dashboards, and an admin console. Works with plain CSV files. No external database required.

> Built by **Shaid** for the Social Eagle Python Challenge (Day 10).

---

## Highlights

- Beautiful landing page with an animated background and neon theme  
- Multi-event registration (attendees can pick multiple events in one go)
- Offer logic: flash sale and early-bird with live seat counters
- Multi-currency price display (USD, INR, EUR) with symbols
- Per-attendee QR tickets (PNG) for check-in
- Automatic waitlist when an event is full
- Voice guidance using the browser SpeechSynthesis API
- YouTube “hover to play” embeds with one-tap sound enable
- Live stats dashboard with optional autorefresh
- Admin console to manage events, export registrations, and recompute seats
- CSV persistence created automatically on first run

---

## Demo Video  


https://github.com/user-attachments/assets/30669a3d-7046-423c-aaf3-a672ac91f3d0



---

## Tech Stack

- Python 3.10+
- Streamlit
- Pandas
- qrcode (Pillow)
- python-dotenv
- Vanilla JS (YouTube Iframe API + SpeechSynthesis)

---

## Project Structure

.
├─ app.py                   # Main Streamlit app (paste your code here)
├─ requirements.txt         # Dependencies
├─ .env                     # Environment variables (optional)
├─ se.png                   # Logo used in the header
├─ events.csv               # Auto-created on first run
├─ registrations.csv        # Auto-created on first run
└─ waitlist.csv             # Auto-created on first run

**requirements.txt**
```txt
streamlit>=1.36
pandas>=2.0
python-dotenv>=1.0
qrcode[pil]>=7.4
# optional (for live autorefresh widget in Live Stats tab)
streamlit-extras>=0.4.0
```

⸻

## Quick Start

- Clone and enter the project
```
git clone https://github.com/<your-username>/hyperlane-events.git
cd hyperlane-events
```

- Create a virtual environment and install deps
```
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```
- Optional: set the admin password

- Create a .env file in the project root:

- ADMIN_PASS=admin123

- If omitted, the app falls back to admin123.
- Add a logo (optional)

- Place se.png in the project root.
- If you skip this, remove or update the get_base64_image("se.png") call at the top of app.py.
-	Run
```
streamlit run app.py
```
Open the local URL that Streamlit prints.

⸻

Environment Variables

Key	Description	Default
ADMIN_PASS	Password for the Admin section	admin123


⸻

Data Files (auto-created)

All data is CSV-based and created on first run if missing.
	•	events.csv
Columns:

id, name, banner_url, start_at, end_at, capacity, price, offer_type,
offer_value, offer_start, offer_end, active


	•	registrations.csv
Columns:

ts, name, email, event_id, price_paid, offer_applied, currency


	•	waitlist.csv
Columns:

ts, name, email, event_id, notified



Datetime fields are parsed automatically. Prices are stored in the attendee’s selected currency at purchase time.

⸻

App Navigation

## Home
- Pick display currency: USD, INR, or EUR.  
- Each event shows a banner, seats left, time-to-start alerts, and any active offer.  
- YouTube embeds play on hover. The first tap enables sound for the session.  
- Share buttons for WhatsApp, X, and LinkedIn.  
- CTA buttons: “Secure my slot” or “Join waitlist”.  

---

## Register
- Form fields: name, email, and a multi-select list of active events.  
- Offer and price are calculated per event in the chosen currency.  
- Duplicate protection by email+event.  
- Adds the user to the waitlist if the event is full.  
- Optional voice guidance that speaks helpful prompts.  

---

## My Tickets
- Lookup by email.  
- Each registration renders a QR ticket that encodes event and attendee details.  

---

## Live Stats
- Total registrations and waitlist size.  
- Per-event metrics: registered, capacity, fill rate, waitlist count.  
- Progress bar and time-to-start labels.  
- Optional autorefresh every 3 seconds with `streamlit-extras`.  

---

## Admin
- Password-protected.  
- Event Management with an in-place editor:  
- Edit capacities, dates, prices, offer windows, and the active flag  
- Save writes to `events.csv`  
- Recompute seat counts from the registration log  
- Export registrations as CSV  
- View waitlist with event mapping  

---

## Pricing and Offers
- Base price is defined per event in USD in `events.csv`.  
- Display conversion uses static rates.  

CURRENCY_RATES = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.93
}


	•	Offer types:
	•	flash: active within 60 minutes before start when seats ≤ 5
	•	early: active when offer_start <= now <= offer_end

You can add more currencies in CURRENCY_RATES and CURRENCY_SYMBOLS.

⸻
## YouTube Embeds
- Uses the official YouTube Iframe API.  
- One-time sound enable sets a session flag that unmutes all embeds.  
- Hover to play. Moving the pointer out pauses playback.  
- If you see muted playback, click the overlay once.  

---

## Seating and Concurrency
- Each event has an in-memory inventory:  
- `taken_seats` is recomputed from `registrations.csv`  
- A short lock prevents rapid multi-click race conditions  
- When seats hit zero, users are added to the waitlist.  

---

## Security Notes
- Admin is password-protected through `.env` or the default value.  
- Emails are normalized to lower case for duplicate detection.  
- For real production needs consider:  
- A relational database (Postgres, SQLite)  
- Server-side sessions  
- A check-in endpoint to validate QR codes  

---

## Customization
- Theme: Edit the `<style>` block injected with `st.markdown`  
- Logos: Replace `se.png`  
- Seed events: Update `init_events_df()` or use the Admin editor  
- Offers: Extend `apply_offer()` with new promo types  
- Currencies: Update `CURRENCY_RATES` and `CURRENCY_SYMBOLS`  

---

## Troubleshooting
- Logo not found: Place `se.png` in the project root or remove the base64 loader.  
- Autorefresh missing: Install `streamlit-extras` or use the manual refresh button.  
- Muted video: Click the overlay once to allow sound.  
- CSV parsing errors: Ensure ISO-like datetime or simply re-save via the Admin editor.  
- Admin login fails: Confirm `.env` loads and `ADMIN_PASS` is set without quotes.  

---

## Roadmap
- Email notifications for registrations and waitlist promotions  
- Payment gateway integration  
- Barcode scanning and a check-in dashboard  
- Coupons and referral codes  
- Role-based admin and audit logs  

---

License

MIT. See LICENSE for details.

---


<div align="center">


🎓 Keep coding, keep learning!
Made with ❤️ by Shaid using Streamlit

⭐ Star this repo if it helped you learn something new! ⭐
