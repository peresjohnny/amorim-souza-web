import re
import base64
import streamlit as st

# =========================
# CONFIG
# =========================
APP_NAME = "AMORIM & SOUZA"
SUBTITLE = "ADVOCACIA"
LOGO_FILE = "1000423374.jpg"  # NOME ORIGINAL
VALID_CPF = "79897789120"     # exemplo
CLIENT_NAME = "Edimar"        # exemplo

PROCESSOS = [
    "0737767-85.2025.8.07.0001",
    "0757632-94.2025.8.07.0001",
    "0722313-65.2025.8.07.0001",
    "0768584-35.2025.8.07.0001",
    "0764797-95.2025.8.07.0001",
]

st.set_page_config(page_title=APP_NAME, layout="centered")

# =========================
# HELPERS
# =========================
def get_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def only_digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")

def format_cpf(d: str) -> str:
    d = only_digits(d)[:11]
    if len(d) <= 3:
        return d
    if len(d) <= 6:
        return f"{d[:3]}.{d[3:]}"
    if len(d) <= 9:
        return f"{d[:3]}.{d[3:6]}.{d[6:]}"
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

# =========================
# STATE
# =========================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("tela", "login")  # login | dashboard | processos
st.session_state.setdefault("cpf_visual", "")
st.session_state.setdefault("cpf_digits", "")

logo_b64 = get_base64(LOGO_FILE)

# =========================
# ICONS (SVG inline)
# =========================
ICON_USER = """
<svg width="22" height="22" viewBox="0 0 24 24" fill="none"
     xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M12 12c2.761 0 5-2.463 5-5.5S14.761 1 12 1 7 3.463 7 6.5 9.239 12 12 12Z"
        fill="currentColor" opacity="0.92"/>
  <path d="M3 22c0-4.418 4.03-8 9-8s9 3.582 9 8"
        stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

ICON_DOC = """
<svg width="22" height="22" viewBox="0 0 24 24" fill="none"
     xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M7 3h7l3 3v15a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z"
        stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
  <path d="M14 3v4a2 2 0 0 0 2 2h4" stroke="currentColor" stroke-width="2"/>
  <path d="M8 12h8M8 16h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

ICON_HANDSHAKE = """
<svg width="22" height="22" viewBox="0 0 24 24" fill="none"
     xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M7 13l3.2 3.2a3 3 0 0 0 4.2 0L17 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M9 11l1.7-1.7a3 3 0 0 1 4.2 0L16 10.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M2 12l4-4 5 5-4 4-5-5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
  <path d="M22 12l-4-4-5 5 4 4 5-5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
</svg>
"""

# =========================
# CSS
# =========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root {{
  --brand: #1E3A8A;
  --sub: rgba(30,58,138,.55);
  --inputBg: #F3F4F6;

  --btn: #2D2BBF;
  --btnHover: #2523A8;

  --cardBorder: rgba(30,58,138,.12);
  --shadow: 0 10px 26px rgba(0,0,0,.08);
  --shadowSoft: 0 12px 22px rgba(0,0,0,.06);

  --radius: 18px;
  --padSide: 22px;

  --headerH: 56px;

  --warnBg: #FFD54A;
  --warnText: #111827;
}}

* {{ box-sizing: border-box !important; }}
html, body {{ margin:0 !important; padding:0 !important; height:100% !important; }}
.stApp {{ background:#FFFFFF !important; font-family: Inter, sans-serif !important; }}

[data-testid="stHeader"], footer, #MainMenu {{ display:none !important; }}
.block-container {{ padding:0 !important; margin:0 !important; }}
[data-testid="stMainViewContainer"] {{ padding:0 !important; margin:0 !important; }}

/* =========================
   LAYOUT ROOT
========================= */
#hero {{
  position: fixed;
  inset: 0;
  background: #FFFFFF;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 0;
}}

.hero-inner {{
  width: 420px;
  max-width: 94vw;
  margin: 0 auto;
  padding: 16px var(--padSide) 70px var(--padSide);
  text-align:center;
}}

