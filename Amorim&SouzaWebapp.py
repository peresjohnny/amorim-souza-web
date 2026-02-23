import re
import base64
import streamlit as st

# =========================
# CONFIG
# =========================
APP_NAME = "AMORIM & SOUZA"
SUBTITLE = "ADVOCACIA"
LOGO_FILE = "1000423374.jpg"  # NOME ORIGINAL
VALID_CPF = "79897789120"     # exemplo
CLIENT_NAME = "Edimar"        # exemplo

PROCESSOS = [
    "0737767-85.2025.8.07.0001",
    "0757632-94.2025.8.07.0001",
    "0722313-65.2025.8.07.0001",
    "0768584-35.2025.8.07.0001",
    "0764797-95.2025.8.07.0001",
]

st.set_page_config(page_title=APP_NAME, layout="centered")

# =========================
# HELPERS
# =========================
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

# =========================
# STATE
# =========================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("tela", "login")  # login | dashboard | processos
st.session_state.setdefault("cpf_visual", "")
st.session_state.setdefault("cpf_digits", "")

logo_b64 = get_base64(LOGO_FILE)

# =========================
# CSS (ROBUSTO)
# =========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root {{
  --brand: #1E3A8A;
  --sub: rgba(30,58,138,.55);
  --inputBg: #F3F4F6;

  /* >>> BOTÃO AZUL (mock) <<< */
  --btn: #2D2BBF;
  --btnHover: #2523A8;

  --cardBorder: rgba(30,58,138,.12);
  --shadow: 0 10px 26px rgba(0,0,0,.08);
  --radius: 18px;
  --padSide: 24px;
}}

* {{ box-sizing: border-box !important; }}
html, body {{ margin:0 !important; padding:0 !important; height:100% !important; }}
body {{ overflow:hidden !important; }}
.stApp {{ background:#FFFFFF !important; font-family: Inter, sans-serif !important; }}

[data-testid="stHeader"], footer, #MainMenu {{ display:none !important; }}
.block-container {{ padding:0 !important; margin:0 !important; }}
[data-testid="stMainViewContainer"] {{ padding:0 !important; margin:0 !important; }}

#hero {{
  position: fixed;
  inset: 0;
  background: #FFFFFF;
  display:flex;
  align-items:center;
  justify-content:center;
  overflow:hidden;
  padding: 16px var(--padSide) 56px var(--padSide);
}}

.hero-inner {{
  width: 380px;
  max-width: 92vw;
  display:flex;
  flex-direction: column;
  align-items:center;
  justify-content:center;
  text-align:center !important;
}}

#hero .stMarkdown,
#hero [data-testid="stMarkdown"],
#hero .element-container,
#hero [data-testid="stVerticalBlock"] {{
  width:100% !important;
  text-align:center !important;
  margin:0 auto !important;
}}

.logo-wrap {{
  width: 320px;
  max-width: 82vw;
  height: 250px;
  overflow: hidden;
  position: relative;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  margin: 0 auto 10px auto;
}}

.logo-img {{
  width: 185%;
  transform: translateY(-8px);
}}

.logo-wrap::after {{
  content:"";
  position:absolute;
  left:0; right:0; bottom:0;
  height: 88px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,.88) 55%,
    rgba(255,255,255,1) 100%);
}}

/* >>> CENTRALIZAÇÃO FORÇADA DO NOME + SUBTÍTULO <<< */
.brand {{
  width:100% !important;
  display:block !important;
  text-align:center !important;
  margin: 2px auto 0 auto !important;
  color: var(--brand);
  font-weight: 900;
  font-size: 32px;
  line-height: 1.05;
  letter-spacing: .10em;
  padding: 0 6px;
}}

.subtitle {{
  width:100% !important;
  display:block !important;
  text-align:center !important;
  margin: 10px auto 18px auto !important;
  color: var(--sub);
  font-weight: 800;
  font-size: 12px;
  line-height: 1;
  letter-spacing: .25em;
}}

/* INPUT: matar borda do wrapper */
div[data-testid="stTextInput"] {{
  width: 100% !important;
}}

div[data-testid="stTextInput"] [data-baseweb="base-input"] {{
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
}}

div[data-testid="stTextInput"] [data-baseweb="input"] {{
  width:100% !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background: var(--inputBg) !important;
  border-radius: var(--radius) !important;
}}

div[data-testid="stTextInput"] input {{
  width:100% !important;
  height: 54px !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background: transparent !important;
  border-radius: var(--radius) !important;
  padding: 0 16px !important;
  font-size: 15px !important;
  color:#111827 !important;
  -webkit-appearance: none !important;
  appearance: none !important;
}}

