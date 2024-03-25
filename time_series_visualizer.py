import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'])
df = df.set_index('date')
df.rename(columns={'value': 'Page Views'}, inplace=True)

# Clean data
df = df[(df['Page Views'] >= df['Page Views'].quantile(0.025)) &
              (df['Page Views'] <= df['Page Views'].quantile(0.975))]



def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 3), dpi=100)
    ax.plot(df.index, df['Page Views'], color='red', linewidth=0.75)
    ax.set(xlabel='Date', ylabel='Page Views',
           title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_yticks(np.arange(20000, 180001, 20000))

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.month_name()

    # grouping and orgenizing the df
    df_bar_group = df_bar.groupby(['year', 'month'])['Page Views'].mean()
    df_bar_group = df_bar_group.unstack(level='month')
    months = sorted(df_bar_group.columns.tolist(), key=lambda x: pd.to_datetime(x, format='%B').month)
    df_bar_group = df_bar_group[months]

    #Draw bar plot
    fig = df_bar_group.plot.bar(figsize=(7,7)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # Set up the figure and axes
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), dpi=100)

    # Boxplot by year
    sns.boxplot(x='Year', y='Page Views', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')

    # Boxplot by month
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(x='Month', y='Page Views', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')

    # Adjust layout
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
