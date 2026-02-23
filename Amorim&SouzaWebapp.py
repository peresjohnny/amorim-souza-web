import re
import base64
import streamlit as st

APP_NAME = "Amorim & Souza"
VALID_CPF = "79897789120"  # exemplo

st.set_page_config(page_title=APP_NAME, layout="centered", initial_sidebar_state="collapsed")

def get_base64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

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

if "logged" not in st.session_state:
    st.session_state["logged"] = False
if "cpf_input" not in st.session_state:
    st.session_state["cpf_input"] = ""
if "cpf_digits" not in st.session_state:
    st.session_state["cpf_digits"] = ""

img_b64 = get_base64("1000423374.jpg")

# =========================
# CSS: topbar FIXO + remove gap do Streamlit + visual “app”
# =========================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

:root{
  --bg: #EFF4F9;
  --blue: #0E4E86;
  --blue2:#0B3E6B;
  --text:#12202B;
  --muted:#607283;
  --stroke: rgba(12, 62, 107, .16);
  --shadowTop: 0 20px 42px rgba(11, 62, 107, 0.22);
  --shadowCard: 0 18px 40px rgba(16, 24, 40, 0.10);
  --shadowSoft: 0 10px 24px rgba(16, 24, 40, 0.08);
  --radius: 22px;
}

/* remove chrome */
[data-testid="stHeader"], footer, #MainMenu{ display:none !important; }

/* zerar padding/margem “culpados” do gap */
html, body { margin:0 !important; padding:0 !important; }
.stApp{
  margin:0 !important;
  padding:0 !important;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif !important;
  background:
    radial-gradient(900px 450px at 50% -160px, rgba(14,78,134,.22), transparent 65%),
    linear-gradient(180deg, rgba(255,255,255,.40) 0%, rgba(255,255,255,0) 36%),
    var(--bg) !important;
}

/* container mobile */
[data-testid="stMainViewContainer"] > div:first-child{
  max-width: 430px !important;
  margin: 0 auto !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
}

/* isso aqui é o que costuma criar o “gap” acima */
.block-container{
  padding-top: 0rem !important;
  padding-bottom: max(env(safe-area-inset-bottom), 18px) !important;
}

/* ===== TOPBAR FIXO COLADO NO TOPO ===== */
.topbar-fixed{
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  z-index: 9999;
  background: linear-gradient(180deg, var(--blue) 0%, var(--blue2) 100%);
  box-shadow: var(--shadowTop);
  padding-top: env(safe-area-inset-top);
  height: calc(70px + env(safe-area-inset-top));
  display:flex;
  align-items:flex-end;
  justify-content:center;
}
.topbar-fixed .title{
  height: 70px;
  display:flex;
  align-items:center;
  justify-content:center;
  width: 100%;
  color:#fff;
  font-weight: 900;
  font-size: 20px;
  letter-spacing: .2px;
}

/* Spacer para o conteúdo começar abaixo do topbar */
.topbar-spacer{
  height: calc(70px + env(safe-area-inset-top) + 18px);
}

/* Central */
.center{
  display:flex;
  flex-direction:column;
  align-items:center;
}

/* Logo */
.logo{
  width: 150px; height: 150px;
  border-radius: 999px;
  object-fit: cover;
  background:#fff;
  border: 6px solid rgba(255,255,255,.92);
  outline: 4px solid rgba(14,78,134,.18);
  box-shadow: var(--shadowSoft);
}

.brand{
  margin-top: 14px;
  font-weight: 900;
  font-size: 30px;
  color: var(--blue2);
  text-align:center;
}

/* Card login */
.login-card{
  width: 100%;
  max-width: 380px;
  margin-top: 18px;
  background: rgba(255,255,255,.92);
  border: 1px solid rgba(16,24,40,.06);
  border-radius: var(--radius);
  box-shadow: var(--shadowCard);
  padding: 18px 16px 16px 16px;
  backdrop-filter: blur(6px);
}

/* Input CPF */
div[data-testid="stTextInput"]{
  width: 100% !important;
}
div[data-testid="stTextInput"] input{
  width: 100% !important;
  height: 56px !important;
  border-radius: 18px !important;
  font-size: 16px !important;
  padding: 0 16px !important;
  border: 1px solid var(--stroke) !important;
  background: #fff !important;
  box-shadow: 0 8px 18px rgba(16, 24, 40, 0.06) !important;
}
div[data-testid="stTextInput"] input:focus{
  border: 1px solid rgba(14,78,134,.55) !important;
  box-shadow: 0 0 0 4px rgba(14,78,134,.12) !important;
}

.helper{
  margin-top: 10px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 600;
}

/* Botão LOGIN centralizado */
.login-btn-wrap{
  display:flex;
  justify-content:center;
  margin-top: 14px;
}
.login-btn-wrap div[data-testid="stButton"]{ width:auto !important; }
.login-btn-wrap div[data-testid="stButton"] > button{
  width: 190px !important;
  height: 58px !important;
  border-radius: 18px !important;
  background: linear-gradient(180deg, var(--blue) 0%, var(--blue2) 100%) !important;
  color:#fff !important;
  border: none !important;
  font-weight: 900 !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  box-shadow: 0 18px 30px rgba(11, 62, 107, 0.30) !important;
}
.login-btn-wrap div[data-testid="stButton"] > button:hover{
  filter: brightness(1.03);
  transform: translateY(-1px);
}
.login-btn-wrap div[data-testid="stButton"] > button:active{ transform: translateY(0px); }

/* Alert mais “card” */
[data-testid="stAlert"]{
  border-radius: 18px !important;
  box-shadow: 0 10px 22px rgba(16,24,40,.06) !important;
}

/* remove label spacing */
label{ display:none !important; }
</style>
""",
    unsafe_allow_html=True
)

# Topbar fixo (colado no topo)
st.markdown(
    """
<div class="topbar-fixed">
  <div class="title">Portal Jurídico</div>
</div>
<div class="topbar-spacer"></div>
""",
    unsafe_allow_html=True
)

# =========================
# LOGIN
# =========================
if not st.session_state["logged"]:
    st.markdown('<div class="center">', unsafe_allow_html=True)

    if img_b64:
        st.markdown(
            f'<img src="data:image/jpeg;base64,{img_b64}" class="logo" />',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="logo" style="display:flex;align-items:center;justify-content:center;color:var(--blue2);font-weight:900;">
              A&S
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(f'<div class="brand">{APP_NAME}</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    cpf_visual = st.text_input(
        "CPF",
        value=st.session_state["cpf_input"],
        placeholder="Digite seu CPF",
        label_visibility="collapsed",
    )

    cpf_digits = only_digits(cpf_visual)
    st.session_state["cpf_digits"] = cpf_digits
    st.session_state["cpf_input"] = format_cpf_digits(cpf_digits)

    st.markdown('<div class="helper">Use apenas números (11 dígitos).</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-btn-wrap">', unsafe_allow_html=True)
    if st.button("LOGIN", key="login_btn"):
        if len(cpf_digits) != 11:
            st.error("CPF inválido. Digite 11 números.")
        elif cpf_digits == VALID_CPF:
            st.session_state["logged"] = True
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")
    st.markdown("</div>", unsafe_allow_html=True)  # login-btn-wrap

    st.markdown("</div>", unsafe_allow_html=True)  # login-card
    st.markdown("</div>", unsafe_allow_html=True)  # center

else:
    st.success("Logado. Próximo passo: dashboard no mesmo padrão visual.")
    if st.button("SAIR"):
        st.session_state["logged"] = False
        st.rerun()