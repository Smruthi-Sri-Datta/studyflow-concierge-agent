import streamlit as st
import requests
import json
import os
import time
import uuid
import html
from datetime import date, time as dt_time

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyFlow",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Syne:wght@300;400;500;600&display=swap');

html, body {
    font-family: 'Syne', sans-serif !important;
    background: #060810 !important;
    color: #e2ddd6 !important;
}
p, span, div, li, a, label { font-family: 'Syne', sans-serif; }

/* display:none so hidden elements don't consume layout space */
#MainMenu, footer, header { display: none !important; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1000px !important; }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% 0%, rgba(255,180,50,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(255,100,80,0.04) 0%, transparent 60%),
        #060810;
}
[data-testid="stSidebar"] {
    background: #0b0e1a !important;
    border-right: 1px solid rgba(255,180,50,0.12) !important;
}
[data-testid="stSidebar"] .block-container { padding: 2.5rem 1.5rem !important; }

/* Logo & Tagline */
.sf-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem; font-weight: 900;
    background: linear-gradient(135deg, #ffb432 0%, #ff6b35 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    letter-spacing: -1px; line-height: 1; margin-bottom: 0.3rem;
}
.sf-tagline {
    font-size: 0.65rem; letter-spacing: 3px;
    color: rgba(255,180,50,0.4); text-transform: uppercase; margin-bottom: 2.5rem;
}

/* Status Pill */
.status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 0.3rem 0.9rem; border-radius: 100px;
    font-size: 0.75rem; font-weight: 500;
    width: 100%; justify-content: center;
}
.status-online  { background: rgba(80,220,120,0.12); border: 1px solid rgba(80,220,120,0.3); color: #50dc78; }
.status-offline { background: rgba(255,80,80,0.10);  border: 1px solid rgba(255,80,80,0.25); color: #ff6060; }

/* Sidebar Nav - inactive */
div[data-testid="stSidebar"] .stButton button {
    width: 100%; text-align: left !important;
    background: transparent !important; border: 1px solid transparent !important;
    color: rgba(226,221,214,0.45) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
    padding: 0.65rem 1rem !important; border-radius: 10px !important;
    margin-bottom: 0.3rem !important; transition: all 0.2s ease !important;
    letter-spacing: 0.3px !important;
}
div[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,180,50,0.07) !important;
    border-color: rgba(255,180,50,0.2) !important;
    color: #ffb432 !important; transform: translateX(3px) !important;
}

/* Sidebar Nav - active (HTML div, not a button) */
.nav-btn-active {
    width: 100%; text-align: left;
    background: rgba(255,180,50,0.1);
    border: 1px solid rgba(255,180,50,0.3);
    border-left: 3px solid #ffb432;
    color: #ffb432;
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem; font-weight: 600;
    padding: 0.65rem 1rem; border-radius: 10px;
    margin-bottom: 0.3rem; letter-spacing: 0.3px;
    display: block; box-sizing: border-box;
}

/* User Badge */
.user-badge {
    margin-top: 2rem; padding: 0.8rem 1rem;
    background: rgba(255,180,50,0.05);
    border: 1px solid rgba(255,180,50,0.1);
    border-radius: 10px; font-size: 0.75rem;
    color: rgba(226,221,214,0.4);
}
.user-badge span { color: #ffb432; font-weight: 600; }

/* Page Header */
.page-header {
    margin-bottom: 2.5rem; padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    animation: fadeSlideIn 0.5s ease both;
}
.page-header h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important; font-weight: 900 !important;
    color: #f0ebe3 !important; margin: 0 0 0.4rem !important;
    letter-spacing: -1.5px !important; line-height: 1.1 !important;
}
.page-header p { color: rgba(226,221,214,0.4); font-size: 0.9rem; margin: 0; font-weight: 300; }

/* Welcome Hero */
.welcome-hero { text-align: center; padding: 5rem 2rem 3rem; animation: fadeSlideIn 0.7s ease both; }
.welcome-hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 4rem; font-weight: 900;
    background: linear-gradient(135deg, #f0ebe3 0%, #ffb432 60%, #ff6b35 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -2px; margin-bottom: 1rem;
}
.welcome-hero p { color: rgba(226,221,214,0.45); font-size: 1rem; font-weight: 300; letter-spacing: 0.5px; }

/* Feature Cards */
.feature-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 1.5rem; margin-bottom: 0.6rem;
    transition: all 0.3s ease; animation: fadeSlideIn 0.6s ease both;
}
.feature-card:hover {
    background: rgba(255,180,50,0.04);
    border-color: rgba(255,180,50,0.15); transform: translateY(-2px);
}
.feature-card .icon {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase;
    color: rgba(255,180,50,0.55); margin-bottom: 0.8rem; display: block;
}
.feature-card h3 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #f0ebe3; margin: 0 0 0.4rem; }
.feature-card p { font-size: 0.8rem; color: rgba(226,221,214,0.4); margin: 0 0 0.6rem; line-height: 1.6; }

