from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON, OSM, ESRI_IMAGERY, get_provider
import numpy as np

def wgs84_to_web_mercator(lon, lat):

    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    
    return x, y


if __name__=="__main__":
    
    output_file("map.html")
    tile_provider = get_provider(OSM)


    x1_center, y1_center =  wgs84_to_web_mercator(-79.95,-2.15)
    x2_center, y2_center =  wgs84_to_web_mercator(-79.90,-2.26)
    x3_center, y3_center =  wgs84_to_web_mercator(-79.95,-2.10)
    x4_center, y4_center =  wgs84_to_web_mercator(-79.92,-2.20)
    x5_center, y5_center =  wgs84_to_web_mercator(-79.89,-2.22)
    x6_center, y6_center =  wgs84_to_web_mercator(-79.93,-2.18)

    data = ColumnDataSource(data=dict(
        x=[x1_center, x2_center, x3_center, x4_center, x5_center, x6_center],
        y=[y1_center, y2_center, y3_center, y4_center, y5_center, y6_center],
        value=[500, 1000, 2000, 100, 700, 1500],
        name=['Ciencias Naturales','Guasmo','A','B','C','D']
    ))

    TOOLTIPS = [
        ("name", "@name"),
        ("value", "@value"),
    ]

    x_axis_start, y_axis_start =  wgs84_to_web_mercator(-80.1,-2.3)
    SIZE = 35000
    x_axis_end = x_axis_start + SIZE
    y_axis_end = y_axis_start + SIZE
    
    map = figure(x_range=(x_axis_start, x_axis_end), y_range=(y_axis_start, y_axis_end), x_axis_type="mercator", y_axis_type="mercator",plot_width=750,plot_height=750,tooltips=TOOLTIPS)
    
    
    map.add_tile(tile_provider)
    
    
    map.circle('x','y',radius='value',fill_alpha=0.5,fill_color='blue', source = data)

    show(map)

    #TOOLTIPS = [('Organisation', '@OrganisationName')]
    #p = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS)