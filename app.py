import json
import os
import random
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & SESSION STATE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="UK LM DAIS - Fun Friday | UFO Presents",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

TEAM_THEMES = [
    {"name": "Team Rocket", "icon": "🚀", "grad": "linear-gradient(135deg, #FF416C, #FF4B2B)", "border": "#FF4B2B", "glow": "rgba(255, 75, 43, 0.4)"},
    {"name": "Team Galaxy", "icon": "🌌", "grad": "linear-gradient(135deg, #7F00FF, #E100FF)", "border": "#E100FF", "glow": "rgba(225, 0, 255, 0.4)"},
    {"name": "Team Thunder", "icon": "⚡", "grad": "linear-gradient(135deg, #F7971E, #FFD200)", "border": "#FFD200", "glow": "rgba(255, 210, 0, 0.4)"},
    {"name": "Team Nova", "icon": "☄️", "grad": "linear-gradient(135deg, #00B4DB, #0083B0)", "border": "#00B4DB", "glow": "rgba(0, 180, 219, 0.4)"},
]

SILLY_TOPICS = [
    "Is cereal legally classified as soup?",
    "Should dogs be allowed to vote in local elections?",
    "Hotdogs are sandwiches, and anyone who disagrees is wrong.",
    "Aliens avoid Earth because humans still haven't mastered printers.",
    "Socks with sandals is the peak of human fashion evolution.",
    "Chairs are a conspiracy by Big Furniture to weaken our legs.",
    "Pigeons are government drones recharging on power lines.",
    "Naps should be mandatory for adults during work hours.",
    "A straw has only one hole, not two.",
    "Pineapple belongs on EVERY pizza, including dessert pizza.",
    "Toilet paper must hang OVER, never under.",
    "Penguins are just overdressed seagulls.",
    "Time travel exists, and deja vu is just a server lag.",
    "Ice cubes are just boneless water.",
]

DEFAULT_PARTICIPANTS = [
    "Ajaz", "Amit", "Ankur", "Arpit",
    "Bhabesh", "Gautam", "Jeet", "Kali",
    "Karishma", "Kartiki", "Obaiah", "Irfan", "Neha", "Nishank", "Prasad", "Pratik", "Pritesh", "Roshni", "Sampada", "Sara", "Shailavi", "Sharvani", "Shubham", "Soham", "Sonali", "Soumyashree", "Sunny", "Swanand"
]

