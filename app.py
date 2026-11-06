import streamlit as st
import pandas as pd
from urllib.parse import quote

# Sivuston perusasetukset (leveä tila)
st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

st.title("⚽ BetAI_Basic – Mobiilivetokeskus")

# 1. YLÄVALIKKO: Nopea ja helppo liikkuminen ilman sivupalkin häiriöitä
nav_options = [
    "TOP 10 Builderit", 
    "TOP 3 Valioliiga", 
    "TOP 20 vihjettä", 
    "TOP 20 Valioliiga Laukaukset",
    "TOP 20 Valioliiga SoT (Maalia kohti)",
    "TOP 20 Valioliiga Rikkeet",
    "Muut liigat: Laukaukset",
    "Muut liigat: SoT (Maalia kohti)",
    "Muut liigat: Rikkeet",
    "Tulevat ottelut & Tuomarit", 
    "Premier League", 
    "Bundesliga", 
    "La Liga", 
    "Serie A", 
    "Seuranta & P&L"
]

nav = st.selectbox("📌 Valitse näkymä:", nav_options, index=0)
st.divider()

SHEET_ID = "14Og1POtwncAIvcFiFkugUvms1oWu8VP0eOO5PHwB15U"

@st.cache_data(ttl=300)
def load_gsheet(sheet_name):
    encoded_sheet_name = quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"
    try:
        df = pd.read_csv(url)
        if isinstance(df, pd.DataFrame) and not df.empty:
            if "<html" in str(df.iloc[0, 0]).lower():
                return f"Virhe: Välilehteä '{sheet_name}' ei löytynyt tai linkki ei toimi."
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        return str(e)

# ==========================================
# MOBIILIKORTTI- JA NÄKYMÄLOGIIKKA
# ==========================================

if nav == "TOP 10 Builderit":
    st.header("🛠️ TOP 10 Bet Builder -yhdistelmät")
    df = load_gsheet("TOP 10 Builderit")
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        for index, row in df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### #{row.get('Rank', index+1)} {row.get('Ottelu', 'Ottelu')}")
                    st.caption(f"📅 {row.get('Pvm', '')}")
                with col2:
                    st.markdown(f"### 🎯 {row.get('Arvioitu Kerroin', '')}")
                
                st.info(f"**Builder Paketti:** \n\n{row.get('Builder Paketti', '')}")
                
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("Pisteet", row.get('Builder Score', ''))
                m2.metric("Lauk.", row.get('Laukaukset (35%)', ''))
                m3.metric("Kulmat", row.get('Kulmat (25%)', ''))
                m4.metric("Kortit", row.get('Kortit (20%)', ''))
                m5.metric("Maalit", row.get('Maalit (20%)', ''))
        
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "TOP 20 vihjettä":
    st.header("💡 TOP 20 Vihjettä & Arviot")
    df = load_gsheet("TOP 20 vihjettä")
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        for index, row in df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### #{row.get('Rank', index+1)} {row.get('Ottelu', '')}")
                    st.caption(f"📅 {row.get('Pvm', '')} | 🏆 {row.get('Sarja', '')}")
                with col2:
                    st.markdown(f"### 📈 {row.get('Kerroin', '')}")
                
                st.success(f"**Suositus Veto:** {row.get('Veto', '')}")
                
                b1, b2, b3 = st.columns(3)
                b1.metric("Todennäk.", row.get('Todennäköisyys', ''))
                b2.metric("EV %", row.get('EV %', ''))
                b3.metric("Luottamus", row.get('Luottamus', ''))
        
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei dataa saatavilla tai taulukko tyhjä.")

elif nav == "TOP 3 Valioliiga":
    st.header("🏆 TOP 3 Valioliiga")
    df = load_gsheet("TOP 3 Valioliiga")
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        for index, row in df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### #{row.get('Rank', index+1)} {row.get('Ottelu', '')}")
                    st.caption(f"📅 {row.get('Pvm', '')}")
                with col2:
                    st.markdown(f"### 🎯 {row.get('Kerroin', '')}")
                
                st.info(f"**Kohde:** {row.get('Vihjekohde', '')}")
                st.metric("Odotettu EV %", row.get('EV %', ''))
        
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei dataa saatavilla tai taulukko tyhjä.")

else:
    # Yleinen mobiilioptimoitu käsittely muille laajoille tilastosivuille (esim. pelaajavedot, liigataulukot)
    st.header(f"📊 {nav}")
    df = load_gsheet(nav)
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.info("💡 Vinkki: Voit selata koko taulukkoa alta tai suurentaa sen tarvittaessa koko ruudulle.")
        st.dataframe(df, use_container_width=True, height=550)
    else:
        st.warning(f"Ei dataa saatavilla välilehdelle '{nav}'. ({df})")
