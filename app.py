import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import database as db
import components as comp
import locale

# Intenta configurar locale para formato de moneda (es opcional si falla)
try:
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
except:
    pass

def format_currency(value):
    try:
        return f"${value:,.0f}".replace(',', '.')
    except:
        return f"${value}"

def format_number(value):
    try:
        return f"{value:,.0f}".replace(',', '.')
    except:
        return str(value)

# Initialize the Dash app with a light premium theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server  # Needed for gunicorn deployment

# Load filter options
grupos, regionales, años, meses = db.get_filter_options()

# Define the Layout
app.layout = dbc.Container([
    dbc.Row([
        # Sidebar for Filters (Col 3)
        dbc.Col([
            html.Div([
                html.H4("Dashboard User", className="mb-4"),
                html.Hr(style={"borderColor": "#3A4B64"}),
                
                html.Label("Grupo Farmacológico"),
                dcc.Dropdown(
                    id='filter-grupo',
                    options=[{'label': g, 'value': g} for g in grupos],
                    placeholder="Todos",
                    className="mb-3"
                ),
                
                html.Label("Año"),
                dcc.Dropdown(
                    id='filter-año',
                    options=[{'label': a, 'value': a} for a in años],
                    placeholder="Todos",
                    className="mb-3"
                ),
                
                html.Label("Mes"),
                dcc.Dropdown(
                    id='filter-mes',
                    options=[{'label': m, 'value': m} for m in meses],
                    placeholder="Todos",
                    className="mb-3"
                ),
                
                html.Label("Regional CAF"),
                dcc.Dropdown(
                    id='filter-regional',
                    options=[{'label': r, 'value': r} for r in regionales],
                    placeholder="Todas",
                    className="mb-4"
                ),
            ], className="sidebar p-4 h-100 shadow-lg")
        ], width=3, className="p-0"),
        
        # Main Content Area
        dbc.Col([
            # KPIs Row
            dbc.Row([
                dbc.Col(comp.create_kpi_card("Personas Atendidas", "0", "kpi-personas", "fas fa-users"), width=4),
                dbc.Col(comp.create_kpi_card("Fórmulas Dispens.", "0", "kpi-formulas", "fas fa-file-prescription"), width=4),
                dbc.Col(comp.create_kpi_card("Costo Prom. Fórm.", "$0", "kpi-costo-prom", "fas fa-dollar-sign"), width=4),
            ], className="mb-4 mt-4 ps-4 pe-4"),
            
            # Charts Row 1
            dbc.Row([
                dbc.Col(html.Div([
                    html.H5("Dispensación en el Tiempo", className="chart-header"),
                    dcc.Graph(id='chart-tiempo', config={'displayModeBar': False}, style={"height": "250px"})
                ], className="chart-card"), width=12)
            ], className="ps-4 pe-4"),
            
            # Charts Row 2
            dbc.Row([
                dbc.Col(html.Div([
                    html.H5("Top 10 Medicamentos por Costo", className="chart-header"),
                    dcc.Graph(id='chart-top-meds', config={'displayModeBar': False}, style={"height": "320px"})
                ], className="chart-card"), width=8),
                dbc.Col(html.Div([
                    html.H5("Costo por PBS", className="chart-header"),
                    dcc.Graph(id='chart-pbs', config={'displayModeBar': False}, style={"height": "320px"})
                ], className="chart-card"), width=4),
            ], className="ps-4 pe-4"),
            
            # Charts Row 3
            dbc.Row([
                dbc.Col(html.Div([
                    html.H5("Costo por Municipio (Top 10)", className="chart-header"),
                    dcc.Graph(id='chart-municipio', config={'displayModeBar': False}, style={"height": "320px"})
                ], className="chart-card"), width=6),
                dbc.Col(html.Div([
                    html.H5("Costo por Tipo Entrega", className="chart-header"),
                    dcc.Graph(id='chart-tipo-entrega', config={'displayModeBar': False}, style={"height": "320px"})
                ], className="chart-card"), width=6),
            ], className="ps-4 pe-4")
            
        ], width=9, className="p-0")
    ], className="g-0")
], fluid=True, className="p-0")

# Callbacks
@app.callback(
    [Output('kpi-personas', 'children'),
     Output('kpi-formulas', 'children'),
     Output('kpi-costo-prom', 'children'),
     Output('chart-tiempo', 'figure'),
     Output('chart-top-meds', 'figure'),
     Output('chart-pbs', 'figure'),
     Output('chart-municipio', 'figure'),
     Output('chart-tipo-entrega', 'figure')],
    [Input('filter-grupo', 'value'),
     Input('filter-año', 'value'),
     Input('filter-mes', 'value'),
     Input('filter-regional', 'value')]
)
def update_dashboard(grupo, año, mes, regional):
    # Get KPIs
    df_kpi = db.get_kpis(grupo, año, mes, regional)
    personas = format_number(df_kpi['total_personas'].iloc[0])
    formulas = format_number(df_kpi['total_formulas'].iloc[0])
    costo_prom = format_currency(df_kpi['costo_promedio'].iloc[0])
    
    # Get Data for Charts
    df_tiempo = db.get_dispensacion_tiempo(grupo, año, mes, regional)
    fig_tiempo = comp.render_line_chart(df_tiempo, 'mes_año', 'dispensaciones')
    
    df_top = db.get_top_medicamentos_costo(grupo, año, mes, regional, limit=10)
    fig_top = comp.render_bar_chart(df_top, 'descripcion', 'costo_total', orientation='h')
    
    df_pbs = db.get_costo_pbs(grupo, año, mes, regional)
    fig_pbs = comp.render_pie_chart(df_pbs, 'pbs', 'costo_total')
    
    df_municipio = db.get_costo_municipio(grupo, año, mes, regional).head(10) # Top 10 municipios
    fig_municipio = comp.render_bar_chart(df_municipio, 'municipio_caf', 'costo_total', orientation='h')
    
    df_tipo = db.get_costo_tipo_entrega(grupo, año, mes, regional)
    fig_tipo = comp.render_pie_chart(df_tipo, 'tipo_entrega', 'costo_total')
    
    return personas, formulas, costo_prom, fig_tiempo, fig_top, fig_pbs, fig_municipio, fig_tipo

if __name__ == '__main__':
    app.run(debug=True, port=8050)
