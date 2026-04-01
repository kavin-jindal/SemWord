import streamlit as st
if st.button("← back to game"):
    st.switch_page("app.py")
st.set_page_config(page_title="How to Play — Semword", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Syne:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.page-title {
    font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 600;
    letter-spacing: 0.08em; color: rgba(255,255,255,0.95);
    padding: 1.5rem 0 0.25rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 2rem;
}
.section-title {
    font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(255,255,255,0.3); margin: 2rem 0 0.75rem;
}
.rule-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px; padding: 14px 16px; margin-bottom: 8px;
    display: flex; gap: 14px; align-items: flex-start;
}
.rule-num {
    font-family: 'IBM Plex Mono', monospace; font-size: 11px;
    color: rgba(255,255,255,0.2); min-width: 20px; padding-top: 2px;
}
.rule-text { font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.6; }
.rule-text b { color: rgba(255,255,255,0.9); font-weight: 500; }

.tier-row {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 16px; border-radius: 6px; margin-bottom: 6px;
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
}
.tier-label {
    font-size: 10px; padding: 3px 10px; border-radius: 4px;
    font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase;
    min-width: 72px; text-align: center;
}
.tier-desc { font-size: 13px; color: rgba(255,255,255,0.5); }

.cold-t    { background: rgba(56,138,221,0.15); color: #7ab3e0; border: 1px solid rgba(56,138,221,0.2); }
.warm-t    { background: rgba(239,159,39,0.15); color: #e0a855; border: 1px solid rgba(239,159,39,0.2); }
.hot-t     { background: rgba(216,90,48,0.15);  color: #e07855; border: 1px solid rgba(216,90,48,0.2); }
.veryhot-t { background: rgba(200,80,20,0.2);   color: #e09060; border: 1px solid rgba(200,80,20,0.25); }
.done-t    { background: rgba(99,153,34,0.2);   color: #90c060; border: 1px solid rgba(99,153,34,0.25); }

.dev-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px; padding: 20px; display: flex; gap: 16px; align-items: center;
    margin-top: 1rem;
}
.dev-avatar {
    width: 48px; height: 48px; border-radius: 50%;
    background: rgba(239,159,39,0.15); border: 1px solid rgba(239,159,39,0.2);
    display: flex; align-items: center; justify-content: center;
    font-family: 'IBM Plex Mono', monospace; font-size: 16px; font-weight: 500;
    color: #e0a855; flex-shrink: 0;
}
.dev-name {
    font-size: 15px; font-weight: 600; color: rgba(255,255,255,0.9);
    letter-spacing: 0.04em;
}
.dev-role { font-size: 12px; color: rgba(255,255,255,0.35); margin-top: 2px; }
.dev-links { display: flex; gap: 10px; margin-top: 8px; }
.dev-link {
    font-size: 11px; padding: 3px 10px; border-radius: 4px;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.5); text-decoration: none; letter-spacing: 0.04em;
}
.dev-link:hover { color: rgba(255,255,255,0.8); }

.footer {
    margin-top: 4rem; padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center; justify-content: space-between;
}
.footer-left { font-size: 11px; color: rgba(255,255,255,0.2); letter-spacing: 0.08em; text-transform: uppercase; }
.footer-right { font-size: 11px; color: rgba(255,255,255,0.2); }
.footer-right a { color: rgba(255,255,255,0.4); text-decoration: none; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">how to play</div>', unsafe_allow_html=True)

# rules
st.markdown('<div class="section-title">the rules</div>', unsafe_allow_html=True)

rules = [
    ("The secret word is always <b>five letters long</b>.", ),
    ("You can guess <b>any word of any length</b> — longer words can help you probe the semantic space.",),
    ("Every guess is scored by how <b>semantically similar</b> it is to the secret word using word embeddings.",),
    ("Use the score to <b>narrow in</b> — think in concepts, not spellings.",),
    ("You can use the <b>hint button</b> to reveal nearby words one at a time, up to 5 hints.",),
    ("If you're stuck, <b>reveal the word</b> — but that ends the game.",),
]

for i, (rule,) in enumerate(rules):
    st.markdown(f"""
    <div class="rule-card">
        <span class="rule-num">0{i+1}</span>
        <span class="rule-text">{rule}</span>
    </div>
    """, unsafe_allow_html=True)

# score tiers
st.markdown('<div class="section-title">score tiers</div>', unsafe_allow_html=True)

tiers = [
    ("cold-t",    "cold",     "semantically far — try a different concept entirely"),
    ("warm-t",    "warm",     "getting closer — you're in the right area"),
    ("hot-t",     "hot",      "very close — refine your thinking"),
    ("veryhot-t", "very hot", "extremely close — one or two words away"),
    ("done-t",    "done!",    "that's the word!"),
]

for cls, label, desc in tiers:
    st.markdown(f"""
    <div class="tier-row">
        <span class="tier-label {cls}">{label}</span>
        <span class="tier-desc">{desc}</span>
    </div>
    """, unsafe_allow_html=True)

# developer
st.markdown('<div class="section-title">developer</div>', unsafe_allow_html=True)

st.markdown("""
<div class="dev-card">
    <div class="dev-avatar">KJ</div>
    <div>
        <div class="dev-name">Kavin Jindal</div>
        <div class="dev-role">Cybersecurity & AI Enthusiast</div>
        <div class="dev-links">
            <a class="dev-link" href="https://deckrdev.vercel.app/kavin-jindal" target="_blank">Deckr</a>
            <a class="dev-link" href="https://github.com/kavin-jindal" target="_blank">github</a>
            <a class="dev-link" href="https://www.linkedin.com/in/kavin-jindal/" target="_blank">linkedin</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# footer
st.markdown("""
<div class="footer">
    <span class="footer-left">semword</span>
    <span class="footer-right">built by <a href="https://deckrdev.vercel.app/kavinjindal" target="_blank">kavin jindal</a></span>
</div>
""", unsafe_allow_html=True)

