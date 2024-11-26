import numpy as np
import math  # Für mathematische Funktionen wie Fakultät
import plotly.graph_objects as go
from scipy.stats import binom


# Funktionen zur Berechnung der Verteilungen

#Normalverteilung
def normal_distribution(mu, sigma):
    x = np.linspace(-10, 10, 500)
    y = (1 / (np.sqrt(2 * np.pi * sigma**2))) * np.exp(-((x - mu)**2) / (2 * sigma**2))
    return x, y

#Exponentialverteilung
def exponential_distribution(lmbda):
    x = np.linspace(0, 10, 500)
    y = lmbda * np.exp(-lmbda * x)
    return x, y

#Poissonverteilung
def poisson_distribution(lmbda, size=20):
    x = np.arange(0, size)
    y = (np.exp(-lmbda) * lmbda**x) / np.array([math.factorial(i) for i in x])
    
    x_lines = []
    y_lines = []
    
    for xi, yi in zip(x, y):
        # Zwei Punkte für jede vertikale Linie
        x_lines.extend([xi, xi, None])  # x-Werte, getrennt durch None für Plotly
        y_lines.extend([0, yi, None])  # y-Werte: Von 0 bis yi
    
    return x_lines, y_lines

#Binomialverteilung
def binomial_distribution(n, p):
    x = np.arange(0, n + 1)
    y = binom.pmf(x, n, p)
    return x, y

def uniform_distribution(a, b):
    x = np.linspace(-10, 10, 500)
    epsilon = 1e-10  # Sehr kleiner Wert
    y = np.where((x >= a) & (x <= b) & (b - a > epsilon), 1 / (b - a + epsilon), 0)
    return x, y

# Student-t-Verteilung
def student_t_distribution(df):
    from scipy.stats import t
    x = np.linspace(-10, 10, 500)
    y = t.pdf(x, df)
    return x, y

#gibt die Spur zurück
def visible_trace(index, total=6):
    return [i == index for i in range(total)]



# Initiale Werte/Default Werte
mu_initial, sigma_initial = 0, 1
lambda_initial = 1
n_initial, p_initial = 10, 0.5
a_default, b_default = -2, 2
df_default = 5


# Normalverteilung: Initiale Daten
x_norm, y_norm = normal_distribution(mu_initial, sigma_initial)

# Exponentialverteilung: Initiale Daten
x_exp, y_exp = exponential_distribution(lambda_initial)

# Poissonverteilung: Initiale Daten
x_pois_lines, y_pois_lines = poisson_distribution(lambda_initial)

# Binomialverteilung: Initiale Daten
x_binom, y_binom = binomial_distribution(n_initial, p_initial)

# Uniformverteilung: Initiale Daten
x_uniform, y_uniform = uniform_distribution(a_default, b_default)

# Student-t-Verteilung: Initiale Daten
x_student, y_student = student_t_distribution(df_default)


# Erstellung der Figur
fig = go.Figure()


# Verteilungen/Spuren hinzufügen
fig.add_trace(go.Scatter(x=x_norm, y=y_norm, mode="lines", name="Normalverteilung", visible=True))
fig.add_trace(go.Scatter(x=x_exp, y=y_exp, mode="lines", name="Exponentialverteilung", visible=False))
#fig.add_trace(go.Bar(x=x_pois, y=y_pois, name="Poissonverteilung", visible=False))
fig.add_trace(go.Scatter(
    x=x_pois_lines, 
    y=y_pois_lines, 
    mode="lines", 
    name="Poissonverteilung (Linien)", 
    visible=False
))

fig.add_trace(go.Scatter(x=x_binom, y=y_binom, mode="markers", name="Binomialverteilung", visible=False))
fig.add_trace(go.Scatter(x=x_uniform, y=y_uniform, mode="lines", name="Uniformverteilung", visible=False))
fig.add_trace(go.Scatter(x=x_student, y=y_student, mode="lines", name="Student-t-Verteilung", visible=False))


# Slider-Konfigurationen
sliders_normal = [
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [normal_distribution(mu, sigma_initial)[1], None, None]},
                    {"title": f"Normalverteilung mit μ={mu} und σ={sigma_initial}"}
                ],
                "label": f"{mu}"
            } for mu in np.arange(-5, 6.1, 0.5)
        ],
        "currentvalue": {"prefix": "Mittelwert μ: "},
        "x": -0.1,
        "y": -0.35  # Slider unterhalb der Grafik
    },
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [normal_distribution(mu_initial, sigma)[1], None, None]},
                    {"title": f"Normalverteilung mit μ={mu_initial} und σ={sigma}"}
                ],
                "label": f"{sigma:.1f}"
            } for sigma in np.arange(0.1, 5.1, 0.5)
        ],
        "currentvalue": {"prefix": "Standardabweichung σ: "},
        "x": -0.1,
        "y": -0.7  # Weiter nach unten verschoben
    }
]

