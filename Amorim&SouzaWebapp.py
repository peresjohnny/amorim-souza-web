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
if "cpf_visual" not in st.session_state:
    st.session_state["cpf_visual"] = ""
if "cpf_digits" not in st.session_state:
    st.session_state["cpf_digits"] = ""

img_b64 = get_base64("1000423374.jpg")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root{
  --bg: #EFF4F9;
  --blue: #0E4E86;
  --blue2:#0B3E6B;
  --text:#10202B;
  --muted:#607283;

  --stroke: rgba(12, 62, 107, .16);
  --shadowTop: 0 18px 36px rgba(11, 62, 107, 0.18);
  --shadowCard: 0 18px 40px rgba(16, 24, 40, 0.10);
  --shadowSoft: 0 10px 24px rgba(16, 24, 40, 0.08);
  --radius: 22px;
}

[data-testid="stHeader"], footer, #MainMenu{ display:none !important; }

html, body { margin:0 !important; padding:0 !important; }

.stApp{
  margin:0 !important;
  padding:0 !important;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif !important;
  background:
    radial-gradient(900px 450px at 50% -160px, rgba(14,78,134,.20), transparent 65%),
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

/* zerar padding que cria “gaps” */
.block-container{
  padding-top: 0rem !important;
  padding-bottom: max(env(safe-area-inset-bottom), 18px) !important;
}

/* Topbar FIXO colado no topo */
.topbar-fixed{
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  z-index: 9999;
  background: linear-gradient(180deg, var(--blue) 0%, var(--blue2) 100%);
  box-shadow: var(--shadowTop);
  padding-top: env(safe-area-inset-top);
  height: calc(66px + env(safe-area-inset-top));
  display:flex;
  align-items:flex-end;
  justify-content:center;
}
.topbar-fixed .title{
  height: 66px;
  display:flex;
  align-items:center;
  justify-content:center;
  width: 100%;
  color:#fff;
  font-weight: 900;
  font-size: 20px;
  letter-spacing: .2px;
}
.topbar-spacer{
  height: calc(66px + env(safe-area-inset-top) + 18px);
}

/* Centro real (sem depender do Streamlit) */
.center-wrap{
  width: 100%;
  display:flex;
  flex-direction:column;
  align-items:center;
}

/* Logo CENTRAL de verdade */
.logo{
  width: 150px; height: 150px;
  border-radius: 999px;
  object-fit: cover;
  background:#fff;
  display:block;
  margin: 0 auto;
  border: 6px solid rgba(255,255,255,.92);
  outline: 4px solid rgba(14,78,134,.18);
  box-shadow: var(--shadowSoft);
}

/* Título */
.brand{
  margin-top: 14px;
  font-weight: 900;
  font-size: 30px;
  color: var(--blue2);
  text-align:center;
}

/* Card do login */
.login-card{
  width: 100%;
  max-width: 380px;
  margin-top: 18px;
  background: rgba(255,255,255,.92);
  border: 1px solid rgba(16,24,40,.06);
  border-radius: var(--radius);
  box-shadow: var(--shadowCard);
  padding: 16px;
  backdrop-filter: blur(6px);
}

/* ========= FIX DO “INPUT DUPLICADO” =========
   Zera backgrounds/paddings do wrapper interno do stTextInput
   e estiliza SOMENTE o input real.
*/
div[data-testid="stTextInput"]{
  width: 100% !important;
}
div[data-testid="stTextInput"] > div{
  background: transparent !important;
  padding: 0 !important;
  margin: 0 !important;
  border: 0 !important;
  box-shadow: none !important;
}
div[data-testid="stTextInput"] > div > div{
  background: transparent !important;
  padding: 0 !important;
  margin: 0 !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* Input real */
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

/* Texto auxiliar */
.helper{
  margin-top: 10px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 600;
}

/* Botão do FORM (submit) centralizado */
div[data-testid="stFormSubmitButton"]{
  display:flex;
  justify-content:center;
  margin-top: 14px;
}
div[data-testid="stFormSubmitButton"] > button{
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
div[data-testid="stFormSubmitButton"] > button:hover{
  filter: brightness(1.03);
  transform: translateY(-1px);
}
div[data-testid="stFormSubmitButton"] > button:active{
  transform: translateY(0px);
}

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

# Topbar fixo
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
    st.markdown('<div class="center-wrap">', unsafe_allow_html=True)

    if img_b64:
        st.markdown(f'<img src="data:image/jpeg;base64,{img_b64}" class="logo" />', unsafe_allow_html=True)
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

    # FORM = render estável no mobile
    with st.form("login_form", clear_on_submit=False):
        cpf_visual = st.text_input(
            "CPF",
            value=st.session_state["cpf_visual"],
            placeholder="Digite seu CPF",
            label_visibility="collapsed",
        )

        cpf_digits = only_digits(cpf_visual)
        st.session_state["cpf_digits"] = cpf_digits
        st.session_state["cpf_visual"] = format_cpf_digits(cpf_digits)

        st.markdown('<div class="helper">Use apenas números (11 dígitos).</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("LOGIN")

    if submitted:
        if len(st.session_state["cpf_digits"]) != 11:
            st.error("CPF inválido. Digite 11 números.")
        elif st.session_state["cpf_digits"] == VALID_CPF:
            st.session_state["logged"] = True
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")

    st.markdown("</div>", unsafe_allow_html=True)  # login-card
    st.markdown("</div>", unsafe_allow_html=True)  # center-wrap

else:
    st.success("Logado. Próximo passo: dashboard no mesmo padrão visual.")
    if st.button("SAIR"):
        st.session_state["logged"] = False
        st.rerun()