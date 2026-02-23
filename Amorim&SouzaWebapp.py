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
  --brand: #1E3A8A;
  --sub: rgba(30,58,138,.55);
  --stroke: rgba(17,24,39,.10);
  --inputBg: #F9FAFB;
  --btn: #1F2DBF;     /* azul flat mock */
  --btnHover: #1A27A8;
  --radius: 18px;
}

*{ box-sizing:border-box !important; }

[data-testid="stHeader"], footer, #MainMenu{display:none !important;}
html, body{ margin:0 !important; padding:0 !important; height:100% !important; }
body{ overflow:hidden !important; }

.stApp{
  background:#FFFFFF !important;
  font-family:Inter, sans-serif !important;
}
.block-container{
  padding:0 !important;
  margin:0 !important;
}
[data-testid="stMainViewContainer"]{
  padding:0 !important;
  margin:0 !important;
}

/* ===== overlay para NÃO ter scroll e NÃO ter “vazio” ===== */
#hero{
  position:fixed !important;
  inset:0 !important;
  background:#FFFFFF !important;

  display:flex !important;
  align-items:center !important;
  justify-content:center !important;

  padding: 22px 18px 62px 18px !important; /* espaço pro copyright */
  overflow:hidden !important;
}

/* ===== o segredo: wrapper central fixo ===== */
.hero-inner{
  width: 360px !important;
  max-width: 92vw !important;
  margin: 0 auto !important;

  display:flex !important;
  flex-direction:column !important;
  align-items:center !important;
  justify-content:center !important;

  text-align:center !important;
}

/* força qualquer markdown a respeitar centralização */
#hero .stMarkdown,
#hero [data-testid="stMarkdown"]{
  width:100% !important;
  display:block !important;
  margin:0 auto !important;
  text-align:center !important;
}

/* ===== LOGO: crop na cintura sem comer mão ===== */
.logo-wrapper{
  width: 320px;
  max-width: 82vw;
  height: 260px;
  overflow:hidden;
  position:relative;
  display:flex;
  align-items:flex-start;
  justify-content:center;
  margin: 0 auto 10px auto;
}
.logo{
  width: 190%;
  height:auto;
  transform: translateY(-14px); /* cintura, mão preservada */
  display:block;
}
.logo-wrapper::after{
  content:"";
  position:absolute;
  left:0; right:0; bottom:0;
  height: 86px;
  background: linear-gradient(
    180deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,.82) 55%,
    rgba(255,255,255,1) 100%
  );
  pointer-events:none;
}

/* ===== TEXTOS ===== */
.brand{
  width:100%;
  font-size:32px;
  font-weight:900;
  letter-spacing:.10em;
  color: var(--brand);
  margin: 2px 0 2px 0;
  text-align:center;
}
.subtitle{
  width:100%;
  font-size:12px;
  letter-spacing:.25em;
  font-weight:800;
  color: var(--sub);
  margin: 0 0 18px 0;
  text-align:center;
}

/* ===== FORM / INPUT / BOTÃO: tudo 100% do wrapper ===== */
#hero form{
  width:100% !important;
  max-width:100% !important;
  margin:0 auto !important;
}

div[data-testid="stTextInput"],
div[data-testid="stFormSubmitButton"]{
  width:100% !important;
  max-width:100% !important;
  margin:0 auto !important;
}

/* mata wrappers “espertinhos” do Streamlit */
div[data-testid="stFormSubmitButton"] > div,
div[data-testid="stFormSubmitButton"] .stButton,
div[data-testid="stFormSubmitButton"] .stButton > div{
  width:100% !important;
  max-width:none !important;
  display:block !important;
  margin:0 !important;
  padding:0 !important;
}

/* input */
div[data-testid="stTextInput"] input{
  width:100% !important;
  height:56px !important;
  border-radius: var(--radius) !important;
  border:1px solid var(--stroke) !important;
  padding:0 16px !important;
  font-size:15px !important;
  background: var(--inputBg) !important;
}
div[data-testid="stTextInput"] input:focus{
  border:1px solid rgba(31,45,191,.45) !important;
  box-shadow:0 0 0 4px rgba(31,45,191,.12) !important;
  background:#FFF !important;
}

/* botão (full width real + flat) */
div[data-testid="stFormSubmitButton"]{
  margin-top: 14px !important;
}
div[data-testid="stFormSubmitButton"] button{
  width:100% !important;
  min-width:100% !important;
  max-width:none !important;

  height:64px !important;
  border-radius: var(--radius) !important;
  border:none !important;

  background: var(--btn) !important;
  color:#FFF !important;
  font-size:17px !important;
  font-weight:800 !important;

  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  text-align:center !important;

  box-shadow: 0 4px 14px rgba(0,0,0,.10) !important; /* flat */
}
div[data-testid="stFormSubmitButton"] button:hover{
  background: var(--btnHover) !important;
}
div[data-testid="stFormSubmitButton"] button:active{
  transform: scale(.98) !important;
}

/* remove labels/captions */
label, small, .stCaption{display:none !important;}

/* copyright fixo */
.copy{
  position:fixed;
  left:0; right:0;
  bottom: 14px;
  text-align:center;
  font-size:11px;
  letter-spacing:.14em;
  font-weight:700;
  color: rgba(30,58,138,.45);
  pointer-events:none;
}
</style>
""",
    unsafe_allow_html=True
)

# ===== estrutura =====
st.markdown('<div id="hero"><div class="hero-inner">', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="logo-wrapper">
      <img src="data:image/jpeg;base64,{logo_b64}" class="logo" />
    </div>
    <div class="brand">{APP_NAME}</div>
    <div class="subtitle">{SUBTITLE}</div>
    """,
    unsafe_allow_html=True
)

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

st.markdown("</div></div>", unsafe_allow_html=True)
st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)