import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def read_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    return df

def get_top_keywords(df, top_n=10):
    # Aggregate counts by keyword
    keyword_total_counts = df.groupby('Keyword')['Frequency'].sum().sort_values(ascending=False)
    
    # Get the top N keywords
    top_keywords = keyword_total_counts.head(top_n).index
    return top_keywords

def generate_all_years(start_year, end_year):
    return list(range(start_year, end_year + 1))

def prepare_data_for_plot(df, top_keywords):
    # Filter the data to include only the top keywords and up to the year 2023
    filtered_df = df[(df['Keyword'].isin(top_keywords)) & (df['Year'] <= 2023)].copy()
    
    # Ensure Year is treated as an integer
    filtered_df.loc[:, 'Year'] = filtered_df['Year'].astype(int)
    
    # Aggregate the frequencies by year
    filtered_df = filtered_df.groupby(['Year', 'Keyword']).agg({'Frequency': 'sum'}).reset_index()
    
    # Generate all years from 2010 to 2023
    all_years = generate_all_years(2010, 2023)
    all_years_df = pd.DataFrame({'Year': all_years})
    
    # Prepare the complete data for each keyword
    complete_data = []
    for keyword in top_keywords:
        keyword_data = filtered_df[filtered_df["Keyword"] == keyword]
        keyword_data = all_years_df.merge(keyword_data, on='Year', how='left').fillna({'Frequency': 0, 'Keyword': keyword})
        complete_data.append(keyword_data)
    
    # Concatenate all keyword data
    complete_df = pd.concat(complete_data, ignore_index=True)
    
    return complete_df

def get_yaxis_range(df):
    max_frequency = df['Frequency'].max()
    max_log_frequency = np.log(max_frequency + 1)
    return max_frequency, max_log_frequency

def plot_keyword_trends(df, top_keywords, smoothing_window=3):
    fig = make_subplots(rows=1, cols=1)
    
    colors = [
        'blue', 'orange', 'green', 'red', 'purple', 'brown', 
        'pink', 'gray', 'olive', 'cyan', 'magenta'
    ]
    
    max_frequency, _ = get_yaxis_range(df)
    
    for idx, keyword in enumerate(top_keywords):
        keyword_data = df[df["Keyword"] == keyword].copy()
        keyword_data.loc[:, 'Smoothed_Frequency'] = keyword_data['Frequency'].rolling(window=smoothing_window, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=keyword_data["Year"], 
            y=keyword_data["Smoothed_Frequency"], 
            mode='lines',
            name=keyword,
            line=dict(color=colors[idx % len(colors)], width=2),
            hoverinfo='name+x+y'
        ), row=1, col=1)

    fig.update_layout(
        title='Top 10 Keyword Trends Over Time (Rolling Avg)',
        xaxis_title='Year',
        yaxis_title='Frequency',
        legend_title='Keyword',
        xaxis=dict(tickangle=45, showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False, range=[-0.1, max_frequency]),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255,255,255,0.7)'
        ),
        hovermode='x unified',
        template='plotly_white',
        legend_itemclick='toggleothers'
    )

    fig.show()

def plot_keyword_trends_log(df, top_keywords, smoothing_window=3):
    fig = make_subplots(rows=1, cols=1)
    
    colors = [
        'blue', 'orange', 'green', 'red', 'purple', 'brown', 
        'pink', 'gray', 'olive', 'cyan', 'magenta'
    ]
    
    _, max_log_frequency = get_yaxis_range(df)
    
    for idx, keyword in enumerate(top_keywords):
        keyword_data = df[df["Keyword"] == keyword].copy()
        keyword_data.loc[:, 'Smoothed_Log_Frequency'] = np.log(keyword_data['Frequency'].rolling(window=smoothing_window, min_periods=1).mean() + 1)  # Add 1 to avoid log(0)
        fig.add_trace(go.Scatter(
            x=keyword_data["Year"], 
            y=keyword_data['Smoothed_Log_Frequency'], 
            mode='lines',
            name=keyword,
            line=dict(color=colors[idx % len(colors)], width=2),
            hoverinfo='name+x+y'
        ), row=1, col=1)

    fig.update_layout(
        title='Top 10 Keyword Trends Over Time (Rolling Avg, Log Scale)',
        xaxis_title='Year',
        yaxis_title='Log(Frequency)',
        legend_title='Keyword',
        xaxis=dict(tickangle=45, showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False, range=[-0.1, max_log_frequency]),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255,255,255,0.7)'
        ),
        hovermode='x unified',
        template='plotly_white',
        legend_itemclick='toggleothers'
    )

    fig.show()

if __name__ == '__main__':
    csv_file = 'data/TAFFC_keywords_by_year.csv'

    # Read the CSV file
    df = read_csv(csv_file)

    # Get the top 10 keywords
    top_keywords = get_top_keywords(df, top_n=10)

    # Prepare data for plotting
    df_prepared = prepare_data_for_plot(df, top_keywords)

    # Plot keyword trends with smoothed frequency
    plot_keyword_trends(df_prepared, top_keywords)

    # Plot keyword trends with smoothed log(frequency)
    plot_keyword_trends_log(df_prepared, top_keywords)
