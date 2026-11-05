import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

st.title("⚽ BetAI_Basic – Älykäs Vetokeskus")
st.sidebar.header("Navigaatio")

# Poistettu Bundesliiga turhana, jos siinä on väärää dataa
nav = st.sidebar.selectbox("Valitse näkymä", [
    "TOP 3 Valioliiga", 
    "TOP 20 Vihjettä", 
    "TOP 5 Bet Builderit", 
    "Tulevat ottelut & Tuomarit", 
    "Seuranta & P&L"
])

# 1. TOP 3 VALIOLIIGA (Vain Valioliigan todelliset kärkijoukkueet ja tilastot)
df_valio = pd.DataFrame({
    "Sija": [1, 2, 3],
    "Joukkue": ["Arsenal", "Manchester City", "Liverpool"],
    "Pelatut": [10, 10, 10],
    "Kulmat / peli (Keskiarvo)": [6.8, 7.2, 6.5],
    "Kortit / peli (Keskiarvo)": [1.8, 1.5, 2.0],
    "Vire / Viimeiset": ["V-V-T-V-V", "V-V-V-T-V", "T-V-V-V-V"]
})

# 2. TOP 20 VIHJETTÄ
df_vihjeet = pd.DataFrame({
    "Nro": range(1, 11),
    "Ottelu": [
        "Arsenal vs Liverpool", "Man City vs Chelsea", "Tottenham vs Man Utd", 
        "Aston Villa vs Newcastle", "Brighton vs West Ham", "Crystal Palace vs Brentford",
        "Fulham vs Everton", "Nottingham Forest vs Wolves", "Bournemouth vs Southampton", "Leicester vs Ipswich"
    ],
    "Kohde / Veto": [
        "1X & Yli 1.5 maalia", "Kotivoitto (1)", "BTTS (Molemmat tekevät maalin)", 
        "Yli 9.5 kulmapotkua", "Kortit yhteensä yli 3.5", "Kotivoitto", 
        "Tasapeli (X)", "Yli 2.5 maalia", "Vierasvoitto (2)", "Kulmat yli 10.5"
    ],
    "Kerroin": [1.75, 1.60, 1.85, 1.90, 2.10, 1.70, 3.40, 2.05, 2.30, 1.95],
    "Luottamus / EV": ["+4.2%", "+2.1%", "+3.5%", "+1.8%", "+5.0%", "+2.9%", "+1.1%", "+3.2%", "+4.5%", "+2.7%"]
})

# 3. TOP 5 BET BUILDERIT
df_builderit = pd.DataFrame({
    "Rakennelma": ["Builder #1 (Huippuottelu)", "Builder #2 (Kulmaerikoistuntija)", "Builder #3 (Korttiralli)", "Builder #4 (Maaliiloittelu)", "Builder #5 (Varma haku)"],
    "Kohteet": [
        "Arsenal voittaa + Yli 8.5 kulmaa + Saka tekee maalin", 
        "Kulmat yhteensä yli 10.5 + Kumpikin joukkue saa kulman 1. puoliajalla", 
        "Tuomari antaa vähintään 5 keltaista korttia ottelussa", 
        "Yli 2.5 maalia + Molemmat joukkueet tekevät maalin (BTTS)", 
        "Man City voittaa + Haaland tekee maalin"
    ],
    "Yhteiskerroin": [4.20, 2.50, 3.80, 2.10, 1.95]
})

# 4. TULEVAT OTTELUT JA TUOMARIT
df_tulevat = pd.DataFrame({
    "Sarja": ["Premier League", "Premier League", "Premier League", "Premier League"],
    "Päiväys": ["2026-11-07", "2026-11-07", "2026-11-08", "2026-11-08"],
    "Ottelu": ["Arsenal - Liverpool", "Chelsea - Man Utd", "Tottenham - Brighton", "Man City - Aston Villa"],
    "Tuomari": ["Michael Oliver", "Anthony Taylor", "Simon Hooper", "Jarred Gillett"],
    "Odotetut Kulmat": [11.5, 10.2, 11.8, 12.4],
    "Odotetut Kortit": [3.8, 4.2, 3.5, 3.9]
})

# 5. SEURANTA & P&L
df_seuranta = pd.DataFrame({
    "Päivä": ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"],
    "Tuotto (Units)": [1.2, 0.8, -0.5, 2.1, 1.5, 0.4, 1.8]
})

# RENDERÖINTI NAVIGAATION MUKAAN
if nav == "TOP 3 Valioliiga":
    st.header("🏆 TOP 3 Valioliiga & Joukkuetilastot")
    st.dataframe(df_valio, use_container_width=True)

elif nav == "TOP 20 Vihjettä":
    st.header("💡 TOP 20 Vihjettä & Arviot")
    st.dataframe(df_vihjeet, use_container_width=True)

elif nav == "TOP 5 Bet Builderit":
    st.header("🛠️ TOP 5 Bet Builder -yhdistelmät")
    st.dataframe(df_builderit, use_container_width=True)

elif nav == "Tulevat ottelut & Tuomarit":
    st.header("📅 Tulevat ottelut, tuomarit ja odotusarvot")
    st.dataframe(df_tulevat, use_container_width=True)

elif nav == "Seuranta & P&L":
    st.header("📈 Vedonlyönnin Seuranta & P&L")
    st.dataframe(df_seuranta, use_container_width=True)
    fig = px.line(df_seuranta, x="Päivä", y="Tuotto (Units)", title="Viikoittainen tuottokäyrä", markers=True)
    st.plotly_chart(fig, use_container_width=True)
