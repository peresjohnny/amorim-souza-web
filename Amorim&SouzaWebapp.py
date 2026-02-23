import re
import base64
import streamlit as st

# =========================
# CONFIGURAÇÕES
# =========================
APP_NAME = "Amorim & Souza"
SUBTITLE = "ADVOCACIA"
LOGO_FILE = "1000423374.jpg"  # <-- manter esse nome (o mesmo do seu GitHub)

# Exemplo de CPF válido (troque/integre com sua base depois)
VALID_CPF = "79897789120"
CLIENT_NAME = "Edimar"

# Lista exemplo de processos (mantida)
PROCESSOS = [
    "0737767-85.2025.8.07.0001",
    "0757632-94.2025.8.07.0001",
    "0722313-65.2025.8.07.0001",
    "0768584-35.2025.8.07.0001",
    "0764797-95.2025.8.07.0001",
]

# =========================
# PÁGINA
# =========================
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
    """
    Validação simples por tamanho + comparação com um CPF autorizado.
    (Se você quiser validação matemática real do CPF, eu coloco aqui também.)
    """
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

# =========================
# ASSETS
# =========================
img_b64 = get_base64(LOGO_FILE)

# =========================
# CSS (ROBUSTO MOBILE)
# =========================
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root {{
  --blue: #2D2BBF;        /* azul do mock */
  --blue-hover: #2523A8;
  --text-blue: #153B7A;   /* azul do nome */
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

[data-testid="stMainViewContainer"] {{
  padding-top: 0rem !important;
}}

[data-testid="stMainBlockContainer"] {{
  max-width: 520px !important;
  padding-left: 18px !important;
  padding-right: 18px !important;
  padding-top: 0px !important;
  padding-bottom: 0px !important;
  margin: 0 auto !important;
}}

.top-spacer {{
  height: 6px;
}}

.hero {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  margin-top: 10px;
}}

.logo-wrap {{
  width: 100%;
  display:flex;
  justify-content:center;
  align-items:center;
  margin-top: 8px;
  margin-bottom: 8px;
}}

.logo-crop {{
  width: 220px;
  height: 250px;             /* controla o corte "na cintura" */
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}}

.logo-crop img {{
  width: 220px;
  height: auto;
  transform: translateY(-10px); /* ajuste fino do corte (sobe/desce) */
  user-select: none;
  -webkit-user-drag: none;
}}

.title {{
  margin-top: 8px;
  font-size: 34px;
  letter-spacing: 3px;
  font-weight: 900;
  color: var(--text-blue);
  text-align: center;
  width: 100%;
}}

.subtitle {{
  margin-top: 6px;
  font-size: 14px;
  letter-spacing: 6px;
  font-weight: 700;
  color: var(--muted);
  text-align: center;
  width: 100%;
}}

.form-wrap {{
  width: 100%;
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}}

div[data-testid="stTextInput"] {{
  width: 100% !important;
}}

div[data-testid="stTextInput"] input {{
  width: 100% !important;
  height: 54px !important;
  border-radius: 18px !important;
  border: 2px solid #D9DDEA !important;     /* sem borda vermelha/bugada */
  background: #FFFFFF !important;
  outline: none !important;
  box-shadow: none !important;
  font-size: 16px !important;
  padding: 0 16px !important;
}}

div[data-testid="stTextInput"] input:focus {{
  border: 2px solid rgba(45,43,191,.45) !important;
  box-shadow: 0 0 0 6px rgba(45,43,191,.10) !important;
}}

div[data-testid="stTextInput"] label {{
  display:none !important;
}}

.help {{
  margin-top: -4px;
  font-size: 13px;
  color: #7C879F;
  text-align: left;
  width: 100%;
}}

/* =========================
   BOTÃO FORÇADO AZUL DEFINITIVO
   ========================= */

.stForm button,
.stButton > button,
button[kind="primary"],
button[data-testid="baseButton-primary"] {{
    width: 100% !important;
    height: 56px !important;        /* menos grosso, estilo mock */
    border-radius: 18px !important;
    border: none !important;

    background-color: var(--blue) !important;
    color: #FFFFFF !important;

    font-weight: 800 !important;
    font-size: 16px !important;

    box-shadow: 0 10px 26px rgba(45,43,191,.22) !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    padding: 0 16px !important;
}}

.stForm button:hover,
.stButton > button:hover,
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {{
    background-color: var(--blue-hover) !important;
}}

.stForm button p,
.stButton > button p {{
  margin: 0 !important;
}}

.copyright {{
  width: 100%;
  text-align: center;
  color: #B0B8CC;
  font-size: 12px;
  letter-spacing: 3px;
  font-weight: 700;
  margin-top: 18px;
  margin-bottom: 10px;
}}

hr {{
  margin: 18px 0 !important;
  border: none !important;
  height: 1px !important;
  background: #EEF1F7 !important;
}}

/* DASHBOARD */
.dash-top {{
  width: 100%;
  margin-top: 8px;
}}

.hello {{
  font-size: 20px;
  font-weight: 800;
  color: var(--text-blue);
  margin-bottom: 12px;
}}

.card {{
  background: #fff;
  border: 1px solid #E8ECF6;
  border-radius: 16px;
  padding: 14px 14px;
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
  margin-bottom: 4px;
}}

.proc-num {{
  font-weight: 800;
  color: #1F2A44;
  font-size: 14px;
  word-break: break-word;
}}

.secondaryBtn button {{
  background: #FFFFFF !important;
  color: var(--text-blue) !important;
  border: 2px solid rgba(45,43,191,.25) !important;
  box-shadow: none !important;
}}

</style>
""",
    unsafe_allow_html=True,
)

# =========================
# UI - LOGIN PAGE
# =========================
def render_login():
    st.markdown('<div class="top-spacer"></div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero">
          <div class="logo-wrap">
            <div class="logo-crop">
              <img src="data:image/jpeg;base64,{img_b64}" />
            </div>
          </div>

          <div class="title">{APP_NAME.upper()}</div>
          <div class="subtitle">{SUBTITLE.upper()}</div>

          <div class="form-wrap">
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        cpf_input = st.text_input(
            "CPF",
            value=st.session_state.cpf,
            placeholder="CPF (000.000.000-00)",
            label_visibility="collapsed",
        )

        st.markdown('<div class="help">Use apenas números (11 dígitos).</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Verificar CPF")

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Persistir CPF no estado
    st.session_state.cpf = cpf_input

    # Ação do submit
    if submitted:
        cpf_digits = only_digits(cpf_input)
        if is_valid_cpf_digits(cpf_digits):
            st.session_state.logado = True
            st.session_state.tela = "dashboard"
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")

    st.markdown('<div class="copyright">© AMR SOFTWARES</div>', unsafe_allow_html=True)

# =========================
# UI - DASHBOARD PAGE
# =========================
def render_dashboard():
    st.markdown('<div class="dash-top"></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="hello">Olá, {CLIENT_NAME}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄  Processos", use_container_width=True):
            st.session_state.tela = "processos"
    with col2:
        if st.button("🤝  Acordos", use_container_width=True):
            st.session_state.tela = "acordos"

    st.markdown("<hr/>", unsafe_allow_html=True)

    if st.session_state.tela == "processos":
        for p in PROCESSOS:
            st.markdown(
                f"""
                <div class="card">
                  <div class="badge">ATUALIZAÇÕES</div>
                  <div class="proc-label">Número do Processo</div>
                  <div class="proc-num">{p}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif st.session_state.tela == "acordos":
        st.info("Em atualização")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Botão sair (secundário)
    st.markdown('<div class="secondaryBtn">', unsafe_allow_html=True)
    if st.button("Sair", use_container_width=True):
        st.session_state.logado = False
        st.session_state.tela = "login"
        st.session_state.cpf = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="copyright">© AMR SOFTWARES</div>', unsafe_allow_html=True)

# =========================
# ROUTER
# =========================
if not st.session_state.logado:
    render_login()
else:
    render_dashboard()