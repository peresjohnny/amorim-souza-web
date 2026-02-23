import re
import base64
import streamlit as st

APP_NAME = "AMORIM & SOUZA"
SUBTITLE = "ADVOCACIA"
VALID_CPF = "79897789120"  # exemplo

st.set_page_config(page_title=APP_NAME, layout="centered")

# =========================
# HELPERS
# =========================
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

# =========================
# LOGO ORIGINAL (SEU ARQUIVO)
# =========================
logo_b64 = get_base64("1000423374.jpg")

# =========================
# CSS LIMPO E FIEL AO MOCK
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
  --blueTop: #2D2BBF;
  --blueBot: #1F1C8F;
  --stroke: rgba(17,24,39,.10);
}

[data-testid="stHeader"], footer, #MainMenu{display:none;}
html, body{margin:0;padding:0;}

.stApp{
  background:#FFFFFF;
  font-family: Inter, sans-serif;
}

.block-container{
  padding-top:40px;
  padding-bottom:40px;
}

.page{
  min-height:100vh;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  text-align:center;
}

.logo{
  width:220px;
  max-width:70vw;
  margin-bottom:12px;
}

.brand{
  font-size:28px;
  font-weight:900;
  letter-spacing:.08em;
}

.subtitle{
  font-size:12px;
  letter-spacing:.25em;
  font-weight:700;
  color:rgba(0,0,0,.4);
  margin-bottom:25px;
}

/* Remove wrapper duplicado */
div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] > div > div{
  background:transparent !important;
  border:0 !important;
  box-shadow:none !important;
}

/* Input */
div[data-testid="stTextInput"] input{
  width:100% !important;
  max-width:360px;
  height:50px !important;
  border-radius:14px !important;
  border:1px solid var(--stroke) !important;
  padding:0 15px !important;
  font-size:15px !important;
  background:#F9FAFB !important;
}

div[data-testid="stTextInput"] input:focus{
  border:1px solid rgba(45,43,191,.5) !important;
  box-shadow:0 0 0 4px rgba(45,43,191,.12) !important;
  background:#FFF !important;
}

/* Botão */
div[data-testid="stFormSubmitButton"] > button{
  width:100% !important;
  max-width:360px;
  height:55px !important;
  border-radius:14px !important;
  border:none !important;
  background:linear-gradient(180deg,var(--blueTop),var(--blueBot)) !important;
  color:#FFF !important;
  font-size:16px !important;
  font-weight:800 !important;
  margin-top:15px;
}

label{display:none;}
</style>
""", unsafe_allow_html=True)

# =========================
# UI
# =========================
st.markdown('<div class="page">', unsafe_allow_html=True)

st.markdown(
    f'<img src="data:image/jpeg;base64,{logo_b64}" class="logo">',
    unsafe_allow_html=True
)

st.markdown(f'<div class="brand">{APP_NAME}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{SUBTITLE}</div>', unsafe_allow_html=True)

with st.form("cpf_form"):
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