import calendar
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import seaborn as sns

pd.options.mode.copy_on_write = True
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
   'fcc-forum-pageviews.csv',
   index_col = 'date',
   date_format='ISO8601')

# Clean data
df = df[
   (df['value'] >= df['value'].quantile(0.025)) &
   (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
   global df
   
   # Draw line plot
   fig, ax = plt.subplots()

   ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
   ax.set_xlabel('Date')
   ax.set_ylabel('Page Views')
   plt.plot(df)

   # Save image and return fig (don't change this part)
   fig.savefig('line_plot.png')
   return fig

def draw_bar_plot():
   global df

   # Copy and modify data for monthly bar plot
   df_bar = df[:]
   df_bar['year'] = df_bar.index.year
   df_bar['month'] = df_bar.index.month
   df_bar = df_bar.groupby(['year', 'month']).mean().unstack(fill_value = 0)

   # Draw bar plot
   fig = df_bar.plot(kind = 'bar').figure
   
   plt.xlabel('Years')
   plt.ylabel('Average Page Views')
   plt.legend(
      labels = list(calendar.month_name[1:]),
      title = 'Months')
   
   # Save image and return fig (don't change this part)
   fig.savefig('bar_plot.png')
   return fig

def draw_box_plot():
   global df
   
   # Prepare data for box plots (this part is done!)
   # But I don't like it, so I changed it.
   #df_box = df.copy()
   #df_box.reset_index(inplace=True)
   #df_box['year'] = [d.year for d in df_box.date]
   #df_box['month'] = [d.strftime('%b') for d in df_box.date]
   df_box = df[:]
   df_box['year'] = df_box.index.year
   df_box['month'] = df_box.index.month

   # Draw box plots (using Seaborn)
   fig, (ax1, ax2) = plt.subplots(ncols=2)

   ax1.set_title('Year-wise Box Plot (Trend)')
   ax1.set_xlabel('Year')
   ax1.set_ylabel('Page Views')
   sns.boxplot(
      ax = ax1,
      data = df_box,
      x = 'year',
      y = 'value')

   ax2.set_title('Month-wise Box Plot (Seasonality)')
   ax2.set_xlabel('Month')
   ax2.set_ylabel('Page Views')
   months = list(calendar.month_abbr[1:])
   ax2.set_xticks(range(len(months)), labels = months)
   sns.boxplot(
      ax =  ax2,
      data = df_box,
      x = 'month',
      y = 'value')

   # Save image and return fig (don't change this part)
   fig.savefig('box_plot.png')
   return fig
