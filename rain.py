from bokeh.plotting import figure, output_file, show
from datetime import datetime, timedelta
from scipy.interpolate import interp1d
import numpy
import csv
import pytz


def readcsv(name):
    result = []
    with open(name, newline='') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvdata:
            result.append(row)
    return result

def extract_by_id(rows, id):
    result = []
    for row in rows:
        if row[1] == str(id):
            if 'PM' in row[0] or 'AM' in row[0]:
                #1/24/2021 4:20:05.873 PM
                timestamp_format = row[0].replace(row[0][len(row[0])-7::],row[0][len(row[0])-3::]) 
                #1/24/2021 4:20:05 PM
                timestamp = datetime.strptime(timestamp_format, '%m/%d/%Y %I:%M:%S %p')
            else:
                timestamp_format = row[0][:19]
                #2021 08:15:00
                timestamp = datetime.strptime(timestamp_format, '%Y-%m-%d %H:%M:%S')
            #timestamp.replace(tzinfo=pytz.timezone('America/Lima'))
            if float(row[2]) > 500:
                value = 500
            elif float(row[2]) < 0:
                value = 0
            else:
                value = float(row[2])
            result.append([timestamp,value])
    return result

def extract_by_id_all(raw, db):
    result = []
    for element in db:
        if element[1] == '100861':
            element_data = extract_by_id(raw,element[1])
            element_name = element[0]
            element_color = element[2]
            result.append([element_name,element_data,element_color])
    return result

def graph_multiple_points(name, points):
    output_file(name)
    fig = figure(y_axis_label="mm/h",x_axis_label="time",title="Rain",x_axis_type='datetime',plot_width=1200,plot_height=600)
      
    for point in points:
        x = []
        y = []
        for row in point[1]:
            x.append(row[0])
            y.append(row[1]) 
        fig.line(x, y, line_width = 1, line_color=point[2], legend_label=point[0])
        fig.circle(x, y, size=5, color=point[2], alpha=0.5)

    show(fig) 

def extract_from_time_range(two_dim_rows, str_start, str_stop):
    datetime_start = datetime.strptime(str_start, '%Y/%m/%d %H:%M:%S')
    datetime_stop = datetime.strptime(str_stop, '%Y/%m/%d %H:%M:%S')
    times_num = []
    times_datetime = []
    values = []
    for row in two_dim_rows:
        if row[0] > datetime_start and row[0] < datetime_stop:
            times_num.append(int(round(row[0].timestamp()*1000)))
            times_datetime.append(row[0])
            values.append(row[1])
    return times_num, times_datetime, values

if __name__=="__main__":
    pluv_raw = readcsv('inputs/inst.csv')
    #pluv_lurgi_conv = extract_by_id(pluv_raw, 89234)
    
    pluv_db = readcsv('inputs/pluviometro_db.csv')

    data_extracted = extract_by_id_all(pluv_raw, pluv_db)

    graph_multiple_points('rain.html',data_extracted)

    #test = readcsv('documents/test_format_datetime.csv')
    #test_result = extract_by_id(test, 89234)
    #print(test_result)


