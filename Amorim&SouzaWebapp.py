import re
import base64
import streamlit as st

# =========================
# CONFIG
# =========================
APP_NAME = "Amorim & Souza"
SUBTITLE = "ADVOCACIA"
LOGO_FILE = "1000423374.jpg"

VALID_CPF = "79897789120"
CLIENT_NAME = "Edimar"

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
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def only_digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")

def is_valid_cpf_digits(cpf_digits: str) -> bool:
    cpf_digits = only_digits(cpf_digits)
    if len(cpf_digits) != 11:
        return False
    return cpf_digits == VALID_CPF

# =========================
# SESSION STATE
# =========================
if "logado" not in st.session_state:
    st.session_state.logado = False
if "tela" not in st.session_state:
    st.session_state.tela = "login"
if "cpf" not in st.session_state:
    st.session_state.cpf = ""

img_b64 = get_base64(LOGO_FILE)

# =========================
# CSS
# =========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root {{
  --blue: #2D2BBF;
  --blue-hover: #2523A8;
  --text-blue: #153B7A;
  --muted: #8A97B0;
  --bg: #ffffff;
  --shadow: 0 14px 32px rgba(0,0,0,.10);
}}

html, body, [class*="stApp"] {{
  background: var(--bg) !important;
  font-family: 'Inter', sans-serif !important;
}}

[data-testid="stHeader"], footer, #MainMenu {{
  display: none !important;
}}

section.main > div {{
  padding-top: 0rem !important;
}}

[data-testid="stMainBlockContainer"] {{
  max-width: 520px !important;
  padding-left: 18px !important;
  padding-right: 18px !important;
  margin: 0 auto !important;
}}

.hero {{
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-top: 10px;
}}

.logo-crop {{
  width: 220px;
  height: 250px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}}

.logo-crop img {{
  width: 220px;
  transform: translateY(-10px);
}}

.title {{
  margin-top: 8px;
  font-size: 34px;
  letter-spacing: 3px;
  font-weight: 900;
  color: var(--text-blue);
}}

.subtitle {{
  margin-top: 6px;
  font-size: 14px;
  letter-spacing: 6px;
  font-weight: 700;
  color: var(--muted);
}}

div[data-testid="stTextInput"] input {{
  width: 100% !important;
  height: 54px !important;
  border-radius: 18px !important;
  border: 2px solid #D9DDEA !important;
  background: #FFFFFF !important;
  font-size: 16px !important;
  padding: 0 16px !important;
}}

div[data-testid="stTextInput"] input:focus {{
  border: 2px solid rgba(45,43,191,.45) !important;
  box-shadow: 0 0 0 6px rgba(45,43,191,.10) !important;
}}

.stForm button,
.stButton > button,
button[kind="primary"],
button[data-testid="baseButton-primary"] {{
    width: 100% !important;
    height: 56px !important;
    border-radius: 18px !important;
    border: none !important;
    background-color: var(--blue) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    box-shadow: var(--shadow) !important;
}}

.stForm button:hover,
.stButton > button:hover,
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {{
    background-color: var(--blue-hover) !important;
}}

.card {{
  background: #fff;
  border: 1px solid #E8ECF6;
  border-radius: 16px;
  padding: 14px;
  margin-bottom: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,.06);
  position: relative;
}}

.badge {{
  position: absolute;
  right: 10px;
  top: 10px;
  background: #FFD24A;
  color: #000;
  font-size: 10px;
  font-weight: 900;
  padding: 4px 8px;
  border-radius: 8px;
}}

.proc-label {{
  font-size: 11px;
  color: #7C879F;
}}

.proc-num {{
  font-weight: 800;
  color: #1F2A44;
  font-size: 14px;
}}

.copyright {{
  text-align: center;
  color: #B0B8CC;
  font-size: 12px;
  letter-spacing: 3px;
  font-weight: 700;
  margin-top: 20px;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================
def render_login():
    st.markdown(f"""
    <div class="hero">
        <div class="logo-crop">
            <img src="data:image/jpeg;base64,{img_b64}" />
        </div>
        <div class="title">{APP_NAME.upper()}</div>
        <div class="subtitle">{SUBTITLE.upper()}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        cpf_input = st.text_input(
            "CPF",
            value=st.session_state.cpf,
            placeholder="CPF (000.000.000-00)",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Verificar CPF")

    st.session_state.cpf = cpf_input

    if submitted:
        if is_valid_cpf_digits(cpf_input):
            st.session_state.logado = True
            st.session_state.tela = "dashboard"
            st.rerun()
        else:
            st.error("CPF não cadastrado.")

    st.markdown('<div class="copyright">© AMR SOFTWARES</div>', unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
def render_dashboard():
    st.markdown(f"<h3>Olá, {CLIENT_NAME}</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Processos", use_container_width=True):
            st.session_state.tela = "processos"
    with col2:
        if st.button("🤝 Acordos", use_container_width=True):
            st.session_state.tela = "acordos"

    if st.session_state.tela == "processos":
        for p in PROCESSOS:
            st.markdown(f"""
            <div class="card">
                <div class="badge">ATUALIZAÇÕES</div>
                <div class="proc-label">Número do Processo</div>
                <div class="proc-num">{p}</div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.tela == "acordos":
        st.info("Em atualização")

    if st.button("Sair", use_container_width=True):
        st.session_state.logado = False
        st.session_state.tela = "login"
        st.session_state.cpf = ""
        st.rerun()

    st.markdown('<div class="copyright">© AMR SOFTWARES</div>', unsafe_allow_html=True)

# =========================
# ROUTER
# =========================
if not st.session_state.logado:
    render_login()
else:
    render_dashboard()