/* Form container — override Streamlit's default white box */
[data-testid="stForm"] {
    background: rgba(15, 18, 32, 0.5) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
}

/* All text inputs — solid dark background so text is visible */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stTimeInput input {
    background: #0d1220 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2ddd6 !important;
    font-family: 'Syne', sans-serif !important;
    transition: border-color 0.2s ease !important;
    caret-color: #ffb432 !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: rgba(255,180,50,0.5) !important;
    box-shadow: 0 0 0 3px rgba(255,180,50,0.08) !important;
    outline: none !important;
}

/* Placeholder text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: rgba(226,221,214,0.28) !important; }

/* Number input wrapper (contains the +/- buttons) */
div[data-testid="stNumberInput"] > div {
    background: #0d1220 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}
div[data-testid="stNumberInput"] > div > input {
    border: none !important; box-shadow: none !important;
}
div[data-testid="stNumberInput"] button {
    background: transparent !important;
    color: rgba(255,180,50,0.7) !important;
    border: none !important;
}
div[data-testid="stNumberInput"] button:hover { color: #ffb432 !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #0d1220 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #e2ddd6 !important;
}
.stSelectbox svg { fill: rgba(255,180,50,0.6) !important; }

/* Date & time input wrappers */
div[data-testid="stDateInput"] > div,
div[data-testid="stTimeInput"] > div {
    background: #0d1220 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* Form field labels */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stNumberInput label, .stDateInput label, .stSlider label, .stTimeInput label {
    color: rgba(226,221,214,0.55) !important; font-size: 0.78rem !important;
    font-weight: 500 !important; letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}

/* Non-primary sidebar/utility buttons (+ Task, - Task, etc.) */
div[data-testid="stSidebar"] ~ div .stButton button:not([kind="primary"]),
.stButton button:not([kind="primary"]) {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: rgba(226,221,214,0.65) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.82rem !important;
    transition: all 0.2s ease !important;
}
.stButton button:not([kind="primary"]):hover {
    background: rgba(255,180,50,0.08) !important;
    border-color: rgba(255,180,50,0.25) !important;
    color: #ffb432 !important;
}

/* Primary Button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #ffb432 0%, #ff6b35 100%) !important;
    color: #060810 !important; border: none !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.85rem !important; letter-spacing: 0.5px !important;
    border-radius: 10px !important; padding: 0.65rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(255,180,50,0.2) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(255,180,50,0.35) !important;
}

/* Section Label */
.section-label {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 2px;
    color: rgba(255,180,50,0.5); margin: 1.8rem 0 1rem;
    display: flex; align-items: center; gap: 10px;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.05); }

