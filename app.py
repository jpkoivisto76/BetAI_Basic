import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

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
    encoded_sheet_name = quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"
    try:
        df = pd.read_csv(url)
        # Poistetaan automaattisesti kaikki tyhjät 'Unnamed'-sarakkeet
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        return str(e)

# Näkymien renderöinti
if nav == "TOP 3 Valioliiga":
    st.header("🏆 TOP 3 Valioliiga & Vihjeet")
    df = load_gsheet("TOP 3 Valioliiga")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "TOP 20 vihjettä":
    st.header("💡 TOP 20 Vihjettä & Arviot")
    df = load_gsheet("TOP 20 vihjettä")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "TOP5 Builderit":
    st.header("🛠️ TOP 5 Bet Builder -yhdistelmät")
    df = load_gsheet("TOP5 Builderit")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "Tulevat ottelut & Tuomarit":
    st.header("📅 Tulevat ottelut, tuomarit ja odotusarvot")
    df = load_gsheet("Tulevat ottelut")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "Premier League":
    st.header("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League - Joukkuetilastot")
    df = load_gsheet("Premier League")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "Bundesliiga":
    st.header("🇩🇪 Bundesliga - Joukkuetilastot")
    df = load_gsheet("Bundesliga")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "La Liga":
    st.header("🇪🇸 La Liga - Joukkuetilastot")
    df = load_gsheet("La Liga")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "Serie A":
    st.header("🇮🇹 Serie A - Joukkuetilastot")
    df = load_gsheet("Serie A")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "Ligue 1":
    st.header("🇫🇷 Ligue 1 - Joukkuetilastot")
    df = load_gsheet("Ligue 1")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. (Virhe: {df})")

elif nav == "Seuranta & P&L":
    st.header("📈 Vedonlyönnin Seuranta & P&L")
    df = load_gsheet("Seuranta & P&L")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.info("Seuranta-taulukko on tällä hetkellä tyhjä Google Sheetsissä.")
