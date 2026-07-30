import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
import pycountry

warnings.filterwarnings('ignore')

# =========================
# CONFIGURAÇÃO INICIAL
# =========================
st.set_page_config(
    page_title="CineAnalytics Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar fechada por padrão para mais espaço
)

# =========================
# CSS MODERNO 2026
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 3rem 1rem 2rem;
        background: linear-gradient(180deg, rgba(78,205,196,0.1) 0%, transparent 100%);
        border-radius: 0 0 40px 40px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(78,205,196,0.03) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.6);
        font-weight: 300;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }
    
    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(78,205,196,0.5), transparent);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(78, 205, 196, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    }
    
    /* Metric Cards */
    .metric-glass {
        background: linear-gradient(135deg, rgba(78,205,196,0.1) 0%, rgba(69,183,209,0.05) 100%);
        border-left: 3px solid #4ECDC4;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #fff;
        margin: 2rem 0 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(78,205,196,0.3), transparent);
        margin-left: 1rem;
    }
    
    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.02);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255,255,255,0.5);
        font-weight: 500;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #fff;
        background: rgba(255,255,255,0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(78,205,196,0.2), rgba(69,183,209,0.1)) !important;
        color: #4ECDC4 !important;
        box-shadow: 0 4px 15px rgba(78,205,196,0.1);
    }
    
    /* Sidebar Modern */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #4ECDC4;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    /* Slider Modern */
    .stSlider > div > div > div {
        background: rgba(255,255,255,0.1) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4ECDC4, #45B7D1);
        color: #0f0f1a;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(78,205,196,0.3);
    }
    
    /* Dataframe */
    .stDataFrame {
        background: rgba(255,255,255,0.02);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.02);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(78,205,196,0.3);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(78,205,196,0.5);
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-blockbuster { background: rgba(255,107,107,0.2); color: #FF6B6B; border: 1px solid rgba(255,107,107,0.3); }
    .badge-high { background: rgba(255,167,38,0.2); color: #FFA726; border: 1px solid rgba(255,167,38,0.3); }
    .badge-medium { background: rgba(78,205,196,0.2); color: #4ECDC4; border: 1px solid rgba(78,205,196,0.3); }
    .badge-low { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.6); border: 1px solid rgba(255,255,255,0.2); }
    
    /* Loading animation */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .loading-shimmer {
        background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.03) 75%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# CARREGAMENTO DE DADOS OTIMIZADO
# =========================
@st.cache_data(show_spinner=False)
def carregar_dados():
    CSV_URL = "https://raw.githubusercontent.com/luccasfsilva/projetopy/main/imdb_movies.csv"
    try:
        df = pd.read_csv(CSV_URL, parse_dates=['date_x'])
        
        # Limpeza robusta
        df["revenue"] = pd.to_numeric(df.get("revenue"), errors="coerce").fillna(0)
        df["score"] = pd.to_numeric(df.get("score"), errors="coerce")
        df["budget_x"] = pd.to_numeric(df.get("budget_x"), errors="coerce").fillna(0)
        
        df["ano"] = df["date_x"].dt.year.fillna(0).astype(int)
        df["mes"] = df["date_x"].dt.month.fillna(0).astype(int)
        
        df["roi"] = np.where(
            df["budget_x"] > 0,
            (df["revenue"] - df["budget_x"]) / df["budget_x"] * 100,
            0
        )
        
        # Categorias de sucesso com percentis dinâmicos
        q80 = df['revenue'].quantile(0.8)
        q60 = df['revenue'].quantile(0.6)
        q40 = df['revenue'].quantile(0.4)
        
        conditions = [
            df['revenue'] >= q80,
            df['revenue'] >= q60,
            df['revenue'] >= q40,
            df['revenue'] < q40
        ]
        choices = ['Blockbuster', 'High', 'Medium', 'Low']
        df['success_category'] = np.select(conditions, choices, default='Low')
        
        # Adiciona coluna de década
        df['decada'] = (df['ano'] // 10) * 10
        
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return None

# Placeholder de loading elegante
with st.spinner(""):
    st.markdown("""
        <div style="text-align: center; padding: 4rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎬</div>
            <div style="color: rgba(255,255,255,0.5); font-size: 1.1rem; letter-spacing: 2px;">CARREGANDO CINEANALYTICS</div>
            <div style="width: 200px; height: 2px; background: rgba(255,255,255,0.1); margin: 1rem auto; border-radius: 2px; overflow: hidden;">
                <div style="width: 60%; height: 100%; background: linear-gradient(90deg, #4ECDC4, #45B7D1); border-radius: 2px; animation: loading 1.5s ease-in-out infinite;"></div>
            </div>
        </div>
        <style>
            @keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(250%); } }
        </style>
    """, unsafe_allow_html=True)
    
    df = carregar_dados()

if df is None or df.empty:
    st.stop()

# =========================
# TRADUÇÕES
# =========================
TRADUCOES_FILMES = {
    "Avatar: The Way of Water": "Avatar: O Caminho da Água",
    "Avengers: Endgame": "Vingadores: Ultimato",
    "Avatar": "Avatar",
    "Titanic": "Titanic",
    "Star Wars: Episode VII - The Force Awakens": "Star Wars: Episódio VII - O Despertar da Força",
    "Avengers: Infinity War": "Vingadores: Guerra Infinita",
    "Spider-Man: No Way Home": "Homem-Aranha: Sem Volta para Casa",
    "Jurassic World": "Mundo Jurássico",
    "The Lion King": "O Rei Leão",
    "The Avengers": "Os Vingadores",
    "Furious 7": "Velozes e Furiosos 7",
    "Frozen II": "Frozen II",
    "Top Gun: Maverick": "Top Gun: Maverick",
    "Barbie": "Barbie",
    "The Super Mario Bros. Movie": "Super Mario Bros.: O Filme",
    "Avengers: Age of Ultron": "Vingadores: Era de Ultron",
    "Black Panther": "Pantera Negra",
    "Harry Potter and the Deathly Hallows: Part 2": "Harry Potter e as Relíquias da Morte: Parte 2",
    "Star Wars: Episode VIII - The Last Jedi": "Star Wars: Episódio VIII - Os Últimos Jedi",
    "Jurassic World: Fallen Kingdom": "Mundo Jurássico: Reino Ameaçado",
    "Frozen": "Frozen: Uma Aventura Congelante",
    "Beauty and the Beast": "A Bela e a Fera",
    "Incredibles 2": "Os Incríveis 2",
    "The Fate of the Furious": "O Destino de Velozes e Furiosos",
    "Iron Man 3": "Homem de Ferro 3",
    "Minions": "Minions",
    "Captain America: Civil War": "Capitão América: Guerra Civil",
    "Aquaman": "Aquaman",
    "The Lord of the Rings: The Return of the King": "O Senhor dos Anéis: O Retorno do Rei",
    "Spider-Man: Far From Home": "Homem-Aranha: Longe de Casa",
    "Transformers: Dark of the Moon": "Transformers: O Lado Oculto da Lua",
    "Skyfall": "007 - Operação Skyfall",
    "Transformers: Age of Extinction": "Transformers: A Era da Extinção",
    "The Dark Knight Rises": "Batman: O Cavaleiro das Trevas Ressurge",
    "Toy Story 4": "Toy Story 4",
    "Toy Story 3": "Toy Story 3",
    "Pirates of the Caribbean: Dead Man's Chest": "Piratas do Caribe: O Baú da Morte",
    "Rogue One: A Star Wars Story": "Rogue One: Uma História Star Wars",
    "Pirates of the Caribbean: On Stranger Tides": "Piratas do Caribe: Navegando em Águas Misteriosas",
    "Despicable Me 3": "Meu Malvado Favorito 3",
    "Jumanji: Welcome to the Jungle": "Jumanji: Bem-vindo à Selva",
    "Justice League": "Liga da Justiça",
    "The Dark Knight": "Batman: O Cavaleiro das Trevas",
    "Finding Dory": "Procurando Dory",
    "Zootopia": "Zootopia: Essa Cidade é o Bicho",
    "Despicable Me 2": "Meu Malvado Favorito 2",
    "The Grinch": "O Grinch",
    "Finding Nemo": "Procurando Nemo",
    "Shrek 2": "Shrek 2",
    "The Secret Life of Pets": "A Vida Secreta dos Bichos",
    "Inside Out": "Divertida Mente",
    "The Incredibles": "Os Incríveis",
    "Shrek the Third": "Shrek Terceiro",
    "Shrek": "Shrek",
    "Madagascar 3: Europe's Most Wanted": "Madagascar 3: Os Procurados",
    "Monsters, Inc.": "Monstros S.A.",
    "Up": "Up: Altas Aventuras",
    "Spider-Man: Into the Spider-Verse": "Homem-Aranha no Aranhaverso",
    "Oppenheimer": "Oppenheimer",
    "Guardians of the Galaxy Vol. 3": "Guardiões da Galáxia Vol. 3",
    "Fast X": "Velozes e Furiosos 10",
    "The Little Mermaid": "A Pequena Sereia",
    "Elemental": "Elementos",
    "Ant-Man and the Wasp: Quantumania": "Homem-Formiga e a Vespa: Quantumania",
    "John Wick: Chapter 4": "John Wick 4: Baba Yaga",
    "The Flash": "The Flash",
    "Transformers: Rise of the Beasts": "Transformers: O Despertar das Feras",
    "Spider-Man: Across the Spider-Verse": "Homem-Aranha: Através do Aranhaverso",
    "Indiana Jones and the Dial of Destiny": "Indiana Jones e o Chamado do Destino",
    "Mission: Impossible - Dead Reckoning Part One": "Missão: Impossível - Acerto de Contas Parte Um",
    "The Marvels": "As Marvels",
    "Wonka": "Wonka",
    "Aquaman and the Lost Kingdom": "Aquaman e o Reino Perdido",
    "The Hunger Games: The Ballad of Songbirds & Snakes": "Jogos Vorazes: A Cantiga dos Pássaros e das Serpentes",
    "The Lord of the Rings: The Two Towers": "O Senhor dos Anéis: As Duas Torres",
    "The Lord of the Rings: The Fellowship of the Ring": "O Senhor dos Anéis: A Sociedade do Anel",
    "The Matrix Reloaded": "Matrix Reloaded",
    "The Twilight Saga: Breaking Dawn - Part 2": "A Saga Crepúsculo: Amanhecer - Parte 2",
    "The Twilight Saga: New Moon": "A Saga Crepúsculo: Lua Nova",
    "The Twilight Saga: Eclipse": "A Saga Crepúsculo: Eclipse",
    "The Twilight Saga: Breaking Dawn - Part 1": "A Saga Crepúsculo: Amanhecer - Parte 1",
    "The Hobbit: An Unexpected Journey": "O Hobbit: Uma Jornada Inesperada",
    "The Hobbit: The Desolation of Smaug": "O Hobbit: A Desolação de Smaug",
    "The Hobbit: The Battle of the Five Armies": "O Hobbit: A Batalha dos Cinco Exércitos",
    "The Da Vinci Code": "O Código Da Vinci",
    "The Chronicles of Narnia: The Lion, the Witch and the Wardrobe": "As Crônicas de Nárnia: O Leão, a Feiticeira e o Guarda-Roupa",
    "The Passion of the Christ": "A Paixão de Cristo",
    "The Exorcist": "O Exorcista",
    "The Sound of Music": "A Noviça Rebelde",
    "The Sting": "Um Golpe de Mestre",
    "Butch Cassidy and the Sundance Kid": "Butch Cassidy e o Menino da Lua",
    "Cidade de Deus": "Cidade de Deus",
    "Tropa de Elite": "Tropa de Elite",
    "Central do Brasil": "Central do Brasil",
    "O Auto da Compadecida": "O Auto da Compadecida",
    "Lisbela e o Prisioneiro": "Lisbela e o Prisioneiro",
}

def traduzir_nome(nome):
    if pd.isna(nome):
        return nome
    return TRADUCOES_FILMES.get(nome, nome)

# =========================
# SIDEBAR MODERNA
# =========================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎛️</div>
            <h2 style="color: #4ECDC4; font-size: 1.2rem; font-weight: 700; margin: 0;">Painel de Controle</h2>
            <p style="color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 0.3rem;">Filtros Avançados</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filtro de anos com estilo
    st.markdown("#### 📅 Período")
    anos_validos = sorted(df[df["ano"] > 0]["ano"].unique())
    if anos_validos:
        ano_min, ano_max = st.select_slider(
            "Intervalo de Anos",
            options=anos_validos,
            value=(min(anos_validos), max(anos_validos)),
            label_visibility="collapsed"
        )
    else:
        ano_min, ano_max = 1900, datetime.now().year
    
    st.markdown("---")
    
    # Filtro de notas
    st.markdown("#### ⭐ Nota IMDb")
    score_min, score_max = st.slider(
        "Faixa de Notas",
        0.0, 10.0, (0.0, 10.0), 0.1,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Filtro de receita
    st.markdown("#### 💰 Receita")
    max_revenue = float(df["revenue"].max())
    receita_min, receita_max = st.slider(
        "Faixa de Receita",
        0.0, max_revenue, (0.0, max_revenue), 1_000_000.0,
        format="$%.0f",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats na sidebar
    total_filmes = len(df)
    st.markdown(f"""
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #4ECDC4;">{total_filmes:,}</div>
            <div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px;">Filmes no Dataset</div>
        </div>
    """, unsafe_allow_html=True)

# =========================
# APLICAR FILTROS
# =========================
df_filtrado = df[
    (df["ano"] >= ano_min) & (df["ano"] <= ano_max) &
    (df["score"] >= score_min) & (df["score"] <= score_max) &
    (df["revenue"] >= receita_min) & (df["revenue"] <= receita_max)
].copy()

df_filtrado["names"] = df_filtrado["names"].apply(traduzir_nome)

if df_filtrado.empty:
    st.error("🎭 Nenhum filme encontrado com os filtros selecionados.")
    st.stop()

# =========================
# HERO SECTION
# =========================
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🎬 CineAnalytics Pro</h1>
        <p class="hero-subtitle">Dashboard Inteligente de Análise Cinematográfica</p>
    </div>
""", unsafe_allow_html=True)

# =========================
# KPI CARDS MODERNOS
# =========================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    receita_total = df_filtrado["revenue"].sum()
    st.markdown(f"""
        <div class="glass-card metric-glass">
            <div class="metric-value">${receita_total/1e9:.1f}B</div>
            <div class="metric-label">Receita Total</div>
            <div class="metric-delta" style="color: #4ECDC4;">↗ Global</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    receita_media = df_filtrado["revenue"].mean()
    st.markdown(f"""
        <div class="glass-card metric-glass" style="border-left-color: #FF6B6B;">
            <div class="metric-value">${receita_media/1e6:.1f}M</div>
            <div class="metric-label">Receita Média</div>
            <div class="metric-delta" style="color: #FF6B6B;">por filme</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    nota_media = df_filtrado["score"].mean()
    st.markdown(f"""
        <div class="glass-card metric-glass" style="border-left-color: #FFA726;">
            <div class="metric-value">{nota_media:.1f}</div>
            <div class="metric-label">Nota Média</div>
            <div class="metric-delta" style="color: #FFA726;">IMDb</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    roi_medio = df_filtrado[df_filtrado["roi"] > 0]["roi"].mean()
    if pd.isna(roi_medio):
        roi_medio = 0
    st.markdown(f"""
        <div class="glass-card metric-glass" style="border-left-color: #45B7D1;">
            <div class="metric-value">{roi_medio:.0f}%</div>
            <div class="metric-label">ROI Médio</div>
            <div class="metric-delta" style="color: #45B7D1;">retorno</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    total_filtrado = len(df_filtrado)
    st.markdown(f"""
        <div class="glass-card metric-glass" style="border-left-color: #9C27B0;">
            <div class="metric-value">{total_filtrado}</div>
            <div class="metric-label">Filmes</div>
            <div class="metric-delta" style="color: #9C27B0;">selecionados</div>
        </div>
    """, unsafe_allow_html=True)

# =========================
# FUNÇÕES DE GRÁFICOS MODERNIZADAS
# =========================
def tema_moderno(fig, altura=450):
    """Aplica tema escuro moderno aos gráficos Plotly"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.8)', family='Inter, sans-serif', size=12),
        title_font=dict(size=16, color='white', family='Inter, sans-serif'),
        legend=dict(
            bgcolor='rgba(0,0,0,0.3)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(size=11)
        ),
        margin=dict(l=60, r=40, t=60, b=40),
        height=altura,
        hoverlabel=dict(
            bgcolor='rgba(20,20,35,0.95)',
            bordercolor='rgba(78,205,196,0.3)',
            font=dict(color='white', size=12)
        )
    )
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)',
        showline=True, linewidth=1, linecolor='rgba(255,255,255,0.1)'
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)',
        showline=True, linewidth=1, linecolor='rgba(255,255,255,0.1)'
    )
    return fig

def grafico_top_filmes(df, top_n=10):
    top = df.nlargest(top_n, 'revenue')[['names', 'revenue', 'score']].copy()
    
    fig = px.bar(
        top, x='revenue', y='names', orientation='h',
        color='revenue', color_continuous_scale=['#1a1a2e', '#4ECDC4', '#45B7D1', '#FF6B6B'],
        hover_data={'names': True, 'revenue': ':$.2s', 'score': ':.1f'}
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate='<b>%{y}</b><br>Receita: %{x:$,.0f}<br>Nota: %{customdata[1]:.1f}<extra></extra>'
    )
    fig.update_layout(
        yaxis=dict(categoryorder='total ascending', title=''),
        xaxis=dict(title='Receita (USD)', tickformat='$,.0f'),
        coloraxis_showscale=False
    )
    return tema_moderno(fig, 500)

def grafico_evolucao_receita(df):
    dados = df.groupby('ano')['revenue'].sum().reset_index()
    dados = dados[dados['ano'] > 0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dados['ano'], y=dados['revenue'],
        mode='lines+markers',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8, color='#4ECDC4', line=dict(width=2, color='rgba(0,0,0,0.5)')),
        fill='tozeroy',
        fillcolor='rgba(78,205,196,0.1)',
        name='Receita Anual'
    ))
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Receita Total',
        yaxis_tickformat='$.2s',
        showlegend=False
    )
    return tema_moderno(fig)