label, small, .stCaption {{ display:none !important; }}

/* =========================
   TOP BAR (Dashboard/Processos)
========================= */
.topbar {{
  position: sticky;
  top: 0;
  z-index: 50;
  height: var(--headerH);
  display:flex;
  align-items:center;
  justify-content:center;
  background: var(--btn);
  color: #fff;
  font-weight: 900;
  letter-spacing: .06em;
  box-shadow: 0 10px 24px rgba(0,0,0,.10);
}}

.topbar-inner {{
  width: 420px;
  max-width: 94vw;
  padding: 0 var(--padSide);
  display:flex;
  align-items:center;
  justify-content:center;
  position: relative;
}}

.back-btn {{
  position: absolute;
  left: var(--padSide);
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display:flex;
  align-items:center;
  justify-content:center;
  color: rgba(255,255,255,.92);
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.20);
}}

.back-btn svg {{
  width: 18px; height: 18px;
}}

.back-btn:active {{
  transform: scale(.98);
}}

/* =========================
   LOGIN HERO (logo + nome)
========================= */
.logo-wrap {{
  width: 320px;
  max-width: 82vw;
  height: 250px;
  overflow: hidden;
  position: relative;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  margin: 0 auto 10px auto;
}}

.logo-img {{
  width: 185%;
  transform: translateY(-8px);
}}

.logo-wrap::after {{
  content:"";
  position:absolute;
  left:0; right:0; bottom:0;
  height: 88px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,.88) 55%,
    rgba(255,255,255,1) 100%);
}}

.brand {{
  width:100% !important;
  display:block !important;
  text-align:center !important;
  margin: 2px auto 0 auto !important;
  color: var(--brand);
  font-weight: 900;
  font-size: 32px;
  line-height: 1.05;
  letter-spacing: .10em;
  padding: 0 6px;
}}

.subtitle {{
  width:100% !important;
  display:block !important;
  text-align:center !important;
  margin: 10px auto 18px auto !important;
  color: var(--sub);
  font-weight: 800;
  font-size: 12px;
  line-height: 1;
  letter-spacing: .25em;
}}

/* =========================
   INPUT (sem borda feia)
========================= */
div[data-testid="stTextInput"] {{
  width: 100% !important;
}}

div[data-testid="stTextInput"] [data-baseweb="base-input"] {{
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
}}

div[data-testid="stTextInput"] [data-baseweb="input"] {{
  width:100% !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background: var(--inputBg) !important;
  border-radius: var(--radius) !important;
}}

div[data-testid="stTextInput"] input {{
  width:100% !important;
  height: 54px !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background: transparent !important;
  border-radius: var(--radius) !important;
  padding: 0 16px !important;
  font-size: 15px !important;
  color:#111827 !important;
  -webkit-appearance: none !important;
  appearance: none !important;
}}

