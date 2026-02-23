import re
import base64
import streamlit as st

APP_NAME = "AMORIM & SOUZA"
SUBTITLE = "ADVOCACIA"
VALID_CPF = "79897789120"  # exemplo

st.set_page_config(page_title=APP_NAME, layout="centered")

def get_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def only_digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")

def format_cpf_digits(d: str) -> str:
    d = only_digits(d)[:11]
    if len(d) <= 3:
        return d
    if len(d) <= 6:
        return f"{d[:3]}.{d[3:]}"
    if len(d) <= 9:
        return f"{d[:3]}.{d[3:6]}.{d[6:]}"
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

if "cpf_visual" not in st.session_state:
    st.session_state["cpf_visual"] = ""
if "cpf_digits" not in st.session_state:
    st.session_state["cpf_digits"] = ""

# logo original do seu github
logo_b64 = get_base64("1000423374.jpg")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
  --blueBrand: #1E3A8A;
  --blueTop: #2D2BBF;
  --blueBot: #1F1C8F;
  --stroke: rgba(17,24,39,.10);
  --radius: 16px;
  --shadowBtn: 0 16px 34px rgba(0,0,0,.16);
  --shadowBtnHover: 0 22px 44px rgba(0,0,0,.18);
}

[data-testid="stHeader"], footer, #MainMenu{display:none !important;}
html, body{margin:0 !important; padding:0 !important;}

.stApp{
  background:#FFFFFF !important;
  font-family: Inter, sans-serif !important;
}

[data-testid="stMainViewContainer"] > div:first-child{
  max-width: 430px !important;
  margin: 0 auto !important;
  padding-left: 18px !important;
  padding-right: 18px !important;
}

.block-container{
  padding-top: 0px !important;
  padding-bottom: 28px !important;
}

/* ====== FIX DO "PARECE EM BRANCO" NO MOBILE ======
   Usa viewport dinâmica e coloca conteúdo no topo, sem empurrar pra baixo */
.page{
  min-height: 100svh;         /* iOS/Android moderno */
  min-height: 100dvh;         /* fallback */
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:flex-start; /* NÃO centraliza vertical */
  text-align:center;
  padding-top: 40px;          /* ajuste fino */
}

/* ===== Logo cortada (na cintura) + fade ===== */
.logo-wrapper{
  width: 230px;
  height: 175px;              /* <<< CORTE REAL: diminui altura */
  overflow: hidden;
  margin: 0 auto 8px auto;
  display: flex;
  justify-content: center;
  position: relative;
}

.logo{
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 5%; /* <<< puxa mais pra cima (cintura corta) */
  display:block;
}

.logo-wrapper::after{
  content:"";
  position:absolute;
  left:0;
  right:0;
  bottom:0;
  height: 70px;
  background: linear-gradient(
    180deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,0.80) 55%,
    rgba(255,255,255,1) 100%
  );
  pointer-events:none;
}

/* Nome em azul legível */
.brand{
  font-size: 30px;
  font-weight: 900;
  letter-spacing: .10em;
  color: var(--blueBrand) !important;
  margin-top: 6px;
}

/* Subtitulo */
.subtitle{
  font-size: 12px;
  letter-spacing: .25em;
  font-weight: 800;
  color: rgba(30, 58, 138, .55);
  margin-bottom: 22px;
}

/* Remove wrapper fantasma do input */
div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] > div > div,
div[data-testid="stTextInput"] > div > div > div{
  background:transparent !important;
  border:0 !important;
  box-shadow:none !important;
  padding:0 !important;
  margin:0 !important;
  height:auto !important;
  min-height:0 !important;
}

/* Input */
div[data-testid="stTextInput"] input{
  width:100% !important;
  max-width:360px !important;
  height:54px !important;
  border-radius: var(--radius) !important;
  border:1px solid var(--stroke) !important;
  padding:0 16px !important;
  font-size:15px !important;
  background:#F9FAFB !important;
}
div[data-testid="stTextInput"] input:focus{
  border:1px solid rgba(45,43,191,.45) !important;
  box-shadow:0 0 0 4px rgba(45,43,191,.12) !important;
  background:#FFF !important;
}

/* ===== BOTÃO: MESMA LARGURA DO INPUT (FULL) =====
   Não depende do DOM exato do Streamlit: pega o primary por atributo */
div[data-testid="stFormSubmitButton"]{
  width: 100% !important;
  max-width: 360px !important;
  margin: 16px auto 0 auto !important;
  display:block !important;
}

/* pega o botão primário mesmo que o Streamlit mude o wrapper */
button[kind="primary"]{
  width: 100% !important;
  max-width: 360px !important;
  height: 60px !important;
  border-radius: 16px !important;
  border: none !important;
  background: linear-gradient(180deg, var(--blueTop), var(--blueBot)) !important;
  color: #FFF !important;
  font-size: 17px !important;
  font-weight: 800 !important;
  box-shadow: var(--shadowBtn) !important;

  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  padding: 0 !important;

  transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
}

button[kind="primary"]:hover{
  transform: translateY(-1px);
  box-shadow: var(--shadowBtnHover) !important;
  filter: brightness(1.03);
}

button[kind="primary"]:active{
  transform: translateY(0px) scale(.99);
  filter: brightness(.99);
  box-shadow: var(--shadowBtn) !important;
}

small, .stCaption { display:none !important; }
label{display:none !important;}
</style>
""",
    unsafe_allow_html=True
)

st.markdown('<div class="page">', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="logo-wrapper">
        <img src="data:image/jpeg;base64,{logo_b64}" class="logo">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(f'<div class="brand">{APP_NAME}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{SUBTITLE}</div>', unsafe_allow_html=True)

with st.form("cpf_form", clear_on_submit=False):
    cpf_visual = st.text_input(
        "CPF",
        value=st.session_state["cpf_visual"],
        placeholder="CPF (000.000.000-00)",
        label_visibility="collapsed"
    )

    cpf_digits = only_digits(cpf_visual)
    st.session_state["cpf_digits"] = cpf_digits
    st.session_state["cpf_visual"] = format_cpf_digits(cpf_digits)

    submitted = st.form_submit_button("Verificar CPF")

if submitted:
    if len(st.session_state["cpf_digits"]) != 11:
        st.error("CPF inválido.")
    elif st.session_state["cpf_digits"] == VALID_CPF:
        st.success("CPF verificado com sucesso.")
    else:
        st.error("CPF não cadastrado.")

st.markdown("</div>", unsafe_allow_html=True)