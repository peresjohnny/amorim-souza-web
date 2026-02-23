import streamlit as st
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Amorim & Souza", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM LOCAL ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

img_base64 = get_base64_image("1000423374.jpg")

# --- CSS PREMIUM MOBILE-FIRST ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Reset Geral */
    .stApp {{
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }}

    /* Container Mobile Rigoroso */
    [data-testid="stMainViewContainer"] > div:first-child {{
        max-width: 420px !important;
        margin: 0 auto !important;
        background-color: #F8FAFC !important;
    }}

    /* Esconder Lixo do Streamlit */
    header, footer, #MainMenu, [data-testid="stHeader"] {{
        display: none !important;
    }}

    /* Logo Circular e Sombra */
    .logo-container {{
        display: flex;
        justify-content: center;
        padding: 40px 0 20px 0;
    }}
    .logo-img {{
        width: 130px;
        height: 130px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 3px solid white;
    }}

    /* Títulos */
    .app-title {{
        color: #1A4A7A;
        text-align: center;
        font-weight: 700;
        font-size: 24px;
        margin-bottom: 40px;
    }}

    /* Inputs Centralizados */
    div[data-testid="stTextInput"] input {{
        border-radius: 12px !important;
        height: 55px !important;
        text-align: center !important;
        border: 1px solid #E2E8F0 !important;
        font-size: 16px !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
    }}

    /* Botão de Login */
    div.stButton > button {{
        width: 100% !important;
        background-color: #1A4A7A !important;
        color: white !important;
        border-radius: 12px !important;
        height: 60px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(26, 74, 122, 0.3) !important;
        transition: all 0.3s;
    }}

    /* Botões Dashboard (Grid) */
    .dash-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-top: 20px;
    }}
    
    .stButton > button[kind="secondary"] {{
        background-color: white !important;
        color: #1A4A7A !important;
        border: 1px solid #E2E8F0 !important;
        height: 100px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
        border-radius: 12px !important;
        font-size: 14px !important;
    }}

    /* Cards de Processo */
    .process-card {{
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        border: 1px solid #E2E8F0;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}
    .tag-yellow {{
        position: absolute;
        top: 15px;
        right: 15px;
        background-color: #FEF08A;
        color: #854D0E;
        font-size: 10px;
        font-weight: 800;
        padding: 4px 8px;
        border-radius: 4px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ESTADOS DO APP ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'view' not in st.session_state:
    st.session_state.view = 'main'

# --- TELA 1: LOGIN ---
if not st.session_state.auth:
    st.markdown(f'<div class="logo-container"><img src="data:image/jpeg;base64,{img_base64}" class="logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<div class="app-title">Amorim & Souza</div>', unsafe_allow_html=True)
    
    cpf_login = st.text_input("CPF", placeholder="Digite seu CPF", label_visibility="collapsed")
    
    if st.button("LOGIN"):
        if cpf_login == "79897789120":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados")

# --- TELA 2: ÁREA INTERNA ---
else:
    st.markdown(f"<h2 style='text-align: center; color: #1A4A7A;'>Olá, Edimar</h2>", unsafe_allow_html=True)
    
    # Grid de botões lado a lado
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📁\nProcessos", key="p_btn", use_container_width=True):
            st.session_state.view = 'processos'
    with col2:
        if st.button("🤝\nAcordos", key="a_btn", use_container_width=True):
            st.session_state.view = 'acordos'

    # Lógica de exibição das seções
    if st.session_state.view == 'processos':
        nums = ["0737767-85.2025.8.07.0001", "0757632-94.2025.8.07.0001", 
                "0722313-65.2025.8.07.0001", "0768584-35.2025.8.07.0001", "0764797-95.2025.8.07.0001"]
        for n in nums:
            st.markdown(f"""
                <div class="process-card">
                    <div class="tag-yellow">AGUARDANDO ATUALIZAÇÃO</div>
                    <div style="font-size: 11px; color: #94A3B8;">Número Processual</div>
                    <div style="font-weight: 700; color: #1E293B; font-size: 15px;">{n}</div>
                </div>
            """, unsafe_allow_html=True)
            
    elif st.session_state.view == 'acordos':
        st.warning("Em atualização")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("SAIR"):
        st.session_state.auth = False
        st.session_state.view = 'main'
        st.rerun()