def grafico_dispersao_nota_receita(df):
    amostra = df.sample(min(2000, len(df))) if len(df) > 2000 else df
    
    fig = px.scatter(
        amostra, x='score', y='revenue',
        color='score', color_continuous_scale=['#FF6B6B', '#FFA726', '#4ECDC4', '#45B7D1'],
        opacity=0.7,
        hover_data=['names']
    )
    fig.update_traces(
        marker=dict(size=8, line=dict(width=1, color='rgba(255,255,255,0.3)')),
        hovertemplate='<b>%{customdata[0]}</b><br>Nota: %{x:.1f}<br>Receita: %{y:$,.0f}<extra></extra>'
    )
    fig.update_layout(
        xaxis_title='Nota IMDb',
        yaxis_title='Receita (USD)',
        yaxis_tickformat='$.2s',
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(title='Nota', tickformat='.1f')
    )
    return tema_moderno(fig)

def grafico_filmes_por_ano(df):
    dados = df[df['ano'] > 0].groupby('ano').size().reset_index(name='count')
    
    fig = px.bar(
        dados, x='ano', y='count',
        color='count', color_continuous_scale=['#1a1a2e', '#45B7D1']
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate='Ano: %{x}<br>Filmes: %{y}<extra></extra>'
    )
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Quantidade',
        coloraxis_showscale=False
    )
    return tema_moderno(fig)

