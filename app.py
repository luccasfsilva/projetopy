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
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="CineAnalytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS - VISUAL EXATO DA IMAGEM
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Background gradiente suave roxo/azul */
    .stApp {
        background: linear-gradient(135deg, #e0e7ff 0%, #d1d5ff 30%, #c7b8ff 60%, #a5b4fc 100%);
    }
    
    /* Remove padding padrão */
    .block-container {
        padding: 1rem 2rem 3rem 2rem;
        max-width: 100%;
    }
    
    /* Sidebar estilo imagem */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.5);
        min-width: 220px !important;
        max-width: 220px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    
    /* Cards principais - estilo imagem */
    .main-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 1.5rem;
        box-shadow: 
            0 4px 20px rgba(139, 92, 246, 0.08),
            0 1px 3px rgba(0,0,0,0.05),
            inset 0 1px 0 rgba(255,255,255,0.6);
        border: 1px solid rgba(255,255,255,0.6);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .main-card:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 8px 30px rgba(139, 92, 246, 0.15),
            0 2px 5px rgba(0,0,0,0.08),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    /* Header card */
    .header-bar {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1rem 2rem;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(255,255,255,0.6);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Logo/Title */
    .app-title {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #7c3aed, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    
    /* Sidebar nav items */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.9rem 1rem;
        border-radius: 16px;
        margin-bottom: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #6b7280;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .nav-item:hover {
        background: rgba(124, 58, 237, 0.08);
        color: #7c3aed;
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        color: white;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }
    
    .nav-icon {
        font-size: 1.3rem;
        width: 28px;
        text-align: center;
    }
    
    /* Section titles inside cards */
    .card-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    /* Big numbers */
    .big-number {
        font-size: 2rem;
        font-weight: 800;
        color: #1f2937;
        line-height: 1;
    }
    
    .big-number.purple { color: #7c3aed; }
    .big-number.blue { color: #3b82f6; }
    .big-number.pink { color: #ec4899; }
    .big-number.cyan { color: #06b6d4; }
    
    .number-label {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 0.4rem;
        font-weight: 500;
    }
    
    /* Filter pills */
    .filter-pill {
        background: rgba(255,255,255,0.9);
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
        font-weight: 500;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .filter-pill:hover, .filter-pill.active {
        border-color: #8b5cf6;
        color: #7c3aed;
        background: rgba(139, 92, 246, 0.05);
    }
    
    /* Chart containers */
    .chart-wrapper {
        background: rgba(255,255,255,0.5);
        border-radius: 16px;
        padding: 0.5rem;
    }
    
    /* Hide streamlit default elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(139, 92, 246, 0.3);
        border-radius: 10px;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: #e5e7eb !important;
    }
    .stSlider [role="slider"] {
        background: #8b5cf6 !important;
        box-shadow: 0 2px 10px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.9) !important;
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
    }
    
    /* Metric row */
    .metric-row {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .metric-badge {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    
    .badge-purple { background: linear-gradient(135deg, #c4b5fd, #a78bfa); }
    .badge-blue { background: linear-gradient(135deg, #93c5fd, #60a5fa); }
    .badge-pink { background: linear-gradient(135deg, #f9a8d4, #f472b6); }
    .badge-cyan { background: linear-gradient(135deg, #67e8f9, #22d3ee); }
    .badge-orange { background: linear-gradient(135deg, #fdba74, #fb923c); }
    
    /* Progress ring simulation */
    .ring-container {
        position: relative;
        width: 120px;
        height: 120px;
        margin: 0 auto;
    }
    
    /* Divider */
    .soft-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.2), transparent);
        margin: 1rem 0;
    }
    
    /* Tab styling override */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.5);
        border-radius: 16px;
        padding: 6px;
        gap: 4px;
        border: 1px solid rgba(255,255,255,0.4);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: #6b7280;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0.5rem 1.2rem;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# DADOS
# =========================
@st.cache_data(show_spinner=False)
def carregar_dados():
    CSV_URL = "https://raw.githubusercontent.com/luccasfsilva/projetopy/main/imdb_movies.csv"
    try:
        df = pd.read_csv(CSV_URL, parse_dates=['date_x'])
        df["revenue"] = pd.to_numeric(df.get("revenue"), errors="coerce").fillna(0)
        df["score"] = pd.to_numeric(df.get("score"), errors="coerce")
        df["budget_x"] = pd.to_numeric(df.get("budget_x"), errors="coerce").fillna(0)
        df["ano"] = df["date_x"].dt.year.fillna(0).astype(int)
        df["mes"] = df["date_x"].dt.month.fillna(0).astype(int)
        df["roi"] = np.where(df["budget_x"] > 0, (df["revenue"] - df["budget_x"]) / df["budget_x"] * 100, 0)
        
        q80, q60, q40 = df['revenue'].quantile([0.8, 0.6, 0.4])
        conditions = [df['revenue'] >= q80, df['revenue'] >= q60, df['revenue'] >= q40, df['revenue'] < q40]
        df['success_category'] = np.select(conditions, ['Blockbuster', 'High', 'Medium', 'Low'], default='Low')
        df['decada'] = (df['ano'] // 10) * 10
        return df
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        return None

df = carregar_dados()
if df is None or df.empty:
    st.stop()

# =========================
# TRADUÇÕES
# =========================
TRADUCOES = {
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

def traduzir(nome):
    return TRADUCOES.get(nome, nome) if pd.notna(nome) else nome

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎬</div>
            <div style="font-weight: 800; font-size: 1.1rem; color: #1f2937;">CineAnalytics</div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.2rem;">Dashboard Inteligente</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="nav-item active">
            <span class="nav-icon">🏠</span>
            <span>Dashboard</span>
        </div>
        <div class="nav-item">
            <span class="nav-icon">📊</span>
            <span>Análises</span>
        </div>
        <div class="nav-item">
            <span class="nav-icon">🎞️</span>
            <span>Filmes</span>
        </div>
        <div class="nav-item">
            <span class="nav-icon">💰</span>
            <span>Financeiro</span>
        </div>
        <div class="nav-item">
            <span class="nav-icon">🌍</span>
            <span>Global</span>
        </div>
        <div class="nav-item">
            <span class="nav-icon">⭐</span>
            <span>Ratings</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    
    # Filtros na sidebar
    st.markdown('<div style="font-size: 0.8rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">⚙️ Filtros</div>', unsafe_allow_html=True)
    
    anos = sorted(df[df["ano"] > 0]["ano"].unique())
    ano_min, ano_max = st.select_slider("Ano", options=anos, value=(min(anos), max(anos)), label_visibility="collapsed")
    
    score_min, score_max = st.slider("Nota", 0.0, 10.0, (0.0, 10.0), 0.1, label_visibility="collapsed")
    
    max_rev = float(df["revenue"].max())
    receita_min, receita_max = st.slider("Receita", 0.0, max_rev, (0.0, max_rev), 1_000_000.0, format="$%.0f", label_visibility="collapsed")

# =========================
# FILTRAR
# =========================
df_f = df[
    (df["ano"] >= ano_min) & (df["ano"] <= ano_max) &
    (df["score"] >= score_min) & (df["score"] <= score_max) &
    (df["revenue"] >= receita_min) & (df["revenue"] <= receita_max)
].copy()

df_f["names"] = df_f["names"].apply(traduzir)

if df_f.empty:
    st.error("Nenhum filme encontrado.")
    st.stop()

# =========================
# HEADER
# =========================
st.markdown(f"""
    <div class="header-bar">
        <div>
            <div class="app-title">🎬 CineAnalytics</div>
            <div style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.2rem;">{len(df_f):,} filmes selecionados • {ano_min}–{ano_max}</div>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <span class="filter-pill active">📅 Anual</span>
            <span class="filter-pill">📊 Mensal</span>
            <span class="filter-pill">🎬 Gênero</span>
            <span class="filter-pill">🌍 País</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# =========================
# KPI ROW
# =========================
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-purple">💰</div>
                <div>
                    <div class="big-number purple">${df_f['revenue'].sum()/1e9:.1f}B</div>
                    <div class="number-label">Receita Total</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-blue">📈</div>
                <div>
                    <div class="big-number blue">${df_f['revenue'].mean()/1e6:.1f}M</div>
                    <div class="number-label">Média por Filme</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-pink">⭐</div>
                <div>
                    <div class="big-number pink">{df_f['score'].mean():.1f}</div>
                    <div class="number-label">Nota Média IMDb</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    roi_m = df_f[df_f['roi'] > 0]['roi'].mean()
    if pd.isna(roi_m): roi_m = 0
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-cyan">🚀</div>
                <div>
                    <div class="big-number cyan">{roi_m:.0f}%</div>
                    <div class="number-label">ROI Médio</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-orange">🎞️</div>
                <div>
                    <div class="big-number" style="color: #f97316;">{len(df_f):,}</div>
                    <div class="number-label">Filmes no Período</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# =========================
# GRÁFICOS - TEMA CLARO
# =========================
def tema_claro(fig, h=350):
    fig.update_layout(
        plot_bgcolor='rgba(255,255,255,0.3)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#4b5563', family='Inter, sans-serif', size=11),
        title_font=dict(size=13, color='#1f2937', family='Inter, sans-serif'),
        margin=dict(l=50, r=30, t=50, b=40),
        height=h,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, bgcolor='rgba(0,0,0,0)'),
        hoverlabel=dict(bgcolor='white', bordercolor='#e5e7eb', font=dict(color='#1f2937'))
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)', showline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)', showline=False)
    return fig

# --- Gráfico 1: Receita Anual (barra + linha) ---
receita_ano = df_f[df_f['ano'] > 0].groupby('ano')['revenue'].sum().reset_index()
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=receita_ano['ano'], y=receita_ano['revenue'],
    marker=dict(
        color=receita_ano['revenue'],
        colorscale=[[0, '#c4b5fd'], [0.5, '#8b5cf6'], [1, '#7c3aed']],
        line=dict(width=0)
    ),
    name='Receita', hovertemplate='%{x}: $%{y:,.0f}<extra></extra>'
))
# Linha suave
fig1.add_trace(go.Scatter(
    x=receita_ano['ano'], y=receita_ano['revenue'],
    mode='lines', line=dict(color='#ec4899', width=3),
    name='Tendência', hoverinfo='skip'
))
fig1.update_layout(
    title='📈 Receita Anual da Indústria',
    xaxis_title='', yaxis_title='', yaxis_tickformat='$.2s',
    barmode='group', showlegend=False
)
fig1 = tema_claro(fig1, 320)

# --- Gráfico 2: Top Filmes ---
top10 = df_f.nlargest(10, 'revenue')[['names', 'revenue', 'score']]
fig2 = px.bar(
    top10, x='revenue', y='names', orientation='h',
    color='revenue', color_continuous_scale=['#ddd6fe', '#a78bfa', '#7c3aed']
)
fig2.update_traces(marker_line_width=0, hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>')
fig2.update_layout(
    title='🏆 Top 10 Filmes por Receita', yaxis_title='', xaxis_title='',
    xaxis_tickformat='$.2s', coloraxis_showscale=False,
    yaxis=dict(categoryorder='total ascending')
)
fig2 = tema_claro(fig2, 320)

# --- Gráfico 3: Pizza Idiomas ---
idiomas = df_f['orig_lang'].value_counts().head(6).reset_index()
idiomas.columns = ['Idioma', 'Qtd']
fig3 = px.pie(
    idiomas, values='Qtd', names='Idioma', hole=0.65,
    color_discrete_sequence=['#8b5cf6', '#a78bfa', '#c4b5fd', '#60a5fa', '#22d3ee', '#f472b6']
)
fig3.update_traces(
    textposition='outside', textinfo='label+percent', textfont=dict(size=10),
    marker=dict(line=dict(color='white', width=2)),
    hovertemplate='<b>%{label}</b><br>%{value} filmes<extra></extra>'
)
fig3.update_layout(
    title='🌎 Idiomas Originais', showlegend=False,
    annotations=[dict(text='IDIOMAS', x=0.5, y=0.5, font_size=14, showarrow=False, font_color='#9ca3af')]
)
fig3 = tema_claro(fig3, 320)

# --- Gráfico 4: Scatter Nota x Receita ---
amostra = df_f.sample(min(1500, len(df_f))) if len(df_f) > 1500 else df_f
fig4 = px.scatter(
    amostra, x='score', y='revenue', color='score',
    color_continuous_scale=['#f472b6', '#fbbf24', '#34d399', '#60a5fa'],
    opacity=0.7, size_max=10
)
fig4.update_traces(
    marker=dict(size=7, line=dict(width=1, color='white')),
    hovertemplate='<b>%{customdata[0]}</b><br>Nota: %{x:.1f}<br>Receita: $%{y:,.0f}<extra></extra>',
    customdata=np.column_stack([amostra['names']])
)
fig4.update_layout(
    title='🎯 Nota vs Receita', xaxis_title='Nota IMDb', yaxis_title='Receita',
    yaxis_tickformat='$.2s', coloraxis_showscale=False
)
fig4 = tema_claro(fig4, 320)

# --- Gráfico 5: Sazonalidade ---
saz = df_f[df_f['mes'] > 0].groupby('mes').agg({'revenue': 'mean', 'names': 'count'}).reset_index()
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
saz['mes_nome'] = saz['mes'].apply(lambda x: meses[x-1])

fig5 = make_subplots(specs=[[{"secondary_y": True}]])
fig5.add_trace(go.Scatter(
    x=saz['mes_nome'], y=saz['revenue'], mode='lines+markers',
    line=dict(color='#8b5cf6', width=3), marker=dict(size=8, color='#8b5cf6'),
    fill='tozeroy', fillcolor='rgba(139,92,246,0.1)',
    name='Receita Média', hovertemplate='%{x}<br>$%{y:,.0f}<extra></extra>'
), secondary_y=False)
fig5.add_trace(go.Bar(
    x=saz['mes_nome'], y=saz['names'], marker_color='rgba(236,72,153,0.5)',
    marker_line_width=0, name='Lançamentos', hovertemplate='%{x}<br>%{y} filmes<extra></extra>'
), secondary_y=True)
fig5.update_layout(
    title='📅 Sazonalidade de Lançamentos', showlegend=False,
    xaxis_title='', yaxis_title='', yaxis_tickformat='$.0f',
    yaxis2_title='', yaxis2_showgrid=False
)
fig5.update_xaxes(categoryorder='array', categoryarray=meses)
fig5 = tema_claro(fig5, 300)

# --- Gráfico 6: Distribuição Sucesso ---
dist = df_f['success_category'].value_counts().reindex(['Blockbuster', 'High', 'Medium', 'Low']).fillna(0)
cores_sucesso = ['#8b5cf6', '#60a5fa', '#22d3ee', '#d1d5db']
fig6 = go.Figure()
for i, (cat, val) in enumerate(dist.items()):
    fig6.add_trace(go.Bar(
        x=[cat], y=[val], marker_color=cores_sucesso[i],
        text=[f"{val:,}"], textposition='outside', textfont=dict(size=12, color='#4b5563'),
        hovertemplate=f'<b>{cat}</b><br>{val:,} filmes<extra></extra>'
    ))
fig6.update_layout(
    title='📊 Categorias de Sucesso', xaxis_title='', yaxis_title='',
    showlegend=False, bargap=0.4
)
fig6 = tema_claro(fig6, 300)

# --- Gráfico 7: ROI Top ---
df_roi = df_f[(df_f['roi'] > 0) & (df_f['budget_x'] > 0) & (df_f['roi'] < 5000)].nlargest(8, 'roi')
fig7 = px.bar(
    df_roi, x='roi', y='names', orientation='h',
    color='roi', color_continuous_scale=['#c4b5fd', '#a78bfa', '#ec4899']
)
fig7.update_traces(marker_line_width=0, hovertemplate='<b>%{y}</b><br>ROI: %{x:.0f}%<extra></extra>')
fig7.update_layout(
    title='🚀 Top ROI', yaxis_title='', xaxis_title='ROI (%)',
    coloraxis_showscale=False, yaxis=dict(categoryorder='total ascending')
)
fig7 = tema_claro(fig7, 300)

# --- Gráfico 8: Mapa ---
fig8 = None
if "country" in df_f.columns and not df_f["country"].isnull().all():
    df_c = df_f.groupby("country")["revenue"].sum().reset_index()
    df_c.columns = ["raw", "value"]
    def iso2_to_iso3(c):
        try:
            if isinstance(c, str) and len(c) == 2:
                return pycountry.countries.get(alpha_2=c.upper()).alpha_3
            if isinstance(c, str) and len(c) == 3:
                return c.upper()
        except: pass
        return None
    df_c["iso3"] = df_c["raw"].apply(iso2_to_iso3)
    df_c = df_c.dropna(subset=["iso3"])
    if not df_c.empty:
        fig8 = px.choropleth(
            df_c, locations="iso3", color="value", hover_name="raw",
            color_continuous_scale=["#ddd6fe", "#a78bfa", "#7c3aed", "#4c1d95"],
            projection="natural earth", labels={"value": "Receita"}
        )
        fig8.update_geos(
            showcountries=True, showcoastlines=True, showland=True,
            landcolor="#f3f4f6", oceancolor="#e5e7eb",
            coastlinecolor="#d1d5db", countrycolor="#e5e7eb"
        )
        fig8.update_layout(margin=dict(r=0, t=50, l=0, b=0), height=400, coloraxis_colorbar=dict(tickformat='$.2s'))
        fig8 = tema_claro(fig8, 400)

# =========================
# LAYOUT EM GRID (ESTILO IMAGEM)
# =========================
# Row 1: 2 colunas grandes
r1c1, r1c2 = st.columns([1.3, 1])

with r1c1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r1c2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2: 3 colunas
r2c1, r2c2, r2c3 = st.columns([1, 1, 1])

with r2c1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r2c2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r2c3:
    # Card de resumo estilo "Balance" da imagem
    top_filme = df_f.nlargest(1, 'revenue').iloc[0]
    st.markdown(f"""
        <div class="main-card" style="text-align: center; display: flex; flex-direction: column; justify-content: center; height: 100%; min-height: 320px;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">🏆 Maior Bilheteria</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem; line-height: 1.3;">{top_filme['names']}</div>
            <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${top_filme['revenue']/1e9:.2f}B</div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-around; margin-top: 0.5rem;">
                    <div>
                        <div style="font-size: 0.75rem; color: #9ca3af;">Nota</div>
                        <div style="font-weight: 700; color: #f59e0b;">{top_filme['score']:.1f} ⭐</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: #9ca3af;">Ano</div>
                        <div style="font-weight: 700; color: #3b82f6;">{int(top_filme['ano'])}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: #9ca3af;">ROI</div>
                        <div style="font-weight: 700; color: #10b981;">{top_filme['roi']:.0f}%</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Row 3: 2 colunas
r3c1, r3c2 = st.columns([1, 1])

with r3c1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r3c2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 4: 2 colunas
r4c1, r4c2 = st.columns([1, 1])

with r4c1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r4c2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    if fig8:
        st.plotly_chart(fig8, use_container_width=True)
    else:
        st.info("Mapa mundi indisponível")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 5: Tabela de dados
st.markdown('<div class="main-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔍 Dados Completos</div>', unsafe_allow_html=True)

cols_vis = st.multiselect(
    "Colunas",
    options=df_f.columns.tolist(),
    default=['names', 'date_x', 'score', 'revenue', 'budget_x', 'roi', 'success_category', 'orig_lang', 'country']
)
st.dataframe(
    df_f[cols_vis],
    use_container_width=True,
    height=400,
    column_config={
        "revenue": st.column_config.NumberColumn("Receita", format="$%.0f"),
        "budget_x": st.column_config.NumberColumn("Orçamento", format="$%.0f"),
        "roi": st.column_config.NumberColumn("ROI", format="%.1f%%"),
        "score": st.column_config.NumberColumn("Nota", format="%.1f ⭐"),
        "names": st.column_config.TextColumn("Filme", width="large")
    },
    hide_index=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #9ca3af; font-size: 0.8rem;">
        CineAnalytics • Dashboard Cinematográfico Interativo
    </div>
""", unsafe_allow_html=True)