sliders_exp = [
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [None, exponential_distribution(lmbda)[1], None]},
                    {"title": f"Exponentialverteilung mit λ={lmbda:.1f}"}
                ],
                "label": f"{lmbda:.1f}"
            } for lmbda in np.arange(0.0, 5.1, 0.5)
        ],
        "currentvalue": {"prefix": "Rate λ: "},
        "x": -0.1,
        "y": -0.35
    }
]

sliders_pois = [
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [None, None, poisson_distribution(lmbda)[1]]},
                    {"title": f"Poissonverteilung mit λ={lmbda:.1f}"}
                ],
                "label": f"{lmbda:.1f}"
            } for lmbda in np.arange(0.0, 6.1, 0.5)
        ],
        "currentvalue": {"prefix": "λ: "},
        "x": -0.1,
        "y": -0.35
    }
]

sliders_binom = [
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [None, None, None, binomial_distribution(n, p_initial)[1]]},
                    {"title": f"Binomialverteilung mit n={n} und p={p_initial:.2f}"}
                ],
                "label": f"{n}"
            } for n in range(0, 21, 1)
        ],
        "currentvalue": {"prefix": "Anzahl n: "},
        "x": -0.1,
        "y": -0.35
    },
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [None, None, None, binomial_distribution(n_initial, p)[1]]},
                    {"title": f"Binomialverteilung mit n={n_initial} und p={p:.2f}"}
                ],
                "label": f"{p:.2f}"
            } for p in np.arange(0.1, 1.1, 0.1)
        ],
        "currentvalue": {"prefix": "Wahrscheinlichkeit p: "},
        "x": -0.1,
        "y": -0.7
    }
]

sliders_uniform = [
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [None, None, None, None, uniform_distribution(a, b_default)[1], None]},
                    {"title": f"Uniformverteilung mit a={a} und b={b_default}"}
                ],
                "label": f"{a}"
            } for a in np.arange(-5, 5, 0.5)
        ],
        "currentvalue": {"prefix": "a: ", "value": a_default},
        "x": -0.1,
        "y": -0.35
    },
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [None, None, None, None, uniform_distribution(a_default, b)[1], None]},
                    {"title": f"Uniformverteilung mit a={a_default} und b={b}"}
                ],
                "label": f"{b}"
            } for b in np.arange(-4, 6, 0.5)
        ],
        "currentvalue": {"prefix": "b: ", "value": b_default},
        "x": -0.1,
        "y": -0.7
    }
]

sliders_student = [
    {
        "steps": [
            {
                "method": "update",
                "args": [
                    {"y": [None, None, None, None, None, student_t_distribution(df)[1]]},
                    {"title": f"Student-t-Verteilung mit ν={df}"}
                ],
                "label": f"{df}"
            } for df in range(1, 21)
        ],
        "currentvalue": {"prefix": "ν: ", "value": df_default},
        "x": -0.1,
        "y": -0.35
    }
]


# Dropdown-Menü zur Auswahl der Verteilung
fig.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "label": "Normalverteilung",
                    "method": "update",
                    "args": [
                        {"visible": [True, False, False, False, False, False]},
                        {"sliders": sliders_normal}  # Zeigt die Slider der Normalverteilung
                    ],
                },
                {
                    "label": "Exponentialverteilung",
                    "method": "update",
                    "args": [
                        {"visible": [False, True, False, False, False, False]},
                        {"sliders": sliders_exp}  # Zeigt die Slider der Exponentialverteilung
                    ],
                },
                {
                    "label": "Poissonverteilung",
                    "method": "update",
                    "args": [
                        {"visible": [False, False, True, False, False, False]},
                        {"sliders": sliders_pois}  # Zeigt die Slider der Poissonverteilung
                    ],
                },
                {
                    "label": "Binomialverteilung",
                    "method": "update",
                    "args": [
                        {"visible": [False, False, False, True, False, False]},
                        {"sliders": sliders_binom}
                    ],
                },
                {
                    "label": "Uniformverteilung",
                    "method": "update",
                    "args": [
                        {"visible": [False, False, False, False, True, False]},
                        {"sliders": sliders_uniform}
                    ],
                },
                {
                    "label": "Student-t-Verteilung",
                    "method": "update",
                    "args": [
                        {"visible": [False, False, False, False, False, True]},
                        {"sliders": sliders_student}
                    ],
                },
            ],
            "direction": "down",
            "showactive": True,
        }
    ],
    sliders=sliders_normal,  # Initial wird die Normalverteilung mit ihren Slidern angezeigt
    title="Interaktive Wahrscheinlichkeitsverteilungen",
    xaxis_title="x",
    yaxis_title="Dichte",
    margin={"l": 40, "r": 40, "t": 50, "b": 200},  # Platz für Slider unterhalb der Grafik
)


# Ausgabe in eine HTML-Datei
fig.write_html("interactive_distributions.html")
print("Interaktive Datei 'interactive_distributions_updated.html' erstellt.")
