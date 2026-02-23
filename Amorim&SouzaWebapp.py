import re
import base64
import streamlit as st
from textwrap import dedent

APP_NAME = "AMORIM & SOUZA"
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


def md(html: str):
    """Renderiza HTML sem vazar como code block (remove indentação do markdown)."""
    st.markdown(dedent(html).strip("\n"), unsafe_allow_html=True)


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


st.session_state.setdefault("logado", False)
st.session_state.setdefault("tela", "login")  # login | dashboard | processos | acordos
st.session_state.setdefault("cpf_visual", "")
st.session_state.setdefault("cpf_digits", "")

logo_b64 = get_base64(LOGO_FILE)

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

BACK_SVG = """
<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"
     xmlns="http://www.w3.org/2000/svg">
  <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2.4"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

md(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
  --brand:#1E3A8A;
  --sub: rgba(30,58,138,.55);
  --inputBg:#F3F4F6;
  --blue:#2D2BBF;
  --blue2:#2523A8;
  --border: rgba(30,58,138,.12);
  --shadow: 0 12px 22px rgba(0,0,0,.06);
  --radius: 16px;
  --pad: 18px;
  --headerH: 54px;
  --warnBg:#FFD54A;
  --warnText:#111827;
}

*{ box-sizing:border-box !important; }
html, body{ margin:0 !important; padding:0 !important; height:100% !important; }
.stApp{ background:#FFFFFF !important; font-family:Inter,sans-serif !important; }

[data-testid="stHeader"], footer, #MainMenu{ display:none !important; }
.block-container{ padding:0 !important; margin:0 !important; }
[data-testid="stMainViewContainer"]{ padding:0 !important; margin:0 !important; }

#wrap{
  position:fixed;
  inset:0;
  background:#fff;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
}

.inner{
  width:420px;
  max-width:94vw;
  margin:0 auto;
  padding: 14px var(--pad) 72px var(--pad);
  text-align:center;
}

label, small, .stCaption{ display:none !important; }

.topbar{
  position:sticky;
  top:0;
  z-index:50;
  height:var(--headerH);
  display:flex;
  align-items:center;
  justify-content:center;
  background: var(--blue);
  color:#fff;
  font-weight:900;
  letter-spacing:.06em;
  box-shadow: 0 10px 24px rgba(0,0,0,.10);
}

.topbar-inner{
  width:420px;
  max-width:94vw;
  padding: 0 var(--pad);
  display:flex;
  align-items:center;
  justify-content:center;
  position:relative;
}

.icon-btn{
  position:absolute;
  left: var(--pad);
  top:50%;
  transform:translateY(-50%);
  width:38px;
  height:38px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.22);
  background: rgba(255,255,255,.12);
  display:flex;
  align-items:center;
  justify-content:center;
  color: rgba(255,255,255,.95);
  text-decoration:none;
}

.icon-btn svg{ width:18px; height:18px; }

.exit-link{
  position:absolute;
  right: var(--pad);
  top:50%;
  transform:translateY(-50%);
  font-size:12px;
  font-weight:900;
  letter-spacing:.10em;
  color: rgba(255,255,255,.95);
  text-decoration:none;
  padding: 10px 10px;
  border-radius: 10px;
  background: rgba(255,255,255,.10);
  border: 1px solid rgba(255,255,255,.18);
}

.user-card{
  width:100%;
  background:#fff;
  border:1px solid var(--border);
  border-radius:18px;
  box-shadow: var(--shadow);
  padding: 14px;
  display:flex;
  align-items:center;
  gap:12px;
  text-align:left;
  margin-top: 14px;
  margin-bottom: 14px;
}

.avatar{
  width:44px;
  height:44px;
  border-radius:14px;
  background: rgba(45,43,191,.10);
  border:1px solid rgba(45,43,191,.18);
  display:flex;
  align-items:center;
  justify-content:center;
  color: var(--blue);
}

.user-title{
  font-size:20px;
  font-weight:900;
  color: var(--brand);
  line-height:1.1;
}

.user-sub{
  margin-top:3px;
  font-size:12px;
  font-weight:800;
  letter-spacing:.10em;
  color: var(--sub);
}

.grid{
  width:100%;
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 8px;
}

.cardlink{
  display:flex;
  flex-direction:column;
  align-items:flex-start;
  gap:10px;
  padding: 16px;
  border-radius: 18px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  background:#fff;
  text-decoration:none;
  color: inherit;
  min-height: 132px;
}

.cardicon{
  width:44px;
  height:44px;
  border-radius:16px;
  display:flex;
  align-items:center;
  justify-content:center;
  background: rgba(45,43,191,.10);
  border:1px solid rgba(45,43,191,.18);
  color: var(--blue);
}

.cardtitle{
  font-size:14px;
  font-weight:900;
  letter-spacing:.08em;
  color: var(--brand);
}

.cardsub{
  font-size:12px;
  font-weight:700;
  color: rgba(17,24,39,.55);
  margin-top:-2px;
}

.proc-card{
  width:100%;
  border-radius:18px;
  border:1px solid var(--border);
  background:#fff;
  box-shadow: var(--shadow);
  padding: 14px;
  margin-bottom: 12px;
  text-align:left;
}

.proc-tag{
  display:inline-block;
  background: var(--warnBg);
  color: var(--warnText);
  font-weight:900;
  font-size:10px;
  padding: 6px 10px;
  border-radius:10px;
  letter-spacing:.06em;
  margin-bottom:10px;
}

.proc-label{
  font-size:11px;
  color: rgba(30,58,138,.70);
  font-weight:800;
}

.proc-number{
  font-size:14px;
  color:#111827;
  font-weight:900;
  margin-top:6px;
}

.copy{
  position:fixed;
  bottom:14px;
  left:0; right:0;
  text-align:center;
  color: rgba(30,58,138,.45);
  font-size:11px;
  letter-spacing:.14em;
  font-weight:800;
  pointer-events:none;
}

/* LOGIN (mantido) */
.logo-wrap{
  width: 320px;
  max-width: 82vw;
  height: 250px;
  overflow: hidden;
  position: relative;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  margin: 0 auto 10px auto;
}
.logo-img{
  width: 185%;
  transform: translateY(-8px);
}
.logo-wrap::after{
  content:"";
  position:absolute;
  left:0; right:0; bottom:0;
  height: 88px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,.88) 55%,
    rgba(255,255,255,1) 100%);
}
.brand{
  width:100%;
  display:block;
  text-align:center;
  margin: 2px auto 0 auto;
  color: var(--brand);
  font-weight: 900;
  font-size: 32px;
  line-height: 1.05;
  letter-spacing: .10em;
  padding: 0 6px;
}
.subtitle{
  width:100%;
  display:block;
  text-align:center;
  margin: 10px auto 18px auto;
  color: var(--sub);
  font-weight: 800;
  font-size: 12px;
  line-height: 1;
  letter-spacing: .25em;
}

/* INPUT sem borda feia */
div[data-testid="stTextInput"]{ width: 100% !important; }
div[data-testid="stTextInput"] [data-baseweb="base-input"]{
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
}
div[data-testid="stTextInput"] [data-baseweb="input"]{
  width:100% !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background: var(--inputBg) !important;
  border-radius: 18px !important;
}
div[data-testid="stTextInput"] input{
  width:100% !important;
  height: 54px !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background: transparent !important;
  border-radius: 18px !important;
  padding: 0 16px !important;
  font-size: 15px !important;
  color:#111827 !important;
}

/* botão login */
.stButton{ width:100% !important; margin-top:12px !important; }
.stButton > button{
  width:100% !important;
  height: 54px !important;
  border-radius: 18px !important;
  border: none !important;
  background: var(--blue) !important;
  color:#fff !important;
  font-weight: 900 !important;
  font-size: 16px !important;
  box-shadow: 0 10px 26px rgba(0,0,0,.08) !important;
}
.stButton > button:hover{ background: var(--blue2) !important; }
</style>
"""
)


