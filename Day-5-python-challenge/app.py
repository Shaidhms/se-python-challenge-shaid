# app.py
# =============================================================================
# README (quick)
# -----------------------------------------------------------------------------
# Unit Converter 🔄 — Streamlit one-page app
#
# Features
# • Live currency conversion using a no-key public API with failover (Frankfurter → Open ER API)
# • Temperature (C/F/K), Length (m, cm, mm, km, in, ft, yd, mi), Weight (g, kg, lb, oz, tonne)
# • Instant updates on every input change (no buttons)
# • Sticky header, light/dark toggle, compact 2×2 grid layout
# • “Find Exchange Centers” hand-off: generates a copyable ChatGPT prompt with the latest rate
# • Caching (15 min), retries (2), timeouts (5s), graceful fallbacks
#
# Setup
# 1) pip install streamlit requests pytz python-dotenv pandas
# 2) Create a `.env` file in your project folder with:  OPENAI_API_KEY=sk-...
# 3) streamlit run app.py
#
# Limitations
# • No on-the-fly theme switch for Streamlit’s built-in theme; we simulate with custom CSS variables.
# • If all currency APIs fail, app falls back to last-good session snapshot (if any) or a static currency list.
# • Local time is derived from the server environment; if unknown, UTC is displayed with a note.
#
# Privacy
# • No OpenAI calls. The exchange-centers panel only prepares a prompt for you to copy into your own ChatGPT.
# =============================================================================

from __future__ import annotations
import base64
import math
import time
import json
import typing as t
from datetime import datetime, timezone, timedelta
import pandas as pd
from dataclasses import dataclass
import os
import requests
import streamlit as st
from pytz import timezone as pytz_timezone, UnknownTimeZoneError
import re
from dotenv import load_dotenv, find_dotenv
# Load .env from the project directory (and parents) without overriding real env vars
load_dotenv(find_dotenv(usecwd=True), override=False)

