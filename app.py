import streamlit as st
import pandas as pd
from urllib.parse import quote

# Sivuston perusasetukset
st.set_page_config(page_title="BetAI_Basic", page_icon="⚽", layout="wide")

# Mukautetut CSS-tyylit korteille ja mobiilioptimoinnille
st.markdown("""
<style>
    .bet-card {
        background-color: var(--secondary-background-color) !important;
    }
    .card-title {
        color: var(--text-color) !important;
        font-weight: bold;
    }
    .card-badge {
        display: inline-block;
        background-color: #e8f4f8;
        color: #1f77b4;
        font-weight: bold;
        font-size: 0.75rem;
        padding: 2px 6px;
        border-radius: 4px;
        margin-bottom: 6px;
    }
    .card-sub {
        font-size: 0.75rem !important;
        color: #6c757d !important;
        margin-bottom: 6px !important;
    }
    .card-info {
        color: var(--text-color) !important;
    }
    
    /* Mobiiliruuduille vielä tarkemmat säädöt */
    @media (max-width: 768px) {
        .card-title { font-size: 0.78rem !important; }
        .card-info { font-size: 0.73rem !important; }
        .card-sub { font-size: 0.68rem !important; }
    }
</style>
""", unsafe_allow_html=True)

st.title("⚽ BetAI_Basic – Vetokeskus")

