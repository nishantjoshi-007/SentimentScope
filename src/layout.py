from dash import html, dcc

def create_layout(min_sentiment_score, max_sentiment_score, min_subjectivity_score, max_subjectivity_score, all_months):
    return html.Div(children=[
        html.H1('Twitter Data Dashboard', style={'textAlign': 'center'}),

        # Month Selection Dropdown
        html.Div(children=[
            html.Label('Filter by Month:', style={'margin': '10px'}),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': month, 'value': month} for month in all_months],
                value='All',  # Default value set to 'All'
                placeholder="Select a Month",
                multi=False,  # Keep single selection
                style={'width': '50%', 'margin': 'auto'}
            )
        ], style={'textAlign': 'center', 'padding': '20px'}),

        # Sentiment Score Range Slider
        html.Div(children=[
            html.Label('Select Sentiment Score Range:', style={'margin': '10px'}),
            dcc.RangeSlider(
                id='sentiment-slider',
                min=min_sentiment_score,
                max=max_sentiment_score,
                value=[min_sentiment_score, max_sentiment_score],
                marks={i: str(i) for i in range(int(min_sentiment_score), int(max_sentiment_score)+1)},
                step=0.1  # Adjust step as needed
            )
        ], style={'width': '80%', 'margin': 'auto', 'padding': '20px'}),

        # Subjectivity Score Range Slider
        html.Div(children=[
            html.Label('Select Subjectivity Score Range:', style={'margin': '10px'}),
            dcc.RangeSlider(
                id='subjectivity-slider',
                min=min_subjectivity_score,
                max=max_subjectivity_score,
                value=[min_subjectivity_score, max_subjectivity_score],
                marks={i: f'{i*0.1:.1f}' for i in range(int(min_subjectivity_score*10), int(max_subjectivity_score*10)+1)},
                step=0.1  # Adjust step as needed
            )
        ], style={'width': '80%', 'margin': 'auto', 'padding': '20px'}),

        # Scatter Plot Graph
        dcc.Graph(
            id='scatter-plot',
            config={
                'scrollZoom': True,  # Enables scroll zooming
                'modeBarButtonsToAdd': [
                    'drawline',
                    'drawopenpath',
                    'drawclosedpath',
                    'drawcircle',
                    'drawrect',
                    'eraseshape',
                    'zoomIn2d',
                    'zoomOut2d',
                    'autoScale2d',
                    'resetScale2d',
                    'hoverClosestCartesian',
                    'hoverCompareCartesian',
                    'toggleSpikelines',
                ],
                'displaylogo': False,  # Hides the Plotly logo
            },
            style={'height': '60vh', 'width': '80%', 'margin': 'auto'}
        ),

        html.H3('Raw Tweets', style={'textAlign': 'center'}),
        html.Div(id='selected-data', style={'margin': '20px', 'padding': '20px', 'border': '1px solid #ddd'})
    ])