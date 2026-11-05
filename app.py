import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

st.title("⚽ BetAI_Basic – Älykäs Vetokeskus")
st.sidebar.header("Navigaatio")

nav = st.sidebar.selectbox("Valitse näkymä", [
    "TOP 3 Valioliiga", 
    "TOP 20 Vihjettä", 
    "TOP 5 Bet Builderit", 
    "Bundesliiga", 
    "Tulevat ottelut & Tuomarit", 
    "Seuranta & P&L"
])

# 1. TOP 3 VALIOLIIGA
df_valio = pd.DataFrame({
    "Ottelu / Joukkue": ["Arsenal - Liverpool", "Man City - Chelsea", "Tottenham - Man Utd"],
    "Pelatut": [10, 10, 10],
    "Kulmat / peli (Keskiarvo)": [11.5, 10.8, 11.2],
    "Kortit / peli (Keskiarvo)": [3.8, 4.1, 3.9],
    "Arvio / Vihje": ["Yli 9.5 kulmaa", "Kortteja yli 3.5", "Kotivoitto + Kulmat"]
})

# 2. TOP 20 VIHJETTÄ
df_vihjeet = pd.DataFrame({
    "Nro": range(1, 6),
    "Ottelu": ["Arsenal vs Liverpool", "Bayern vs Leipzig", "Dortmund vs Leverkusen", "Man City vs Chelsea", "Stuttgart vs Frankfurt"],
    "Kohde / Veto": ["1X & Yli 1.5 maalia", "Kotivoitto (1)", "BTTS (Molemmat joukkueet tekevät maalin)", "Yli 9.5 kulmapotkua", "Kortit yhteensä yli 4.5"],
    "Kerroin": [1.75, 1.60, 1.85, 1.90, 2.10],
    "Luottamus / EV": ["+4.2%", "+2.1%", "+3.5%", "+1.8%", "+5.0%"]
})

# 3. TOP 5 BET BUILDERIT
df_builderit = pd.DataFrame({
    "Rakennelma": ["Builder #1 (Valioliiga)", "Builder #2 (Bundesliiga)", "Builder #3 (Kulmaerikoistuntija)", "Builder #4 (Korttiralli)", "Builder #5 (Huippuottelu)"],
    "Kohteet": [
        "Arsenal voittaa + Yli 8.5 kulmaa + Saka tekee maalin", 
        "Bayern -1.5 + Yli 2.5 maalia", 
        "Kulmat yhteensä yli 10.5 + Kumpikin joukkue saa kulman 1. puoliajalla", 
        "Tuomari antaa vähintään 5 keltaista korttia", 
        "Tasapeli tai vierasvoitto + Molemmat saavat kortin"
    ],
    "Yhteiskerroin": [4.20, 3.10, 2.50, 3.80, 5.10]
})

# 4. BUNDESLIGA
df_buli = pd.DataFrame({
    "Joukkue": ["Bayern Munich", "Dortmund", "Leipzig", "Leverkusen", "Stuttgart"],
    "Pelatut": [9, 9, 9, 9, 9],
    "Kulmat / peli": [6.8, 6.2, 5.5, 6.0, 5.1],
    "Kortit / peli": [1.6, 1.9, 2.2, 1.7, 2.1]
})

# 5. TULEVAT OTTELUT JA TUOMARIT
df_tulevat = pd.DataFrame({
    "Sarja": ["Premier League", "Premier League", "Bundesliga", "Bundesliga"],
    "Päiväys": ["2026-11-07", "2026-11-07", "2026-11-08", "2026-11-08"],
    "Ottelu": ["Arsenal - Liverpool", "Chelsea - Man Utd", "Bayern - Leipzig", "Dortmund - Leverkusen"],
    "Tuomari": ["Michael Oliver", "Anthony Taylor", "Felix Zwayer", "Deniz Aytekin"],
    "Odotetut Kulmat": [11.5, 10.2, 12.0, 11.1],
    "Odotetut Kortit": [3.8, 4.2, 3.5, 4.0]
})

# 6. SEURANTA & P&L
df_seuranta = pd.DataFrame({
    "Päivä": ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"],
    "Tuotto (Units)": [1.2, 0.8, -0.5, 2.1, 1.5, 0.4, 1.8]
})

# RENDERÖINTI NAVIGAATION MUKAAN
if nav == "TOP 3 Valioliiga":
    st.header("🏆 TOP 3 Valioliiga & Tilastot")
    st.dataframe(df_valio, use_container_width=True)

elif nav == "TOP 20 Vihjettä":
    st.header("💡 TOP 20 Vihjettä & Arviot")
    st.dataframe(df_vihjeet, use_container_width=True)

elif nav == "TOP 5 Bet Builderit":
    st.header("🛠️ TOP 5 Bet Builder -yhdistelmät")
    st.dataframe(df_builderit, use_container_width=True)

elif nav == "Bundesliiga":
    st.header("🏆 Bundesliigan Joukkuetilastot")
    st.dataframe(df_buli, use_container_width=True)

elif nav == "Tulevat ottelut & Tuomarit":
    st.header("📅 Tulevat ottelut, tuomarit ja odotusarvot")
    st.dataframe(df_tulevat, use_container_width=True)

elif nav == "Seuranta & P&L":
    st.header("📈 Vedonlyönnin Seuranta & P&L")
    st.dataframe(df_seuranta, use_container_width=True)
    fig = px.line(df_seuranta, x="Päivä", y="Tuotto (Units)", title="Viikoittainen tuottokäyrä", markers=True)
    st.plotly_chart(fig, use_container_width=True)
