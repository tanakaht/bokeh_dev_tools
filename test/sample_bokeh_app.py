from bokeh.models import HoverTool, ColumnDataSource, LassoSelectTool
from bokeh.plotting import figure, output_notebook, output_file, reset_output, show
from bokeh.models.plots import Plot
from bokeh.layouts import gridplot, column, row
from bokeh.models.widgets import Select, Button, Toggle
import numpy as np

def mod_doc(doc):
    p = figure()
    d = dict(x=np.random.rand(3000), y=np.random.rand(3000))
    ds = ColumnDataSource(d)
    r = p.circle(x='x', y='y', source=ds)
    doc.add_root(p)
