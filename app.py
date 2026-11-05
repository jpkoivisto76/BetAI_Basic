import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

st.title("⚽ BetAI_Basic – Älykäs Vetokeskus")
st.sidebar.header("Navigaatio")

nav = st.sidebar.selectbox("Valitse näkymä", [
    "TOP 3 Valioliiga", 
    "TOP 20 vihjettä", 
    "TOP5 Builderit", 
    "Tulevat ottelut & Tuomarit", 
    "Premier League", 
    "Bundesliga", 
    "La Liga", 
    "Serie A", 
    "Ligue 1",
    "Seuranta & P&L"
])

SHEET_ID = "14Og1POtwncAIvcFiFkugUvms1oWu8VP0eOO5PHwB15U"

@st.cache_data(ttl=300)
def load_gsheet(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return None

if nav == "TOP 3 Valioliiga":
    st.header("🏆 TOP 3 Valioliiga & Vihjeet")
    df = load_gsheet("TOP 3 Valioliiga")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "TOP 20 vihjettä":
    st.header("💡 TOP 20 Vihjettä & Arviot")
    df = load_gsheet("TOP 20 vihjettä")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "TOP5 Builderit":
    st.header("🛠️ TOP 5 Bet Builder -yhdistelmät")
    df = load_gsheet("TOP5 Builderit")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "Tulevat ottelut & Tuomarit":
    st.header("📅 Tulevat ottelut, tuomarit ja odotusarvot")
    df = load_gsheet("Tulevat ottelut")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "Premier League":
    st.header("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League - Joukkuetilastot")
    df = load_gsheet("Premier League")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "Bundesliiga":
    st.header("🇩🇪 Bundesliga - Joukkuetilastot")
    df = load_gsheet("Bundesliga")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "La Liga":
    st.header("🇪🇸 La Liga - Joukkuetilastot")
    df = load_gsheet("La Liga")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "Serie A":
    st.header("🇮🇹 Serie A - Joukkuetilastot")
    df = load_gsheet("Serie A")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "Ligue 1":
    st.header("🇫🇷 Ligue 1 - Joukkuetilastot")
    df = load_gsheet("Ligue 1")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "Seuranta & P&L":
    st.header("📈 Vedonlyönnin Seuranta & P&L")
    df = load_gsheet("Seuranta & P&L")
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Seuranta-taulukko on tällä hetkellä tyhjä.")