def grafico_media_notas(df):
    dados = df[df['ano'] > 0].groupby('ano')['score'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dados['ano'], y=dados['score'],
        mode='lines+markers',
        line=dict(color='#FFA726', width=3),
        marker=dict(size=6, color='#FFA726'),
        name='Média de Notas'
    ))
    # Linha de tendência
    if len(dados) > 1:
        z = np.polyfit(dados['ano'], dados['score'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=dados['ano'], y=p(dados['ano']),
            mode='lines',
            line=dict(color='rgba(255,167,38,0.3)', width=2, dash='dash'),
            name='Tendência'
        ))
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Nota Média',
        yaxis_range=[0, 10],
        showlegend=True
    )
    return tema_moderno(fig)

def grafico_idiomas(df):
    idiomas = df['orig_lang'].value_counts().head(8).reset_index()
    idiomas.columns = ['Idioma', 'Quantidade']
    
    fig = px.pie(
        idiomas, values='Quantidade', names='Idioma',
        hole=0.6,
        color_discrete_sequence=['#4ECDC4', '#45B7D1', '#FF6B6B', '#FFA726', '#9C27B0', '#E91E63', '#00BCD4', '#8BC34A']
    )
    fig.update_traces(
        textposition='outside',
        textinfo='label+percent',
        textfont=dict(size=11, color='rgba(255,255,255,0.8)'),
        hovertemplate='<b>%{label}</b><br>Filmes: %{value}<br>%{percent}<extra></extra>',
        marker=dict(line=dict(color='rgba(0,0,0,0.3)', width=2))
    )
    fig.update_layout(
        annotations=[dict(text='IDIOMAS', x=0.5, y=0.5, font_size=16, showarrow=False, font_color='rgba(255,255,255,0.5)')],
        showlegend=False
    )
    return tema_moderno(fig, 400)