# =========================
# Page config and styling
# =========================
st.set_page_config(
    page_title="Unit Converter 🔄",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("se.png")

st.markdown(
    f"""
    <h2 class="main-header">
        <center>  <img src="data:image/png;base64,{logo_base64}" width="40" style="vertical-align: middle; margin-left:5px;"></center>
           <center> Social Eagle Python Challenge </center>
        <center> Day 5 - Unit Converter</center>
    </h2>
    """,
    unsafe_allow_html=True
)
# Session defaults
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "last_good_rates" not in st.session_state:
    st.session_state.last_good_rates = {}  # per-base snapshot
if "last_conversion" not in st.session_state:
    st.session_state.last_conversion = {
        "from": "USD",
        "to": "INR",
        "amount": 100.0,
        "rate": None,
        "source": None,
        "time_local": None,
    }

# 1) Put this right after st.set_page_config(...) and BEFORE any UI:

st.markdown('<div class="app-root">', unsafe_allow_html=True)
# Simulated theme toggle via CSS variables
# 2) Replace your inject_css_vars(...) function with this one:

def inject_css_vars(dark: bool) -> None:
    if dark:
        bg = "#0f1115"
        card = "#161a22"
        text = "#e6e7ea"
        subtext = "#b7beca"
        border = "#2a2f3a"
        field_bg = "#0f1115"
        field_text = "#e6e7ea"
        field_border = "#3a4150"
        menu_bg = "#11151c"
    else:
        bg = "#ffffff"
        card = "#f7f7f9"
        text = "#101828"        # very dark gray for strong contrast
        subtext = "#475569"     # slate-ish for helper text
        border = "#d0d7de"
        field_bg = "#ffffff"
        field_text = "#101828"
        field_border = "#c9d2dc"
        menu_bg = "#ffffff"

    accent = "#4f46e5"  # indigo
    chip_ok = "#16a34a"; chip_warn = "#ca8a04"; chip_err = "#dc2626"

    st.markdown(
        f"""
        <style>
        :root {{
          --bg:{bg}; --card:{card}; --text:{text}; --subtext:{subtext}; --border:{border};
          --accent:{accent}; --chip-ok:{chip_ok}; --chip-warn:{chip_warn}; --chip-err:{chip_err};
          --field-bg:{field_bg}; --field-text:{field_text}; --field-border:{field_border};
          --menu-bg:{menu_bg};
        }}

        .stApp, .app-root {{ background: var(--bg); color: var(--text); }}

        /* Headings, paragraphs, captions */
        .app-root h1, .app-root h2, .app-root h3, .app-root h4, .app-root h5, .app-root h6,
        .app-root p, .app-root span, .app-root li, .app-root label, .app-root .stMarkdown,
        .app-root .stCaption, .app-root .stText, .app-root .stHeader {{
            color: var(--text);
        }}
        .muted {{ color: var(--subtext) !important; }}

        /* Cards and layout */
        .header-wrap {{
            position: sticky; top: 0; z-index: 999; background: var(--bg);
            border-bottom: 1px solid var(--border); padding: .5rem .75rem .75rem .75rem;
            margin-bottom: .75rem;
        }}
        .title-row {{ display:flex; align-items:center; justify-content:space-between; gap:.5rem; }}
        .title-row h1 {{ font-size:1.1rem; margin:0; color:var(--text); }}
        # .card {{
        #     background: var(--card); border:1px solid var(--border); border-radius:12px;
        #     padding:.9rem; box-shadow:0 1px 2px rgba(0,0,0,.05);
        # }}
        .result-number {{ font-size:1.2rem; font-weight:600; margin-top:.25rem; word-break:break-word; }}

        /* Status chips */
        .chip {{ display:inline-flex; align-items:center; gap:.4rem; padding:.15rem .5rem;
                 font-size:.75rem; border-radius:999px; border:1px solid var(--border);
                 background:rgba(255,255,255,0.02); position:relative; }}
        .chip.ok {{
            position: relative;
            color: var(--chip-ok);
            border-color: var(--chip-ok);
            background: rgba(22, 163, 74, 0.1);
        }}
        .chip.ok::before {{
            content: '';
            position: absolute;
            left: 8px;
            top: 50%;
            transform: translateY(-50%);
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--chip-ok);
            box-shadow: 0 0 0 0 rgba(22,163,74, 0.6);
            animation: pulse-green 1.5s infinite;
        }}
        @keyframes pulse-green {{
            0% {{ transform: translateY(-50%) scale(0.9); box-shadow: 0 0 0 0 rgba(22,163,74,0.7); }}
            70% {{ transform: translateY(-50%) scale(1.2); box-shadow: 0 0 0 6px rgba(22,163,74,0); }}
            100% {{ transform: translateY(-50%) scale(0.9); box-shadow: 0 0 0 0 rgba(22,163,74,0); }}
        }}
        .chip.warn {{ color:var(--chip-warn); border-color:var(--chip-warn); }}
        .chip.err {{ color:var(--chip-err); border-color:var(--chip-err); }}

        .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.75rem; }}
        @media (max-width: 900px) {{ .grid {{ grid-template-columns:1fr; }} }}

        /* --- Form controls: make selects/inputs match the theme --- */
        /* Text/number inputs */
        .stTextInput input, .stNumberInput input, .stTextArea textarea,
        .stDateInput input, .stTimeInput input {{
            background: var(--field-bg) !important;
            color: var(--field-text) !important;
            border: 1px solid var(--field-border) !important;
            box-shadow: none !important;
        }}
        /* BaseWeb Select used by Streamlit */
        div[data-baseweb="select"] > div {{
            background: var(--field-bg) !important;
            color: var(--field-text) !important;
            border: 1px solid var(--field-border) !important;
            box-shadow: none !important;
        }}
        div[data-baseweb="popover"] {{ background: var(--menu-bg) !important; color: var(--field-text) !important; }}
        div[data-baseweb="menu"]    {{ background: var(--menu-bg) !important; color: var(--field-text) !important; }}
        /* Make labels readable */
        label, .stMarkdown small, .stMarkdown span {{
            color: var(--text) !important;
        }}

        /* Accent button helper */
        .accent-btn button {{ background: var(--accent) !important; border-color: var(--accent) !important; color: #fff !important; }}

        /* --- Improve heading/label contrast & reset unwanted opacity --- */
        .app-root h1, .app-root h2, .app-root h3, .app-root h4, .app-root h5, .app-root h6,
        .card h1, .card h2, .card h3, .card h4, .card h5, .card h6,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4,
        [data-testid="stMarkdownContainer"] h5,
        [data-testid="stMarkdownContainer"] h6 {{
            color: var(--text) !important;
            opacity: 1 !important;
        }}
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stWidgetLabel"],
        .stMarkdown, .stText, .stHeader, label {{
            color: var(--text) !important;
            opacity: 1 !important;
        }}
        .stCaption, .caption, .stMarkdown small {{
            color: var(--subtext) !important;
            opacity: 1 !important;
        }}
        /* Placeholder text readable on light/dark */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder,
        .stNumberInput input::placeholder {{
            color: rgba(127,137,152,0.9) !important;
        }}
        /* Hint card for fun facts */
        .fun-card {{
            margin-top: .5rem;
            margin-bottom: .25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: .75rem .9rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--card);
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        .fun-card .fun-text {{
            text-align: center;
            font-size: 1.05rem; /* slightly bigger than body */
            line-height: 1.35;
            color: var(--text);
        }}
        /* Better wrapping for ChatGPT markdown output */
        [data-testid="stMarkdownContainer"] {{ overflow-wrap: anywhere; word-break: break-word; }}
        [data-testid="stMarkdownContainer"] table {{ display:block; width:100%; overflow-x:auto; border-collapse: collapse; }}
        [data-testid="stMarkdownContainer"] th, [data-testid="stMarkdownContainer"] td {{ white-space: normal; }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# =========================
# Utilities
# =========================

def try_get_local_tz() -> t.Optional[str]:
    """Best-effort guess for a reasonable local timezone string."""
    # Streamlit Cloud often uses UTC, local dev uses host TZ. Leaving configurable in future.
    # As a safe default, return None to display UTC explicitly.
    return None

def fmt_dt_local(utc_dt: datetime) -> tuple[str, str]:
    """Return (local_str, tz_label) for display."""
    tz_name = try_get_local_tz()
    if tz_name:
        try:
            tz = pytz_timezone(tz_name)
            local = utc_dt.astimezone(tz)
            return (local.strftime("%Y-%m-%d %H:%M:%S %Z"), tz_name)
        except UnknownTimeZoneError:
            pass
    # Fallback: display UTC and label
    return (utc_dt.strftime("%Y-%m-%d %H:%M:%S UTC"), "UTC")

def clamp_non_negative(x: float) -> float:
    return max(0.0, x)

def fmt_num(x: float, digits: int = 6) -> str:
    # Adaptive precision: show up to digits, keep readability
    if x == 0:
        return "0"
    mag = abs(x)
    if mag >= 1e9 or mag < 1e-4:
        return f"{x:.6e}"
    if mag >= 1e6:
        return f"{x:,.0f}"
    if mag >= 1e3:
        return f"{x:,.2f}"
    return f"{x:,.6f}".rstrip("0").rstrip(".")

# =========================
# Currency data layer
# =========================

@dataclass
class RateBlob:
    base: str
    rates: dict[str, float]
    source: str
    fetched_at_utc: datetime

PRIMARY_SOURCE = "Frankfurter (ECB)"
FALLBACK_SOURCE = "Open ER API"

def _fetch_frankfurter(base: str, timeout: int = 5) -> RateBlob:
    # API: https://api.frankfurter.app/latest?from=USD
    url = f"https://api.frankfurter.app/latest?from={base.upper()}"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    # data: { "amount":1.0,"base":"USD","date":"YYYY-MM-DD","rates":{...}}
    base_ccy = (data.get("base") or base).upper()
    rates = {k.upper(): float(v) for k, v in (data.get("rates") or {}).items()}
    if base_ccy not in rates:
        rates[base_ccy] = 1.0
    fetched_at = datetime.now(timezone.utc)
    return RateBlob(base=base_ccy, rates=rates, source=PRIMARY_SOURCE, fetched_at_utc=fetched_at)

def _fetch_open_erapi(base: str, timeout: int = 5) -> RateBlob:
    # API: https://open.er-api.com/v6/latest/USD
    url = f"https://open.er-api.com/v6/latest/{base.upper()}"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    if data.get("result") != "success":
        raise RuntimeError("Open ER API result not success")
    base_ccy = (data.get("base_code") or base).upper()
    rates = {k.upper(): float(v) for k, v in (data.get("rates") or {}).items()}
    if base_ccy not in rates:
        rates[base_ccy] = 1.0
    fetched_at = datetime.now(timezone.utc)
    return RateBlob(base=base_ccy, rates=rates, source=FALLBACK_SOURCE, fetched_at_utc=fetched_at)

@st.cache_data(ttl=15 * 60, show_spinner=False)
def get_rates_cached(base: str, source_pref: str) -> RateBlob:
    """
    Cached fetcher with simple retries and optional source forcing.
    source_pref: "Auto", PRIMARY_SOURCE, FALLBACK_SOURCE
    """
    attempts = []
    def try_once(fn: t.Callable[[], RateBlob]) -> RateBlob:
        last_exc = None
        for _ in range(2):  # retries
            try:
                return fn()
            except Exception as e:  # noqa: BLE001
                last_exc = e
                time.sleep(0.5)
        raise last_exc  # type: ignore[misc]

    base_up = base.upper()

    if source_pref == "Auto":
        # Primary → Fallback
        try:
            return try_once(lambda: _fetch_frankfurter(base_up))
        except Exception as e1:  # noqa: BLE001
            attempts.append(str(e1))
            return try_once(lambda: _fetch_open_erapi(base_up))
    elif source_pref == PRIMARY_SOURCE:
        return try_once(lambda: _fetch_frankfurter(base_up))
    elif source_pref == FALLBACK_SOURCE:
        return try_once(lambda: _fetch_open_erapi(base_up))
    else:
        # Unknown option, default to Auto
        try:
            return try_once(lambda: _fetch_frankfurter(base_up))
        except Exception:
            return try_once(lambda: _fetch_open_erapi(base_up))

def safe_get_rates(base: str, source_pref: str) -> tuple[RateBlob | None, str]:
    """
    Wrapper to provide graceful fallback to last-good session snapshot.
    Returns (rate_blob_or_none, status: "live" | "cached" | "stale" | "error")
    """
    try:
        rb = get_rates_cached(base, source_pref)
        # Snapshot into session as last-good
        st.session_state.last_good_rates[rb.base] = rb
        return rb, "live"
    except Exception:
        # Fallback to session snapshot if exists
        snap = st.session_state.last_good_rates.get(base.upper())
        if snap:
            # If snapshot older than 15m consider stale, else cached
            age_sec = (datetime.now(timezone.utc) - snap.fetched_at_utc).total_seconds()
            status = "stale" if age_sec > 15 * 60 else "cached"
            return snap, status
        return None, "error"


def compute_cross_rate(rb: RateBlob, from_ccy: str, to_ccy: str) -> float:
    """Return units of to_ccy per 1 unit of from_ccy."""
    f = from_ccy.upper()
    t = to_ccy.upper()
    if f == t:
        return 1.0
    # Rates are expressed relative to rb.base
    # cross rate r(f→t) = r(base→t) / r(base→f)
    r_to = rb.rates.get(t)
    r_from = rb.rates.get(f)
    if r_to is None or r_from is None or r_from == 0:
        raise ValueError("Missing or zero rate for requested currency")
    return r_to / r_from


# =========================
# 5-year timeseries fetcher (cached)
# =========================
@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def get_pair_timeseries_cached(from_ccy: str, to_ccy: str) -> tuple[pd.DataFrame, str]:
    """Fetch ~5 years of daily (business-day) FX for the selected pair.
    Primary: Frankfurter range API, Fallback: exchangerate.host timeseries.
    Returns (DataFrame with columns ['date','rate'], source_label).
    """
    start = (datetime.now(timezone.utc) - timedelta(days=365 * 5 + 5)).date().isoformat()
    end = datetime.now(timezone.utc).date().isoformat()
    f_from = from_ccy.upper()
    f_to = to_ccy.upper()

    # --- Try Frankfurter timeseries ---
    try:
        url = f"https://api.frankfurter.app/{start}..{end}?from={f_from}&to={f_to}"
        r = requests.get(url, timeout=7)
        r.raise_for_status()
        data = r.json()
        rates = data.get("rates") or {}
        rows = []
        for d, obj in sorted(rates.items()):
            val = obj.get(f_to)
            if val is not None:
                rows.append((d, float(val)))
        if rows:
            df = pd.DataFrame(rows, columns=["date", "rate"])  
            return df, "Frankfurter (ECB)"
    except Exception:
        pass

    # --- Fallback: exchangerate.host timeseries ---
    try:
        url = (
            "https://api.exchangerate.host/timeseries"
            f"?start_date={start}&end_date={end}&base={f_from}&symbols={f_to}"
        )
        r = requests.get(url, timeout=7)
        r.raise_for_status()
        data = r.json()
        if not data.get("success", True):
            raise RuntimeError("exchangerate.host returned failure")
        rates = data.get("rates") or {}
        rows = []
        for d, obj in sorted(rates.items()):
            inner = obj or {}
            val = inner.get(f_to)
            if val is not None:
                rows.append((d, float(val)))
        if rows:
            df = pd.DataFrame(rows, columns=["date", "rate"])  
            return df, "exchangerate.host"
    except Exception:
        pass

    # Final fallback: empty frame
    return pd.DataFrame({"date": [], "rate": []}), "(no data)"

# Static currency list fallback
STATIC_CURRENCIES = [
    "USD","EUR","GBP","INR","JPY","AUD","CAD","CHF","CNY","SGD","HKD","NZD","SEK",
    "NOK","DKK","ZAR","AED","SAR","THB","KRW","IDR","MYR","PHP","VND","BRL","MXN",
]

# =========================
# Converters (pure funcs)
# =========================

def convert_temperature(value: float, from_u: str, to_u: str) -> float:
    f = from_u.upper()
    t = to_u.upper()
    if f == t:
        return value

    # Normalize to Kelvin
    if f == "°C" or f == "C":
        k = value + 273.15
    elif f == "°F" or f == "F":
        k = (value - 32) * 5.0 / 9.0 + 273.15
    elif f == "K":
        k = value
    else:
        raise ValueError("Unsupported temperature unit")

    # Kelvin to target
    if t == "°C" or t == "C":
        return k - 273.15
    elif t == "°F" or t == "F":
        return (k - 273.15) * 9.0 / 5.0 + 32
    elif t == "K":
        return k
    else:
        raise ValueError("Unsupported temperature unit")

LENGTH_FACTORS_TO_M = {
    "m": 1.0,
    "cm": 0.01,
    "mm": 0.001,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

def convert_length(value: float, from_u: str, to_u: str) -> float:
    if from_u == to_u:
        return value
    fm = LENGTH_FACTORS_TO_M.get(from_u)
    tm = LENGTH_FACTORS_TO_M.get(to_u)
    if fm is None or tm is None:
        raise ValueError("Unsupported length unit")
    meters = value * fm
    return meters / tm

WEIGHT_FACTORS_TO_G = {
    "g": 1.0,
    "kg": 1000.0,
    "lb": 453.59237,
    "oz": 28.349523125,
    "tonne": 1_000_000.0,
}

def convert_weight(value: float, from_u: str, to_u: str) -> float:
    if from_u == to_u:
        return value
    fg = WEIGHT_FACTORS_TO_G.get(from_u)
    tg = WEIGHT_FACTORS_TO_G.get(to_u)
    if fg is None or tg is None:
        raise ValueError("Unsupported weight unit")
    grams = value * fg
    return grams / tg

# =========================
# Fun facts helpers
# =========================

def _fmt_small(text: str) -> str:
    # Return raw text; we’ll style via a centered card instead of a muted inline span
    return f"💡 {text}"


def _to_html_bold(md: str) -> str:
    """Very small Markdown→HTML: only **bold** → <strong>. Keeps other chars as-is."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", md)


def render_hint_card(text: str) -> None:
    """Render the fun fact inside a centered card with slightly larger text."""
    if not text:
        return
    html = f"<div class='fun-card'><div class='fun-text'>{_to_html_bold(text)}</div></div>"
    st.markdown(html, unsafe_allow_html=True)


# =========================
# OpenAI (optional): execute the exchange-centers prompt
# =========================

def _get_openai_api_key() -> str | None:
    """Read API key from env (populated by .env) or Streamlit secrets.
    Priority: real environment > .env > st.secrets."""
    # Environment (could be populated by .env via load_dotenv)
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    # Fallback: Streamlit secrets
    try:
        sec = st.secrets.get("OPENAI_API_KEY")  # type: ignore[attr-defined]
        if sec:
            return str(sec)
    except Exception:
        pass
    return None


def call_openai_chat_markdown(prompt: str, model: str = "gpt-4o-mini") -> tuple[str | None, str | None]:
    """Call OpenAI Chat Completions API and return (markdown, error).
    Uses `requests` and the key from .env/env/secrets.
    """
    api_key = _get_openai_api_key()
    if not api_key:
        return None, "OpenAI API key not found. Add OPENAI_API_KEY to your .env or environment."
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a travel money concierge AI. Be accurate, local, and up-to-date. When uncertain, clearly say so and provide next-step instructions."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "response_format": {"type": "text"},
    }
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code != 200:
            return None, f"OpenAI API error {resp.status_code}: {resp.text[:300]}"
        data = resp.json()
        md = data.get("choices", [{}])[0].get("message", {}).get("content")
        if not md:
            return None, "Empty response from model."
        return md, None
    except Exception as e:  # noqa: BLE001
        return None, f"Request failed: {e}"