# Valikon 15 näkymää – "Seuranta & P&L" nostettu ensimmäiseksi
nav_options = [
    "Seuranta & P&L",
    "Tuplaus", 
    "TOP 10 Builderit", 
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
    "Serie A"
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
# APUFUNKTIO: Puhdas, responsiivinen korttinäkymä
# ==========================================
def render_clean_mobile_cards(df, title_col, badge_col=None, info_col=None):
    for index, row in df.iterrows():
        with st.container(border=True):
            raw_title = str(row.get(title_col, f"Kohde #{index+1}"))
            main_title = raw_title.replace(".", " ")
            rank_num = row.get('Rank', index+1)
            
            badge_text = ""
            if badge_col and badge_col in row and pd.notna(row[badge_col]):
                badge_text = f"<div class='card-badge'>🎯 Yhteiskerroin: {row[badge_col]}</div>"
            
            sub_info = []
            for col in ['Pvm', 'Sarja', 'Joukkue', 'Pelipaikka']:
                if col in row and pd.notna(row[col]) and str(row[col]) != '':
                    sub_info.append(str(row[col]))
            sub_str = f"<div class='card-sub'>📅 {' | '.join(sub_info)}</div>" if sub_info else ""
            
            info_str = ""
            if info_col and info_col in row and pd.notna(row[info_col]):
                info_val = str(row[info_col])
                clean_info_col = info_col.replace(".", " ")
                info_str = f"<div class='card-info'><b>{clean_info_col}:</b><br>{info_val}</div>"

            card_html = f"""
            <div class='bet-card' style='border: none; padding: 0; margin: 0; background: transparent;'>
                <div class='card-title'>#{rank_num} {main_title}</div>
                {badge_text}
                {sub_str}
                {info_str}
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            exclude_cols = ['Rank', 'Pvm', 'Sarja', 'Joukkue', 'Pelipaikka', title_col, badge_col, info_col]
            other_cols = [c for c in df.columns if c not in exclude_cols]
            if other_cols:
                cols = st.columns(min(len(other_cols), 2))
                for i, col_name in enumerate(other_cols[:4]):
                    val = row[col_name]
                    if pd.notna(val):
                        clean_col_name = col_name.replace(".", " ").replace("..", "-%")
                        cols[i % 2].markdown(
                            f"""
                            <div style="background:#f8f9fa; padding:6px 8px; border-radius:6px; margin-bottom:4px; border:1px solid #eee;">
                                <div style="font-size:0.68rem; color:#666; font-weight:500;">{clean_col_name}</div>
                                <div style="font-size:0.82rem; font-weight:700; color:#111;">{val}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

# ==========================================
# NÄKYMIEN RENDERÖINTI
# ==========================================

if nav == "Seuranta & P&L":
    st.header("📈 Vedonlyöntiseuranta & P&L")
    
    df_raw = load_gsheet("Seuranta_Data")
    
    if isinstance(df_raw, pd.DataFrame) and not df_raw.empty:
        # Muutetaan numeeriset sarakkeet turvallisesti luvuiksi (tuetaan myös pilkkua desimaalina)
        tuotto_series = pd.to_numeric(df_raw["Tuotto"].astype(str).str.replace(",", "."), errors="coerce").fillna(0)
        panos_series = pd.to_numeric(df_raw["Panos"].astype(str).str.replace(",", "."), errors="coerce").fillna(0)
        
        status_str = df_raw["Status"].astype(str)
        osuma_mask = status_str.str.contains("Osuma", case=False, na=False)
        huti_mask = status_str.str.contains("Huti", case=False, na=False)
        ratkenneet_mask = osuma_mask | huti_mask
        
        tot_v = len(df_raw)
        tot_o = int(osuma_mask.sum())
        tot_h = int(huti_mask.sum())
        tot_avoin = tot_v - (tot_o + tot_h)
        
        # Lasketaan panokset ja tuotto ratkenneista vedoista (jotta avoimet vedot eivät vääristä ROI:ta)
        ratkenneet_panos = round(panos_series[ratkenneet_mask].sum(), 2) if ratkenneet_mask.any() else round(panos_series.sum(), 2)
        tot_panos = round(panos_series.sum(), 2)
        tot_tuotto = round(tuotto_series.sum(), 2)
        
        roi = round((tot_tuotto / max(0.01, ratkenneet_panos)) * 100, 1) if ratkenneet_panos > 0 else 0.0
        win_rate = round((tot_o / max(1, tot_o + tot_h)) * 100, 1)
        
        # Keskikertoimet (jos Kerroin-sarake löytyy)
        kerroin_col = next((c for c in df_raw.columns if "kerroin" in c.lower()), None)
        if kerroin_col:
            kerroin_series = pd.to_numeric(df_raw[kerroin_col].astype(str).str.replace(",", "."), errors="coerce")
            avg_odds_all = round(kerroin_series.mean(), 2) if kerroin_series.notna().any() else 0.0
            avg_odds_won = round(kerroin_series[osuma_mask].mean(), 2) if (osuma_mask.any() and kerroin_series[osuma_mask].notna().any()) else 0.0
        else:
            avg_odds_all = 0.0
            avg_odds_won = 0.0

        # Kumulatiivinen kassakehitys ja Max Drawdown
        cum_profit = tuotto_series.cumsum()
        running_max = cum_profit.cummax()
        drawdown = cum_profit - running_max
        max_dd = round(drawdown.min(), 2) if not drawdown.empty else 0.0
        
        # Rivi 1: Päätunnusluvut
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Kokonaisuotto", f"{tot_tuotto:+.2f} u", f"ROI: {roi:+.1f}%")
        with col2:
            st.metric("Osumatarkkuus", f"{win_rate}%", f"{tot_o} osumaa / {tot_h} hutia")
        with col3:
            st.metric("Vedot yhteensä", f"{tot_v} kpl", f"Avoimet: {tot_avoin} kpl")
            
        # Rivi 2: Lisätunnusluvut (kertoimet, panostus, drawdown)
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("Keskikerroin", f"{avg_odds_all:.2f}", f"Osuneet ka: {avg_odds_won:.2f}")
        with col5:
            st.metric("Kokonaispanostus", f"{tot_panos:.1f} u", f"Ratkenneet: {ratkenneet_panos:.1f} u")
        with col6:
            st.metric("Max Drawdown", f"{max_dd:.2f} u", "Suurin kuoppa huipusta", delta_color="off")

        st.divider()

        # Kassakehityksen graafi
        st.subheader("📊 Kumulatiivinen kassakehitys (u)")
        chart_df = pd.DataFrame({
            "Veto #": range(1, len(cum_profit) + 1),
            "Kumulatiivinen tuotto (u)": cum_profit.values
        }).set_index("Veto #")
        st.line_chart(chart_df, use_container_width=True)

        # Kategoriakohtainen erittely (jos taulukossa on kategoria/tyyppi/sarja-sarake)
        cat_col = next((c for c in df_raw.columns if c.lower() in ["kategoria", "tyyppi", "välilehti", "kohdetyyppi", "sarja"]), None)
        if cat_col:
            st.subheader(f"📂 Tulokset sarakkeen '{cat_col}' mukaan")
            df_calc = df_raw.copy()
            df_calc["_Tuotto"] = tuotto_series
            df_calc["_Panos"] = panos_series
            df_calc["_Osuma"] = osuma_mask.astype(int)
            df_calc["_Huti"] = huti_mask.astype(int)
            
            cat_summary = df_calc.groupby(cat_col, dropna=False).agg(
                Vedot=("_Tuotto", "count"),
                Osumat=("_Osuma", "sum"),
                Hudit=("_Huti", "sum"),
                Panokset_u=("_Panos", "sum"),
                Tuotto_u=("_Tuotto", "sum")
            ).reset_index()
            
            cat_summary["Osuma %"] = (cat_summary["Osumat"] / (cat_summary["Osumat"] + cat_summary["Hudit"]).replace(0, 1) * 100).round(1)
            cat_summary["ROI %"] = (cat_summary["Tuotto_u"] / cat_summary["Panokset_u"].replace(0, 1) * 100).round(1)
            cat_summary["Tuotto_u"] = cat_summary["Tuotto_u"].round(2)
            cat_summary["Panokset_u"] = cat_summary["Panokset_u"].round(1)
            
            st.dataframe(cat_summary, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("📋 Kaikki seuratut vedot")
        # Näytetään uusimmat vedot ylimpänä
        st.dataframe(df_raw.iloc[::-1], use_container_width=True, height=500)
        
    else:
        df_pnl = load_gsheet("Seuranta & P&L")
        if isinstance(df_pnl, pd.DataFrame) and not df_pnl.empty:
            st.dataframe(df_pnl, use_container_width=True, height=580)
        else:
            st.warning("Ei seurantadataa saatavilla.")

elif nav == "Tuplaus":
    st.header("🎯 Päivän Tuplaus (Yhteiskerroin ~2.00)")
    df = load_gsheet("Tuplaus")
    if isinstance(df, pd.DataFrame) and not df.empty:
        title_column = "Tuplauksen Ottelut" if "Tuplauksen Ottelut" in df.columns else df.columns[1]
        render_clean_mobile_cards(df, title_col=title_column, badge_col="Yhteiskerroin", info_col="Valitut Kohteet")
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei tuplauskohteita saatavilla tällä hetkellä. Aja Colab-master-skripti päivittääksesi tiedot.")

elif nav == "TOP 10 Builderit":
    st.header("🛠️ TOP 10 Bet Builder -yhdistelmät")
    df = load_gsheet("TOP 10 Builderit")
    if isinstance(df, pd.DataFrame) and not df.empty:
        render_clean_mobile_cards(df, title_col="Ottelu", badge_col="Arvioitu Kerroin", info_col="Builder Paketti")
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Ei dataa saatavilla.")

elif nav == "TOP 20 vihjettä":
    st.header("💡 TOP 20 Vihjettä & Arviot")
    df = load_gsheet("TOP 20 vihjettä")
    if isinstance(df, pd.DataFrame) and not df.empty:
        render_clean_mobile_cards(df, title_col="Ottelu", badge_col="Kerroin", info_col="Veto")
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
        
        render_clean_mobile_cards(df, title_col=title_field, badge_col=badge_field, info_col=info_field)
        with st.expander("📂 Näytä perinteisenä taulukkona"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"Ei dataa saatavilla välilehdelle '{target_sheet}'.")

else:
    sheet_name_map = {
        "Tulevat ottelut & Tuomarit": "Tulevat ottelut",
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