/* AI Response Box */
.ai-response {
    background: rgba(255,180,50,0.04);
    border: 1px solid rgba(255,180,50,0.15);
    border-radius: 16px; padding: 1.8rem 2rem;
    margin-top: 1.5rem; position: relative;
    animation: fadeSlideIn 0.4s ease both;
}
.ai-response::before {
    content: 'AI'; position: absolute; top: 1rem; right: 1.2rem;
    font-size: 0.65rem; letter-spacing: 2px;
    color: rgba(255,180,50,0.4); font-weight: 600;
}
.ai-response p { color: #cfc9bf; line-height: 1.8; font-size: 0.92rem; margin: 0; white-space: pre-wrap; }

/* Metrics Row - responsive: 4-col wide, 2-col on narrow screens */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 1rem; margin-bottom: 2rem;
}
.metric-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 1.4rem 1rem; text-align: center;
    transition: all 0.3s ease; animation: fadeSlideIn 0.5s ease both;
}
.metric-card:hover { border-color: rgba(255,180,50,0.2); background: rgba(255,180,50,0.03); }
.metric-card .val {
    font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 700;
    background: linear-gradient(135deg, #ffb432, #ff6b35);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1; margin-bottom: 0.4rem;
}
.metric-card .lbl { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(226,221,214,0.35); }

/* Task Row */
.task-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.9rem 1.2rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px; margin-bottom: 0.5rem; transition: all 0.2s ease;
}
.task-row:hover { border-color: rgba(255,180,50,0.15); background: rgba(255,180,50,0.03); }
.task-title { font-size: 0.88rem; color: #e2ddd6; }
.task-sub { font-size: 0.75rem; color: rgba(226,221,214,0.35); margin-top: 2px; }
.priority-high { color: #ff6b35; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
.priority-low  { color: #50dc78; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }

/* Banners */
.info-banner {
    background: rgba(255,180,50,0.06); border: 1px solid rgba(255,180,50,0.15);
    border-radius: 12px; padding: 1rem 1.4rem; margin-bottom: 2rem;
    font-size: 0.85rem; color: rgba(255,180,50,0.8);
    display: flex; align-items: center; gap: 10px;
    animation: fadeSlideIn 0.4s ease both;
}
.info-banner-top { margin-top: 2rem; }
.warn-banner {
    background: rgba(255,80,80,0.06); border: 1px solid rgba(255,80,80,0.2);
    border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 2rem;
    font-size: 0.88rem; color: rgba(255,130,130,0.9);
    display: flex; align-items: center; gap: 10px;
    animation: fadeSlideIn 0.4s ease both;
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.stSuccess { background: rgba(80,220,120,0.08) !important; border-color: rgba(80,220,120,0.2) !important; border-radius: 10px !important; }
.stError   { background: rgba(255,80,80,0.08) !important;  border-color: rgba(255,80,80,0.2) !important;  border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "page"              not in st.session_state: st.session_state.page              = "home"
if "user_id"           not in st.session_state: st.session_state.user_id           = "demo_user"
if "base_url"          not in st.session_state: st.session_state.base_url          = os.environ.get("STUDYFLOW_API_URL", "")
if "health_status"     not in st.session_state: st.session_state.health_status     = None
if "health_checked_at" not in st.session_state: st.session_state.health_checked_at = 0.0
if "status_result"     not in st.session_state: st.session_state.status_result     = None
if "status_err"        not in st.session_state: st.session_state.status_err        = None
if "task_count"        not in st.session_state: st.session_state.task_count        = 3
if "plan_session_id"   not in st.session_state: st.session_state.plan_session_id   = str(uuid.uuid4())[:8]

HEALTH_TTL = 10  # seconds before cached health result expires

# ─── Helpers ─────────────────────────────────────────────────────────────────
def api_post(endpoint: str, payload: dict):
    try:
        r = requests.post(
            st.session_state.base_url.rstrip("/") + endpoint,
            json=payload, timeout=30,
        )
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the backend. Is uvicorn running?"
    except requests.exceptions.Timeout:
        return None, "Request timed out (>30 s)."
    except requests.exceptions.HTTPError as e:
        return None, f"Server error {e.response.status_code}: {e.response.text[:200]}"
    except Exception as e:
        return None, str(e)


def api_get(endpoint: str, params=None):
    try:
        r = requests.get(
            st.session_state.base_url.rstrip("/") + endpoint,
            params=params, timeout=30,
        )
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the backend."
    except requests.exceptions.Timeout:
        return None, "Request timed out (>30 s)."
    except requests.exceptions.HTTPError as e:
        return None, f"Server error {e.response.status_code}: {e.response.text[:200]}"
    except Exception as e:
        return None, str(e)


def health_check(force: bool = False) -> bool:
    """Return True if backend is reachable; result cached for HEALTH_TTL seconds."""
    now = time.monotonic()
    if not force and (now - st.session_state.health_checked_at) < HEALTH_TTL:
        return bool(st.session_state.health_status)
    try:
        r = requests.get(st.session_state.base_url.rstrip("/") + "/", timeout=4)
        result = r.status_code == 200
    except Exception:
        result = False
    st.session_state.health_status = result
    st.session_state.health_checked_at = now
    return result


def h(value: object) -> str:
    """HTML-escape a value before injecting into markup (prevents XSS)."""
    return html.escape(str(value))


def no_backend_banner() -> None:
    st.markdown(
        '<div class="warn-banner">No backend connected — enter your backend URL in the sidebar to use this feature.</div>',
        unsafe_allow_html=True,
    )


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sf-logo">StudyFlow</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-tagline">Concierge Agent</div>', unsafe_allow_html=True)

    url = st.text_input(
        "Backend URL",
        value=st.session_state.base_url,
        placeholder="http://127.0.0.1:8000",
    )
    if url != st.session_state.base_url:
        st.session_state.base_url = url
        st.session_state.health_checked_at = 0.0  # invalidate cached result

    if st.session_state.base_url:
        pill_col, refresh_col = st.columns([5, 1])
        with pill_col:
            ok = health_check()
            if ok:
                st.markdown('<div class="status-pill status-online">Connected</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-pill status-offline">Unreachable</div>', unsafe_allow_html=True)
        with refresh_col:
            if st.button("R", key="health_refresh", help="Re-check connection"):
                health_check(force=True)
                st.rerun()

    st.markdown("---")

    nav = {
        "home":    "Home",
        "setup":   "Setup Profile",
        "plan":    "Plan My Day",
        "reflect": "Reflect",
        "status":  "Status",
    }

    for key, label in nav.items():
        if key == st.session_state.page:
            # Active page: styled HTML div avoids fighting st.button CSS for active state
            st.markdown(f'<div class="nav-btn-active">{label}</div>', unsafe_allow_html=True)
        else:
            if st.button(label, key=f"nav_{key}"):
                st.session_state.page = key
                st.rerun()

    st.markdown(
        f'<div class="user-badge">Signed in as <span>{h(st.session_state.user_id)}</span></div>',
        unsafe_allow_html=True,
    )

# ─── HOME ─────────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    st.markdown("""
    <div class="welcome-hero">
        <h1>StudyFlow</h1>
        <p>Your AI-powered study planning concierge. Smarter sessions, better results.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="icon">Setup</span>
            <h3>Setup Profile</h3>
            <p>Add your courses and tasks once. StudyFlow remembers everything.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Setup", key="home_nav_setup"):
            st.session_state.page = "setup"
            st.rerun()

        st.markdown("""
        <div class="feature-card">
            <span class="icon">Reflect</span>
            <h3>Reflect</h3>
            <p>Log how your session went. The agent adapts and improves over time.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Reflect", key="home_nav_reflect"):
            st.session_state.page = "reflect"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="icon">Plan</span>
            <h3>Plan My Day</h3>
            <p>Get a personalized AI study plan based on your deadlines and energy.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Plan", key="home_nav_plan"):
            st.session_state.page = "plan"
            st.rerun()

        st.markdown("""
        <div class="feature-card">
            <span class="icon">Status</span>
            <h3>Status</h3>
            <p>Track streaks, completed tasks, and session ratings at a glance.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Status", key="home_nav_status"):
            st.session_state.page = "status"
            st.rerun()

    if not st.session_state.base_url:
        st.markdown(
            '<div class="info-banner info-banner-top">Enter your backend URL in the sidebar to connect</div>',
            unsafe_allow_html=True,
        )

# ─── SETUP ────────────────────────────────────────────────────────────────────
elif st.session_state.page == "setup":
    st.markdown("""
    <div class="page-header">
        <h1>Setup Profile</h1>
        <p>Configure your courses, tasks, and study preferences.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.base_url:
        no_backend_banner()
    else:
        # Task count controls live outside the form so they trigger immediate reruns
        st.markdown('<div class="section-label">Tasks</div>', unsafe_allow_html=True)
        tc_col1, tc_col2, tc_info = st.columns([1, 1, 5])
        with tc_col1:
            if st.button("+ Task", key="add_task"):
                st.session_state.task_count = min(st.session_state.task_count + 1, 15)
                st.rerun()
        with tc_col2:
            if st.button("- Task", key="remove_task"):
                st.session_state.task_count = max(st.session_state.task_count - 1, 1)
                st.rerun()
        with tc_info:
            st.caption(f"{st.session_state.task_count} task row(s) — max 15")

        with st.form("setup_form"):
            col1, col2 = st.columns(2)
            with col1:
                name    = st.text_input("Your Name", placeholder="e.g. Datta")
                user_id = st.text_input("User ID", value=st.session_state.user_id)
            with col2:
                block_mins = st.number_input("Study Block (minutes)", min_value=15, max_value=120, value=45, step=15)
                max_blocks = st.number_input("Max Blocks Per Day", min_value=1, max_value=10, value=4)

            st.markdown('<div class="section-label">Courses</div>', unsafe_allow_html=True)
            courses_raw = st.text_area(
                "Courses (one per line)",
                placeholder="Machine Learning\nDeep Learning\nNLP",
                height=90,
            )

            st.markdown('<div class="section-label">Task Details</div>', unsafe_allow_html=True)
            hc0, hc1, hc2, hc3, hc4 = st.columns([0.4, 2.5, 2, 2, 1.2])
            hc0.markdown("**#**"); hc1.markdown("**Task**"); hc2.markdown("**Course ID**")
            hc3.markdown("**Deadline**"); hc4.markdown("**Status**")

            tasks = []
            for i in range(st.session_state.task_count):
                cc0, cc1, cc2, cc3, cc4 = st.columns([0.4, 2.5, 2, 2, 1.2])
                cc0.markdown(
                    f"<span style='color:rgba(255,180,50,0.4);font-size:0.8rem'>{i + 1}</span>",
                    unsafe_allow_html=True,
                )
                title    = cc1.text_input("t", key=f"tt{i}", label_visibility="collapsed", placeholder=f"Task {i + 1}")
                course   = cc2.text_input("c", key=f"tc{i}", label_visibility="collapsed", placeholder="course_id")
                deadline = cc3.date_input("d", key=f"td{i}", label_visibility="collapsed", value=date.today())
                status   = cc4.selectbox("s", ["pending", "done", "partial"], key=f"ts{i}", label_visibility="collapsed")
                if title:
                    tasks.append({
                        "task_id":       f"task_{i + 1}",
                        "course_id":     course or "general",
                        "title":         title,
                        "deadline_date": str(deadline),
                        "status":        status,
                    })

            submitted = st.form_submit_button("Save & Continue", type="primary")

        if submitted:
            if not tasks:
                st.error("Add at least one task.")
            else:
                st.session_state.user_id = user_id
                # Invalidate cached status when user profile changes
                st.session_state.status_result = None
                st.session_state.status_err    = None

                courses = [
                    {"course_id": line.lower().replace(" ", "_"), "name": line}
                    for line in [c.strip() for c in courses_raw.strip().split("\n") if c.strip()]
                ]
                payload = {
                    "user_id": user_id,
                    "courses": courses,
                    "tasks":   tasks,
                    "profile": {
                        "name":                    name,
                        "preferred_block_minutes": block_mins,
                        "max_blocks_per_day":      max_blocks,
                    },
                }
                with st.spinner("Saving..."):
                    result, err = api_post("/setup_user", payload)
                if err:
                    st.error(err)
                else:
                    st.success("Profile saved! Head to Plan My Day.")
                    with st.expander("API Response"):
                        st.json(result)

# ─── PLAN ─────────────────────────────────────────────────────────────────────
elif st.session_state.page == "plan":
    st.markdown("""
    <div class="page-header">
        <h1>Plan My Day</h1>
        <p>Tell the agent your availability and get a smart study schedule.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.base_url:
        no_backend_banner()
    else:
        with st.form("plan_form"):
            col1, col2 = st.columns(2)
            with col1:
                plan_date  = st.date_input("Study Date", value=date.today())
                session_id = st.text_input(
                    "Session ID",
                    value=st.session_state.plan_session_id,
                    help="Auto-generated — edit to track a specific session.",
                )
            with col2:
                st.markdown("**Available Time Windows**")
                w1a, w1b = st.columns(2)
                with w1a:
                    start1 = st.time_input("Window 1 Start", value=dt_time(9, 0))
                with w1b:
                    end1   = st.time_input("Window 1 End",   value=dt_time(12, 0))

                w2a, w2b = st.columns(2)
                with w2a:
                    start2 = st.time_input("Window 2 Start (optional)", value=None)
                with w2b:
                    end2   = st.time_input("Window 2 End (optional)",   value=None)

            submitted = st.form_submit_button("Generate My Plan", type="primary")

        if submitted:
            windows = [{"start": start1.strftime("%H:%M"), "end": end1.strftime("%H:%M")}]
            if start2 and end2:
                windows.append({"start": start2.strftime("%H:%M"), "end": end2.strftime("%H:%M")})

            payload = {
                "user_id":            st.session_state.user_id,
                "date":               str(plan_date),
                "available_windows":  windows,
                "session_id":         session_id or None,
            }
            # Rotate session ID ready for next plan
            st.session_state.plan_session_id = str(uuid.uuid4())[:8]

            with st.spinner("Generating your plan..."):
                result, err = api_post("/plan_day", payload)
            if err:
                st.error(err)
            else:
                plan_text = (
                    result.get("plan") or result.get("message") or json.dumps(result, indent=2)
                ) if isinstance(result, dict) else str(result)
                # h() escapes API-returned text so it cannot inject HTML/JS into the page
                st.markdown(
                    f'<div class="ai-response"><p>{h(plan_text)}</p></div>',
                    unsafe_allow_html=True,
                )

# ─── REFLECT ──────────────────────────────────────────────────────────────────
elif st.session_state.page == "reflect":
    st.markdown("""
    <div class="page-header">
        <h1>Reflect</h1>
        <p>Log your session and let the agent learn from your progress.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.base_url:
        no_backend_banner()
    else:
        with st.form("reflect_form"):
            col1, col2 = st.columns(2)
            with col1:
                reflect_date  = st.date_input("Session Date", value=date.today())
                difficulty    = st.slider("Difficulty Rating (1-5)", 1, 5, 3)
                completed_raw = st.text_area("Completed Task IDs (one per line)", placeholder="task_1\ntask_3", height=100)
            with col2:
                partial_raw = st.text_area("Partial Task IDs", placeholder="task_2", height=80)
                notes       = st.text_area("Notes", placeholder="What went well? What was hard?", height=100)
            submitted = st.form_submit_button("Submit Reflection", type="primary")

        if submitted:
            completed = [t.strip() for t in completed_raw.strip().split("\n") if t.strip()]
            partial   = [t.strip() for t in partial_raw.strip().split("\n") if t.strip()]
            payload = {
                "user_id":            st.session_state.user_id,
                "completed_task_ids": completed,
                "partial_task_ids":   partial,
                "difficulty_rating":  difficulty,
                "notes":              notes or "",
                "date":               str(reflect_date),
            }
            with st.spinner("Processing..."):
                result, err = api_post("/reflect", payload)
            if err:
                st.error(err)
            else:
                feedback = (
                    result.get("feedback") or result.get("message") or json.dumps(result, indent=2)
                ) if isinstance(result, dict) else str(result)
                st.markdown(
                    f'<div class="ai-response"><p>{h(feedback)}</p></div>',
                    unsafe_allow_html=True,
                )

# ─── STATUS ───────────────────────────────────────────────────────────────────
elif st.session_state.page == "status":
    st.markdown("""
    <div class="page-header">
        <h1>Status</h1>
        <p>Your study progress at a glance.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.base_url:
        no_backend_banner()
    else:
        refresh_col, _ = st.columns([2, 5])
        with refresh_col:
            if st.button("Refresh", key="status_refresh", type="primary"):
                with st.spinner("Fetching..."):
                    result, err = api_get("/status", params={"user_id": st.session_state.user_id})
                st.session_state.status_result = result
                st.session_state.status_err    = err

        # Auto-fetch once on first visit; cached thereafter until Refresh is clicked
        if st.session_state.status_result is None and st.session_state.status_err is None:
            with st.spinner("Fetching..."):
                result, err = api_get("/status", params={"user_id": st.session_state.user_id})
            st.session_state.status_result = result
            st.session_state.status_err    = err

        err    = st.session_state.status_err
        result = st.session_state.status_result

        if err:
            st.error(err)
        elif isinstance(result, dict):
            done   = h(result.get("tasks_completed", result.get("completed",      "—")))
            total  = h(result.get("tasks_total",     result.get("total_tasks",    "—")))
            streak = h(result.get("streak_days",     result.get("streak",         "—")))
            rating = h(result.get("avg_rating",      result.get("average_rating", "—")))

            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-card"><div class="val">{done}</div><div class="lbl">Completed</div></div>
                <div class="metric-card"><div class="val">{total}</div><div class="lbl">Total Tasks</div></div>
                <div class="metric-card"><div class="val">{streak}</div><div class="lbl">Day Streak</div></div>
                <div class="metric-card"><div class="val">{rating}</div><div class="lbl">Avg Rating</div></div>
            </div>
            """, unsafe_allow_html=True)

            pending = result.get("pending_tasks", result.get("tasks", []))
            if pending and isinstance(pending, list):
                st.markdown('<div class="section-label">Pending Tasks</div>', unsafe_allow_html=True)
                for task in pending:
                    if isinstance(task, dict):
                        title    = h(task.get("title",         "Untitled"))
                        subject  = h(task.get("course_id",     task.get("subject",   "")))
                        deadline = h(task.get("deadline_date", task.get("deadline",  "")))
                        status   = h(task.get("status",        "pending"))
                        p_class  = "priority-high" if task.get("status") == "pending" else "priority-low"
                        st.markdown(f"""
                        <div class="task-row">
                            <div>
                                <div class="task-title">{title}</div>
                                <div class="task-sub">{subject} &middot; {deadline}</div>
                            </div>
                            <span class="{p_class}">{status}</span>
                        </div>
                        """, unsafe_allow_html=True)

            with st.expander("Raw Response"):
                st.json(result)
        elif result is not None:
            st.write(result)