defaults = {
    "screen": 1,
    "participants": DEFAULT_PARTICIPANTS.copy(),
    "original_participants": DEFAULT_PARTICIPANTS.copy(),
    "num_teams": 3,
    "team_names": [t["name"] for t in TEAM_THEMES[:3]],
    "team_icons": [t["icon"] for t in TEAM_THEMES[:3]],
    "teams": [],
    "highlighted": set(),
    "scores": {},
    "sfx": True,
    "sfx_trigger": None,
    "confetti_trigger": False,
    "show_winner_screen": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------------------------------------------------------
# 2. SLEEK COSMIC STYLING
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    #MainMenu, footer, header { visibility: hidden; }

    .stApp {
        background: radial-gradient(circle at 50% 25%, #32286b 0%, #161d40 50%, #0a0e24 100%);
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stRadio label, .stTextInput label, .stSelectbox label, p, span, div {
        color: #f8fafc !important;
    }

    .bg-particle {
        position: absolute;
        border-radius: 50%;
        background: rgba(56, 189, 248, 0.15);
        animation: floatParticle 8s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }
    @keyframes floatParticle {
        0%, 100% { transform: translateY(0px) scale(1); opacity: 0.3; }
        50% { transform: translateY(-20px) scale(1.15); opacity: 0.7; }
    }

    .block-container {
        padding: 1.5rem 2rem !important;
        max-width: 1400px !important;
        margin: auto !important;
    }

    .hero-container {
        text-align: center;
        padding: 1.5rem 1rem;
        background: rgba(30, 27, 75, 0.5);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 24px;
        backdrop-filter: blur(14px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5);
        width: 100%;
        max-width: 720px;
        margin: 0 auto;
    }
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(30px, 4.2vw, 48px);
        font-weight: 900;
        background: linear-gradient(135deg, #fffbeb 30%, #fde047 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 2px;
        filter: drop-shadow(0 0 18px rgba(253, 224, 71, 0.4));
    }
    .hero-sub {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(14px, 1.8vw, 20px);
        font-weight: 800;
        background: linear-gradient(135deg, #f472b6 30%, #db2777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .presenter-pill {
        display: inline-block;
        padding: 2px 14px;
        border-radius: 30px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.4);
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        font-weight: 700;
        color: #38bdf8;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .event-title {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(20px, 2.6vw, 28px);
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 2px;
        text-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }
    .tagline {
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        color: #cbd5e1;
        margin: 8px 0 12px 0;
    }

    .ufo-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 10px 0;
        animation: floatUfo 3.5s ease-in-out infinite;
        filter: drop-shadow(0 10px 18px rgba(56, 189, 248, 0.35));
    }
    @keyframes floatUfo {
        0%, 100% { transform: translateY(0px) rotate(-1deg); }
        50% { transform: translateY(-8px) rotate(1deg); }
    }
    [data-testid="stImage"] { display: flex; justify-content: center; width: 100%; }

    .glass-panel {
        background: rgba(20, 29, 58, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 1.2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 1rem;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 6px;
        margin-top: 8px;
    }
    .feature-chip {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(139, 92, 246, 0.35);
        padding: 4px 12px;
        border-radius: 30px;
        font-size: 11px;
        font-weight: 600;
        color: #f1f5f9;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    .team-card {
        background: rgba(20, 29, 58, 0.85);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        min-height: 200px;
        margin-bottom: 1rem;
    }
    .team-banner {
        font-family: 'Orbitron', sans-serif;
        font-size: 15px;
        font-weight: 800;
        text-align: center;
        padding: 8px;
        border-radius: 10px;
        color: #ffffff;
        margin-bottom: 8px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    .player-row {
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid rgba(56, 189, 248, 0.7);
        padding: 6px 10px;
        border-radius: 6px;
        margin-bottom: 4px;
        font-size: 13px;
        font-weight: 600;
        color: #f8fafc;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .player-swapped {
        background: linear-gradient(90deg, rgba(250, 204, 21, 0.2), rgba(244, 114, 182, 0.2)) !important;
        border-left: 3px solid #facc15 !important;
        color: #fde047 !important;
    }

    div.stButton > button {
        width: 100%;
        min-height: 46px;
        font-family: 'Orbitron', sans-serif;
        font-size: 12px;
        font-weight: 800;
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
        color: #ffffff;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        transition: all 0.15s ease;
        letter-spacing: 0.5px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        box-shadow: 0 6px 16px rgba(139, 92, 246, 0.6);
        color: #fde047;
        border-color: rgba(253, 224, 71, 0.5);
    }
    div.stButton > button:active {
        transform: translateY(2px);
    }

    .stTextInput input, .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.85) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(139, 92, 246, 0.35) !important;
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
    }
    </style>

    <div class="bg-particle" style="width: 140px; height: 140px; top: 10%; left: 10%; animation-duration: 8s;"></div>
    <div class="bg-particle" style="width: 200px; height: 200px; top: 55%; left: 80%; animation-duration: 11s; background: rgba(127, 0, 255, 0.12);"></div>
    <div class="bg-particle" style="width: 90px; height: 90px; top: 75%; left: 15%; animation-duration: 6s; background: rgba(244, 114, 182, 0.12);"></div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. AUDIO & CONFETTI ENGINE
# -----------------------------------------------------------------------------
def run_fx():
    sfx = st.session_state.sfx_trigger if st.session_state.sfx else None
    confetti = st.session_state.confetti_trigger
    st.session_state.sfx_trigger = None
    st.session_state.confetti_trigger = False

    if not sfx and not confetti:
        return

    components.html(
        f"""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
        const sfx = {json.dumps(sfx)};
        const doConfetti = {json.dumps(confetti)};

        if (doConfetti && typeof confetti === 'function') {{
            confetti({{ particleCount: 150, spread: 100, origin: {{ y: 0.5 }} }});
        }}

        if (sfx) {{
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const playTone = (freq, type, start, dur, vol=0.1) => {{
                try {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(freq, ctx.currentTime + start);
                    gain.gain.setValueAtTime(vol, ctx.currentTime + start);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + start + dur);
                    osc.connect(gain); gain.connect(ctx.destination);
                    osc.start(ctx.currentTime + start);
                    osc.stop(ctx.currentTime + start + dur);
                }} catch(e) {{}}
            }};

            if (sfx === 'click') {{
                playTone(580, 'sine', 0, 0.07);
                playTone(880, 'sine', 0.03, 0.07);
            }} else if (sfx === 'shuffle') {{
                [330, 440, 554, 659, 880].forEach((f, i) => playTone(f, 'triangle', i * 0.03, 0.08));
            }} else if (sfx === 'fanfare') {{
                [523.25, 659.25, 783.99, 1046.5, 1318.5].forEach((f, i) => playTone(f, 'sawtooth', i * 0.08, 0.4, 0.12));
            }} else if (sfx === 'tie') {{
                [400, 350, 300, 250].forEach((f, i) => playTone(f, 'square', i * 0.1, 0.15, 0.1));
            }}
        }}
        </script>
        """,
        height=0,
        width=0,
    )

# -----------------------------------------------------------------------------
# 4. TEAM LOGIC & UI HELPERS
# -----------------------------------------------------------------------------
def distribute_teams(names, n):
    pool = names.copy()
    random.shuffle(pool)
    teams = [[] for _ in range(n)]
    for i, person in enumerate(pool):
        teams[i % n].append(person)
    return teams

def render_team_grid(teams, highlighted=None, show_scores=False):
    if highlighted is None:
        highlighted = set()
    cols = st.columns(len(teams))
    for idx, team in enumerate(teams):
        theme = TEAM_THEMES[idx % len(TEAM_THEMES)]
        custom_names = st.session_state.get("team_names", [])
        custom_icons = st.session_state.get("team_icons", [])
        t_name = custom_names[idx] if idx < len(custom_names) else theme["name"]
        t_icon = custom_icons[idx] if idx < len(custom_icons) else theme["icon"]

        if t_name not in st.session_state.scores:
            st.session_state.scores[t_name] = 0

        with cols[idx]:
            rows_html = ""
            for p in team:
                is_swapped = p in highlighted
                cls = "player-row player-swapped" if is_swapped else "player-row"
                badge = "✨ NEW" if is_swapped else "🎙️"
                rows_html += f'<div class="{cls}"><span>{p}</span><span style="font-size: 10px;">{badge}</span></div>'
            score_badge = (
                f"🏆 SCORE: {st.session_state.scores[t_name]}"
                if show_scores
                else f"{len(team)} Players"
            )
            st.markdown(
                f"""
                <div class="team-card">
                    <div class="team-banner" style="background: {theme['grad']}; border: 1px solid {theme['border']}; box-shadow: 0 3px 10px {theme['glow']};">
                        {t_icon} {t_name}<br>
                        <span style="font-size: 10px; font-weight: 600; opacity: 0.9;">{score_badge}</span>
                    </div>
                    {rows_html}
                </div>
                """,
                unsafe_allow_html=True,
            )
            if show_scores and not st.session_state.show_winner_screen:
                st.markdown("<div style='height: 2px'></div>", unsafe_allow_html=True)
                if st.button(f"+1: {t_name}", key=f"pt_{t_name}"):
                    st.session_state.scores[t_name] += 1
                    st.session_state.sfx_trigger = "fanfare"
                    st.session_state.confetti_trigger = True
                    st.rerun()

def render_top_hud():
    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        if st.session_state.screen > 1:
            if st.button("⬅️ Back", key="hud_back"):
                st.session_state.screen -= 1
                st.session_state.sfx_trigger = "click"
                st.rerun()
    with c2:
        stages = ["1. Portal", "2. Lobby", "3. Squads", "4. Custom", "5. Shuffle", "6. Stage"]
        hud = " &nbsp;▸&nbsp; ".join(
            f"<span style='color: #fde047; font-weight: 800;'>{s}</span>"
            if (i + 1) == st.session_state.screen
            else f"<span style='color: #64748b; font-weight: 600;'>{s}</span>"
            for i, s in enumerate(stages)
        )
        st.markdown(
            f"<div style='text-align: center; font-family: Orbitron; font-size: 11px; padding-top: 4px;'>{hud}</div>",
            unsafe_allow_html=True,
        )
    with c3:
        lbl = "🔊 SFX ON" if st.session_state.sfx else "🔇 SFX OFF"
        if st.button(lbl, key="hud_sfx"):
            st.session_state.sfx = not st.session_state.sfx
            st.rerun()

# -----------------------------------------------------------------------------
# 5. SCREENS
# -----------------------------------------------------------------------------
render_top_hud()

# SCREEN 1: HERO LAUNCH PORTAL
if st.session_state.screen == 1:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    _, center_hero, _ = st.columns([0.5, 3, 0.5])
    with center_hero:
        st.markdown(
            """
            <div class="hero-container">
                <div class="presenter-pill">UK LM DAIS PRESENTS</div>
                <div class="hero-title">FUN FRIDAY</div>
                <div class="hero-sub">🛸 UFO ARENA 🛸</div>
                <div class="event-title" style="font-size: clamp(16px, 2vw, 22px); color: #38bdf8; margin-top: 2px;">
                    Debate On Silly Topics
                </div>
            """,
            unsafe_allow_html=True,
        )
        
        lc, mc, rc = st.columns([1, 0.5, 1])
        with mc:
            if os.path.exists("ufo_logo.png"):
                st.image("ufo_logo.png", width=180)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    """
                    <div style="text-align:centre;">
                    <div style= "font-size:55px;text-shadow: 0 0 20px rgba(56,189,248,0.5)">
                    🛸
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
        st.markdown(
            """
                <p class="tagline">Defend the Undefendable. Argue the Absurd. Win the Crowd.</p>
                <div class="chip-row">
                    <span class="feature-chip">🚀 Custom Teams</span>
                    <span class="feature-chip">⚡ Shuffler</span>
                    <span class="feature-chip">🎙️ Topic Roulette</span>
                    <span class="feature-chip">🏆 Live Score</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        _, cta_col, _ = st.columns([1, 0.3, 1])
        with cta_col:
            if st.button("🚀 START", key="start_btn"):
                st.session_state.screen = 2
                st.session_state.sfx_trigger = "fanfare"
                st.rerun()

# SCREEN 2: PARTICIPANT LOBBY
elif st.session_state.screen == 2:
    st.markdown('<div class="event-title" style="margin-top: 2px;">📋 Player Lobby</div>', unsafe_allow_html=True)
    st.markdown("<div class='tagline'>Remove absent participants from the preset list or reset if needed.</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 6px'></div>", unsafe_allow_html=True)
    
    left, right = st.columns([1, 1.2])
    with left:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-family: Orbitron; font-size: 15px; margin-bottom: 8px;'>Roster Controls</h3>", unsafe_allow_html=True)
        
        if st.button("🔄 Reset Roster to Full"):
            st.session_state.participants = st.session_state.original_participants.copy()
            st.session_state.sfx_trigger = "click"
            st.rerun()
            
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        with st.form("add_custom_player", clear_on_submit=True):
            new_p = st.text_input("Add Participant:")
            if st.form_submit_button("➕ Add Player") and new_p.strip():
                if new_p.strip() not in st.session_state.participants:
                    st.session_state.participants.append(new_p.strip())
                st.session_state.sfx_trigger = "click"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with right:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        cnt = len(st.session_state.participants)
        badge_bg = "#38bdf8" if cnt >= 4 else "#f472b6"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h3 style="margin: 0; font-family: Orbitron; font-size: 15px;">Active Roster</h3>
                <span style="background: {badge_bg}; color: #020617; padding: 2px 10px; border-radius: 20px; font-weight: 800; font-size: 11px;">{cnt} Players</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if cnt == 0:
            st.info("No active participants. Click Reset Roster.")
        else:
            for idx, name in enumerate(list(st.session_state.participants)):
                p1, p2 = st.columns([4, 1])
                with p1:
                    st.markdown(f"<div style='padding: 4px 0; font-weight: 600; font-size: 13px;'>{idx+1}. {name}</div>", unsafe_allow_html=True)
                with p2:
                    if st.button("✕", key=f"rm_{idx}"):
                        st.session_state.participants.remove(name)
                        st.session_state.sfx_trigger = "click"
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("<div style='height: 4px'></div>", unsafe_allow_html=True)
    if cnt < 4:
        st.warning(f"⚠️ Need {4 - cnt} more player(s) to continue.")
    else:
        if st.button("NEXT: SQUAD CONFIGURATION ➡️"):
            st.session_state.screen = 3
            st.session_state.sfx_trigger = "click"
            st.rerun()

# SCREEN 3: TEAM SPLIT CONFIGURATION
elif st.session_state.screen == 3:
    st.markdown('<div class="event-title">⚡ Squad Splitter</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
    
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="glass-panel" style="text-align: center;">', unsafe_allow_html=True)
        choice = st.radio(
            "Select Squad Split:",
            ["Split into 2 Teams", "Split into 3 Teams", "Split into 4 Teams"],
            index=st.session_state.num_teams - 2,
            horizontal=True,
        )
        st.session_state.num_teams = int(choice.split()[2])
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
        if st.button("NEXT: CUSTOMIZE TEAM NAMES & ICONS ➡️"):
            st.session_state.team_names = [TEAM_THEMES[i]["name"] for i in range(st.session_state.num_teams)]
            st.session_state.team_icons = [TEAM_THEMES[i]["icon"] for i in range(st.session_state.num_teams)]
            st.session_state.screen = 4
            st.session_state.sfx_trigger = "click"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# SCREEN 4: CUSTOM TEAM NAME EDITOR
elif st.session_state.screen == 4:
    st.markdown('<div class="event-title">✏️ Customize Teams</div>', unsafe_allow_html=True)
    st.markdown("<div class='tagline'>Personalize team names and pick custom emojis before generating rosters!</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    cols = st.columns(st.session_state.num_teams)
    
    for i in range(st.session_state.num_teams):
        with cols[i]:
            theme = TEAM_THEMES[i % len(TEAM_THEMES)]
            st.markdown(f"<div style='font-family: Orbitron; font-size: 13px; font-weight: 700; color: #38bdf8; margin-bottom: 4px;'>Team {i+1} Setup</div>", unsafe_allow_html=True)
            
            current_name = st.session_state.team_names[i] if i < len(st.session_state.team_names) else theme["name"]
            new_name = st.text_input(f"Name {i+1}", value=current_name, key=f"t_name_{i}", label_visibility="collapsed")
            st.session_state.team_names[i] = new_name if new_name else theme["name"]
            
            current_icon = st.session_state.team_icons[i] if i < len(st.session_state.team_icons) else theme["icon"]
            new_icon = st.text_input(f"Emoji {i+1}", value=current_icon, key=f"t_icon_{i}", label_visibility="collapsed")
            st.session_state.team_icons[i] = new_icon if new_icon else theme["icon"]

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 6px'></div>", unsafe_allow_html=True)
    
    _, gen_col, _ = st.columns([1, 0.4, 1])
    with gen_col:
        if st.button("🎲 GENERATE SQUADS"):
            st.session_state.teams = distribute_teams(st.session_state.participants, st.session_state.num_teams)
            st.session_state.highlighted = set()
            st.session_state.show_winner_screen = False
            st.session_state.screen = 5
            st.session_state.sfx_trigger = "shuffle"
            st.session_state.confetti_trigger = True
            st.rerun()

# SCREEN 5: TEAM SHUFFLE ARENA
elif st.session_state.screen == 5:
    st.markdown('<div class="event-title">🔀 Team Shuffle Arena</div>', unsafe_allow_html=True)
    st.markdown(
        "<div class='tagline' style='margin-bottom: 6px;'>Swapped debaters light up in gold! Balance squads before locking in.</div>",
        unsafe_allow_html=True,
    )
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔀 Shuffle All"):
            old_map = {m: i for i, t in enumerate(st.session_state.teams) for m in t}
            new_t = distribute_teams(st.session_state.participants, st.session_state.num_teams)
            st.session_state.highlighted = {m for i, t in enumerate(new_t) for m in t if old_map.get(m) != i}
            st.session_state.teams = new_t
            st.session_state.sfx_trigger = "shuffle"
            st.rerun()
    with c2:
        if st.button("🔄 Member Swap"):
            teams = st.session_state.teams
            if len(teams) >= 2:
                t1, t2 = random.sample(range(len(teams)), 2)
                i1, i2 = random.randrange(len(teams[t1])), random.randrange(len(teams[t2]))
                p1, p2 = teams[t1][i1], teams[t2][i2]
                teams[t1][i1], teams[t2][i2] = p2, p1
                st.session_state.highlighted = {p1, p2}
                st.session_state.sfx_trigger = "shuffle"
                st.rerun()
    with c3:
        if st.button("⚖️ Rebalance"):
            flat = [m for t in st.session_state.teams for m in t]
            n = st.session_state.num_teams
            reb = [flat[i::n] for i in range(n)]
            old_map = {m: i for i, t in enumerate(st.session_state.teams) for m in t}
            st.session_state.highlighted = {m for i, t in enumerate(reb) for m in t if old_map.get(m) != i}
            st.session_state.teams = reb
            st.session_state.sfx_trigger = "click"
            st.rerun()
    with c4:
        if st.button("✏️ Edit Names"):
            st.session_state.screen = 4
            st.session_state.sfx_trigger = "click"
            st.rerun()
            
    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
    render_team_grid(st.session_state.teams, st.session_state.highlighted)
    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    
    _, conf, _ = st.columns([1, 0.5, 1])
    with conf:
        if st.button("✅ LOCK TEAMS & START DEBATE"):
            st.session_state.highlighted = set()
            st.session_state.show_winner_screen = False
            st.session_state.screen = 6
            st.session_state.sfx_trigger = "fanfare"
            st.session_state.confetti_trigger = True
            st.rerun()

# SCREEN 6: LIVE BROADCAST DEBATE STAGE & DEDICATED WINNER CELEBRATION SCREEN
elif st.session_state.screen == 6:
    
    if st.session_state.show_winner_screen:
        scores = st.session_state.scores
        max_score = max(scores.values(), default=0) if scores else 0
        winners = [t for t, sc in scores.items() if sc == max_score] if scores else []
        is_tie = len(winners) > 1

        if is_tie:
            title_text = "🤝 EPIC TIE-BREAKER! 🤝"
            body_text = f"Tied Squads: <b>{' & '.join(winners)}</b> ({max_score} Points each)"
            card_grad = "linear-gradient(135deg, #831843, #581c87)"
            border_color = "#38bdf8"
            sound_type = "tie"
        else:
            winner_name = winners[0] if winners else "No Team"
            title_text = f"🏆 CHAMPION: {winner_name}! 🏆"
            body_text = f"Final Winning Score: <b>{max_score} Points</b>"
            card_grad = "linear-gradient(135deg, #4c1d95, #1e1b4b)"
            border_color = "#fde047"
            sound_type = "fanfare"

        # Embedded HTML component containing both the celebratory card and guaranteed sound + confetti execution
        components.html(
            f"""
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@800;900&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
            body {{
                margin: 0; padding: 0; background: transparent; font-family: 'Plus Jakarta Sans', sans-serif;
                display: flex; justify-content: center; align-items: center; height: 100vh;
            }}
            .celebration-card {{
                background: {card_grad};
                border: 3px solid {border_color};
                border-radius: 28px;
                padding: 2.5rem 2rem;
                text-align: center;
                color: white;
                box-shadow: 0 0 60px rgba(0,0,0,0.9), 0 0 40px {border_color};
                width: 90%;
                max-width: 580px;
                animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }}
            @keyframes popIn {{
                from {{ transform: scale(0.6); opacity: 0; }}
                to {{ transform: scale(1); opacity: 1; }}
            }}
            .title {{
                font-family: 'Orbitron', sans-serif;
                font-size: clamp(22px, 2.5vw, 32px);
                font-weight: 900;
                color: #fde047;
                text-shadow: 0 0 18px rgba(253, 224, 71, 0.6);
                margin-bottom: 12px;
            }}
            .body-text {{
                font-size: 18px;
                color: #f8fafc;
                margin-bottom: 15px;
            }}
            </style>

            <div class="celebration-card">
                <div style="font-size: 60px; margin-bottom: 10px;">🎉🛸👑</div>
                <div class="title">{title_text}</div>
                <div class="body-text">{body_text}</div>
                <p style="font-size: 13px; color: #cbd5e1; max-width: 400px; margin: 0 auto;">Absolute mastery of absurd logic and witty rebuttals! Thank you for participating in Fun Friday UFO Arena.</p>
            </div>

            <script>
            // Fire Confetti
            if (typeof confetti === 'function') {{
                confetti({{ particleCount: 180, spread: 120, origin: {{ y: 0.5 }} }});
            }}

            // Guaranteed WebAudio Sound Effect playback inside component
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const sound = "{sound_type}";
                
                const playTone = (freq, type, start, dur, vol=0.15) => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(freq, ctx.currentTime + start);
                    gain.gain.setValueAtTime(vol, ctx.currentTime + start);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + start + dur);
                    osc.connect(gain); gain.connect(ctx.destination);
                    osc.start(ctx.currentTime + start);
                    osc.stop(ctx.currentTime + start + dur);
                }};

                if (sound === 'fanfare') {{
                    [523.25, 659.25, 783.99, 1046.5, 1318.5].forEach((f, i) => playTone(f, 'sawtooth', i * 0.08, 0.4, 0.15));
                }} else {{
                    [400, 350, 300, 250].forEach((f, i) => playTone(f, 'square', i * 0.1, 0.15, 0.12));
                }}
            }} catch(e) {{ console.log(e); }}
            </script>
            """,
            height=380,
        )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        _, btn_c, _ = st.columns([1, 1.5, 1])
        with btn_c:
            if st.button("🔄 START NEW DEBATE SESSION"):
                st.session_state.screen = 1
                st.session_state.show_winner_screen = False
                st.session_state.scores = {}
                st.session_state.sfx_trigger = "click"
                st.rerun()

    else:
        # NORMAL LIVE STAGE VIEW
        st.markdown('<div class="event-title" style="margin-bottom: 2px;">🎙️ Live Debate Stage</div>', unsafe_allow_html=True)
        topics_json = json.dumps(SILLY_TOPICS)
        
        components.html(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
            body {{
                background: transparent;
                color: #ffffff;
                font-family: 'Plus Jakarta Sans', sans-serif;
                margin: 0;
                padding: 0;
                text-align: center;
            }}
            .stage-box {{
                background: rgba(20, 29, 58, 0.85);
                border: 1px solid rgba(139, 92, 246, 0.35);
                border-radius: 16px;
                padding: 10px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.5);
                backdrop-filter: blur(12px);
            }}
            .topic-card {{
                font-size: clamp(15px, 1.8vw, 20px);
                font-weight: 800;
                color: #fde047;
                margin: 6px 0;
                text-shadow: 0 0 12px rgba(253, 224, 71, 0.4);
                min-height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .clock-display {{
                font-family: 'Orbitron', sans-serif;
                font-size: clamp(30px, 4vw, 48px);
                font-weight: 900;
                color: #38bdf8;
                text-shadow: 0 0 18px rgba(56, 189, 248, 0.5);
                margin: 4px 0;
            }}
            .urgent {{
                color: #f472b6 !important;
                animation: pulseUrgent 0.5s infinite alternate;
            }}
            @keyframes pulseUrgent {{
                from {{ transform: scale(1); text-shadow: 0 0 10px #f472b6; }}
                to {{ transform: scale(1.03); text-shadow: 0 0 22px #f472b6; }}
            }}
            .btn-row {{
                display: flex;
                justify-content: center;
                gap: 8px;
                flex-wrap: wrap;
                margin-top: 6px;
            }}
            .arcade-btn {{
                font-family: 'Orbitron', sans-serif;
                font-size: 11px;
                font-weight: 800;
                background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
                color: #ffffff;
                padding: 7px 14px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                cursor: pointer;
                box-shadow: 0 3px 8px rgba(79, 70, 229, 0.4);
                transition: all 0.15s ease;
            }}
            .arcade-btn:hover {{ transform: translateY(-2px); filter: brightness(1.15); color: #fde047; }}
            .arcade-btn:active {{ transform: translateY(2px); }}
            </style>

            <div class="stage-box">
                <div style="font-family: 'Orbitron'; font-size: 11px; color: #38bdf8; letter-spacing: 1px;">🎰 SILLY TOPIC ROULETTE</div>
                <div id="topic-display" class="topic-card">Press spin to draw a debate topic!</div>
                <div id="clock" class="clock-display">02:00</div>
                <div class="btn-row">
                    <button class="arcade-btn" onclick="spinTopic()">🎲 SPIN TOPIC</button>
                    <button class="arcade-btn" onclick="startTimer()">▶️ START TIMER</button>
                    <button class="arcade-btn" onclick="pauseTimer()" style="background: linear-gradient(135deg, #9333ea, #c084fc);">⏸️ PAUSE</button>
                    <button class="arcade-btn" onclick="resetTimer()" style="background: linear-gradient(135deg, #475569, #334155);">🔄 RESET</button>
                </div>
            </div>

            <script>
            const topics = {topics_json};
            let timeLeft = 120;
            let timerId = null;

            function beep(freq, dur) {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const o = ctx.createOscillator(); 
                const g = ctx.createGain();
                o.frequency.value = freq; 
                g.gain.value = 0.08;
                o.connect(g); 
                g.connect(ctx.destination);
                o.start(); 
                o.stop(ctx.currentTime + dur);
            }}

            function spinTopic() {{
                let spins = 0;
                const el = document.getElementById('topic-display');
                const interval = setInterval(() => {{
                    el.innerText = topics[Math.floor(Math.random() * topics.length)];
                    beep(400 + spins * 25, 0.03);
                    spins++;
                    if (spins > 16) {{
                        clearInterval(interval);
                        beep(880, 0.2);
                    }}
                }}, 60);
            }}

            function updateClock() {{
                const m = String(Math.floor(timeLeft / 60)).padStart(2, '0');
                const s = String(timeLeft % 60).padStart(2, '0');
                const c = document.getElementById('clock');
                c.innerText = m + ":" + s;
                if (timeLeft <= 15 && timeLeft > 0) c.classList.add('urgent');
                else c.classList.remove('urgent');
            }}

            function startTimer() {{
                if (timerId) return;
                timerId = setInterval(() => {{
                    if (timeLeft > 0) {{
                        timeLeft--;
                        updateClock();
                        if (timeLeft <= 10 && timeLeft > 0) beep(660, 0.06);
                        if (timeLeft === 0) {{
                            beep(220, 0.6);
                            clearInterval(timerId);
                            timerId = null;
                        }}
                    }}
                }}, 1000);
            }}

            function pauseTimer() {{ 
                clearInterval(timerId); 
                timerId = null; 
            }}

            function resetTimer() {{ 
                pauseTimer(); 
                timeLeft = 120; 
                updateClock(); 
            }}
            </script>
            """,
            height=230,
        )

        st.markdown("<div style='height: 2px'></div>", unsafe_allow_html=True)
        render_team_grid(st.session_state.teams, show_scores=True)
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
        
        # STOP DEBATE & DECLARE WINNER BUTTON
        _, stop_col, _ = st.columns([1, 1.4, 1])
        with stop_col:
            if st.button("🛑 STOP DEBATE & DECLARE WINNER"):
                st.session_state.show_winner_screen = True
                st.rerun()

    run_fx()
