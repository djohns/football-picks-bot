import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from model import remove_vig, simple_poisson_model, expected_value
from db import create_tables, save_prediction

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

SPORT = "soccer_epl"  # Puedes cambiar luego

def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    response = requests.get(url, params=params)
    return response.json()

def generate_predictions():
    matches = get_odds()

    for match in matches:

        league = match["sport_title"]
        home_team = match["home_team"]
        away_team = match["away_team"]
        match_date = match["commence_time"]

        bookmakers = match["bookmakers"]
        if not bookmakers:
            continue

        markets = bookmakers[0]["markets"]
        outcomes = markets[0]["outcomes"]

        home_odds = draw_odds = away_odds = None

        for o in outcomes:
            if o["name"] == home_team:
                home_odds = o["price"]
            elif o["name"] == away_team:
                away_odds = o["price"]
            else:
                draw_odds = o["price"]

        if not home_odds or not draw_odds or not away_odds:
            continue

        # Probabilidades mercado sin vig
        market_probs = remove_vig(home_odds, draw_odds, away_odds)

        # Modelo propio
        model_probs = simple_poisson_model()

        markets_names = ["Home", "Draw", "Away"]

        for i in range(3):
            ev = expected_value(model_probs[i], [home_odds, draw_odds, away_odds][i])

            if ev > 0.05:  # Solo guardamos si hay valor real

                save_prediction((
                    league,
                    home_team,
                    away_team,
                    markets_names[i],
                    model_probs[i],
                    [home_odds, draw_odds, away_odds][i],
                    ev,
                    datetime.fromisoformat(match_date.replace("Z","+00:00"))
                ))

def main():
    create_tables()
    generate_predictions()

if __name__ == "__main__":
    main()