def grafico_mapa_mundi(df):
    if "country" not in df.columns or df["country"].isnull().all():
        return None
    
    df_country = df.groupby("country")["revenue"].sum().reset_index()
    df_country.columns = ["country_raw", "value"]
    
    def iso2_to_iso3(code):
        try:
            if isinstance(code, str) and len(code) == 2:
                return pycountry.countries.get(alpha_2=code.upper()).alpha_3
            if isinstance(code, str) and len(code) == 3:
                return code.upper()
        except:
            pass
        return None
    
    df_country["iso3"] = df_country["country_raw"].apply(iso2_to_iso3)
    df_country = df_country.dropna(subset=["iso3"])
    
    if df_country.empty:
        return None
    
    fig = px.choropleth(
        df_country, locations="iso3", color="value",
        hover_name="country_raw", color_continuous_scale="Plasma",
        projection="natural earth",
        labels={"value": "Receita"}
    )
    fig.update_geos(
        showcountries=True, showcoastlines=True, showland=True,
        landcolor="#1a1a2e", oceancolor="#0f0f1a",
        coastlinecolor="rgba(255,255,255,0.1)", countrycolor="rgba(255,255,255,0.05)"
    )
    fig.update_layout(
        margin=dict(r=0, t=50, l=0, b=0), height=520,
        coloraxis_colorbar=dict(title='Receita (USD)', tickformat='$.2s')
    )
    return tema_moderno(fig)

