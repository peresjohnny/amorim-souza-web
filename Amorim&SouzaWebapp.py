import re
import base64
import streamlit as st

APP_NAME = "AMORIM & SOUZA"
SUBTITLE = "ADVOCACIA"

VALID_CPF = "79897789120"  # exemplo
CLIENT_NAME = "Edimar"      # exemplo

PROCESSOS = [
    "0737767-85.2025.8.07.0001",
    "0757632-94.2025.8.07.0001",
    "0722313-65.2025.8.07.0001",
    "0768584-35.2025.8.07.0001",
    "0764797-95.2025.8.07.0001",
]

st.set_page_config(page_title=APP_NAME, layout="centered")

def get_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def only_digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")

def format_cpf_digits(d: str) -> str:
    d = only_digits(d)[:11]
    if len(d) <= 3: return d
    if len(d) <= 6: return f"{d[:3]}.{d[3:]}"
    if len(d) <= 9: return f"{d[:3]}.{d[3:6]}.{d[6:]}"
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

# ===== STATE =====
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "tela" not in st.session_state:
    st.session_state["tela"] = "login"  # login | dashboard | processos
if "cpf_visual" not in st.session_state:
    st.session_state["cpf_visual"] = ""
if "cpf_digits" not in st.session_state:
    st.session_state["cpf_digits"] = ""

logo_b64 = get_base64("1000423374.jpg")  # nome ORIGINAL no GitHub

# ===== CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
  --brand: #1E3A8A;
  --sub: rgba(30,58,138,.55);
  --inputBg: #F3F4F6;
  --btn: #2D2BBF;
  --btnHover:#2523A8;
  --radius:18px;
}

*{box-sizing:border-box !important;}
[data-testid="stHeader"], footer, #MainMenu{display:none !important;}
html, body{margin:0 !important; padding:0 !important; height:100% !important;}
body{overflow:hidden !important;}
.stApp{background:#FFFFFF !important; font-family:Inter,sans-serif !important;}
.block-container{padding:0 !important; margin:0 !important;}
[data-testid="stMainViewContainer"]{padding:0 !important; margin:0 !important;}

/* ====== FULLSCREEN WRAPPER ====== */
#hero{
  position:fixed;
  inset:0;
  background:#FFFFFF;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:22px 18px 60px 18px;
  overflow:hidden;
}
.hero-inner{
  width:360px;
  max-width:92vw;
  margin:0 auto;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  text-align:center;
}

/* centraliza markdown */
#hero .stMarkdown, #hero [data-testid="stMarkdown"]{
  width:100% !important;
  margin:0 auto !important;
  text-align:center !important;
}

/* ===== LOGO LOGIN ===== */
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
  background:linear-gradient(180deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,.82) 55%,
    rgba(255,255,255,1) 100%);
}

/* ===== TEXT ===== */
.brand{
  font-size:32px;
  font-weight:900;
  letter-spacing:.10em;
  color:var(--brand);
  margin:2px 0;
}
.subtitle{
  font-size:12px;
  letter-spacing:.25em;
  font-weight:800;
  color:var(--sub);
  margin-bottom:18px;
}

/* ===== INPUT ===== */
div[data-testid="stTextInput"]{ width:100% !important; }
div[data-testid="stTextInput"] input{
  width:100% !important;
  height:56px !important;
  border-radius:var(--radius) !important;
  border:none !important;
  outline:none !important;
  padding:0 16px !important;
  font-size:15px !important;
  background:var(--inputBg) !important;
}
div[data-testid="stTextInput"] input:focus{
  box-shadow:0 0 0 2px rgba(31,45,191,.22) !important;
  background:#FFFFFF !important;
}

/* ===== BUTTON ===== */
.stButton{ width:100% !important; }
.stButton > button{
  width:100% !important;
  height:64px !important;
  border-radius:var(--radius) !important;
  border:none !important;
  background:var(--btn) !important;
  color:#FFF !important;
  font-size:17px !important;
  font-weight:800 !important;
  box-shadow:0 4px 12px rgba(0,0,0,.12) !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  text-align:center !important;
}
.stButton > button:hover{ background:var(--btnHover) !important; }
.stButton > button:active{ transform:scale(.98) !important; }

label, small, .stCaption{display:none !important;}

