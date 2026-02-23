import re
import base64
import streamlit as st

# =========================
# CONFIG
# =========================
APP_NAME = "Amorim & Souza"
VALID_CPF = "79897789120"  # exemplo

st.set_page_config(page_title=APP_NAME, layout="centered", initial_sidebar_state="collapsed")

# =========================
# HELPERS
# =========================
def get_base64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def only_digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")

def format_cpf_digits(d: str) -> str:
    """Mascara visual simples: 000.000.000-00"""
    d = only_digits(d)[:11]
    if len(d) <= 3:
        return d
    if len(d) <= 6:
        return f"{d[:3]}.{d[3:]}"
    if len(d) <= 9:
        return f"{d[:3]}.{d[3:6]}.{d[6:]}"
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

def set_screen(name: str):
    st.session_state["screen"] = name

def logout():
    st.session_state["logged"] = False
    st.session_state["screen"] = "login"
    st.session_state["cpf_input"] = ""
    st.session_state["cpf_digits"] = ""
    st.rerun()

# =========================
# SESSION STATE
# =========================
if "logged" not in st.session_state:
    st.session_state["logged"] = False
if "screen" not in st.session_state:
    st.session_state["screen"] = "login"
if "cpf_input" not in st.session_state:
    st.session_state["cpf_input"] = ""
if "cpf_digits" not in st.session_state:
    st.session_state["cpf_digits"] = ""

# =========================
# ASSETS
# =========================
img_b64 = get_base64("1000423374.jpg")

# Ícones em SVG (estilo simples, “app-like”)
ICON_DOC = """
<svg width="22" height="22" viewBox="0 0 24 24" fill="none">
  <path d="M7 3h7l3 3v15a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z" stroke="currentColor" stroke-width="2" />
  <path d="M14 3v4a1 1 0 0 0 1 1h4" stroke="currentColor" stroke-width="2"/>
  <path d="M8 12h8M8 16h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

ICON_HANDSHAKE = """
<svg width="22" height="22" viewBox="0 0 24 24" fill="none">
  <path d="M8 13l2 2a2 2 0 0 0 3 0l4-4a2 2 0 0 1 3 0l1 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M2 12l4-4 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M22 12l-4-4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M7 19l1 1a2 2 0 0 0 3 0" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

# =========================
# CSS (visual próximo do print)
# =========================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root{
  --bg: #EEF3F8;
  --blue: #0E4E86;         /* topo */
  --blue2: #0B3E6B;        /* botão/ativo */
  --text: #1E2A36;
  --muted: #6B7B8B;
  --card: #FFFFFF;
  --stroke: rgba(14, 78, 134, .20);
  --shadow: 0 10px 20px rgba(16, 24, 40, 0.08);
  --radius: 18px;
  --tile-radius: 16px;
  --yellow: #FFD24A;
}

/* Fundo + fonte */
.stApp {
  background: var(--bg) !important;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif !important;
}

/* Centraliza e limita largura (parecido com “mobile frame”) */
[data-testid="stMainViewContainer"] > div:first-child{
  max-width: 430px !important;
  margin: 0 auto !important;
  padding-left: 14px !important;
  padding-right: 14px !important;
}

/* Remove header/footer/menu */
[data-testid="stHeader"], footer, #MainMenu { display: none !important; }

/* Espaços melhores */
.block-container { padding-top: 0.0rem !important; padding-bottom: 1.2rem !important; }

/* TOP BAR */
.topbar{
  background: linear-gradient(180deg, var(--blue) 0%, var(--blue2) 100%);
  height: 66px;
  border-bottom-left-radius: 22px;
  border-bottom-right-radius: 22px;
  box-shadow: 0 12px 24px rgba(11, 62, 107, 0.20);
  display:flex;
  align-items:center;
  padding: 0 12px;
  margin: 0 -14px 18px -14px; /* “encosta” nas bordas do container */
}
.topbar .back{
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display:flex;
  align-items:center;
  justify-content:center;
  background: rgba(255,255,255,.12);
  color: #fff;
  font-size: 20px;
  line-height: 20px;
  user-select:none;
}
.topbar .title{
  flex:1;
  text-align:center;
  color:#fff;
  font-weight: 700;
  font-size: 18px;
  margin-right: 44px; /* compensa o back pra centralizar */
}

/* Logo circular */
.logo-wrap{
  display:flex;
  justify-content:center;
  margin-top: 12px;
  margin-bottom: 12px;
}
.logo{
  width: 146px;
  height: 146px;
  border-radius: 999px;
  object-fit: cover;
  border: 5px solid rgba(255,255,255,.9);
  outline: 4px solid rgba(14, 78, 134, .25);
  box-shadow: var(--shadow);
  background: #fff;
}

/* Título central */
.brand{
  text-align:center;
  color: var(--blue2);
  font-weight: 700;
  font-size: 24px;
  margin: 6px 0 18px 0;
}

