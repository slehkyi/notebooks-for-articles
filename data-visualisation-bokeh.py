from bokeh.io import output_file, show
from bokeh.plotting import figure
plot = figure(plot_width=400, tools='pan,box_zoom')
plot.circle([1,2,3,4,5], [8,6,5,2,3])
output_file('circle.html')
show(plot)