/* ===== DASHBOARD ===== */
.topbar{
  width:100%;
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:14px;
}
.hello{
  font-size:18px;
  font-weight:800;
  color:var(--brand);
}
.card-row{
  width:100%;
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:12px;
  margin:10px 0 18px 0;
}
.action{
  background:#FFFFFF;
  border:1px solid rgba(30,58,138,.12);
  border-radius:16px;
  padding:14px 12px;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
  font-weight:800;
  color:var(--brand);
  box-shadow:0 6px 18px rgba(0,0,0,.06);
}
.action span{font-size:18px;}
.section-title{
  width:100%;
  text-align:left;
  font-weight:900;
  color:var(--brand);
  margin:4px 0 10px 0;
  font-size:14px;
}
.pcard{
  width:100%;
  background:#FFFFFF;
  border:1px solid rgba(30,58,138,.10);
  border-radius:14px;
  padding:14px 14px;
  margin-bottom:10px;
  box-shadow:0 6px 18px rgba(0,0,0,.05);
}
.badge{
  display:inline-block;
  font-size:10px;
  font-weight:900;
  padding:4px 8px;
  border-radius:8px;
  background:#FFDD57;
  color:#111827;
  margin-bottom:10px;
}
.pnum{
  font-weight:900;
  color:#111827;
  letter-spacing:.02em;
}

/* copyright */
.copy{
  position:fixed;
  bottom:14px;
  left:0; right:0;
  text-align:center;
  font-size:11px;
  letter-spacing:.14em;
  font-weight:700;
  color:rgba(30,58,138,.45);
  pointer-events:none;
}
</style>
""", unsafe_allow_html=True)

# ====== VIEWS ======

def view_login():
    st.markdown('<div id="hero"><div class="hero-inner">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="logo-wrapper">
      <img src="data:image/jpeg;base64,{logo_b64}" class="logo"/>
    </div>
    <div class="brand">{APP_NAME}</div>
    <div class="subtitle">{SUBTITLE}</div>
    """, unsafe_allow_html=True)

    cpf_visual = st.text_input(
        "CPF",
        value=st.session_state["cpf_visual"],
        placeholder="CPF (000.000.000-00)",
        label_visibility="collapsed",
    )

    cpf_digits = only_digits(cpf_visual)
    st.session_state["cpf_digits"] = cpf_digits
    st.session_state["cpf_visual"] = format_cpf_digits(cpf_digits)

    if st.button("Verificar CPF", use_container_width=True):
        if len(cpf_digits) != 11:
            st.error("CPF inválido.")
        elif cpf_digits == VALID_CPF:
            st.session_state["logado"] = True
            st.session_state["tela"] = "dashboard"
            st.rerun()
        else:
            st.error("CPF não cadastrado.")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)


def view_dashboard():
    st.markdown('<div id="hero"><div class="hero-inner">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="topbar">
      <div class="hello">Olá, {CLIENT_NAME}</div>
    </div>
    """, unsafe_allow_html=True)

    # Ações
    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("📄  Processos", use_container_width=True):
            st.session_state["tela"] = "processos"
            st.rerun()
    with c2:
        if st.button("🤝  Acordos", use_container_width=True):
            st.warning("Em atualização.")

    st.markdown('<div class="section-title">Últimos Processos</div>', unsafe_allow_html=True)

    for p in PROCESSOS[:3]:
        st.markdown(f"""
        <div class="pcard">
          <div class="badge">ATUALIZAÇÕES</div>
          <div class="pnum">{p}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Sair", use_container_width=True):
        st.session_state["logado"] = False
        st.session_state["tela"] = "login"
        st.session_state["cpf_visual"] = ""
        st.session_state["cpf_digits"] = ""
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)


def view_processos():
    st.markdown('<div id="hero"><div class="hero-inner">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="topbar">
      <div class="hello">Processos</div>
    </div>
    """, unsafe_allow_html=True)

    for p in PROCESSOS:
        st.markdown(f"""
        <div class="pcard">
          <div class="badge">AGUARDANDO ATUALIZAÇÃO</div>
          <div class="pnum">{p}</div>
        </div>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("Voltar", use_container_width=True):
            st.session_state["tela"] = "dashboard"
            st.rerun()
    with c2:
        if st.button("Sair", use_container_width=True):
            st.session_state["logado"] = False
            st.session_state["tela"] = "login"
            st.session_state["cpf_visual"] = ""
            st.session_state["cpf_digits"] = ""
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)


# ===== ROUTER =====
if not st.session_state["logado"]:
    view_login()
else:
    if st.session_state["tela"] == "dashboard":
        view_dashboard()
    elif st.session_state["tela"] == "processos":
        view_processos()
    else:
        st.session_state["tela"] = "dashboard"
        st.rerun()