import streamlit as st
import pandas as pd
from urllib.parse import quote

# Sivuston perusasetukset
st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

st.title("⚽ BetAI_Basic – Vetokeskus")

# Valikon 15 näkymää
nav_options = [
    "Tuplaus", 
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
# APUFUNKTIO: Mobiilioptimoitu korttinäkymä
# ==========================================
def render_mobile_cards(df, title_col, badge_col=None, info_col=None):
    for index, row in df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                main_title = str(row.get(title_col, f"Kohde #{index+1}"))
                rank_num = row.get('Rank', index+1)
                st.markdown(f"### #{rank_num} {main_title}")
                
                # Apitiedot otsikon alle (päivämäärä, sarja, joukkue tai pelipaikka)
                sub_info = []
                for col in ['Pvm', 'Sarja', 'Joukkue', 'Pelipaikka']:
                    if col in row and pd.notna(row[col]) and str(row[col]) != '':
                        sub_info.append(str(row[col]))
                if sub_info:
                    st.caption(f"📅 {' | '.join(sub_info)}")
            
            # Oikea yläkulma (esim. Yhteiskerroin, Kerroin tai osuma-%)
            with col2:
                if badge_col and badge_col in row and pd.notna(row[badge_col]):
                    st.markdown(f"### 🎯 {row[badge_col]}")
            
            # Keskiosa (esim. Tuplauksen kohteet, Builder paketti tai suositusveto)
            if info_col and info_col in row and pd.notna(row[info_col]):
                st.info(f"**{info_col}:** \n\n{row[info_col]}")
            
            # Muut sarakkeet mittareina tai tekstinä alarivissä
            exclude_cols = ['Rank', 'Pvm', 'Sarja', 'Joukkue', 'Pelipaikka', title_col, badge_col, info_col]
            other_cols = [c for c in df.columns if c not in exclude_cols]
            if other_cols:
                cols = st.columns(min(len(other_cols), 4))
                for i, col_name in enumerate(other_cols[:4]):
                    val = row[col_name]
                    cols[i].metric(col_name, str(val) if pd.notna(val) else "-")

# ==========================================
# NÄKYMIEN RENDERÖINTI
# ==========================================

# 1. TUPLAUS-NÄKYMÄ (Kortit + perinteinen taulukko laajennuksessa)
if nav == "Tuplaus":
    st.header("🎯 Päivän Tuplaus (Yhteiskerroin ~2.00)")
    df = load_gsheet("Tuplaus")
    if isinstance(df, pd.DataFrame) and not df.empty:
        render_mobile_cards(df, title_col="Tuplauksen Ottelut", badge_col="Yhteiskerroin", info_col="Valitut Kohteet")
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei tuplauskohteita saatavilla tällä hetkellä. Aja Colab-master-skripti päivittääksesi tiedot.")

# 2. VETOVIHJEET JA BUILDERIT (Mobiilikortit)
elif nav == "TOP 10 Builderit":
    st.header("🛠️ TOP 10 Bet Builder -yhdistelmät")
    df = load_gsheet("TOP 10 Builderit")
    if isinstance(df, pd.DataFrame) and not df.empty:
        render_mobile_cards(df, title_col="Ottelu", badge_col="Arvioitu Kerroin", info_col="Builder Paketti")
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei dataa saatavilla.")

elif nav == "TOP 20 vihjettä":
    st.header("💡 TOP 20 Vihjettä & Arviot")
    df = load_gsheet("TOP 20 vihjettä")
    if isinstance(df, pd.DataFrame) and not df.empty:
        render_mobile_cards(df, title_col="Ottelu", badge_col="Kerroin", info_col="Veto")
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei dataa saatavilla.")

elif nav == "TOP 3 Valioliiga":
    st.header("🏆 TOP 3 Valioliiga")
    df = load_gsheet("TOP 3 Valioliiga")
    if isinstance(df, pd.DataFrame) and not df.empty:
        render_mobile_cards(df, title_col="Ottelu", badge_col="Kerroin", info_col="Vihjekohde")
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei dataa saatavilla.")

# 3. LAUKAUKSET, SOT JA RIKKEET (Mobiilikortit älykkäällä tunnistuksella)
elif nav in ["TOP 20 Valioliiga Laukaukset", "TOP 20 Valioliiga SoT (Maalia kohti)", "TOP 20 Valioliiga Rikkeet", 
             "Muut liigat: Laukaukset", "Muut liigat: SoT (Maalia kohti)", "Muut liigat: Rikkeet"]:
    
    sheet_name_map = {
        "TOP 20 Valioliiga Laukaukset": "TOP 20 Bet Builder Laukaukset",
        "TOP 20 Valioliiga SoT (Maalia kohti)": "TOP 20 SoT Vedot",
        "TOP 20 Valioliiga Rikkeet": "TOP 20 Rikevedot",
        "Muut liigat: Laukaukset": "Muut TOP5 Bet Builder Laukaukset",
        "Muut liigat: SoT (Maalia kohti)": "Muut TOP5 SoT Vedot",
        "Muut liigat: Rikkeet": "Muut TOP5 Rikevedot"
    }
    target_sheet = sheet_name_map.get(nav, nav)
    st.header(f"📊 {nav}")
    df = load_gsheet(target_sheet)
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        # Tunnistetaan sarakkeet automaattisesti pelaajapohjaisille vedoille
        title_field = "Pelaaja" if "Pelaaja" in df.columns else df.columns[0]
        badge_field = "Kerroin" if "Kerroin" in df.columns else ("Arvioitu Kerroin" if "Arvioitu Kerroin" in df.columns else None)
        info_field = "Suositus Veto" if "Suositus Veto" in df.columns else (df.columns[1] if len(df.columns) > 1 else None)
        
        render_mobile_cards(df, title_col=title_field, badge_col=badge_field, info_col=info_field)
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"Ei dataa saatavilla välilehdelle '{target_sheet}'.")

# 4. SARJATAULUKOT JA TULEVAT OTTELUT (Perinteinen laaja taulukko)
else:
    sheet_name_map = {
        "Tulevat ottelut & Tuomarit": "Tulevat ottelut",
        "Seuranta & P&L": "Seuranta & P&L",
        "Premier League": "Premier League",
        "Bundesliga": "Bundesliga",
        "La Liga": "La Liga",
        "Serie A": "Serie A"
    }
    
    target_sheet = sheet_name_map.get(nav, nav)
    st.header(f"📊 {nav}")
    df = load_gsheet(target_sheet)
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(df, use_container_width=True, height=580)
    else:
        st.warning(feyn := f"Ei dataa saatavilla välilehdelle '{target_sheet}'.")
