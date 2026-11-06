import streamlit as st
import pandas as pd
from urllib.parse import quote

# Sivuston perusasetukset
st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

# Vahvistettu CSS: Tiukemmat fonttikoot ja täydellinen rivitys korteille
st.markdown("""
<style>
    .mobile-card-title {
        font-size: 0.9rem !important;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 0.2rem;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    .mobile-card-sub {
        font-size: 0.75rem !important;
        color: #6c757d;
        margin-bottom: 0.4rem;
        word-break: break-word !important;
    }
    .mobile-card-info {
        font-size: 0.8rem !important;
        line-height: 1.35;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 6px;
        border-left: 3px solid #1f77b4;
        margin-top: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .mobile-badge {
        display: inline-block;
        background-color: #e8f4f8;
        color: #1f77b4;
        font-weight: bold;
        font-size: 0.8rem;
        padding: 2px 6px;
        border-radius: 4px;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

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
            # Haetaan otsikko turvallisesti oikeasta sarakkeesta (tuplauksessa "Tuplauksen Ottelut")
            main_title = str(row.get(title_col, f"Kohde #{index+1}"))
            rank_num = row.get('Rank', index+1)
            
            # Kerroin-badge
            badge_html = ""
            if badge_col and badge_col in row and pd.notna(row[badge_col]):
                badge_html = f"<div class='mobile-badge'>🎯 Yhteiskerroin: {row[badge_col]}</div>"
            
            st.markdown(f"<div class='mobile-card-title'>#{rank_num} {main_title}</div>", unsafe_allow_html=True)
            if badge_html:
                st.markdown(badge_html, unsafe_allow_html=True)
                
            # Päivämäärät ja sarjat
            sub_info = []
            for col in ['Pvm', 'Sarja', 'Joukkue', 'Pelipaikka']:
                if col in row and pd.notna(row[col]) and str(row[col]) != '':
                    sub_info.append(str(row[col]))
            if sub_info:
                st.markdown(f"<div class='mobile-card-sub'>📅 {' | '.join(sub_info)}</div>", unsafe_allow_html=True)
            
            # Valitut kohteet siistissä, pienifonttisessa ja rivittyvässä laatikossa
            if info_col and info_col in row and pd.notna(row[info_col]):
                info_val = str(row[info_col])
                st.markdown(f"<div class='mobile-card-info'><b>{info_col}:</b><br>{info_val}</div>", unsafe_allow_html=True)
            
            # Muut sarakkeet mittareina (esim. Luottamus, Osuma-%)
            exclude_cols = ['Rank', 'Pvm', 'Sarja', 'Joukkue', 'Pelipaikka', title_col, badge_col, info_col]
            other_cols = [c for c in df.columns if c not in exclude_cols]
            if other_cols:
                cols = st.columns(min(len(other_cols), 2))
                for i, col_name in enumerate(other_cols[:4]):
                    val = row[col_name]
                    cols[i % 2].metric(col_name, str(val) if pd.notna(val) else "-")

# ==========================================
# TUPLAUS-NÄKYMÄN KUTSU
# ==========================================
if nav == "Tuplaus":
    st.header("🎯 Päivän Tuplaus (Yhteiskerroin ~2.00)")
    df = load_gsheet("Tuplaus")
    if isinstance(df, pd.DataFrame) and not df.empty:
        # Varmistetaan, että otsikkosarakkeen nimi vastaa tasan Google Sheetsin saraketta ("Tuplauksen Ottelut")
        title_column = "Tuplauksen Ottelut" if "Tuplauksen Ottelut" in df.columns else df.columns[1]
        render_mobile_cards(df, title_col=title_column, badge_col="Yhteiskerroin", info_col="Valitut Kohteet")
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei tuplauskohteita saatavilla tällä hetkellä. Aja Colab-master-skripti päivittääksesi tiedot.")

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
        title_field = "Pelaaja" if "Pelaaja" in df.columns else df.columns[0]
        badge_field = "Kerroin" if "Kerroin" in df.columns else ("Arvioitu Kerroin" if "Arvioitu Kerroin" in df.columns else None)
        info_field = "Suositus Veto" if "Suositus Veto" in df.columns else (df.columns[1] if len(df.columns) > 1 else None)
        
        render_mobile_cards(df, title_col=title_field, badge_col=badge_field, info_col=info_field)
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"Ei dataa saatavilla välilehdelle '{target_sheet}'.")

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
        st.warning(f"Ei dataa saatavilla välilehdelle '{target_sheet}'.")