div[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {{
  background: #FFFFFF !important;
  box-shadow: 0 0 0 2px rgba(45,43,191,.14) !important;
}}

div[data-testid="stTextInput"] input:invalid,
div[data-testid="stTextInput"] input:focus:invalid {{
  border:none !important;
  outline:none !important;
  box-shadow:none !important;
}}

div[data-testid="stTextInput"] input:-webkit-autofill,
div[data-testid="stTextInput"] input:-webkit-autofill:hover,
div[data-testid="stTextInput"] input:-webkit-autofill:focus {{
  -webkit-text-fill-color:#111827 !important;
  box-shadow: 0 0 0px 1000px var(--inputBg) inset !important;
  border:none !important;
  outline:none !important;
}}

/* BOTÃO full width, azul */
.stButton {{
  width: 100% !important;
  margin-top: 12px !important;
}}

.stButton > button {{
  width: 100% !important;
  height: 54px !important;
  border-radius: var(--radius) !important;
  border: none !important;
  background: var(--btn) !important;
  color: #FFFFFF !important;
  font-weight: 800 !important;
  font-size: 16px !important;
  box-shadow: var(--shadow) !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  text-align:center !important;
  padding: 0 16px !important;
}}

.stButton > button:hover {{
  background: var(--btnHover) !important;
}}

.stButton > button:active {{
  transform: scale(.99) !important;
}}

label, small, .stCaption {{ display:none !important; }}

/* copyright fixo */
.copy {{
  position: fixed;
  bottom: 14px;
  left: 0; right: 0;
  text-align:center;
  color: rgba(30,58,138,.45);
  font-size: 11px;
  letter-spacing: .14em;
  font-weight: 700;
  pointer-events:none;
}}

/* Dashboard */
.dash-title {{
  color: var(--brand);
  font-weight: 900;
  font-size: 22px;
  letter-spacing: .03em;
  margin: 0 0 10px 0;
  text-align:center;
}}

.dash-sub {{
  color: var(--sub);
  font-weight: 700;
  font-size: 12px;
  letter-spacing: .10em;
  margin: 0 0 12px 0;
  text-align:center;
}}

.card {{
  width:100%;
  border-radius: 16px;
  border: 1px solid var(--cardBorder);
  background: #FFFFFF;
  box-shadow: 0 12px 22px rgba(0,0,0,.05);
  padding: 14px;
  margin-bottom: 10px;
  text-align:left;
}}

.tag {{
  display:inline-block;
  background: #FFD54A;
  color:#111827;
  font-weight: 900;
  font-size: 10px;
  padding: 4px 8px;
  border-radius: 8px;
  letter-spacing: .06em;
  margin-bottom: 10px;
}}

.proc-label {{
  font-size: 11px;
  color: rgba(30,58,138,.70);
  font-weight: 700;
}}

.proc-number {{
  font-size: 14px;
  color: #111827;
  font-weight: 800;
  margin-top: 6px;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# VIEWS
# =========================
def view_login():
    st.markdown('<div id="hero"><div class="hero-inner">', unsafe_allow_html=True)

    st.markdown(f"""
      <div class="logo-wrap">
        <img src="data:image/jpeg;base64,{logo_b64}" class="logo-img" />
      </div>
      <div class="brand">{APP_NAME}</div>
      <div class="subtitle">{SUBTITLE}</div>
    """, unsafe_allow_html=True)

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
                st.session_state["tela"] = "dashboard"
                st.rerun()
            else:
                st.error("CPF não cadastrado.")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)

def view_dashboard():
    st.markdown('<div id="hero"><div class="hero-inner">', unsafe_allow_html=True)

    st.markdown(f"<div class='dash-title'>Olá, {CLIENT_NAME}</div>", unsafe_allow_html=True)
    st.markdown("<div class='dash-sub'>Selecione uma opção</div>", unsafe_allow_html=True)

    colA, colB = st.columns(2, gap="small")

    with colA:
        if st.button("📄  PROCESSOS", use_container_width=True):
            st.session_state["tela"] = "processos"
            st.rerun()

    with colB:
        if st.button("🤝  ACORDOS", use_container_width=True):
            st.warning("Em atualização")

    if st.session_state["tela"] == "processos":
        st.markdown("<div class='dash-sub' style='margin-top:10px;'>Últimos processos</div>", unsafe_allow_html=True)
        for p in PROCESSOS:
            st.markdown(f"""
              <div class="card">
                <div class="tag">ATUALIZAÇÕES</div>
                <div class="proc-label">Número do Processo</div>
                <div class="proc-number">{p}</div>
              </div>
            """, unsafe_allow_html=True)

    if st.button("SAIR", use_container_width=True):
        st.session_state["logado"] = False
        st.session_state["tela"] = "login"
        st.session_state["cpf_visual"] = ""
        st.session_state["cpf_digits"] = ""
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="copy">© AMR SOFTWARES</div>', unsafe_allow_html=True)

# =========================
# ROUTER
# =========================
if not st.session_state["logado"]:
    view_login()
else:
    view_dashboard()