def sync_route():
    params = st.query_params
    go = (params.get("go") or "").strip().lower()
    if go in {"dashboard", "processos", "acordos"}:
        st.session_state["tela"] = go


def goto(tela: str):
    st.session_state["tela"] = tela
    st.query_params.clear()
    st.query_params["go"] = tela
    st.rerun()


def logout():
    st.session_state["logado"] = False
    st.session_state["tela"] = "login"
    st.session_state["cpf_visual"] = ""
    st.session_state["cpf_digits"] = ""
    st.query_params.clear()
    st.rerun()


def topbar(title: str, show_back: bool, back_to: str, show_exit: bool):
    back_html = ""
    exit_html = ""
    if show_back:
        # target="_self" para NÃO abrir nova aba no mobile
        back_html = f'<a class="icon-btn" href="?go={back_to}" target="_self" rel="noopener">{BACK_SVG}</a>'
    if show_exit:
        exit_html = '<a class="exit-link" href="?go=logout" target="_self" rel="noopener">SAIR</a>'

    md(
        f"""
<div class="topbar">
  <div class="topbar-inner">
    {back_html}
    <div>{title}</div>
    {exit_html}
  </div>
</div>
"""
    )


def view_login():
    md('<div id="wrap"><div class="inner">')

    md(
        f"""
<div class="logo-wrap">
  <img src="data:image/jpeg;base64,{logo_b64}" class="logo-img" />
</div>
<div class="brand">{APP_NAME}</div>
<div class="subtitle">{SUBTITLE}</div>
"""
    )

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
                goto("dashboard")
            else:
                st.error("CPF não cadastrado.")

    md("</div></div>")
    md('<div class="copy">© AMR SOFTWARES</div>')


