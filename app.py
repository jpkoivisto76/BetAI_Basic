import pandas as pd
import plotly.express as px
import streamlit as st

# Sivuston asetukset
st.set_page_config(
    page_title="BetAI Pro – Vedonlyöntikeskus", page_icon="⚽", layout="centered"
)

# Alustetaan virtuaalinen vetokuponki
if "vetokuponki" not in st.session_state:
  st.session_state.vetokuponki = []

st.title("⚽ BetAI Pro – Älykäs Vetokeskus")
st.markdown("Oma mobiilipohjainen vedonlyönti- ja Bet Builder -keskus.")

SHEET_ID = "14Og1POtwncAIvcFiFkugUvms1oWu8VP0eOO5PHwB15U"


@st.cache_data(ttl=300)
def load_data(sheet_name):
  url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
  try:
    return pd.read_csv(url)
  except Exception as e:
    return None


# Sivupalkki (Navigaatio & Vetokuponki)
st.sidebar.header("Navigaatio")
valinta = st.sidebar.selectbox(
    "Valitse näkymä:",
    [
        "TOP 3 Valioliiga",
        "TOP 20 Vihjeet",
        "TOP5 Builderit (Kaikki sarjat)",
        "Pelaajaerikoiset (Laukaukset / SoT)",
        "Seuranta & P&L",
    ],
)

# Vetokuponin hallinta sivupalkissa
st.sidebar.markdown("---")
st.sidebar.subheader(
    f"🎟️ Vetokuponki ({len(st.session_state.vetokuponki)} kohdetta)"
)
if st.session_state.vetokuponki:
  total_odds = 1.0
  for item in st.session_state.vetokuponki:
    total_odds *= item["Kerroin"]
    st.sidebar.text(f"• {item['Ottelu']} ({item['Kohde']}) @ {item['Kerroin']}")

  st.sidebar.info(f"Yhteiskerroin: **{round(total_odds, 2)}**")
  panos = st.sidebar.number_input(
      "Panokset yht (€/u):", min_value=1.0, value=10.0, step=1.0
  )
  st.sidebar.success(
      f"Mahdollinen palautus: **{round(total_odds * panos, 2)} €**"
  )

  if st.sidebar.button("Tyhjennä kuponki"):
    st.session_state.vetokuponki = []
    st.rerun()
else:
  st.sidebar.text("Kuponki on tyhjä. Lisää kohteita korteista!")

# ==========================================
# 1. TOP 3 VALIOLIIGA
# ==========================================
if valinta == "TOP 3 Valioliiga":
  st.subheader("🏴󠁧󠁢󠁥󠁮󠁧󠁿 TOP 3 Valioliiga -päivän kohteet")
  df = load_data("TOP 3 Valioliiga")

  if df is not None and not df.empty:
    haku = st.text_input("🔍 Etsi joukkueella (esim. Arsenal, Chelsea):", "")
    if haku:
      df = df[df["Ottelu"].str.contains(haku, case=False, na=False)]

    for _, row in df.iterrows():
      with st.container():
        st.markdown(
            f"### **#{row.get('Rank', 1)} {row.get('Ottelu', 'Ottelu')}**"
        )
        st.write(f"🎯 **Kohde:** {row.get('Vihjekohde', '-')}")

        col1, col2, col3 = st.columns(3)
        with col1:
          st.metric(label="Kerroin", value=row.get("Kerroin", "-"))
        with col2:
          st.metric(label="EV / Arvo", value=row.get("EV %", "-"))
        with col3:
          if st.button("Lisää kuponkiin 🎟️", key=f"pl_{row.get('Ottelu', '')}"):
            st.session_state.vetokuponki.append({
                "Ottelu": row.get("Ottelu"),
                "Kohde": row.get("Vihjekohde"),
                "Kerroin": float(row.get("Kerroin", 1.0)),
            })
            st.toast("Kohde lisätty vetokuponkiin!", icon="✅")
        st.markdown("---")
  else:
    st.info("Ei dataa saatavilla tai taulukko tyhjä.")

