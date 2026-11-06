# -*- coding: utf-8 -*-
# Kaytatata_Master.ipynb

# --- 1. KESKEISET KIRJASTOT JA ASETUKSET ---
library(googlesheets4)
library(dplyr)
library(httr)
library(jsonlite)
library(googledrive)

# Määritetään välimuistikansio, jotta token säilyy Colab-istuntojen välillä
options(gargle_oauth_cache = ".secrets")

# Kirjaudutaan sisään välimuistia käyttäen
gs4_auth(email = TRUE, cache = ".secrets")
drive_auth(email = TRUE, cache = ".secrets")

sheet_id <- "14Og1POtwncAIvcFiFkugUvms1oWu8VP0eOO5PHwB15U"
api_token <- "7949b939cbfb4f8488061f8cbd0c16a8"
openweather_token <- "89adb68065570180e41bbd2f1f8f8556"
options(timeout = 180)

safe_download <- function(url, destfile) {
  tryCatch({
    download.file(url, destfile, mode = "wb", quiet = TRUE)
    TRUE
  }, error = function(e) { FALSE })
}

cat("--- Aloitetaan Master-skriptin suoritus (Täydellinen versio kaikilla 24 välilehdellä) ---\n")

# Siivotaan vanhat turhat välilehdet ja varmistetaan että kaikki 24 vaadittua lehteä löytyy
current_sheets <- sheet_properties(sheet_id)$name

sheets_to_remove <- c("TOP 20 Bet Builderit", "Muut TOP5 Bet Builderit", "TOP5 Builderit")
for (s in sheets_to_remove) {
  if (s %in% current_sheets) {
    tryCatch({ sheet_delete(sheet_id, sheet = s) }, error = function(e) {})
  }
}

required_sheets <- c(
  "Tulevat ottelut",
  "TOP 10 Builderit",
  "TOP 20 vihjettä",
  "TOP 20 Bet Builder Laukaukset",
  "TOP 20 SoT Vedot",
  "TOP 20 Rikevedot",
  "Muut TOP5 Bet Builder Laukaukset",
  "Muut TOP5 SoT Vedot",
  "Muut TOP5 Rikevedot",
  "TOP 3 Valioliiga",
  "Seuranta & P&L",
  "Tuomarit",
  "API-Kertoimet",
  "Premier League",
  "Bundesliga",
  "Serie A",
  "La Liga",
  "Ligue 1",
  "Valioliiga_Pelaajat",
  "Bundesliiga_Pelaajat",
  "LaLiga_Pelaajat",
  "SerieA_Pelaajat",
  "Maalivahdit",
  "Pelaajatilastot"
)

current_sheets_updated <- sheet_properties(sheet_id)$name
for (req in required_sheets) {
  if (!(req %in% current_sheets_updated)) {
    sheet_add(sheet_id, sheet = req)
  }
}

map_team_name <- function(name) {
  name_map <- c(
    "Arsenal FC" = "Arsenal", "Aston Villa FC" = "Aston Villa",
    "AFC Bournemouth" = "Bournemouth", "Brentford FC" = "Brentford",
    "Brighton & Hove Albion FC" = "Brighton", "Chelsea FC" = "Chelsea",
    "Coventry City FC" = "Coventry", "Coventry City" = "Coventry", "Coventry" = "Coventry",
    "Crystal Palace FC" = "Crystal Palace", "Everton FC" = "Everton",
    "Fulham FC" = "Fulham", "Hull City AFC" = "Hull", "Hull City" = "Hull", "Hull" = "Hull",
    "Ipswich Town FC" = "Ipswich", "Ipswich Town" = "Ipswich", "Ipswich" = "Ipswich",
    "Leeds United FC" = "Leeds", "Leeds United" = "Leeds", "Leeds" = "Leeds",
    "Liverpool FC" = "Liverpool", "Manchester City FC" = "Man City",
    "Manchester United FC" = "Man United", "Newcastle United FC" = "Newcastle",
    "Nottingham Forest FC" = "Nott'm Forest", "Sunderland AFC" = "Sunderland",
    "Sunderland" = "Sunderland", "Tottenham Hotspur FC" = "Tottenham",
    "Tottenham Hotspur" = "Tottenham", "Brighton & Hove Albion" = "Brighton",
    "Manchester City" = "Man City", "Manchester United" = "Man United", "Newcastle United FC" = "Newcastle", "Newcastle United" = "Newcastle", "Newcastle Utd" = "Newcastle",
    "Nottingham Forest" = "Nott'm Forest",
    "FC Augsburg" = "Augsburg", "FC Bayern München" = "Bayern Munich",
    "Borussia Dortmund" = "Dortmund", "Eintracht Frankfurt" = "Ein Frankfurt",
    "1. FC Köln" = "FC Koln", "FC Köln" = "FC Koln", "Köln" = "FC Koln",
    "SC Freiburg" = "Freiburg", "Hamburger SV" = "Hamburg",
    "TSG 1899 Hoffenheim" = "Hoffenheim", "Bayer 04 Leverkusen" = "Leverkusen",
    "Borussia Mönchengladbach" = "M'gladbach", "1. FSV Mainz 05" = "Mainz",
    "SC Paderborn 07" = "Paderborn", "RB Leipzig" = "RB Leipzig",
    "FC Schalke 04" = "Schalke 04", "VfB Stuttgart" = "Stuttgart",
    "1. Union Berlin" = "1. Union Berlin", "Union Berlin" = "1. Union Berlin",
    "SV Werder Bremen" = "Werder Bremen", "SV 07 Elversberg" = "Elversberg",
    "FC St. Pauli 1910" = "St. Pauli", "St. Pauli" = "St. Pauli",
    "VfL Bochum 1848" = "Bochum", "Bochum" = "Bochum",
    "1. FC Heidenheim 1846" = "Heidenheim", "Heidenheim" = "Heidenheim",
    "Holstein Kiel" = "Holstein Kiel", "Kiel" = "Holstein Kiel",
    "VfL Wolfsburg" = "Wolfsburg", "Atalanta BC" = "Atalanta",
    "Bologna FC 1909" = "Bologna", "Bologna 1909" = "Bologna",
    "Cagliari Calcio" = "Cagliari", "Como 1907" = "Como", "Como" = "Como",
    "ACF Fiorentina" = "Fiorentina", "FC Internazionale Milano" = "Inter",
    "Juventus FC" = "Juventus", "SS Lazio" = "Lazio",
    "AC Milan" = "Milan", "SSC Napoli" = "Napoli", "AS Roma" = "Roma",
    "Torino FC" = "Torino", "Udinese Calcio" = "Udinese", "US Lecce" = "Lecce",
    "Genoa CFC" = "Genoa", "AC Monza" = "Monza", "Hellas Verona FC" = "Verona",
    "Empoli FC" = "Empoli", "Vene
