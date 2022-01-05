import pandas as pd

from script.kumulatif import *
from script.harian import *
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.io import show, output_file

#Create Dataframe
df = pd.read_csv(join(dirname(__file__), "data", "covid_19_indonesia.csv"))
df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m/%d")

#Create Tabs
tab1 = harian(df)
tab2 = kumulatif(df)
tab = Tabs(tabs=[tab1, tab2])

#Create Curdoc
curdoc().add_root(tab)
curdoc().title = "Indonesia Corona Cases"
show(curdoc)

#HTML File
output_file("final_project.html")