# ==========================================
# 2. TOP 20 VIHJEET
# ==========================================
elif valinta == "TOP 20 Vihjeet":
  st.subheader("🔥 TOP 20 Vihjettä (Kaikki sarjat)")
  df = load_data("TOP 20 vihjettä")

  if df is not None and not df.empty:
    if "Sarja" in df.columns:
      sarja_valinta = st.selectbox(
          "Suodata sarjan mukaan:", ["Kaikki"] + list(df["Sarja"].unique())
      )
      if sarja_valinta != "Kaikki":
        df = df[df["Sarja"] == sarja_valinta]

    st.dataframe(df, use_container_width=True)
  else:
    st.info("Ei vihjeitä ladattavissa.")

# ==========================================
# 3. TOP5 BUILDERIT (KAIKKI SARJAT)
# ==========================================
elif valinta == "TOP5 Builderit (Kaikki sarjat)":
  st.subheader("🎯 Päivän TOP5 Bet Builder -paketit")

  # Valitaan tarkasteltava builder-taulukko
  builder_valinta = st.radio(
      "Valitse osio:",
      ["Valioliiga / Pääkohdat (TOP5 Builderit)", "Muut TOP5 Sarjat (Laukaukset)"],
  )

  sheet_to_load = (
      "TOP5 Builderit"
      if "TOP5 Builderit" in builder_valinta
      else "Muut TOP5 Bet Builder Laukaukset"
  )
  df = load_data(sheet_to_load)

  if df is not None and not df.empty:
    for _, row in df.iterrows():
      with st.container():
        st.markdown(
            f"### **Ottelu / Pelaaja:** {row.get('Ottelu', row.get('Pelaaja', '-'))}"
        )
        paketti_teksti = row.get("Builder Paketti", row.get("Suositus Veto", "-"))
        st.info(f"🧩 **Veto / Paketti:** {paketti_teksti}")

        col1, col2 = st.columns(2)
        with col1:
          st.metric(
              label="Arvioitu Kerroin",
              value=row.get("Arvioitu Kerroin", row.get("Kerroin", "-")),
          )
        with col2:
          st.metric(
              label="Pisteet / Score",
              value=row.get(
                  "Builder Score", row.get("Todennäköisyys", "-")
              ),
          )
        st.markdown("---")
  else:
    st.info("Ei buildereita saatavilla tälle osiolle.")

# ==========================================
# 4. PELAAJAERIKOISET (Laukaukset / SoT / Rikkeet)
# ==========================================
elif valinta == "Pelaajaerikoiset (Laukaukset / SoT)":
  st.subheader("👤 Pelaajakohtaiset erikoisvedot")

  pelaaja_osio = st.selectbox(
      "Valitse pelityyppi:",
      [
          "TOP 20 Bet Builder Laukaukset",
          "TOP 20 SoT Vedot",
          "TOP 20 Rikevedot",
          "Muut TOP5 SoT Vedot",
          "Muut TOP5 Rikevedot",
      ],
  )
  df = load_data(pelaaja_osio)

  if df is not None and not df.empty:
    haku_pelaaja = st.text_input("🔍 Etsi pelaajalla tai joukkueella:", "")
    if haku_pelaaja:
      df = df[
          df["Pelaaja"].str.contains(haku_pelaaja, case=False, na=False)
          | df["Joukkue"].str.contains(haku_pelaaja, case=False, na=False)
      ]

    st.dataframe(df, use_container_width=True)
  else:
    st.info("Ei pelaajadataa saatavilla valitussa kategoriassa.")

# ==========================================
# 5. SEURANTA & P&L
# ==========================================
elif valinta == "Seuranta & P&L":
  st.subheader("📊 Seuranta & P&L / Luottamuspisteiden validointi")
  df = load_data("Seuranta & P&L")

  if df is not None and not df.empty:
    st.dataframe(df, use_container_width=True)

    if "Tuotto" in df.columns:
      st.markdown("### 📈 Tuottohistoria")
      df_chart = df.copy()
      df_chart["Kumulatiivinen Tuotto"] = df_chart["Tuotto"].cumsum()
      fig = px.line(
          df_chart,
          y="Kumulatiivinen Tuotto",
          title="Tuottojen kehitys (Units)",
          markers=True,
      )
      st.plotly_chart(fig, use_container_width=True)
  else:
    st.info("Ei seurantadataa saatavilla.")