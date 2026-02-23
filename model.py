import numpy as np

def implied_probability(odds):
    return 1 / odds

def remove_vig(home_odds, draw_odds, away_odds):
    p_home = implied_probability(home_odds)
    p_draw = implied_probability(draw_odds)
    p_away = implied_probability(away_odds)

    total = p_home + p_draw + p_away

    return (
        p_home / total,
        p_draw / total,
        p_away / total
    )

def simple_poisson_model(home_attack=1.5, away_attack=1.2):
    # Modelo base simplificado
    # Puedes mejorar esto después con datos reales históricos
    
    home_prob = 0.45 + (home_attack - away_attack) * 0.05
    draw_prob = 0.25
    away_prob = 1 - home_prob - draw_prob

    return home_prob, draw_prob, away_prob

def expected_value(model_prob, market_odds):
    return (model_prob * market_odds) - 1
