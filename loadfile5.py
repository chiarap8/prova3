from bokeh.io import curdoc
from bokeh.models.widgets import FileInput, Button
from base64 import b64decode
import pandas as pd
import io
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Circle
from bokeh.plotting import figure
import numpy as np


import sys
#creo un bottone per chiudereil servere e avere il prompt di anaconda libero
def button_callback():
    sys.exit()  # Stop the server
# Button to stop the server
ex_button = Button(label="Clicca per chiudere", button_type="success")
ex_button.on_click(button_callback)





# funzione che parte quando faccio il load del file: carica i dati
# nota la presenza delle variabili globali, perche i dati servono in funzioni successive
def upload_fit_data(attr, old, new):
    # i print sono per controllo! vengon stampati nel pompt
    print("data upload succeeded")
    #to convert the base64 string to what you want and plot the data.
    decoded = b64decode(new)
    f = io.BytesIO(decoded)
    df = pd.read_csv(f)
    print(df)
    global x, y, s1
    x=list(df.time)
    y=list(df.ch2)    
    s1 = ColumnDataSource(data=dict(x=x, y=y))
    
file_input = FileInput(accept=".csv,.json,.txt,.pdf,.xls") #se vuo formato diverso da csv devi cambiare la funzione precedente di pandas:new_df = pd.read_csv(f)
file_input.on_change('value', upload_fit_data)


# create a plot and style its properties
p = figure(title="dati acquisiti", tools="reset,pan,box_zoom, hover, tap, poly_select, box_select ")
p.border_fill_color = 'white'
p.background_fill_color = 'white'
p.outline_line_color = None
p.grid.grid_line_color = None



#creo un bottone per plottare i dati
def button_grafico():
  global r
  r=p.circle("x", "y", source=s1, color="blue")
  
    
grafico_button = Button(label="Clicca per plot", button_type="success")
grafico_button.on_click(button_grafico)


#r.selection_glyph = Circle(fill_color="orange", line_color=None)
#r.nonselection_glyph = Circle(fill_color="black", line_color=None)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(file_input,p, grafico_button, ex_button))
