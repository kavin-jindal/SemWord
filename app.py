import streamlit as st
import main
from pinecone import Pinecone
import os
from dotenv import load_dotenv
pc = Pinecone(api_key=os.getenv("PINECONE"))
index = pc.Index("semword-index")

st.set_page_config(page_title="Semword", layout="centered")
st.logo(
    "logo.png",
    link="https://streamlit.io/gallery",
    icon_image="logo.png",
)
st.set_page_config(page_icon="logo.png")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Syne:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.appview-container .main .block-container {
    padding-bottom: 1rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}
.main-header {
    display: flex; align-items: baseline; justify-content: space-between;
    padding: 1.5rem 0 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.5rem;
}
.game-title {
    font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 600;
    letter-spacing: 0.08em; color: rgba(255,255,255,0.95);
}
.game-subtitle {
    font-size: 12px; color: rgba(255,255,255,0.3);
    letter-spacing: 0.12em; text-transform: uppercase;
}
.stats-row { display: flex; gap: 24px; align-items: center; text-align: right; }
.stat { display: flex; flex-direction: column; gap: 2px; }
.stat-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 20px; font-weight: 500; color: rgba(255,255,255,0.9);
}
.stat-label {
    font-size: 10px; letter-spacing: 0.1em;
    text-transform: uppercase; color: rgba(255,255,255,0.3);
}
.guess-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 11px 16px; border-radius: 6px; margin-bottom: 5px;
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
}
.guess-row:hover { background: rgba(255,255,255,0.07); }
.guess-left { display: flex; align-items: center; gap: 12px; }
.rank {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: rgba(255,255,255,0.2); min-width: 24px;
}
.guess-word {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px; color: rgba(255,255,255,0.85);
}
.temp-label {
    font-size: 10px; padding: 3px 10px; border-radius: 4px;
    font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase;
}
.tier-cold    { background: rgba(56,138,221,0.15); color: #7ab3e0; border: 1px solid rgba(56,138,221,0.2); }
.tier-warm    { background: rgba(239,159,39,0.15); color: #e0a855; border: 1px solid rgba(239,159,39,0.2); }
.tier-hot     { background: rgba(216,90,48,0.15);  color: #e07855; border: 1px solid rgba(216,90,48,0.2); }
.tier-veryhot { background: rgba(200,80,20,0.2);   color: #e09060; border: 1px solid rgba(200,80,20,0.25); }
.tier-done    { background: rgba(99,153,34,0.2);   color: #90c060; border: 1px solid rgba(99,153,34,0.25); }

.hint-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid rgba(239,159,39,0.5);
    border-radius: 6px; padding: 14px 16px; margin: 12px 0;
    font-size: 13px; color: rgba(255,255,255,0.6);
    line-height: 1.6;
}
.hint-label {
    font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;
    color: rgba(239,159,39,0.7); font-style: normal;
    font-weight: 500; display: block; margin-bottom: 10px;
}
.win-msg {
    text-align: center; padding: 2rem 0;
    font-size: 13px; color: rgba(255,255,255,0.4); letter-spacing: 0.05em;
}
.win-word {
    font-family: 'IBM Plex Mono', monospace; font-size: 32px; font-weight: 500;
    color: rgba(144,192,96,0.9); display: block; margin-bottom: 8px;
}
.reveal-word {
    font-family: 'IBM Plex Mono', monospace; font-size: 32px; font-weight: 500;
    color: rgba(221,138,56,0.9); display: block; margin-bottom: 8px;
}
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.2rem 0; }
</style>
            


""", unsafe_allow_html=True)

TIER_CLASS = {
    "Cold":     "tier-cold",
    "Warm":     "tier-warm",
    "Hot":      "tier-hot",
    "Very Hot": "tier-veryhot",
    "Done!":    "tier-done",
}
def footer():
    st.markdown("""
    <div style="margin-top:4rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.06);
    display:flex;align-items:center;justify-content:space-between;">
        <span style="font-size:11px;color:rgba(255,255,255,0.2);letter-spacing:0.08em;text-transform:uppercase;">
            semword
        </span>
        <span style="font-size:11px;color:rgba(255,255,255,0.2);">
            built by <a href="https://deckrdev.vercel.app/kavinjindal" target="_blank"
            style="color:rgba(255,255,255,0.4);text-decoration:none;">kavin jindal</a>
        </span>
    </div>
    """, unsafe_allow_html=True)

col_nav1, col_nav2 = st.columns([1, 1])
with col_nav1:
    st.markdown('<span style="font-size:11px;color:rgba(255,255,255,0.2);letter-spacing:0.08em;text-transform:uppercase;">semword · by kavin jindal</span>', unsafe_allow_html=True)
with col_nav2:
    if st.button("how to play →", use_container_width=True):
        st.switch_page("how_to_play")
if "word" not in st.session_state:
    st.session_state.word = main.gen_word()
if "guesses" not in st.session_state:
    st.session_state.guesses = {}
if "won" not in st.session_state:
    st.session_state.won = False
if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0
if "revealed" not in st.session_state:
    st.session_state.revealed = False
if "confirm_reveal" not in st.session_state:
    st.session_state.confirm_reveal = False
if "all_hints" not in st.session_state:
    st.session_state.all_hints = []
if "hint_index" not in st.session_state:
    st.session_state.hint_index = 0

word = st.session_state.word
MAX_HINTS = 5

# header
st.markdown(f"""
<div class="main-header">
    <div>
        <div class="game-title">semword</div>
        <div class="game-subtitle">semantic word game</div>
    </div>
    <div class="stats-row">
        <div class="stat">
            <span class="stat-val">{len(st.session_state.guesses)}</span>
            <span class="stat-label">guesses</span>
        </div>
        <div class="stat">
            <span class="stat-val">{st.session_state.hints_used}</span>
            <span class="stat-label">hints</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# hint + reveal buttons
if not st.session_state.won and not st.session_state.revealed:
    col1, col2 = st.columns(2)
    with col1:
        hints_exhausted = st.session_state.hint_index >= MAX_HINTS
        if st.button(
            "get hint" if not hints_exhausted else "no more hints",
            use_container_width=True,
            disabled=hints_exhausted
        ):
            if not st.session_state.all_hints:
                st.session_state.all_hints = main.get_hints(word, n=MAX_HINTS)
            st.session_state.hint_index += 1
            st.session_state.hints_used += 1
            st.toast(f"hint {st.session_state.hint_index} of {MAX_HINTS} revealed!")
            st.rerun()
    with col2:
        if st.button("reveal word", use_container_width=True):
            st.session_state.confirm_reveal = True
            st.rerun()

# confirm reveal dialog
if st.session_state.confirm_reveal:
    st.warning("are you sure you want to reveal the word? this will end the game.")
    yes, no = st.columns(2)
    with yes:
        if st.button("yes, reveal", use_container_width=True):
            st.session_state.revealed = True
            st.session_state.confirm_reveal = False
            st.rerun()
    with no:
        if st.button("cancel", use_container_width=True):
            st.session_state.confirm_reveal = False
            st.rerun()

# hint box — show one pill at a time
if st.session_state.hint_index > 0 and st.session_state.all_hints:
    visible_hints = st.session_state.all_hints[:st.session_state.hint_index]
    pills = "".join([
        f'<span style="font-family:monospace;font-size:12px;padding:4px 10px;border-radius:4px;background:rgba(239,159,39,0.1);color:#e0a855;border:1px solid rgba(239,159,39,0.2);margin-right:6px;display:inline-block;margin-bottom:4px;">{w}</span>'
        for w in visible_hints
    ])
    st.markdown(f"""
    <div class="hint-box">
        <span class="hint-label">nearby words ({st.session_state.hint_index}/{MAX_HINTS})</span>
        {pills}
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# win screen
if st.session_state.won:
    st.markdown(f"""
    <div class="win-msg">
        <span class="win-word">{word}</span>
        you guessed it in {len(st.session_state.guesses)} guess{'es' if len(st.session_state.guesses) != 1 else ''}
        · {st.session_state.hints_used} hint{'s' if st.session_state.hints_used != 1 else ''} used
    </div>
    """, unsafe_allow_html=True)
    if st.button("play again", use_container_width=True):
        for key in ["word", "guesses", "won", "hints_used", "revealed", "confirm_reveal", "all_hints", "hint_index"]:
            del st.session_state[key]
        st.rerun()

# revealed screen
elif st.session_state.revealed:
    st.markdown(f"""
    <div class="win-msg">
        <span class="reveal-word">{word}</span>
        better luck next time
    </div>
    """, unsafe_allow_html=True)
    if st.button("play again", use_container_width=True):
        for key in ["word", "guesses", "won", "hints_used", "revealed", "confirm_reveal", "all_hints", "hint_index"]:
            del st.session_state[key]
        st.rerun()

# input
else:
    user_in = st.chat_input("type a word...")
    if user_in:
        user_in = user_in.strip().lower()
        
        result = index.fetch(ids=[user_in.lower()])

        if not result["vectors"]:
            st.error("word not found — try another")
        else:
            label = main.cos(main.get_vector(word.lower()), main.get_vector(user_in.lower()))
            st.session_state.guesses[user_in] = label
            if label == "Done!":
                st.session_state.won = True
            st.rerun()

# guess rows — latest on top
for i, (guessed_word, label) in enumerate(reversed(list(st.session_state.guesses.items()))):
    css_class = TIER_CLASS.get(label, "tier-cold")
    actual_rank = len(st.session_state.guesses) - i
    st.markdown(f"""
    <div class="guess-row">
        <div class="guess-left">
            <span class="rank">#{actual_rank}</span>
            <span class="guess-word">{guessed_word}</span>
        </div>
        <span class="temp-label {css_class}">{label}</span>
    </div>
    """, unsafe_allow_html=True)