def view_dashboard():
    md('<div id="wrap">')
    topbar("Dashboard", show_back=False, back_to="dashboard", show_exit=True)
    md('<div class="inner">')

    md(
        f"""
<div class="user-card">
  <div class="avatar">{ICON_USER}</div>
  <div>
    <div class="user-title">Olá, {CLIENT_NAME}</div>
    <div class="user-sub">Selecione uma opção</div>
  </div>
</div>
"""
    )

    # target="_self" evita abrir outra aba no mobile
    md(
        f"""
<div class="grid">
  <a class="cardlink" href="?go=processos" target="_self" rel="noopener">
    <div class="cardicon">{ICON_DOC}</div>
    <div class="cardtitle">PROCESSOS</div>
    <div class="cardsub">Consultar andamento</div>
  </a>

  <a class="cardlink" href="?go=acordos" target="_self" rel="noopener">
    <div class="cardicon">{ICON_HANDSHAKE}</div>
    <div class="cardtitle">ACORDOS</div>
    <div class="cardsub">Ver propostas</div>
  </a>
</div>
"""
    )

    md("</div></div>")
    md('<div class="copy">© AMR SOFTWARES</div>')


def view_processos():
    md('<div id="wrap">')
    topbar("Processos", show_back=True, back_to="dashboard", show_exit=True)
    md('<div class="inner">')

    for p in PROCESSOS:
        md(
            f"""
<div class="proc-card">
  <div class="proc-tag">AGUARDANDO ATUALIZAÇÃO</div>
  <div class="proc-label">Número do Processo</div>
  <div class="proc-number">{p}</div>
</div>
"""
        )

    md("</div></div>")
    md('<div class="copy">© AMR SOFTWARES</div>')


def view_acordos():
    md('<div id="wrap">')
    topbar("Acordos", show_back=True, back_to="dashboard", show_exit=True)
    md('<div class="inner">')

    st.info("Em atualização")

    md("</div></div>")
    md('<div class="copy">© AMR SOFTWARES</div>')


sync_route()

if st.query_params.get("go") == "logout":
    logout()

if not st.session_state["logado"]:
    view_login()
else:
    tela = st.session_state["tela"]
    if tela == "processos":
        view_processos()
    elif tela == "acordos":
        view_acordos()
    else:
        view_dashboard()