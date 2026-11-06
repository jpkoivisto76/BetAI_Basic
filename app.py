import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

st.title("⚽ BetAI_Basic – Älykäs Vetokeskus")
st.sidebar.header("Navigaatio")

nav = st.sidebar.selectbox("Valitse näkymä", [
    "TOP 3 Valioliiga", 
    "TOP 20 Vihjeet", 
    "TOP 10 Builderit",  # <-- Päivitetty TOP5 -> TOP10
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
])

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

# Näkymien renderöinti
if nav == "TOP 3 Valioliiga":
    st.header("🏆 TOP 3 Valioliiga & Vihjeet")
    df = load_gsheet("TOP 3 Valioliiga")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "TOP 20 Vihjeet":
    st.header("💡 TOP 20 Vihjettä & Arviot")
    df = load_gsheet("TOP 20 vihjettä")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "TOP 10 Builderit":
    st.header("🛠️ TOP 10 Bet Builder -yhdistelmät & Erikoiskohteet")
    df = load_gsheet("TOP 10 Builderit")
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        # Mobiiliystävällinen korttinäkymä puhelimelle ja työpöydälle
        for index, row in df.iterrows():
            with st.container(border=True):
                # Otsikkorivi: Sijoitus, Ottelu ja Kerroin
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### #{row.get('Rank', index+1)} {row.get('Ottelu', 'Ottelu')} ({row.get('Pvm', '')})")
                with col2:
                    st.markdown(f"### 🎯 {row.get('Arvioitu Kerroin', '')}")
                
                # Builder Paketti kokonaan näkyvissä ilman katkeamista
                st.info(f"**Builder Paketti:** \n\n{row.get('Builder Paketti', '')}")
                
                # Alarivi: Builder Score ja komponenttipisteet
                m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
                m_col1.metric("Pisteet", row.get('Builder Score', ''))
                m_col2.metric("Laukaukset", row.get('Laukaukset (35%)', ''))
                m_col3.metric("Kulmat", row.get('Kulmat (25%)', ''))
                m_col4.metric("Kortit", row.get('Kortit (20%)', ''))
                m_col5.metric("Maalit", row.get('Maalit (20%)', ''))
        
        with st.expander("Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True, height=400)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "TOP 20 Valioliiga Laukaukset":
    st.header("🎯 TOP 20 Bet Builder - Laukaukset (Valioliiga)")
    df = load_gsheet("TOP 20 Bet Builder Laukaukset")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "TOP 20 Valioliiga SoT (Maalia kohti)":
    st.header("🎯 TOP 20 Laukaukset maalia kohti - SoT (Valioliiga)")
    df = load_gsheet("TOP 20 SoT Vedot")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "TOP 20 Valioliiga Rikkeet":
    st.header("⚠️ TOP 20 Rikevedot (Valioliiga)")
    df = load_gsheet("TOP 20 Rikevedot")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "Muut liigat: Laukaukset":
    st.header("🎯 Muut liigat: Bet Builder - Laukaukset")
    df = load_gsheet("Muut TOP5 Bet Builder Laukaukset")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "Muut liigat: SoT (Maalia kohti)":
    st.header("🎯 Muut liigat: Laukaukset maalia kohti (SoT)")
    df = load_gsheet("Muut TOP5 SoT Vedot")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "Muut liigat: Rikkeet":
    st.header("⚠️ Muut liigat: Rikevedot")
    df = load_gsheet("Muut TOP5 Rikevedot")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "Tulevat ottelut & Tuomarit":
    st.header("📅 Tulevat ottelut, tuomarit ja odotusarvot")
    df = load_gsheet("Tulevat ottelut")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "Premier League":
    st.header("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League - Joukkuetilastot")
    df = load_gsheet("Premier League")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "Bundesliga":
    st.header("🇩🇪 Bundesliga - Joukkuetilastot")
    df = load_gsheet("Bundesliga")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "La Liga":
    st.header("🇪🇸 La Liga - Joukkuetilastot")
    df = load_gsheet("La Liga")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "Serie A":
    st.header("🇮🇹 Serie A - Joukkuetilastot")
    df = load_gsheet("Serie A")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning(f"Ei dataa saatavilla tai taulukko tyhjä. ({df})")

elif nav == "Seuranta & P&L":
    st.header("📈 Vedonlyönnin Seuranta & P&L")
    df = load_gsheet("Seuranta & P&L")
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.info("Seuranta-taulukko on tällä hetkellä tyhjä Google Sheetsissä.")
