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

logo_b64 = get_base64("1000423374.jpg")  # NOME ORIGINAL

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
  --blueBrand: #1E3A8A;
  --blueTop: #2D2BBF;
  --blueBot: #1F1C8F;
  --stroke: rgba(17,24,39,.10);
  --radius: 18px;
  --shadowBtn: 0 18px 40px rgba(0,0,0,.18);
  --shadowBtnHover: 0 24px 54px rgba(0,0,0,.22);
}

/* Remove chrome do Streamlit */
[data-testid="stHeader"], footer, #MainMenu{display:none !important;}
html, body{margin:0 !important; padding:0 !important; height:100% !important;}
body{overflow:hidden !important;}              /* <<< SEM ROLAGEM */

/* App clean */
.stApp{
  background:#FFFFFF !important;
  font-family: Inter, sans-serif !important;
}

/* Mata paddings que criam “buraco” */
.block-container{
  padding:0 !important;
  margin:0 !important;
}

/* Container principal do Streamlit (garante centralização) */
[data-testid="stMainViewContainer"]{
  padding:0 !important;
  margin:0 !important;
}

/* ====== SOLUÇÃO DEFINITIVA: tela fixa full-screen ======
   Mesmo que o Streamlit injete margens, isso fica por cima e centraliza tudo.
*/
#hero{
  position: fixed;
  inset: 0;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  background:#FFFFFF;
  overflow:hidden;                 /* sem scroll */
  padding: 24px 18px;
  text-align:center;
}

/* Largura “app-like” */
.hero-inner{
  width:100%;
  max-width: 380px;
  display:flex;
  flex-direction:column;
  align-items:center;
}

/* ===== LOGO: maior + crop real ===== */
.logo-wrapper{
  width: 300px;          /* <<< maior */
  max-width: 78vw;
  height: 230px;         /* “cintura” */
  overflow:hidden;
  position:relative;
  display:flex;
  align-items:flex-start;
  justify-content:center;
  margin-bottom: 10px;
}

/* zoom real + deslocamento */
.logo{
  width: 185%;           /* <<< zoom forte (porque seu jpg tem ar branco) */
  height: auto;
  transform: translateY(-28px); /* <<< sobe pra cortar a cintura */
  display:block;
}

/* fade premium */
.logo-wrapper::after{
  content:"";
  position:absolute;
  left:0; right:0; bottom:0;
  height: 76px;
  background: linear-gradient(
    180deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,0.82) 55%,
    rgba(255,255,255,1) 100%
  );
  pointer-events:none;
}

/* Textos */
.brand{
  font-size: 32px;
  font-weight: 900;
  letter-spacing: .10em;
  color: var(--blueBrand);
  margin: 2px 0 2px 0;
}

.subtitle{
  font-size: 12px;
  letter-spacing: .25em;
  font-weight: 800;
  color: rgba(30, 58, 138, .55);
  margin: 0 0 18px 0;
}

/* ===== INPUT E BOTÃO: mesma largura, centralizados ===== */
.form-wrap{
  width: 100%;
  max-width: 360px;
  margin: 0 auto;
}

/* tira wrappers do input */
div[data-testid="stTextInput"]{ width:100% !important; }
div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] > div > div,
div[data-testid="stTextInput"] > div > div > div{
  background:transparent !important;
  border:0 !important;
  box-shadow:none !important;
  padding:0 !important;
  margin:0 !important;
}

/* input */
div[data-testid="stTextInput"] input{
  width:100% !important;
  height:56px !important;
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

/* submit wrapper */
div[data-testid="stFormSubmitButton"]{
  width:100% !important;
  margin-top: 14px !important;
}

/* ===== botão: força full width em QUALQUER caso ===== */
div[data-testid="stFormSubmitButton"] button,
button[kind="primary"],
.stButton > button{
  width:100% !important;
  min-width:100% !important;
  height:64px !important;                /* <<< grande como no mock */
  border-radius: 18px !important;
  border:none !important;
  background: linear-gradient(180deg, var(--blueTop), var(--blueBot)) !important;
  color:#FFF !important;
  font-size: 17px !important;
  font-weight: 800 !important;
  box-shadow: var(--shadowBtn) !important;

  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  text-align:center !important;
  padding:0 !important;

  transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
  position:relative;
  overflow:hidden;
}

div[data-testid="stFormSubmitButton"] button::before,
button[kind="primary"]::before,
.stButton > button::before{
  content:"";
  position:absolute;
  top:-30%;
  left:-60%;
  width: 50%;
  height: 160%;
  background: linear-gradient(120deg, rgba(255,255,255,0), rgba(255,255,255,.22), rgba(255,255,255,0));
  transform: rotate(18deg);
  opacity: 0;
}

div[data-testid="stFormSubmitButton"] button:hover,
button[kind="primary"]:hover,
.stButton > button:hover{
  transform: translateY(-1px);
  box-shadow: var(--shadowBtnHover) !important;
  filter: brightness(1.03);
}
div[data-testid="stFormSubmitButton"] button:hover::before,
button[kind="primary"]:hover::before,
.stButton > button:hover::before{
  animation: sheen .85s ease;
  opacity: 1;
}
div[data-testid="stFormSubmitButton"] button:active,
button[kind="primary"]:active,
.stButton > button:active{
  transform: translateY(0px) scale(.99);
  filter: brightness(.99);
  box-shadow: var(--shadowBtn) !important;
}

@keyframes sheen{
  0%   { left:-60%; opacity:0; }
  20%  { opacity:1; }
  100% { left:120%; opacity:0; }
}

small, .stCaption { display:none !important; }
label{display:none !important;}
</style>
""",
    unsafe_allow_html=True
)

# ====== UI em camada fixa (hero) ======
st.markdown('<div id="hero"><div class="hero-inner">', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="logo-wrapper">
      <img src="data:image/jpeg;base64,{logo_b64}" class="logo"/>
    </div>
    <div class="brand">{APP_NAME}</div>
    <div class="subtitle">{SUBTITLE}</div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="form-wrap">', unsafe_allow_html=True)

with st.form("cpf_form", clear_on_submit=False):
    cpf_visual = st.text_input(
        "CPF",
        value=st.session_state["cpf_visual"],
        placeholder="CPF (000.000.000-00)",
        label_visibility="collapsed",
    )

    cpf_digits = only_digits(cpf_visual)
    st.session_state["cpf_digits"] = cpf_digits
    st.session_state["cpf_visual"] = format_cpf_digits(cpf_digits)

    submitted = st.form_submit_button("Verificar CPF")

st.markdown('</div>', unsafe_allow_html=True)  # form-wrap

# mensagens abaixo do form (ainda dentro do hero)
if submitted:
    if len(st.session_state["cpf_digits"]) != 11:
        st.error("CPF inválido.")
    elif st.session_state["cpf_digits"] == VALID_CPF:
        st.success("CPF verificado com sucesso.")
    else:
        st.error("CPF não cadastrado.")

st.markdown('</div></div>', unsafe_allow_html=True)  # hero-inner + hero