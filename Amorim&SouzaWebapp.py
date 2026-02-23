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


# ===== State =====
st.session_state.setdefault("logado", False)
st.session_state.setdefault("tela", "login")  # login | dashboard | processos | acordos
st.session_state.setdefault("cpf_visual", "")
st.session_state.setdefault("cpf_digits", "")

logo_b64 = get_base64(LOGO_FILE)

# ===== CSS =====
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

/* container full-screen */
#wrap{
  position:fixed;
  inset:0;
  background:#fff;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
}

/* Topbar fixa (resolve a faixa branca em cima) */
.topbar{
  position:fixed;
  top:0;
  left:0;
  right:0;
  z-index:9999;
  height: calc(var(--headerH) + env(safe-area-inset-top));
  padding-top: env(safe-area-inset-top);
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
  height: var(--headerH);
}

.topbar-title{
  font-weight:900;
}

.topbar-actions{
  position:absolute;
  right: var(--pad);
  top:50%;
  transform: translateY(-50%);
}

/* Conteúdo começa abaixo da topbar */
.inner{
  width:420px;
  max-width:94vw;
  margin:0 auto;
  padding: calc(var(--headerH) + env(safe-area-inset-top) + 14px) var(--pad) 72px var(--pad);
  text-align:center;
}

label, small, .stCaption{ display:none !important; }

/* Botão SAIR no topo: pequeno e alinhado */
.topbar-actions .stButton{
  width:auto !important;
  margin:0 !important;
}
.topbar-actions .stButton > button{
  width:auto !important;
  height:38px !important;
  min-height:38px !important;
  padding: 0 12px !important;
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,.20) !important;
  background: rgba(255,255,255,.12) !important;
  color: rgba(255,255,255,.95) !important;
  font-weight: 900 !important;
  font-size: 12px !important;
  letter-spacing: .10em !important;
  box-shadow: none !important;
  text-align:center !important;
}
.topbar-actions .stButton > button:hover{
  background: rgba(255,255,255,.18) !important;
}

/* User card */
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
  font-size:20px;
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

/* Cards = botões (sem hyperlink, sem “ponto preto”) */
.card-grid{ width:100%; margin-top: 8px; }
.card-grid .stButton{ width:100% !important; margin:0 !important; }
.card-grid .stButton > button{
  width:100% !important;
  min-height: 132px !important;
  border-radius: 18px !important;
  border: 1px solid var(--border) !important;
  background:#fff !important;
  color: #111827 !important;
  box-shadow: var(--shadow) !important;
  padding: 16px !important;
  text-align:left !important;

  display:flex !important;
  flex-direction:column !important;
  align-items:flex-start !important;
  justify-content:flex-start !important;

  white-space: pre-line !important; /* permite \n */
  font-weight: 900 !important;
  font-size: 14px !important;
}
.card-grid .stButton > button:hover{
  border-color: rgba(30,58,138,.22) !important;
}
.card-grid .stButton > button:focus{
  outline: none !important;
  box-shadow: var(--shadow) !important;
}
.card-grid .stButton > button:active{
  transform: translateY(0px) !important;
}

/* Processos cards */
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

/* LOGIN */
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

/* TextInput */
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

/* Submit do form (azul) */
div[data-testid="stFormSubmitButton"] .stButton > button,
div[data-testid="stFormSubmitButton"] button{
  min-height: 54px !important;
  height: 54px !important;
  border-radius: 18px !important;
  border: none !important;
  background: var(--blue) !important;
  color:#fff !important;
  font-weight: 900 !important;
  font-size: 16px !important;
  box-shadow: 0 10px 26px rgba(0,0,0,.08) !important;
  align-items:center !important;
  justify-content:center !important;
  text-align:center !important;
}
div[data-testid="stFormSubmitButton"] button:hover{
  background: var(--blue2) !important;
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
</style>
"""
)


def goto(tela: str):
    st.session_state["tela"] = tela
    st.rerun()


def logout():
    st.session_state["logado"] = False
    st.session_state["tela"] = "login"
    st.session_state["cpf_visual"] = ""
    st.session_state["cpf_digits"] = ""
    st.rerun()


def topbar(title: str, show_exit: bool):
    md(
        f"""
<div class="topbar">
  <div class="topbar-inner">
    <div class="topbar-title">{title}</div>
  </div>
</div>
"""
    )
    if show_exit:
        # Renderiza o botão no canto direito por cima da barra
        md('<div class="topbar"><div class="topbar-inner"><div class="topbar-actions">')
        if st.button("SAIR", key=f"exit_{title}"):
            logout()
        md("</div></div></div>")


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
    topbar("Dashboard", show_exit=True)
    md('<div class="inner">')

    md(
        f"""
<div class="user-card">
  <div class="avatar">👤</div>
  <div>
    <div class="user-title">Olá, {CLIENT_NAME}</div>
    <div class="user-sub">Selecione uma opção</div>
  </div>
</div>
"""
    )

    md('<div class="card-grid">')
    c1, c2 = st.columns(2, gap="large")

    with c1:
        # Botão-card: 2 linhas sem hyperlink
        if st.button("📄  PROCESSOS\nConsultar andamento", key="go_processos"):
            goto("processos")

    with c2:
        if st.button("🤝  ACORDOS\nVer propostas", key="go_acordos"):
            goto("acordos")
    md("</div>")

    md("</div></div>")
    md('<div class="copy">© AMR SOFTWARES</div>')


def view_processos():
    md('<div id="wrap">')
    topbar("Processos", show_exit=True)
    md('<div class="inner">')

    # Voltar como botão normal (sem hack)
    if st.button("◀  Voltar", key="back_proc"):
        goto("dashboard")

    md("<div style='height:10px'></div>")

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
    topbar("Acordos", show_exit=True)
    md('<div class="inner">')

    if st.button("◀  Voltar", key="back_acord"):
        goto("dashboard")

    md("<div style='height:10px'></div>")
    st.info("Em atualização")

    md("</div></div>")
    md('<div class="copy">© AMR SOFTWARES</div>')


# ===== Router =====
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