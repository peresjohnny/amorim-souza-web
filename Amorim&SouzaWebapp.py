import re
import base64
import streamlit as st

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
    return len(cpf_digits) == 11 and cpf_digits == VALID_CPF


if "logado" not in st.session_state:
    st.session_state.logado = False
if "tela" not in st.session_state:
    st.session_state.tela = "login"
if "cpf" not in st.session_state:
    st.session_state.cpf = ""

img_b64 = get_base64(LOGO_FILE)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
  --blue:#2D2BBF;
  --blue-hover:#2523A8;
  --text-blue:#153B7A;
  --muted:#8A97B0;
  --border:#D9DDEA;
  --shadow: 0 12px 26px rgba(0,0,0,.10);
}

html, body, [class*="stApp"]{
  background:#fff !important;
  font-family:'Inter', sans-serif !important;
}

[data-testid="stHeader"], footer, #MainMenu{ display:none !important; }

section.main > div{ padding-top: 0rem !important; }

[data-testid="stMainBlockContainer"]{
  max-width: 520px !important;
  padding-left: 18px !important;
  padding-right: 18px !important;
  margin: 0 auto !important;
}

.hero{
  display:flex;
  flex-direction:column;
  align-items:center;
  text-align:center;
  margin-top: 10px;
}

.logo-crop{
  width: 240px;
  height: 260px;
  overflow:hidden;
  display:flex;
  justify-content:center;
  align-items:flex-start;
}

.logo-crop img{
  width: 240px;
  transform: translateY(-6px);
}

.title{
  margin-top: 10px;
  font-size: 34px;
  letter-spacing: 3px;
  font-weight: 900;
  color: var(--text-blue);
  line-height: 1.05;
  text-align:center;
}

.subtitle{
  margin-top: 8px;
  font-size: 14px;
  letter-spacing: 6px;
  font-weight: 800;
  color: var(--muted);
  text-align:center;
}

.center-wrap{
  width:100%;
  margin: 18px auto 0 auto;
}

div[data-testid="stTextInput"]{
  width:100% !important;
}

div[data-testid="stTextInput"] input{
  width:100% !important;
  height: 54px !important;
  border-radius: 18px !important;
  border: 2px solid var(--border) !important;
  background:#fff !important;
  font-size: 16px !important;
  padding: 0 16px !important;
  outline: none !important;
  box-shadow: none !important;
}

div[data-testid="stTextInput"] input:focus{
  border: 2px solid rgba(45,43,191,.45) !important;
  box-shadow: 0 0 0 6px rgba(45,43,191,.10) !important;
  outline: none !important;
}

.stButton > button,
button[kind="primary"],
button[data-testid="baseButton-primary"]{
  width:100% !important;
  height: 54px !important;
  border-radius: 18px !important;
  border: none !important;
  background: var(--blue) !important;
  color: #fff !important;
  font-weight: 900 !important;
  font-size: 16px !important;
  box-shadow: var(--shadow) !important;
}

.stButton > button:hover,
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover{
  background: var(--blue-hover) !important;
}

.stButton > button:focus{
  outline: none !important;
  box-shadow: 0 0 0 6px rgba(45,43,191,.10), var(--shadow) !important;
}

.copyright{
  text-align:center;
  color:#B0B8CC;
  font-size:12px;
  letter-spacing:3px;
  font-weight:800;
  margin-top: 18px;
}
</style>
""",
    unsafe_allow_html=True,
)


def render_login():
    st.markdown(
        f"""
        <div class="hero">
            <div class="logo-crop">
                <img src="data:image/jpeg;base64,{img_b64}" />
            </div>
            <div class="title">{APP_NAME.upper()}</div>
            <div class="subtitle">{SUBTITLE.upper()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_m, col_r = st.columns([1, 10, 1])
    with col_m:
        st.markdown('<div class="center-wrap">', unsafe_allow_html=True)

        cpf_input = st.text_input(
            "CPF",
            value=st.session_state.cpf,
            placeholder="CPF (000.000.000-00)",
            label_visibility="collapsed",
        )
        st.session_state.cpf = cpf_input

        clicked = st.button("Verificar CPF", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if clicked:
            if is_valid_cpf_digits(cpf_input):
                st.session_state.logado = True
                st.session_state.tela = "dashboard"
                st.rerun()
            else:
                st.error("CPF não cadastrado.")

    st.markdown('<div class="copyright">© AMR SOFTWARES</div>', unsafe_allow_html=True)


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
            st.markdown(
                f"""
                <div style="
                    background:#fff;
                    border:1px solid #E8ECF6;
                    border-radius:16px;
                    padding:14px;
                    margin-bottom:10px;
                    box-shadow:0 8px 24px rgba(0,0,0,.06);
                    position:relative;">
                  <div style="
                      position:absolute;
                      right:10px;
                      top:10px;
                      background:#FFD24A;
                      color:#000;
                      font-size:10px;
                      font-weight:900;
                      padding:4px 8px;
                      border-radius:8px;">ATUALIZAÇÕES</div>
                  <div style="font-size:11px;color:#7C879F;">Número do Processo</div>
                  <div style="font-weight:900;color:#1F2A44;font-size:14px;">{p}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif st.session_state.tela == "acordos":
        st.info("Em atualização")

    if st.button("Sair", use_container_width=True):
        st.session_state.logado = False
        st.session_state.tela = "login"
        st.session_state.cpf = ""
        st.rerun()

    st.markdown('<div class="copyright">© AMR SOFTWARES</div>', unsafe_allow_html=True)


if not st.session_state.logado:
    render_login()
else:
    render_dashboard()