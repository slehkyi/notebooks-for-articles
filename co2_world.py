import pandas as pd

from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper, Slider
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row


# Data cleaning and preparation
data = pd.read_csv('data/co2_emissions_tonnes_per_person.csv')
data.head()

# data.loc[:, data.isnull().all()]

gapminder = pd.read_csv('data/gapminder_tidy.csv')
gapminder.head()

df = gapminder[['Country', 'region']].drop_duplicates()
data_with_regions = pd.merge(data, df, left_on='country', right_on='country', how='inner')

data_with_regions.head()

new_df = pd.melt(data_with_regions, id_vars=['country', 'region'])
new_df.head()

columns = ['country', 'region', 'year', 'co2']
new_df.columns = columns


upd_new_df = new_df[new_df['year'].astype('int64') > 1963]
upd_new_df.info()
upd_new_df = upd_new_df.sort_values(by=['country', 'year'])
upd_new_df['year'] = upd_new_df['year'].astype('int64')

df_gdp = gapminder[['Country', 'Year', 'gdp']]
df_gdp.columns = ['country', 'year', 'gdp']
df_gdp.info()

final_df = pd.merge(upd_new_df, df_gdp, on=['country', 'year'], how='left')
final_df = final_df.dropna()
final_df.head()

# Creating visualization app with Bokeh.io
regions_list = final_df.region.unique().tolist()
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x': final_df.gdp[final_df['year'] == 1964],
    'y': final_df.co2[final_df['year'] == 1964],
    'country': final_df.country[final_df['year'] == 1964],
    'region': final_df.region[final_df['year'] == 1964],
})

# Save the minimum and maximum values of the fertility column: xmin, xmax
xmin, xmax = min(final_df.gdp), max(final_df.gdp)

# Save the minimum and maximum values of the life expectancy column: ymin, ymax
ymin, ymax = min(final_df.co2), max(final_df.co2)

# Create the figure: plot
plot = figure(title='Gapminder Data for 1964', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

# Add circle glyphs to the plot
plot.circle(x='x', y='y', fill_alpha=0.8, source=source, legend='region',
            color=dict(field='region', transform=color_mapper))

# Set the legend.location attribute of the plot to 'top_right'
plot.legend.location = 'top_right'

# Set the x-axis label
plot.xaxis.axis_label = 'GDP'

# Set the y-axis label
plot.yaxis.axis_label = 'CO2 emissions (tonnes per person)'


def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider.value
    #x = x_select.value
    #y = y_select.value
    # Label axes of plot
    #plot.xaxis.axis_label = x
    #plot.yaxis.axis_label = y

    new_data = {
        'x': final_df.gdp[final_df['year'] == yr],
        'y': final_df.co2[final_df['year'] == yr],
        'country': final_df.country[final_df['year'] == yr],
        'region': final_df.region[final_df['year'] == yr],
    }
    source.data = new_data

    # Set the range of all axes
    #plot.x_range.start = min(data[x])
    #plot.x_range.end = max(data[x])
    #plot.y_range.start = min(data[y])
    #plot.y_range.end = max(data[y])

    # Add title to figure: plot.title.text
    plot.title.text = 'Gapminder data for %d' % yr


# Make a slider object: slider
slider = Slider(start=1964, end=2013, step=1, value=1964, title='Year')

# Attach the callback to the 'value' property of slider
slider.on_change('value', update_plot)

# Create a HoverTool: hover
hover = HoverTool(tooltips=[('Country', '@country')])

# Add the HoverTool to the plot
plot.add_tools(hover)

# Make a row layout of widgetbox(slider) and plot and add it to the current document
layout = row(widgetbox(slider), plot)
curdoc().add_root(layout)