def grafico_decadas(df):
    df_temp = df[df['ano'] > 1900].copy()
    if df_temp.empty:
        return None
    
    stats = df_temp.groupby('decada').agg({
        'revenue': 'sum', 'score': 'mean', 'names': 'count'
    }).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=stats['decada'], y=stats['names'],
        name='Filmes', marker_color='rgba(78,205,196,0.7)',
        marker_line_width=0, hovertemplate='Década: %{x}s<br>Filmes: %{y}<extra></extra>'
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=stats['decada'], y=stats['revenue'],
        name='Receita', mode='lines+markers',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8, color='#FF6B6B'),
        hovertemplate='Década: %{x}s<br>Receita: $%{y:,.0f}<extra></extra>'
    ), secondary_y=True)
    
    fig.update_layout(
        xaxis_title='Década',
        yaxis_title='Número de Filmes',
        yaxis2_title='Receita Total (USD)',
        yaxis2_tickformat='$.2s',
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return tema_moderno(fig)

def grafico_sazonalidade(df):
    if 'mes' not in df.columns or df['mes'].isnull().all():
        return None
    
    dados = df[df['mes'] > 0].groupby('mes').agg({
        'revenue': 'mean', 'names': 'count'
    }).reset_index()
    
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    dados['mes_nome'] = dados['mes'].apply(lambda x: meses[x-1])
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(
        x=dados['mes_nome'], y=dados['revenue'],
        name='Receita Média', mode='lines+markers',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8),
        fill='tozeroy', fillcolor='rgba(78,205,196,0.1)',
        hovertemplate='%{x}<br>Receita Média: $%{y:,.0f}<extra></extra>'
    ), secondary_y=False)
    
    fig.add_trace(go.Bar(
        x=dados['mes_nome'], y=dados['names'],
        name='Lançamentos', marker_color='rgba(255,107,107,0.5)',
        marker_line_width=0,
        hovertemplate='%{x}<br>Lançamentos: %{y}<extra></extra>'
    ), secondary_y=True)
    
    fig.update_layout(
        xaxis_title='Mês',
        yaxis_title='Receita Média (USD)',
        yaxis_tickformat='$.2s',
        yaxis2_title='Número de Lançamentos',
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    fig.update_xaxes(categoryorder='array', categoryarray=meses)
    return tema_moderno(fig)

def grafico_orcamento_receita(df):
    df_temp = df[(df['budget_x'] > 0) & (df['revenue'] > 0)].copy()
    if len(df_temp) < 10:
        return None
    
    amostra = df_temp.sample(min(1500, len(df_temp))) if len(df_temp) > 1500 else df_temp
    
    fig = px.scatter(
        amostra, x='budget_x', y='revenue',
        color='score', color_continuous_scale=['#FF6B6B', '#FFA726', '#4ECDC4'],
        size='score', size_max=15,
        opacity=0.6,
        hover_data=['names']
    )
    fig.update_traces(
        marker_line_width=1, marker_line_color='rgba(255,255,255,0.2)',
        hovertemplate='<b>%{customdata[0]}</b><br>Orçamento: $%{x:,.0f}<br>Receita: $%{y:,.0f}<extra></extra>'
    )
    # Linha de break-even
    max_val = max(amostra['budget_x'].max(), amostra['revenue'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_val], y=[0, max_val],
        mode='lines', line=dict(color='rgba(255,255,255,0.2)', width=2, dash='dash'),
        name='Break-even', hoverinfo='skip'
    ))
    fig.update_layout(
        xaxis_title='Orçamento (USD)', yaxis_title='Receita (USD)',
        xaxis_tickformat='$.2s', yaxis_tickformat='$.2s',
        showlegend=True
    )
    return tema_moderno(fig)

def grafico_distribuicao_notas(df):
    fig = px.histogram(
        df, x='score', nbins=40,
        color_discrete_sequence=['#4ECDC4'],
        marginal='box'
    )
    fig.update_traces(
        marker_line_width=0, opacity=0.8,
        hovertemplate='Nota: %{x:.1f}<br>Filmes: %{y}<extra></extra>'
    )
    fig.update_layout(
        xaxis_title='Nota IMDb', yaxis_title='Frequência',
        bargap=0.1
    )
    return tema_moderno(fig)

def grafico_roi(df):
    df_roi = df[(df['roi'] > 0) & (df['budget_x'] > 0) & (df['roi'] < 5000)].nlargest(10, 'roi')
    if df_roi.empty:
        return None
    
    fig = px.bar(
        df_roi, x='roi', y='names', orientation='h',
        color='roi', color_continuous_scale=['#45B7D1', '#4ECDC4', '#FFA726', '#FF6B6B'],
        hover_data={'names': True, 'roi': ':.0f', 'revenue': ':$.2s'}
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate='<b>%{y}</b><br>ROI: %{x:.0f}%<extra></extra>'
    )
    fig.update_layout(
        yaxis=dict(categoryorder='total ascending', title=''),
        xaxis=dict(title='ROI (%)'),
        coloraxis_showscale=False
    )
    return tema_moderno(fig, 400)

