import numpy as np
import plotly.graph_objects as go

# Funktionen zur Berechnung der Verteilungen
def normal_distribution(mu, sigma):
    x = np.linspace(-10, 10, 500)
    y = (1 / (np.sqrt(2 * np.pi * sigma**2))) * np.exp(-((x - mu)**2) / (2 * sigma**2))
    return x, y

def exponential_distribution(lmbda):
    x = np.linspace(0, 10, 500)
    y = lmbda * np.exp(-lmbda * x)
    return x, y

# Initiale Werte
mu_initial, sigma_initial = 0, 1
lambda_initial = 1

# Normalverteilung: Initiale Daten
x_norm, y_norm = normal_distribution(mu_initial, sigma_initial)

# Exponentialverteilung: Initiale Daten
x_exp, y_exp = exponential_distribution(lambda_initial)

# Erstellung der Figur
fig = go.Figure()

# Normalverteilung hinzufügen
fig.add_trace(go.Scatter(x=x_norm, y=y_norm, mode="lines", name="Normalverteilung"))

# Exponentialverteilung hinzufügen
fig.add_trace(go.Scatter(x=x_exp, y=y_exp, mode="lines", name="Exponentialverteilung"))

# Schritte für Slider (Normalverteilung - Mittelwert μ)
steps_mu = []
for mu in np.arange(-5, 6, 1):  # Slider für Mittelwert (μ)
    x, y = normal_distribution(mu, sigma_initial)
    step = {
        "method": "update",
        "args": [{"y": [y, y_exp]}, {"title": f"Normalverteilung mit μ={mu}, σ={sigma_initial}"}],
        "label": f"μ={mu}",
    }
    steps_mu.append(step)

# Schritte für Slider (Normalverteilung - Standardabweichung σ)
steps_sigma = []
for sigma in np.arange(0.5, 3.5, 0.5):  # Slider für Standardabweichung (σ)
    x, y = normal_distribution(mu_initial, sigma)
    step = {
        "method": "update",
        "args": [{"y": [y, y_exp]}, {"title": f"Normalverteilung mit μ={mu_initial}, σ={sigma:.1f}"}],
        "label": f"σ={sigma:.1f}",
    }
    steps_sigma.append(step)

# Schritte für Slider (Exponentialverteilung - Rate λ)
steps_lambda = []
for lmbda in np.arange(0.5, 3.5, 0.5):  # Slider für Rate (λ)
    x, y = exponential_distribution(lmbda)
    step = {
        "method": "update",
        "args": [{"y": [y_norm, y]}, {"title": f"Exponentialverteilung mit λ={lmbda:.1f}"}],
        "label": f"λ={lmbda:.1f}",
    }
    steps_lambda.append(step)

# Slider hinzufügen und vertikal anordnen
fig.update_layout(
    sliders=[
        {
            "active": 5,
            "steps": steps_mu,
            "len": 1.0,
            "y": -0.25,  # Position des ersten Sliders
        },
        {
            "active": 2,
            "steps": steps_sigma,
            "len": 1.0,
            "y": -0.6,  # Position des zweiten Sliders
        },
        {
            "active": 1,
            "steps": steps_lambda,
            "len": 1.0,
            "y": -0.9,  # Position des dritten Sliders
        },
    ],
    title="Interaktive Wahrscheinlichkeitsverteilungen",
    xaxis_title="x",
    yaxis_title="Dichte",
    margin={"l": 40, "r": 40, "t": 50, "b": 150},  # Zusätzlicher Platz für Slider
)

# Ausgabe in eine HTML-Datei
fig.write_html("interactive_distributions.html")
print("Die interaktive Visualisierung wurde als 'interactive_distributions.html' gespeichert.")