/* Input CPF */
div[data-testid="stTextInput"] input{
  border-radius: 16px !important;
  height: 56px !important;
  font-size: 16px !important;
  padding: 0 16px !important;
  border: 1px solid var(--stroke) !important;
  background: #fff !important;
  box-shadow: 0 6px 18px rgba(16, 24, 40, 0.06) !important;
}
div[data-testid="stTextInput"] input:focus{
  border: 1px solid rgba(14, 78, 134, .55) !important;
  box-shadow: 0 0 0 4px rgba(14, 78, 134, .12) !important;
}

/* Botão primário */
div.stButton > button{
  width: 100% !important;
  height: 56px !important;
  border-radius: 16px !important;
  background: linear-gradient(180deg, var(--blue) 0%, var(--blue2) 100%) !important;
  color:#fff !important;
  border: none !important;
  font-weight: 800 !important;
  letter-spacing: 0.6px !important;
  box-shadow: 0 12px 22px rgba(11, 62, 107, 0.25) !important;
  text-transform: uppercase !important;
}
div.stButton > button:hover{
  filter: brightness(1.02);
}
div.stButton > button:active{
  transform: translateY(1px);
}

/* Greeting card */
.greet{
  background: var(--card);
  border: 1px solid rgba(16,24,40,.06);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 14px;
  display:flex;
  align-items:center;
  gap: 12px;
  margin-bottom: 14px;
}
.avatar{
  width: 40px;
  height: 40px;
  border-radius: 999px;
  background: #dbe7f5;
  display:flex;
  align-items:center;
  justify-content:center;
  color: var(--blue2);
  font-weight: 800;
}
.greet .text{
  font-weight: 700;
  color: var(--text);
  font-size: 16px;
}

/* Tiles (botões 2x2) */
.tile-row{
  display:flex;
  gap: 12px;
  margin: 10px 0;
}
.tile{
  flex:1;
  background: #fff;
  border: 1px solid var(--stroke);
  border-radius: var(--tile-radius);
  box-shadow: 0 10px 16px rgba(16, 24, 40, 0.06);
  padding: 14px;
  display:flex;
  align-items:center;
  justify-content:center;
  gap: 10px;
}
.tile .label{
  font-weight: 800;
  letter-spacing: .3px;
  font-size: 14px;
}
.tile.secondary{
  color: var(--blue2);
  background: #fff;
}
.tile.primary{
  color: #fff;
  background: linear-gradient(180deg, var(--blue) 0%, var(--blue2) 100%);
  border-color: rgba(255,255,255,.15);
}
.tile svg{ display:block; }

/* “Últimos Processos” */
.section-title{
  margin: 18px 0 10px 0;
  color: var(--text);
  font-weight: 800;
  font-size: 14px;
}
.proc-card{
  background: #fff;
  border: 1px solid rgba(16,24,40,.08);
  border-radius: 16px;
  box-shadow: 0 10px 16px rgba(16, 24, 40, 0.05);
  padding: 14px;
  margin-bottom: 12px;
  position: relative;
}
.proc-card .tag{
  position:absolute;
  right: 10px;
  top: 10px;
  background: var(--yellow);
  color: #1a1a1a;
  font-size: 10px;
  font-weight: 900;
  padding: 4px 8px;
  border-radius: 999px;
}
.proc-card .small{
  font-size: 12px;
  color: var(--muted);
  font-weight: 600;
  margin-bottom: 6px;
}
.proc-card .num{
  font-size: 14px;
  font-weight: 800;
  color: var(--text);
}

/* Mensagens de erro menos “Streamlitão” */
[data-testid="stAlert"]{
  border-radius: 16px !important;
  box-shadow: 0 10px 18px rgba(16,24,40,.06) !important;
}