def fun_fact_temperature(value_in: float, from_u: str, to_u: str, out_value: float) -> str:
    """Return a short, fun temperature fact based on the converted value.
    We normalize comparisons to Celsius for easier ranges."""
    try:
        c = convert_temperature(out_value, to_u, "°C")
    except Exception:
        return ""
    tips = []
    if c <= -50:
        tips.append("That’s colder than **Antarctic winter** averages 🧊.")
    elif c <= -10:
        tips.append("Colder than a **home freezer** (~-18°C).")
    elif -10 < c < 5:
        tips.append("Close to a **chilly winter day**.")
    elif 5 <= c < 18:
        tips.append("Typical **spring/fall weather** range.")
    elif 18 <= c < 27:
        tips.append("Around **room temperature** (20–25°C).")
    elif 27 <= c < 40:
        tips.append("That’s a **hot day** in many cities ☀️.")
    elif 40 <= c < 60:
        tips.append("Approaching **desert heat** levels.")
    elif 60 <= c < 100:
        tips.append("Hotter than the **hottest recorded air temps** on Earth.")
    elif 100 <= c < 160:
        tips.append("Above **water’s boiling point** (at sea level).")
    elif c >= 500:
        tips.append("You’re in **pizza‑oven** territory 🍕.")

    # Anchors
    anchors = []
    if abs(c - 0) < 0.5:
        anchors.append("Very close to **water’s freezing point** (0°C).")
    if abs(c - 37) < 0.5:
        anchors.append("That’s about **human body temperature** (~37°C).")
    if abs(c - 100) < 0.5:
        anchors.append("Right near **boiling point of water** (100°C).")

    line = " ".join(tips[:1] + anchors[:1])
    return f"💡 {line}" if line else ""


