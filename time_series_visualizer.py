import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. استيراد البيانات وتجهيزها
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_index='date')

# 2. تنظيف البيانات (حذف القيم الشاذة)
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # نسخ البيانات
    df_line = df.copy()

    # رسم المخطط الخطي
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # حفظ الصورة والعودة بالمتغير fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # تجهيز البيانات للمخطط العمودي
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # تجميع البيانات وحساب المتوسط
    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # ترتيب الشهور
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    df_bar_grouped = df_bar_grouped.reindex(columns=months)

    # رسم المخطط
    fig = df_bar_grouped.plot(kind='bar', figsize=(10, 8), legend=True).get_figure()
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # حفظ الصورة والعودة بالمتغير fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # تجهيز البيانات لـ Box Plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # رسم المخططات باستخدام Seaborn
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # المخطط الأول: السنوي (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # المخطط الثاني: الشهري (Seasonality)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=month_order)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # حفظ الصورة والعودة بالمتغير fig
    fig.savefig('box_plot.png')
    return fig