def grafico_sucesso(df):
    dist = df['success_category'].value_counts()
    cores = {'Blockbuster': '#FF6B6B', 'High': '#FFA726', 'Medium': '#4ECDC4', 'Low': 'rgba(255,255,255,0.3)'}
    
    fig = go.Figure()
    for cat in ['Blockbuster', 'High', 'Medium', 'Low']:
        if cat in dist:
            fig.add_trace(go.Bar(
                x=[cat], y=[dist[cat]],
                marker_color=cores[cat],
                name=cat,
                text=[f"{dist[cat]} ({dist[cat]/dist.sum()*100:.1f}%)"],
                textposition='outside',
                textfont=dict(color='white', size=12),
                hovertemplate=f'<b>{cat}</b><br>Filmes: %{{y}}<extra></extra>'
            ))
    fig.update_layout(
        xaxis_title='Categoria', yaxis_title='Número de Filmes',
        showlegend=False, bargap=0.4
    )
    return tema_moderno(fig, 400)

# =========================
# TABS MODERNAS
# =========================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏆 Destaques", "📈 Tendências", "🎯 Correlações",
    "🌎 Distribuição", "💰 Financeiro", "📅 Sazonalidade", "🔍 Dados"
])

with tab1:
    st.markdown('<div class="section-title">🏆 Filmes em Destaque</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        top_n = st.slider("Quantidade no ranking", 5, 20, 10, key="top_n")
        st.plotly_chart(grafico_top_filmes(df_filtrado, top_n), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(grafico_distribuicao_notas(df_filtrado), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Top ROI mini-card
        st.markdown('<div class="glass-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown("**📈 Maior ROI do Período**")
        if not df_filtrado[(df_filtrado['roi'] > 0)].empty:
            top_roi = df_filtrado[df_filtrado['roi'] > 0].nlargest(1, 'roi').iloc[0]
            st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 1rem; margin-top: 0.5rem;">
                    <div style="font-size: 2rem;">🥇</div>
                    <div>
                        <div style="font-weight: 600; color: white;">{top_roi['names']}</div>
                        <div style="color: #4ECDC4; font-size: 1.2rem; font-weight: 700;">{top_roi['roi']:.0f}% ROI</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">📈 Análise Temporal</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(grafico_evolucao_receita(df_filtrado), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
        st.plotly_chart(grafico_filmes_por_ano(df_filtrado), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(grafico_media_notas(df_filtrado), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
        fig_dec = grafico_decadas(df_filtrado)
        if fig_dec:
            st.plotly_chart(fig_dec, use_container_width=True)
        else:
            st.info("Dados insuficientes para análise por décadas")
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">🎯 Correlações entre Variáveis</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(grafico_dispersao_nota_receita(df_filtrado), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Insight card
        corr = df_filtrado[['score', 'revenue']].corr().iloc[0,1]
        st.markdown(f"""
            <div class="glass-card" style="margin-top: 1rem; border-left: 3px solid #4ECDC4;">
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px;">Correlação Nota × Receita</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #4ECDC4; margin-top: 0.3rem;">{corr:.3f}</div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.4); margin-top: 0.3rem;">
                    {'Forte correlação positiva' if corr > 0.5 else 'Correlação moderada' if corr > 0.3 else 'Correlação fraca'}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_orc = grafico_orcamento_receita(df_filtrado)
        if fig_orc:
            st.plotly_chart(fig_orc, use_container_width=True)
        else:
            st.info("Dados de orçamento insuficientes")
        st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-title">🌎 Distribuições Globais</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(grafico_idiomas(df_filtrado), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(grafico_sucesso(df_filtrado), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    fig_mapa = grafico_mapa_mundi(df_filtrado)
    if fig_mapa:
        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.info("Mapa mundi indisponível para os dados selecionados")
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="section-title">💰 Análise Financeira</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(grafico_roi(df_filtrado), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Cards financeiros detalhados
        orc_medio = df_filtrado[df_filtrado["budget_x"] > 0]["budget_x"].mean()
        lucro_medio = (df_filtrado["revenue"] - df_filtrado["budget_x"]).mean()
        
        st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div class="glass-card" style="border-left: 3px solid #45B7D1;">
                    <div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px;">Orçamento Médio</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: white; margin-top: 0.3rem;">${orc_medio/1e6:.1f}M</div>
                </div>
                <div class="glass-card" style="border-left: 3px solid #4ECDC4;">
                    <div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px;">Lucro Médio</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #4ECDC4; margin-top: 0.3rem;">${lucro_medio/1e6:.1f}M</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Tabela de top blockbusters
        st.markdown("**🏆 Top Blockbusters**")
        top_block = df_filtrado[df_filtrado['success_category'] == 'Blockbuster'].nlargest(5, 'revenue')[['names', 'revenue', 'score', 'roi']]
        top_block['revenue'] = top_block['revenue'].apply(lambda x: f"${x/1e6:.0f}M")
        top_block['roi'] = top_block['roi'].apply(lambda x: f"{x:.0f}%")
        top_block.columns = ['Filme', 'Receita', 'Nota', 'ROI']
        st.dataframe(top_block, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab6:
    st.markdown('<div class="section-title">📅 Sazonalidade</div>', unsafe_allow_html=True)
    
    fig_saz = grafico_sazonalidade(df_filtrado)
    if fig_saz:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_saz, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Dados de sazonalidade indisponíveis")
    
    # Insights de sazonalidade
    if 'mes' in df_filtrado.columns and not df_filtrado['mes'].isnull().all():
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        rec_mes = df_filtrado[df_filtrado['mes'] > 0].groupby('mes')['revenue'].mean()
        if not rec_mes.empty:
            melhor_mes = meses[rec_mes.idxmax()-1]
            pior_mes = meses[rec_mes.idxmin()-1]
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                    <div class="glass-card" style="border-left: 3px solid #4ECDC4;">
                        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">Melhor Mês para Receita</div>
                        <div style="font-size: 2rem; font-weight: 700; color: #4ECDC4;">{melhor_mes}</div>
                        <div style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">${rec_mes.max()/1e6:.1f}M média</div>
                    </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                    <div class="glass-card" style="border-left: 3px solid #FF6B6B;">
                        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">Pior Mês para Receita</div>
                        <div style="font-size: 2rem; font-weight: 700; color: #FF6B6B;">{pior_mes}</div>
                        <div style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">${rec_mes.min()/1e6:.1f}M média</div>
                    </div>
                """, unsafe_allow_html=True)

with tab7:
    st.markdown('<div class="section-header">🔍 Dados Completos</div>', unsafe_allow_html=True)
    
    # Filtro de colunas
    col_vis = st.multiselect(
        "Colunas visíveis",
        options=df_filtrado.columns.tolist(),
        default=['names', 'date_x', 'score', 'revenue', 'budget_x', 'roi', 'success_category', 'orig_lang']
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.dataframe(
        df_filtrado[col_vis],
        use_container_width=True,
        height=600,
        column_config={
            "revenue": st.column_config.NumberColumn("Receita", format="$%.0f"),
            "budget_x": st.column_config.NumberColumn("Orçamento", format="$%.0f"),
            "roi": st.column_config.NumberColumn("ROI", format="%.1f%%"),
            "score": st.column_config.NumberColumn("Nota", format="%.1f ⭐"),
            "success_category": st.column_config.TextColumn("Sucesso"),
            "names": st.column_config.TextColumn("Filme", width="large")
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Download CSV Filtrado",
        csv,
        f"cineanalytics_{ano_min}-{ano_max}.csv",
        "text/csv",
        use_container_width=True
    )

# Footer
st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem 1rem; color: rgba(255,255,255,0.3); font-size: 0.8rem; letter-spacing: 1px;">
        CINEANALYTICS PRO • DASHBOARD INTERATIVO • 2026
    </div>
""", unsafe_allow_html=True)