def fun_fact_length(out_value: float, out_unit: str) -> str:
    """Return a short, fun length fact. Compare in meters for consistency."""
    fm = LENGTH_FACTORS_TO_M.get(out_unit)
    if not fm:
        return ""
    meters = out_value * fm
    # References
    marathon_m = 42195
    football_field_m = 91.44  # soccer ~105m, but we’ll use gridiron/similar field length
    eiffel_m = 324

    if meters >= marathon_m:
        n = meters / marathon_m
        return f"💡 That’s about **{n:.2f}×** a **marathon** distance."
    if meters >= eiffel_m:
        n = meters / eiffel_m
        return f"💡 Roughly **{n:.2f}×** the height of the **Eiffel Tower** (324 m)."
    if meters >= football_field_m:
        n = meters / football_field_m
        return f"💡 Around **{n:.2f}** **football fields** long (~91.44 m each)."
    if meters >= 1:
        return "💡 Just over a **meter**—about one big step."
    if 0 < meters < 0.01:
        return "💡 That’s **millimeter‑scale**—think **paper thickness**."
    return ""


def fun_fact_weight(out_value: float, out_unit: str) -> str:
    """Return a short, fun weight fact. Compare in grams for consistency."""
    fg = WEIGHT_FACTORS_TO_G.get(out_unit)
    if not fg:
        return ""
    grams = out_value * fg
    apple_g = 182.0     # average medium apple
    laptop_g = 1500.0   # light laptop
    bowling_g = 6800.0  # ~15 lb

    if grams >= bowling_g:
        n = grams / bowling_g
        return f"💡 About **{n:.2f}×** a **bowling ball** (~6.8 kg). 🎳"
    if grams >= laptop_g:
        n = grams / laptop_g
        return f"💡 Roughly **{n:.2f}×** a **light laptop** (~1.5 kg). 💻"
    if grams >= apple_g:
        n = grams / apple_g
        return f"💡 Close to **{n:.2f}×** a **medium apple** (~182 g). 🍎"
    if grams > 0 and grams < 10:
        return "💡 That’s **feather‑light**—a few paperclips."
    return ""

