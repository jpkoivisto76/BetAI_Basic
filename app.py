import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

st.title("⚽ BetAI_Basic – Älykäs Vetokeskus")
st.sidebar.header("Navigaatio")

nav = st.sidebar.selectbox("Valitse näkymä", [
    "TOP 3 Valioliiga", 
    "Bundesliiga", 
    "Tulevat ottelut & Tuomarit", 
    "Seuranta & P&L"
])

# Testidata
df_valio = pd.DataFrame({
    "Joukkue": ["Arsenal", "Man City", "Liverpool", "Chelsea", "Tottenham"],
    "Pelatut": [10, 10, 10, 10, 10],
    "Kulmat / peli": [6.5, 7.1, 5.8, 5.2, 5.9],
    "Kortit / peli": [1.8, 1.5, 2.1, 2.4, 2.0]
})

df_buli = pd.DataFrame({
    "Joukkue": ["Bayern Munich", "Dortmund", "Leipzig", "Leverkusen", "Stuttgart"],
    "Pelatut": [9, 9, 9, 9, 9],
    "Kulmat / peli": [6.8, 6.2, 5.5, 6.0, 5.1],
    "Kortit / peli": [1.6, 1.9, 2.2, 1.7, 2.1]
})

df_tulevat = pd.DataFrame({
    "Sarja": ["Premier League", "Premier League", "Bundesliga", "Bundesliga"],
    "Päiväys": ["2026-11-07", "2026-11-07", "2026-11-08", "2026-11-08"],
    "Ottelu": ["Arsenal - Liverpool", "Chelsea - Man Utd", "Bayern - Leipzig", "Dortmund - Leverkusen"],
    "Tuomari": ["Michael Oliver", "Anthony Taylor", "Felix Zwayer", "Deniz Aytekin"],
    "Odotetut Kulmat": [11.5, 10.2, 12.0, 11.1],
    "Odotetut Kortit": [3.8, 4.2, 3.5, 4.0]
})

df_seuranta = pd.DataFrame({
    "Päivä": ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"],
    "Tuotto (Units)": [1.2, 0.8, -0.5, 2.1, 1.5, 0.4, 1.8]
})

# Näkymien renderöinti
if nav == "TOP 3 Valioliiga":
    st.header("🏆 Valioliigan Joukkuetilastot")
    st.dataframe(df_valio)

elif nav == "Bundesliiga":
    st.header("🏆 Bundesliigan Joukkuetilastot")
    st.dataframe(df_buli)

elif nav == "Tulevat ottelut & Tuomarit":
    st.header("📅 Tulevat ottelut, tuomarit ja odotusarvot")
    st.dataframe(df_tulevat)

elif nav == "Seuranta & P&L":
    st.header("📈 Vedonlyönnin Seuranta & P&L")
    st.dataframe(df_seuranta)
    fig = px.line(df_seuranta, x="Päivä", y="Tuotto (Units)", title="Viikoittainen tuottokäyrä", markers=True)
    st.plotly_chart(fig)
