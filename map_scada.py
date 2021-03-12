from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON, OSM, ESRI_IMAGERY, get_provider
from bokeh.transform import factor_cmap, factor_mark
import numpy as np
import csv

def wgs84_to_web_mercator(lon, lat):

    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    
    return x, y

def lon_to_web_mercator(lon):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    return x

def lat_to_web_mercator(lat):
    k = 6378137
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return y


def readcsv(name):
    result = []
    with open(name, newline='') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvdata:
            result.append(row)
    return result

if __name__=="__main__":
    
    locations = readcsv("inputs/location_scada.csv")
    y = []
    x = []
    channel = []
    name = []

    for location in locations:
        y.append(lat_to_web_mercator(float(location[2])))
        x.append(lon_to_web_mercator(float(location[3])))
        name.append(location[0])
        if 'Radio.Modbus' in location[0]:
            channel.append('Radio Modbus')
        elif 'Radio.DNP3' in location[0]:
            channel.append('Radio DNP3')
        elif 'GPRS.DNP3' in location[0]:
            channel.append('GPRS DNP3')
        elif 'GPRS.Modbus' in location[0]:
            channel.append('GPRS Modbus')
        elif 'LAN' in location[0]:
            channel.append('LAN')
        else:
            channel.append('Other')

    output_file("map_scada.html")
    tile_provider = get_provider(OSM)

    type_channel = ['Radio DNP3','Radio Modbus','GPRS DNP3','GPRS Modbus','LAN']
    marker_channel = ['triangle','triangle_dot','circle','circle_dot','square']

    data = ColumnDataSource(data=dict(
        x=x,
        y=y,
        channel=channel,
        name=name
    ))

    TOOLTIPS = [
        ("Nombre", "@name"),
        ("Canal", "@channel"),
    ]

    x_axis_start, y_axis_start =  wgs84_to_web_mercator(-80.1,-2.3)
    SIZE = 35000
    x_axis_end = x_axis_start + SIZE
    y_axis_end = y_axis_start + SIZE
    
    map = figure(x_range=(x_axis_start, x_axis_end), y_range=(y_axis_start, y_axis_end), x_axis_type="mercator", y_axis_type="mercator",plot_width=750,plot_height=750,tooltips=TOOLTIPS)
    
    
    map.add_tile(tile_provider)
    
    #for i in range(len(channel)):
    #    if channel[i] == 'Radio DNP3':
    #        map.circle(x[i],y[i],size=10,fill_alpha=0.5,fill_color='blue', source=ColumnDataSource(data=dict(name=name[i],channel=channel[i])))
    #    if channel[i] == 'GPRS DNP3':
    #        map.square(x[i],y[i],size=10,fill_alpha=0.5,fill_color='red',  source=ColumnDataSource(data=dict(name=name[i],channel=channel[i])))

    map.scatter(source=data, legend_field="channel", fill_alpha=0.4, size=10,
          marker=factor_mark('channel', marker_channel, type_channel))
          #color=factor_cmap('species', 'Category10_3', SPECIES))
        
    show(map)

    #map.circle('x','y',radius=100,fill_alpha=0.5,fill_color='blue', source = data)

    #TOOLTIPS = [('Organisation', '@OrganisationName')]
    #p = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS)