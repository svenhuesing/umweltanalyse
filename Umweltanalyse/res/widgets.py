from ipyleaflet import Map, Marker, LayersControl, MarkerCluster, LayerGroup, WidgetControl, Polyline, Popup
from ipywidgets import IntSlider, Play, Layout, Output, VBox, HTML, Button, Dropdown, Combobox, HBox, Text, AppLayout
import pandas as pd
import numpy as np
import time
import datetime
import chart_studio.plotly as py
import cufflinks as cf
import plotly.offline
from IPython.display import clear_output
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

'''
Klasse Steuerung übernimmt das Einlesen und Verwalten der Datensätze (per Dropdown Menü)
'''


class Steuerung:
    loadButton = Button(description='Lade die Umweltdaten', disabled=False, button_style='', 
                    layout = Layout(width = '300px'))



    auswahl = Dropdown(options=['Feinstaub', 'Temperatur', 'Luftfeuchtigkeit'], value='Feinstaub',
                   description='Datei auswählen:', layout = Layout(width = '300px'), disabled=False, 
                   style = {'description_width': 'initial'})
    
    def __init__(self, *args, **kwargs):
        self.data = pd.DataFrame()
        self.output_maske = Output(layout = Layout(width ='auto', max_width = '700px', border = '1px solid gray'))
        pd.set_option('display.max_rows',6)


    def ladeDatei(self, datei):
        if(datei == "ggf. später mehr"):
            print("Später kommen noch andere Datensätze. Wähle bitte einen anderen")
        else:
            if (datei == "Temperatur"):
                self.data = pd.read_csv('Daten/temp.csv', parse_dates=['value'])
            elif (datei == "Feinstaub"):
                self.data = pd.read_csv('Daten/pm.csv', parse_dates=['value'])
            elif (datei == "Luftfeuchtigkeit"):
                self.data = pd.read_csv('Daten/hum.csv', parse_dates=['value'])
            else:
                print("Bitte gültigen Datensatz eingeben.")
            self.data = self.datatype_correction(self.data)
            print(datei + "-Daten wurden geladen")
            

    def buttonLoadData_onclick(self, b):
        Steuerung.ladeDatei(self, datei = Steuerung.auswahl.value)
            
    def loadDataFrame(path: str):
        data = pd.read_csv(path)
        data = datatype_correction(data)
        if data.index.name != 'timestamp':
            df = df.set('timestamp')

    def datatype_correction(self, df):
        df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True,errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        #df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        #df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        #df['hight'] = pd.to_numeric(df['hight'], errors='coerce')
        if df.index.name != 'timestamp':
            df = df.set_index('timestamp')
        return df
    
    def datatype_correction_round30min(df):
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        #df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        #df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        #df['hight'] = pd.to_numeric(df['hight'], errors='coerce')
        df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True,errors='coerce').dt.floor('30T')
        return df


