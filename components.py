import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go

# Color settings based on reference image
COLORS = {
    'primary': '#11223A',
    'secondary': '#F39C12',
    'chart_bars': '#E29731', # Or '#11223A' and '#F39C12'
    'bg_card': '#FFFFFF',
    'text': '#3A4B64'
}

def create_kpi_card(title, value, id, icon_class="fas fa-chart-line"):
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6(title, className="kpi-title text-uppercase mb-2"),
                    html.H2(id=id, children=value, className="kpi-value mb-0"),
                ], width=8),
                dbc.Col([
                    html.I(className=f"{icon_class} kpi-icon")
                ], width=4, className="text-end d-flex align-items-center justify-content-end")
            ])
        ]),
        className="kpi-card h-100"
    )

def render_empty_figure(text="Buscando datos..."):
    fig = go.Figure()
    fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{"text": text, "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 20}}],
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def render_line_chart(df, x_col, y_col):
    if df.empty: return render_empty_figure()
    fig = px.area(df, x=x_col, y=y_col, template="plotly_white", markers=True)
    fig.update_traces(line_color=COLORS['secondary'], fillcolor='rgba(243, 156, 18, 0.2)')
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        xaxis_title=None, yaxis_title=None
    )
    return fig

def render_bar_chart(df, x_col, y_col, orientation='v'):
    if df.empty: return render_empty_figure()
    
    color_discrete_sequence=[COLORS['primary'], COLORS['secondary']]
    
    if orientation == 'h':
        fig = px.bar(df, x=y_col, y=x_col, orientation='h', template="plotly_white", 
                     color_discrete_sequence=[COLORS['primary']], text_auto='.2s')
        fig.update_layout(yaxis={'categoryorder':'total ascending', 'automargin': True})
        fig.update_traces(textposition='outside', textfont_size=12, cliponaxis=False)
        labels = df[x_col].astype(str).apply(lambda x: x[:30] + '...' if len(x) > 30 else x).tolist()
        fig.update_yaxes(ticktext=labels, tickvals=df[x_col].tolist())
    else:
        fig = px.bar(df, x=x_col, y=y_col, template="plotly_white", 
                     color_discrete_sequence=[COLORS['secondary']], text_auto='.2s')
        fig.update_traces(textposition='outside', textfont_size=12, cliponaxis=False)
        
    fig.update_layout(
        margin=dict(l=20, r=40, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']), coloraxis_showscale=False,
        xaxis_title=None, yaxis_title=None
    )
    return fig

def render_pie_chart(df, names_col, values_col):
    if df.empty: return render_empty_figure()
    fig = px.pie(df, names=names_col, values=values_col, template="plotly_white", hole=0.5, 
                 color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], '#A0B2C6', '#3A4B64'])
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig
