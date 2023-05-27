import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd

# Sample data for the plots
df=pd.read_csv('submission.csv')

# Sample data for the plots
data = pd.DataFrame({
    'Industry': df['Industry'],
    'Total Deal Amount': df['Total Deal Amount'],
    'Seasons': df['Season Number']
})




# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    style={'border': '1px solid black', 'padding': '10px'},
    children=[
        html.H1('Dashboard', style={'text-align': 'center'}),
        html.Div(
            style={'display': 'flex'},
            children=[
                html.Div(
                    style={'flex': '1'},
                    children=[
                        dcc.Dropdown(
                            id='season-dropdown',
                            options=[{'label': str(season), 'value': season} for season in data['Seasons'].unique()],
                            value=data['Seasons'].unique()[0],
                            clearable=False
                        ),
                        dcc.Graph(
                            id='total-deal-industry-type-plot',
                            style={'height': '400px'}
                        )
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'margin-left': '20px'},
                    children=[
                        dcc.Graph(
                            id='percentage-deal-industry-type-plot',
                            style={'height': '400px'}
                        )
                    ]
                )
            ]
        )
    ]
)

# Callback for the first plot
@app.callback(
    dash.dependencies.Output('total-deal-industry-type-plot', 'figure'),
    [dash.dependencies.Input('season-dropdown', 'value')]
)
def update_total_deal_industry_type_plot(selected_season):
    filtered_data = data[data['Seasons'] == selected_season]
    grouped_data = filtered_data.groupby('Industry')['Total Deal Amount'].sum().reset_index()

    trace = go.Bar(x=grouped_data['Industry'], y=grouped_data['Total Deal Amount'])

    layout = go.Layout(
        title='Sum of Total Deal Amount per Industry Type',
        xaxis={'title': 'Industry'},
        yaxis={'title': 'Total Deal Amount'}
    )

    return go.Figure(data=[trace], layout=layout)

# Callback for the second plot
@app.callback(
    dash.dependencies.Output('percentage-deal-industry-type-plot', 'figure'),
    [dash.dependencies.Input('season-dropdown', 'value')]
)
def update_percentage_deal_industry_type_plot(selected_season):
    filtered_data = data[data['Seasons'] == selected_season]
    grouped_data = filtered_data.groupby('Industry')['Total Deal Amount'].sum().reset_index()
    total_deal_amount = grouped_data['Total Deal Amount'].sum()
    percentage_data = grouped_data['Total Deal Amount'] / total_deal_amount * 100

    trace = go.Pie(labels=grouped_data['Industry'], values=percentage_data)

    layout = go.Layout(
        title='Percentage of Sum Deal Amount per Industry Type'
    )

    return go.Figure(data=[trace], layout=layout)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