# =========================
# Header
# =========================
with st.container():
    st.markdown('<div class="header-wrap">', unsafe_allow_html=True)
    colA, colB = st.columns([0.7, 0.2])
    with colA:
        st.markdown('<div class="title-row"><h1>🔄 Unit Converter - with AI powered currency exchange finder</h1></div>', unsafe_allow_html=True)
        st.caption("Minimal, fast, and accurate. Live currency rates, temperature, length, and weight.")
    with colB:
        st.toggle("Dark mode", key="dark_mode", help="Toggle page colors")
    st.markdown('</div>', unsafe_allow_html=True)
inject_css_vars(st.session_state.dark_mode)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("### About")
    st.write(
        "This app performs instant conversions and fetches live mid-market FX rates "
        "from public, no-key APIs."
    )
    st.divider()
    st.markdown("### Data sources")
    st.markdown(
        "- Primary: **Frankfurter (ECB)**\n"
        "- Fallback: **Open ER API**"
    )
    # Will populate timestamp below after fetching

# =========================
# Main layout: Tabs (one converter per tab)
# =========================

currency_tab, temp_tab, length_tab, weight_tab = st.tabs([
    "💱 Currency", "🌡️ Temperature", "📏 Length", "⚖️ Weight"
])


#patch

def _swap_currencies():
    f = st.session_state.get("ccy_from")
    t = st.session_state.get("ccy_to")
    if f and t:
        st.session_state["ccy_from"] = t
        st.session_state["ccy_to"] = f