</style>
""",
    unsafe_allow_html=True
)

# =========================
# UI BUILDING BLOCKS
# =========================
def topbar(title: str, show_back: bool):
    # O “back” visual é HTML. O clique real é via st.button logo abaixo (invisível)
    back_html = '<div class="back">‹</div>' if show_back else '<div style="width:44px"></div>'
    st.markdown(
        f"""
        <div class="topbar">
            {back_html}
            <div class="title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def tile_buttons():
    # Como Streamlit não dá pra “clicar HTML” e mudar estado sem gambiarra JS,
    # usamos botões nativos invisíveis + tiles só visuais em volta.
    # Resultado: fica com visual de tile, e a ação funciona.

    # Linha 1 (Processos / Acordos)
    c1, c2 = st.columns(2, gap="small")
    with c1:
        # tile visual
        st.markdown(
            f"""
            <div class="tile secondary">
              <div style="color: var(--blue2);">{ICON_DOC}</div>
              <div class="label">PROCESSOS</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(" ", key="go_proc_1"):
            set_screen("processos")
            st.rerun()

    with c2:
        st.markdown(
            f"""
            <div class="tile primary">
              <div style="color: #fff;">{ICON_HANDSHAKE}</div>
              <div class="label">ACORDOS</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("  ", key="go_acordo_1"):
            set_screen("acordos")
            st.rerun()

    # Linha 2 (Processos / Acordos) - repetido como no print (se você quiser só 1 linha, apaga isso)
    c3, c4 = st.columns(2, gap="small")
    with c3:
        st.markdown(
            f"""
            <div class="tile primary">
              <div style="color: #fff;">{ICON_DOC}</div>
              <div class="label">PROCESSOS</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("   ", key="go_proc_2"):
            set_screen("processos")
            st.rerun()

    with c4:
        st.markdown(
            f"""
            <div class="tile secondary">
              <div style="color: var(--blue2);">{ICON_HANDSHAKE}</div>
              <div class="label">ACORDOS</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("    ", key="go_acordo_2"):
            set_screen("acordos")
            st.rerun()

    # Deixa os botões “invisíveis” (só pra capturar clique)
    st.markdown(
        """
        <style>
          button[kind="secondary"], button[kind="primary"] { outline: none !important; }
          /* esconde os botões de clique (ficam logo abaixo dos tiles) */
          div[data-testid="stButton"] > button { margin-top: -54px !important; opacity: 0 !important; height: 52px !important; }
          div[data-testid="stButton"] { height: 0px !important; margin-bottom: 14px !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

# =========================
# SCREENS
# =========================
if not st.session_state["logged"]:
    # LOGIN
    topbar("Portal Jurídico", show_back=False)

    # Logo
    if img_b64:
        st.markdown(
            f'<div class="logo-wrap"><img src="data:image/jpeg;base64,{img_b64}" class="logo"></div>',
            unsafe_allow_html=True
        )
    else:
        # fallback simples (sem imagem)
        st.markdown(
            """
            <div class="logo-wrap">
              <div class="logo" style="display:flex;align-items:center;justify-content:center;color:var(--blue2);font-weight:900;">
                A&S
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(f'<div class="brand">{APP_NAME}</div>', unsafe_allow_html=True)

    # CPF input com “máscara” amigável (visual) e validação real por dígitos
    cpf_visual = st.text_input(
        "CPF",
        value=st.session_state["cpf_input"],
        placeholder="Digite seu CPF",
        label_visibility="collapsed"
    )

    cpf_digits = only_digits(cpf_visual)
    # atualiza estado e “corrige” visual quando possível
    st.session_state["cpf_digits"] = cpf_digits
    st.session_state["cpf_input"] = format_cpf_digits(cpf_digits)

    # Se o usuário colar/editar, a máscara pode “atrasar” 1 render — ok.
    # Quando clica LOGIN, usamos sempre cpf_digits.
    if st.button("LOGIN"):
        if len(cpf_digits) != 11:
            st.error("CPF inválido. Digite 11 números.")
        elif cpf_digits == VALID_CPF:
            st.session_state["logged"] = True
            st.session_state["screen"] = "dashboard"
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")

else:
    # LOGADO
    screen = st.session_state["screen"]

    if screen in ("dashboard", "processos", "acordos"):
        topbar("Dashboard" if screen == "dashboard" else ("Processos" if screen == "processos" else "Acordos"),
               show_back=(screen != "dashboard"))

        # Back real (botão invisível sobre o “‹” do header)
        if screen != "dashboard":
            colb1, colb2 = st.columns([1, 7])
            with colb1:
                if st.button(" ", key="back_btn"):
                    st.session_state["screen"] = "dashboard"
                    st.rerun()

            # esconde esse botão também
            st.markdown(
                """
                <style>
                  div[data-testid="stButton"] > button#back_btn { opacity:0 !important; height:44px !important; margin-top:-68px !important; }
                </style>
                """,
                unsafe_allow_html=True
            )

        # Greeting card (como no print)
        st.markdown(
            """
            <div class="greet">
              <div class="avatar">E</div>
              <div class="text">Olá, Edimar</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if screen == "dashboard":
            tile_buttons()

            st.markdown('<div class="section-title">Últimos Processos</div>', unsafe_allow_html=True)

            procs = [
                "0737767-85.2025.8.07.0001",
                "0757632-94.2025.8.07.0001",
                "0722313-65.2025.8.07.0001",
            ]
            for p in procs:
                st.markdown(
                    f"""
                    <div class="proc-card">
                      <div class="tag">ATUALIZAÇÕES</div>
                      <div class="small">Últimos Processos</div>
                      <div class="num">{p}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        elif screen == "processos":
            st.markdown('<div class="section-title">Todos os Processos</div>', unsafe_allow_html=True)

            procs = [
                "0737767-85.2025.8.07.0001",
                "0757632-94.2025.8.07.0001",
                "0722313-65.2025.8.07.0001",
                "0768584-35.2025.8.07.0001",
                "0764797-95.2025.8.07.0001",
            ]
            for p in procs:
                st.markdown(
                    f"""
                    <div class="proc-card">
                      <div class="tag">ATUALIZAÇÕES</div>
                      <div class="small">Número do Processo</div>
                      <div class="num">{p}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        elif screen == "acordos":
            st.warning("Em atualização")

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.button("SAIR"):
            logout()
    else:
        # fallback (se alguma tela inválida entrar no estado)
        st.session_state["screen"] = "dashboard"
        st.rerun()