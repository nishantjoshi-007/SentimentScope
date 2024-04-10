import dash
from dash import dcc, html, Input, Output, callback, callback_context
import pandas as pd
import plotly.express as px
from src.layout import create_layout

# Load the dataset
df = pd.read_csv('./data/ProcessedTweets.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Extract necessary data for the layout
min_sentiment_score = df['Sentiment'].min()
max_sentiment_score = df['Sentiment'].max()
min_subjectivity_score = df['Subjectivity'].min()  # Corrected from max to min
max_subjectivity_score = df['Subjectivity'].max()
all_months = df['Month'].unique()

# Set the app layout
app.layout = create_layout(min_sentiment_score, max_sentiment_score, min_subjectivity_score, max_subjectivity_score, all_months)

# Callback for updating scatter plot based on selections
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('sentiment-slider', 'value'),
     Input('subjectivity-slider', 'value')]
)
def update_scatter_plot(selected_month, sentiment_range, subjectivity_range):
    # Check if 'All' is selected or no month is selected, and adjust the filter accordingly
    if selected_month == 'All' or selected_month is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[df['Month'] == selected_month]

    # Apply sentiment and subjectivity filters
    filtered_df = filtered_df[
        (filtered_df['Sentiment'] >= sentiment_range[0]) & (filtered_df['Sentiment'] <= sentiment_range[1]) &
        (filtered_df['Subjectivity'] >= subjectivity_range[0]) & (filtered_df['Subjectivity'] <= subjectivity_range[1])
    ]

    # Generate the scatter plot
    fig = px.scatter(
        filtered_df,
        x='Dimension 1',
        y='Dimension 2',
        hover_data=['RawTweet']
    )
    
    fig.update_layout(
        title='',
        xaxis_title='',
        yaxis_title='',
    )
    
    return fig

@app.callback(
    Output('selected-data', 'children'),
    [Input('scatter-plot', 'selectedData')]
)
def display_selected_data(selectedData):
    if selectedData is None or not selectedData['points']:
        return 'Select points using the lasso tool to see the raw tweets.'
    indices = [point['pointIndex'] for point in selectedData['points']]
    selected_tweets = df.iloc[indices]['RawTweet']
    tweets_div = [html.Div(tweet, style={'padding': '5px', 'border-bottom': '1px solid #ddd'}) for tweet in selected_tweets]
    return tweets_div

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)