# ---------- Currency Tab ----------
with currency_tab:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
       # st.markdown("#### 💱 Currency", help="Rates are mid-market. Cash rates at counters may include spread/fees.")
        top_c1, top_c2, top_c3 = st.columns([0.42, 0.28, 0.30])
        with top_c1:
            source_pref = st.selectbox(
                "Source",
                ["Auto", PRIMARY_SOURCE, FALLBACK_SOURCE],
                help="Choose the API or let Auto fail over to the fallback if the primary is unavailable.",
                index=0,
                key="currency_source_pref",
            )
        with top_c2:
            st.write("")
        with top_c3:
            st.write("")



        # --- Choose From / ⇄ / To / Amount
        cols = st.columns([0.34, 0.06, 0.34, 0.26])  # From | Swap | To | Amount

        default_from = st.session_state.last_conversion["from"]
        default_to = st.session_state.last_conversion["to"]

        _tmp_rb, _status = safe_get_rates(default_from, source_pref)
        if _tmp_rb:
            ccy_list = sorted(list(_tmp_rb.rates.keys()))
        else:
            ccy_list = STATIC_CURRENCIES

        with cols[0]:
            current_from = st.session_state.get("ccy_from", st.session_state.last_conversion["from"])
            if current_from not in ccy_list:
                current_from = ccy_list[0]
            from_ccy = st.selectbox("From", ccy_list, index=ccy_list.index(current_from), key="ccy_from")
        # with cols[0]:
        #     from_ccy = st.selectbox(
        #         "From",
        #         ccy_list,
        #         index=max(ccy_list.index(default_from) if default_from in ccy_list else 0, 0),
        #         key="ccy_from"
        #     )
        with cols[1]:
            st.write("")  # vertical align
            st.button(
        "⇄",
        key="swap_ccy",
        help="Swap From and To",
        use_container_width=True,
        on_click=_swap_currencies,   # ✅ do the swap in a callback
    )
        # with cols[1]:
        #     st.write("")  # vertical align
        #     if st.button("⇄", key="swap_ccy", help="Swap From and To", use_container_width=True):
        #         f = st.session_state.get("ccy_from", from_ccy)
        #         t = st.session_state.get("ccy_to", default_to)
        #         st.session_state.ccy_from, st.session_state.ccy_to = t, f
        #         st.rerun()

        with cols[2]:
            current_to = st.session_state.get("ccy_to", st.session_state.last_conversion["to"])
            if current_to not in ccy_list:
        # gentle fallback preference for INR if available
                current_to = "INR" if "INR" in ccy_list else ccy_list[0]
            to_ccy = st.selectbox("To", ccy_list, index=ccy_list.index(current_to), key="ccy_to")
        # with cols[2]:
        #     to_ccy = st.selectbox(
        #         "To",
        #         ccy_list,
        #         index=max(
        #             ccy_list.index(default_to) if default_to in ccy_list
        #             else (ccy_list.index("INR") if "INR" in ccy_list else 0),
        #             0
        #         ),
        #         key="ccy_to"
        #     )

        with cols[3]:
            amount = st.number_input(
                "Amount",
                min_value=0.0,
                value=float(st.session_state.last_conversion["amount"]),
                step=1.0,
                format="%.4f",
                key="ccy_amount"
            )

        # Fetch latest for selected base
        rb, status = safe_get_rates(from_ccy, source_pref)
        status_map = {
            "live": ("● live", "ok"),
            "cached": ("● cached", "warn"),
            "stale": ("● stale", "warn"),
            "error": ("● error", "err"),
        }
        label, cls = status_map[status]

        chip_col, stat_col = st.columns([0.5, 0.5])
        with chip_col:
            st.markdown(f'<span class="chip {cls}">{label} &nbsp; mid-market</span>', unsafe_allow_html=True)
        with stat_col:
            if rb:
                local_str, tz_label = fmt_dt_local(rb.fetched_at_utc)
                st.markdown(f'<div class="muted" style="text-align:right;">{rb.source} @ <span class="mono">{local_str}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="muted" style="text-align:right;">No live data</div>', unsafe_allow_html=True)

        conv_text = "Unavailable"
        rate_text = ""
        if rb:
            try:
                rate = compute_cross_rate(rb, from_ccy, to_ccy)
                converted = amount * rate
                conv_text = f"{fmt_num(amount)} {from_ccy} = **{fmt_num(converted)} {to_ccy}**"
                rate_text = f"1 {from_ccy} = {fmt_num(rate)} {to_ccy}"
                st.session_state.last_conversion.update({
                    "from": from_ccy, "to": to_ccy, "amount": amount,
                    "rate": rate, "source": rb.source, "time_local": fmt_dt_local(rb.fetched_at_utc)[0]
                })
            except Exception as e:  # noqa: BLE001
                conv_text = f"Error: {e}"

        st.markdown("**Result**", help="Conversion uses latest available mid-market rate.")
        st.markdown(f"<div class='result-number'>{conv_text}</div>", unsafe_allow_html=True)
        if rate_text:
            st.caption(rate_text)

        # --- 5-year FX history chart ---
        with st.expander("📈 5-year history (mid-market)", expanded=False):
            df_hist, src_hist = get_pair_timeseries_cached(from_ccy, to_ccy)
            if not df_hist.empty:
                df_plot = df_hist.copy()
                df_plot["date"] = pd.to_datetime(df_plot["date"])
                df_plot = df_plot.set_index("date").sort_index()
                st.line_chart(df_plot["rate"], height=220)
                st.caption(f"Source: {src_hist}. Range: last ~5 years (business days)")
            else:
                st.info("No historical data available right now. Try different currencies or later.")

        st.markdown('</div>', unsafe_allow_html=True)  # end currency card

    # --- Find Exchange Centers (within Currency tab) ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🧭 Locate Best Exchange Centers")
        st.caption("Powered by ChatGPT. It uses the latest mid-market rate shown above.")

        # Row 1: City | PIN
        ec1_fx, ec2_fx = st.columns([0.5, 0.5])
        with ec1_fx:
            city_fx = st.text_input("City", placeholder="e.g., Chennai", key="ec_city_fxcenters")
        with ec2_fx:
            pin_fx = st.text_input("PIN / Postal code", placeholder="e.g., 600001", key="ec_pin_fxcenters")

        # small gap
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        # Row 2 (same line): Execute | Model
        act1_fx, act2_fx = st.columns([0.56, 0.44])
        with act1_fx:
            run_it_fx = st.button("▶ Find Location", type="primary", use_container_width=True, key="exec_exchange_fxcenters")
        with act2_fx:
            model_fx = st.selectbox(
                "Model",
                ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
                index=0,
                key="model_select_fxcenters",
                help="Reads your OPENAI_API_KEY from environment/.env if available."
            )

        # Build the prompt using the latest conversion snapshot
        lc = st.session_state.last_conversion
        has_rate = lc.get("rate") is not None
        if not has_rate:
            st.info("Run a currency conversion to embed a fresh rate in the prompt.")

        amount_str = fmt_num(float(lc["amount"])) if lc.get("amount") is not None else "100"
        converted_amt = ""
        if has_rate:
            try:
                converted_amt = fmt_num(float(lc["amount"]) * float(lc["rate"]))
            except Exception:
                converted_amt = ""

        prompt = f"""**Title:** Find cash currency exchange centers near {city_fx or '{city}'}, {pin_fx or '{pin}'} with best live rates
**System:** You are a travel money concierge. Be accurate, local, and up-to-date.
**User:** Given the live mid-market rate {amount_str} {lc.get('from','USD')} → {lc.get('to','INR')} = {converted_amt or '{converted_amount}'} ({lc.get('source','source')} @ {lc.get('time_local','time')}), find **cash** currency exchange centers near **{city_fx or '{city}'}, {pin_fx or '{pin}'}**. Return a table with: Center name, Address, Distance, Phone, Hours, Today’s quoted **cash** rate for {lc.get('from','USD')}→{lc.get('to','INR')}, Fees/commission, Notes, Source link, and the **effective rate after fees**. Prefer recent sources (last 48h). Then summarize the top 3 by effective rate and highlight any ID requirements or limits. If quotes unavailable, call ahead instructions and typical spreads for this area.
**Assistant:** : STRICT INSTRUCTION : DONT ADD ANY FOLLOWUP QUESTIONS.
"""

        # Collapsible Generated Prompt
        with st.expander("📋 Generated Prompt (click to expand)", expanded=False):
            st.code(prompt, language="markdown")

        # Execute (optional; requires OPENAI_API_KEY)
        if run_it_fx:
            with st.spinner("Contacting ChatGPT…"):
                md, err = call_openai_chat_markdown(prompt, model=model_fx)
            if err:
                st.error(err)
            else:
                st.markdown("### Results")
                st.markdown(md)

        st.markdown('</div>', unsafe_allow_html=True)
# ---------- Temperature Tab ----------
with temp_tab:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
       # st.markdown("#### 🌡️ Temperature", help="Formulas: C↔F: F = C×9/5 + 32, K = C + 273.15")
        c1, c2, c3 = st.columns([0.34, 0.34, 0.32])
        with c1:
            t_from = st.selectbox("From", ["°C","°F","K"], index=0, key="t_from")
        with c2:
            t_to = st.selectbox("To", ["°C","°F","K"], index=1, key="t_to")
        with c3:
            t_val = st.number_input("Value", value=25.0, format="%.4f", key="t_val")
        try:
            t_out = convert_temperature(t_val, t_from, t_to)
            st.markdown(f"**Result**")
            st.markdown(f"<div class='result-number'>{fmt_num(t_val)} {t_from} = **{fmt_num(t_out)} {t_to}**</div>", unsafe_allow_html=True)
            ff = fun_fact_temperature(t_val, t_from, t_to, t_out)
            render_hint_card(ff)
        except Exception as e:  # noqa: BLE001
            st.error(str(e))
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Length Tab ----------
with length_tab:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
       # st.markdown("#### 📏 Length", help="All conversions via meters as the base unit.")
        c1, c2, c3 = st.columns([0.34, 0.34, 0.32])
        with c1:
            l_from = st.selectbox("From", list(LENGTH_FACTORS_TO_M.keys()), index=0, key="l_from")
        with c2:
            l_to = st.selectbox("To", list(LENGTH_FACTORS_TO_M.keys()), index=3, key="l_to")
        with c3:
            l_val_raw = st.number_input("Value", value=1.0, min_value=0.0, format="%.6f", key="l_val")
        l_val = clamp_non_negative(l_val_raw)
        if l_val_raw < 0:
            st.caption("Negative length clamped to 0.")
        try:
            l_out = convert_length(l_val, l_from, l_to)
            st.markdown("**Result**")
            st.markdown(f"<div class='result-number'>{fmt_num(l_val)} {l_from} = **{fmt_num(l_out)} {l_to}**</div>", unsafe_allow_html=True)
            ff = fun_fact_length(l_out, l_to)
            render_hint_card(ff)
        except Exception as e:  # noqa: BLE001
            st.error(str(e))
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Weight Tab ----------
with weight_tab:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        #st.markdown("#### ⚖️ Weight", help="All conversions via grams as the base unit.")
        c1, c2, c3 = st.columns([0.34, 0.34, 0.32])
        with c1:
            w_from = st.selectbox("From", list(WEIGHT_FACTORS_TO_G.keys()), index=1, key="w_from")
        with c2:
            w_to = st.selectbox("To", list(WEIGHT_FACTORS_TO_G.keys()), index=2, key="w_to")
        with c3:
            w_val_raw = st.number_input("Value", value=1.0, min_value=0.0, format="%.6f", key="w_val")
        w_val = clamp_non_negative(w_val_raw)
        if w_val_raw < 0:
            st.caption("Negative weight clamped to 0.")
        try:
            w_out = convert_weight(w_val, w_from, w_to)
            st.markdown("**Result**")
            st.markdown(f"<div class='result-number'>{fmt_num(w_val)} {w_from} = **{fmt_num(w_out)} {w_to}**</div>", unsafe_allow_html=True)
            ff = fun_fact_weight(w_out, w_to)
            render_hint_card(ff)
        except Exception as e:  # noqa: BLE001
            st.error(str(e))
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Finalize Sidebar timestamp
# =========================
with st.sidebar:
    st.divider()
    lc = st.session_state.last_conversion
    if lc.get("source") and lc.get("time_local"):
        st.markdown("**Last FX rate**")
        st.write(f"{lc['source']} @ {lc['time_local']}")
    else:
        st.write("No rate fetched yet.")

# =========================
# Self-checks (unit tests)
# =========================
def _almost(a: float, b: float, eps: float = 1e-6) -> bool:
    return abs(a - b) <= eps

def _run_self_tests() -> dict[str, bool]:
    ok = {}

    # Temperature
    ok["temp_C_to_F"] = _almost(convert_temperature(0, "°C", "°F"), 32.0)
    ok["temp_F_to_C"] = _almost(convert_temperature(212, "°F", "°C"), 100.0)
    ok["temp_C_to_K"] = _almost(convert_temperature(100, "°C", "K"), 373.15)

    # Length
    ok["len_m_to_ft"] = _almost(convert_length(1, "m", "ft"), 3.280839895013123)
    ok["len_mi_to_km"] = _almost(convert_length(1, "mi", "km"), 1.609344)

    # Weight
    ok["wt_kg_to_lb"] = _almost(convert_weight(1, "kg", "lb"), 2.2046226218487757)
    ok["wt_lb_to_oz"] = _almost(convert_weight(1, "lb", "oz"), 16.0)

    return ok
# 4) Add this once at the VERY end of the file to close the wrapper:
st.markdown('</div>', unsafe_allow_html=True)


# Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    results = _run_self_tests()
    print(json.dumps(results, indent=2))


# =============================================================================
# Testing Checklist
# - [ ] Currency fetch works; fallback path tested.
# - [ ] Cache TTL respected; timestamp shown.
# - [ ] Each unit converter matches known test pairs.
# - [ ] Copy-prompt includes latest rate and location.
# - [ ] Layout fits on a common 13–15″ laptop without scroll.
# =============================================================================