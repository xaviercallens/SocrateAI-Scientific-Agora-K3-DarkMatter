import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import scipy.integrate as integrate

# --- Physics Constants and Data ---
H0_target = 71.92
Omega_m = 0.315
c = 299792.458 # km/s

# Mocking DESI DR1 BAO data points (z, D_M/r_d)
desi_z = np.array([0.3, 0.51, 0.71, 0.93, 1.32, 2.33])
desi_dm_rd = np.array([10.0, 16.5, 21.0, 25.5, 33.0, 39.5])
desi_err = desi_dm_rd * 0.02
rd_approx = 147.0 # Mpc

# Baseline LCDM
def E_lcdm(z):
    return np.sqrt(Omega_m * (1+z)**3 + (1 - Omega_m))

def DM_lcdm(z):
    res, _ = integrate.quad(lambda x: 1.0 / E_lcdm(x), 0, z)
    return (c / H0_target) * res

DM_rd_lcdm = np.array([DM_lcdm(z_val)/rd_approx for z_val in desi_z])
chi2_lcdm = np.sum(((desi_dm_rd - DM_rd_lcdm)/desi_err)**2)
bic_lcdm = 1 * np.log(len(desi_z)) + chi2_lcdm


# Initialize App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.Div([
        html.H1("Interactive Cosmological Fitter", className="app-title"),
        html.P("Real-time optimization of K3 Torus Dark Energy dynamics", style={'color': 'var(--text-muted)'})
    ], className="app-header"),

    dbc.Row([
        # LEFT PANEL - Controls
        dbc.Col([
            html.Div([
                html.H4("Torus Parameters", style={'marginBottom': '20px', 'color': 'var(--accent-neon-blue)'}),
                
                html.Div([
                    html.Label([
                        "Torus Potential Slope (w0)",
                        html.Span(id="w0-val-display", style={'color': 'white'})
                    ], className="control-label"),
                    dcc.Slider(
                        id='w0-slider',
                        min=-1.5, max=-0.5, step=0.01, value=-0.95,
                        tooltip={"placement": "bottom", "always_visible": False},
                        className="custom-slider"
                    )
                ], className="control-group"),

                html.Div([
                    html.Label([
                        "Initial Field Velocity (wa)",
                        html.Span(id="wa-val-display", style={'color': 'white'})
                    ], className="control-label"),
                    dcc.Slider(
                        id='wa-slider',
                        min=-1.0, max=1.0, step=0.01, value=-0.1,
                        tooltip={"placement": "bottom", "always_visible": False},
                        className="custom-slider"
                    )
                ], className="control-group"),

            ], className="glass-panel", style={'height': '100%'}),
        ], md=4),

        # RIGHT PANEL - Graph and Metrics
        dbc.Col([
            html.Div([
                dcc.Graph(id='hubble-graph', config={'displayModeBar': False}, style={'height': '400px'})
            ], className="glass-panel", style={'marginBottom': '20px', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.Div("X² T² Torus", className="metric-title"),
                    html.Div(id="chi2-val", className="metric-value")
                ], className="metric-card"),
                
                html.Div([
                    html.Div("ΔX² (vs ΛCDM)", className="metric-title"),
                    html.Div(id="delta-chi2-val", className="metric-value")
                ], className="metric-card"),

                html.Div([
                    html.Div("ΔBIC", className="metric-title"),
                    html.Div(id="delta-bic-val", className="metric-value")
                ], className="metric-card")
            ], className="metrics-container glass-panel")
        ], md=8)
    ])
], fluid=True, style={'paddingTop': '20px', 'maxWidth': '1400px'})


@app.callback(
    [Output('hubble-graph', 'figure'),
     Output('chi2-val', 'children'),
     Output('delta-chi2-val', 'children'),
     Output('delta-chi2-val', 'className'),
     Output('delta-bic-val', 'children'),
     Output('delta-bic-val', 'className'),
     Output('w0-val-display', 'children'),
     Output('wa-val-display', 'children')],
    [Input('w0-slider', 'value'),
     Input('wa-slider', 'value')]
)
def update_dashboard(w0, wa):
    # Physics Calculation for T2
    def E_T2(z):
        a = 1.0 / (1.0 + z)
        f_z = (1+z)**(3*(1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
        return np.sqrt(Omega_m * (1+z)**3 + (1 - Omega_m) * f_z)

    def DM_T2(z):
        res, _ = integrate.quad(lambda x: 1.0 / E_T2(x), 0, z)
        return (c / H0_target) * res

    # Calculate stats
    try:
        DM_rd_th = np.array([DM_T2(z_val)/rd_approx for z_val in desi_z])
        chi2_T2 = np.sum(((desi_dm_rd - DM_rd_th)/desi_err)**2)
        bic_T2 = 3 * np.log(len(desi_z)) + chi2_T2
        
        delta_chi2 = chi2_T2 - chi2_lcdm
        delta_bic = bic_T2 - bic_lcdm
    except:
        chi2_T2, delta_chi2, delta_bic = 9999, 9999, 9999
        
    # Plotting
    z_grid = np.linspace(0.01, 3, 100)
    
    fig = go.Figure()
    
    # LCDM
    fig.add_trace(go.Scatter(
        x=z_grid, y=[E_lcdm(z) for z in z_grid],
        mode='lines', name='ΛCDM',
        line=dict(color='#00f0ff', width=2, dash='dash')
    ))
    
    # T2 Torus
    fig.add_trace(go.Scatter(
        x=z_grid, y=[E_T2(z) for z in z_grid],
        mode='lines', name='T² Torus',
        line=dict(color='#ff00ea', width=3)
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        title=dict(text="Hubble Expansion Rate E(z)", font=dict(family='Outfit', size=20)),
        xaxis=dict(title="Redshift z", gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title="E(z)", gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Status Colors
    chi2_class = "metric-value val-good" if delta_chi2 <= 0 else "metric-value val-bad"
    bic_class = "metric-value val-good" if delta_bic <= 0 else "metric-value val-bad"

    return (
        fig, 
        f"{chi2_T2:.2f}", 
        f"{delta_chi2:+.2f}", chi2_class,
        f"{delta_bic:+.2f}", bic_class,
        f"{w0:.2f}", f"{wa:.2f}"
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)