div[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {{
  background: #FFFFFF !important;
  box-shadow: 0 0 0 2px rgba(45,43,191,.14) !important;
}}

div[data-testid="stTextInput"] input:invalid,
div[data-testid="stTextInput"] input:focus:invalid {{
  border:none !important;
  outline:none !important;
  box-shadow:none !important;
}}

div[data-testid="stTextInput"] input:-webkit-autofill,
div[data-testid="stTextInput"] input:-webkit-autofill:hover,
div[data-testid="stTextInput"] input:-webkit-autofill:focus {{
  -webkit-text-fill-color:#111827 !important;
  box-shadow: 0 0 0px 1000px var(--inputBg) inset !important;
  border:none !important;
  outline:none !important;
}}

/* =========================
   BUTTON PRIMARY
========================= */
.stButton {{
  width: 100% !important;
  margin-top: 12px !important;
}}

.stButton > button {{
  width: 100% !important;
  height: 54px !important;
  border-radius: var(--radius) !important;
  border: none !important;
  background: var(--btn) !important;
  color: #FFFFFF !important;
  font-weight: 800 !important;
  font-size: 16px !important;
  box-shadow: var(--shadow) !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  text-align:center !important;
  padding: 0 16px !important;
}}

.stButton > button:hover {{
  background: var(--btnHover) !important;
}}

.stButton > button:active {{
  transform: scale(.99) !important;
}}

/* =========================
   DASHBOARD USER CARD
========================= */
.user-card {{
  width: 100%;
  background: #FFFFFF;
  border: 1px solid var(--cardBorder);
  box-shadow: var(--shadowSoft);
  border-radius: 18px;
  padding: 14px 14px;
  display:flex;
  align-items:center;
  gap: 12px;
  margin-top: 14px;
  margin-bottom: 16px;
  text-align:left;
}}

.user-avatar {{
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: rgba(45,43,191,.10);
  border: 1px solid rgba(45,43,191,.18);
  display:flex;
  align-items:center;
  justify-content:center;
  color: var(--btn);
}}

.user-title {{
  font-size: 20px;
  font-weight: 900;
  color: var(--brand);
  line-height: 1.1;
}}

.user-sub {{
  font-size: 12px;
  font-weight: 800;
  color: var(--sub);
  letter-spacing: .10em;
  margin-top: 3px;
}}

/* =========================
   DASHBOARD ACTION CARDS (2 col)
========================= */
.action-grid {{
  width: 100%;
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 8px;
}}

.action-btn {{
  width: 100%;
  border-radius: 20px;
  border: 1px solid var(--cardBorder);
  background: #FFFFFF;
  box-shadow: var(--shadowSoft);
  padding: 18px 14px;
  display:flex;
  flex-direction: column;
  align-items:flex-start;
  justify-content:center;
  gap: 10px;
}}

.action-icon {{
  width: 44px;
  height: 44px;
  border-radius: 16px;
  display:flex;
  align-items:center;
  justify-content:center;
  background: rgba(45,43,191,.10);
  border: 1px solid rgba(45,43,191,.18);
  color: var(--btn);
}}

.action-label {{
  font-size: 14px;
  font-weight: 900;
  letter-spacing: .08em;
  color: var(--brand);
}}

.action-hint {{
  font-size: 12px;
  font-weight: 700;
  color: rgba(17,24,39,.55);
  margin-top: -4px;
}}

.action-btn:active {{
  transform: scale(.99);
}}

/* remover estilo feio do st.button wrapper pra esses cards */
div.action-click > div {{
  margin: 0 !important;
}}
div.action-click .stButton {{
  margin: 0 !important;
}}
div.action-click .stButton > button {{
  all: unset !important;
  display:block !important;
  width:100% !important;
}}
div.action-click .stButton > button:focus {{
  outline: none !important;
}}

/* =========================
   PROCESS CARDS
========================= */
.proc-card {{
  width:100%;
  border-radius: 18px;
  border: 1px solid var(--cardBorder);
  background: #FFFFFF;
  box-shadow: var(--shadowSoft);
  padding: 14px;
  margin-bottom: 12px;
  text-align:left;
}}

.proc-tag {{
  display:inline-block;
  background: var(--warnBg);
  color: var(--warnText);
  font-weight: 900;
  font-size: 10px;
  padding: 6px 10px;
  border-radius: 10px;
  letter-spacing: .06em;
  margin-bottom: 10px;
}}

.proc-label {{
  font-size: 11px;
  color: rgba(30,58,138,.70);
  font-weight: 800;
  letter-spacing: .02em;
}}

.proc-number {{
  font-size: 14px;
  color: #111827;
  font-weight: 900;
  margin-top: 6px;
}}

/* =========================
   COPYRIGHT
========================= */
.copy {{
  position: fixed;
  bottom: 14px;
  left: 0; right: 0;
  text-align:center;
  color: rgba(30,58,138,.45);
  font-size: 11px;
  letter-spacing: .14em;
  font-weight: 800;
  pointer-events:none;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# VIEWS
# =========================
def view_login():
    st.markdown('<div id="hero"><div class="hero-inner">', unsafe_allow_html=True)

    st.markdown(f"""
      <div class="logo-wrap">
        <img src="data:image/jpeg;base64,{logo_b64}" class="logo-img" />
      </div>
      <div class="brand">{APP_NAME}</div>
      <div class="subtitle">{SUBTITLE}</div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        cpf_visual = st.text_input(
            "CPF",
            value=st.session_state["cpf_visual"],
            placeholder="CPF (000.000.000-00)",
            label_visibility="collapsed",
        )

        digits = only_digits(cpf_visual)
        st.session_state["cpf_digits"] = digits
        st.session_state["cpf_visual"] = format_cpf(digits)

        submitted = st.form_submit_button("Verificar CPF", use_container_width=True)

        if submitted:
            if len(digits) != 11:
                st.error("CPF inválido.")
            elif digits == VALID_CPF:
                st.session_state["logado"] = True
                st.session_state["tela"] = "dashboard"
                st.rerun()
            else:
                st.error("CPF não cadastrado.")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)


def _back_svg():
    return """
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"
         xmlns="http://www.w3.org/2000/svg">
      <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2.4"
            stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """


def topbar(title: str, show_back: bool = False):
    back_html = ""
    if show_back:
        back_html = f"""
        <div class="back-btn" onclick="window.scrollTo(0,0)">
          {_back_svg()}
        </div>
        """

    st.markdown(
        f"""
        <div class="topbar">
          <div class="topbar-inner">
            {back_html}
            <div>{title}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def view_dashboard():
    st.markdown('<div id="hero">', unsafe_allow_html=True)
    topbar("Dashboard", show_back=False)
    st.markdown('<div class="hero-inner">', unsafe_allow_html=True)

    # User card (como o mock)
    st.markdown(
        f"""
        <div class="user-card">
          <div class="user-avatar">{ICON_USER}</div>
          <div>
            <div class="user-title">Olá, {CLIENT_NAME}</div>
            <div class="user-sub">Selecione uma opção</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Botões minimalistas (2 col) - sem emojis
    st.markdown('<div class="action-grid">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown('<div class="action-click">', unsafe_allow_html=True)
        if st.button(" ", key="go_processos", use_container_width=True):
            st.session_state["tela"] = "processos"
            st.rerun()
        st.markdown(
            f"""
            <div class="action-btn" onclick="document.querySelector('button[kind][data-testid],button').click()">
              <div class="action-icon">{ICON_DOC}</div>
              <div class="action-label">PROCESSOS</div>
              <div class="action-hint">Consultar andamento</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="action-click">', unsafe_allow_html=True)
        if st.button(" ", key="go_acordos", use_container_width=True):
            st.session_state["tela"] = "acordos"
            st.rerun()
        st.markdown(
            f"""
            <div class="action-btn" onclick="document.querySelectorAll('button')[document.querySelectorAll('button').length-1].click()">
              <div class="action-icon">{ICON_HANDSHAKE}</div>
              <div class="action-label">ACORDOS</div>
              <div class="action-hint">Ver propostas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Conteúdo da tela “acordos” (placeholder)
    if st.session_state.get("tela") == "acordos":
        st.info("Em atualização")

    # Sair
    if st.button("SAIR", use_container_width=True):
        st.session_state["logado"] = False
        st.session_state["tela"] = "login"
        st.session_state["cpf_visual"] = ""
        st.session_state["cpf_digits"] = ""
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)


def view_processos():
    st.markdown('<div id="hero">', unsafe_allow_html=True)
    topbar("Processos", show_back=True)
    st.markdown('<div class="hero-inner">', unsafe_allow_html=True)

    for p in PROCESSOS:
        st.markdown(
            f"""
            <div class="proc-card">
              <div class="proc-tag">AGUARDANDO ATUALIZAÇÃO</div>
              <div class="proc-label">Número do Processo</div>
              <div class="proc-number">{p}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("VOLTAR", use_container_width=True):
        st.session_state["tela"] = "dashboard"
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)

# =========================
# ROUTER
# =========================
if not st.session_state["logado"]:
    view_login()
else:
    if st.session_state["tela"] == "processos":
        view_processos()
    else:
        view_dashboard()