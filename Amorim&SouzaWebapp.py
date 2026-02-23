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

logo_b64 = get_base64("1000423374.jpg")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

*{ box-sizing:border-box !important; }

[data-testid="stHeader"], footer, #MainMenu{display:none !important;}
html, body{margin:0 !important; padding:0 !important; height:100% !important;}
body{overflow:hidden !important;}

.stApp{ background:#FFFFFF !important; font-family:Inter,sans-serif !important; }
.block-container{ padding:0 !important; margin:0 !important; }

#hero{
  position:fixed !important;
  inset:0 !important;
  display:flex !important;
  flex-direction:column !important;
  align-items:center !important;
  justify-content:center !important;
  padding:22px 18px 60px 18px !important;
  background:#FFFFFF !important;
  text-align:center !important;
}

/* ===== LOGO ===== */
.logo-wrapper{
  width:320px;
  max-width:82vw;
  height:260px;
  overflow:hidden;
  position:relative;
  display:flex;
  align-items:flex-start;
  justify-content:center;
  margin:0 auto 10px auto;
}

.logo{
  width:190%;
  transform:translateY(-14px);
}

.logo-wrapper::after{
  content:"";
  position:absolute;
  left:0; right:0; bottom:0;
  height:86px;
  background:linear-gradient(
    180deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,.82) 55%,
    rgba(255,255,255,1) 100%
  );
}

.brand{
  font-size:32px;
  font-weight:900;
  letter-spacing:.10em;
  color:#1E3A8A;
  margin:2px 0;
}

.subtitle{
  font-size:12px;
  letter-spacing:.25em;
  font-weight:800;
  color:rgba(30,58,138,.55);
  margin-bottom:18px;
}

/* ===== FORM ===== */
#hero form{
  width:100% !important;
  max-width:360px !important;
  margin:0 auto !important;
}

/* ===== INPUT ===== */
div[data-testid="stTextInput"]{
  width:100% !important;
  max-width:360px !important;
  margin:0 auto !important;
}

div[data-testid="stTextInput"] input{
  width:100% !important;
  height:56px !important;
  border-radius:18px !important;
  border:1px solid rgba(17,24,39,.10) !important;
  padding:0 16px !important;
  font-size:15px !important;
  background:#F9FAFB !important;
}

div[data-testid="stTextInput"] input:focus{
  border:1px solid rgba(45,43,191,.45) !important;
  box-shadow:0 0 0 4px rgba(45,43,191,.12) !important;
  background:#FFF !important;
}

/* =======================================================
   ===== BOTÃO FINAL (FULL WIDTH REAL + FLAT STYLE) =====
   ======================================================= */

#hero [data-testid="stFormSubmitButton"]{
  width:100% !important;
  max-width:360px !important;
  margin:14px auto 0 auto !important;
}

#hero [data-testid="stFormSubmitButton"] > div,
#hero .stButton,
#hero .stButton > div{
  width:100% !important;
  max-width:none !important;
  display:block !important;
  margin:0 !important;
  padding:0 !important;
}

#hero button{
  width:100% !important;
  min-width:100% !important;
  max-width:none !important;
  height:64px !important;

  border-radius:18px !important;
  border:none !important;

  background:#1F2DBF !important;   /* azul flat do mock */
  color:#FFFFFF !important;
  font-size:17px !important;
  font-weight:800 !important;

  text-align:center !important;

  box-shadow:0 4px 14px rgba(0,0,0,.12) !important; /* sombra suave */
  transition:all .15s ease;
}

#hero button:hover{
  background:#1A27A8 !important;
}

#hero button:active{
  transform:scale(.98) !important;
}

/* ===== COPYRIGHT ===== */
.copy{
  position:fixed;
  bottom:14px;
  left:0;
  right:0;
  text-align:center;
  font-size:11px;
  letter-spacing:.14em;
  font-weight:700;
  color:rgba(30,58,138,.45);
}

label, small, .stCaption{display:none !important;}

</style>
""", unsafe_allow_html=True)

st.markdown('<div id="hero">', unsafe_allow_html=True)

st.markdown(f"""
<div class="logo-wrapper">
  <img src="data:image/jpeg;base64,{logo_b64}" class="logo"/>
</div>
<div class="brand">{APP_NAME}</div>
<div class="subtitle">{SUBTITLE}</div>
""", unsafe_allow_html=True)

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

if submitted:
    if len(st.session_state["cpf_digits"]) != 11:
        st.error("CPF inválido.")
    elif st.session_state["cpf_digits"] == VALID_CPF:
        st.success("CPF verificado com sucesso.")
    else:
        st.error("CPF não cadastrado.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)