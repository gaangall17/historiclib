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

def writecsv(name, values):
    with open(name, 'w', newline='') as csvfile:
        csvdata = csv.writer(csvfile, delimiter=',', quotechar='|')
        csvdata.writerows(values)

def geohistoric_formatted_by_id(data, id, fields, decimals):
    result = []
    raw_times = []
    raw_values = []
    i = 0
    for field in fields:
        if field == 'RecordTime': time_ind = i
        elif field == 'ValueAsReal': value_ind = i
        elif field == 'Id': id_ind = i
        i += 1
    for row in data:
        if row[id_ind] == str(id):
            timestamp = datetime.strptime(row[time_ind][:19], '%Y-%m-%d %H:%M:%S')
            value = round(float(row[value_ind]), decimals)
            raw_times.append(timestamp)
            raw_values.append(value)
            result.append([timestamp,value])
    return result, raw_times, raw_values

def create_time_vals_minutes(str_start, str_stop, step_minutes):
    datetime_start = datetime.strptime(str_start, '%Y-%m-%d %H:%M:%S')
    datetime_stop = datetime.strptime(str_stop, '%Y-%m-%d %H:%M:%S')
    step = timedelta(minutes=step_minutes)

    time_vals = [datetime_start]
    
    if datetime_stop > datetime_start:
        while (time_vals[-1] + step) < datetime_stop:
            time_vals.append(time_vals[-1] + step)
    
    return time_vals


def get_report_minutes(vals, str_start, str_stop, step_minutes):
    #time_vals = create_time_vals_minutes(str_start, str_stop, step_minutes)
    pass

# New functions

def extract_time_range_for_interp(data, str_start, str_stop):
    datetime_start = datetime.strptime(str_start, '%Y-%m-%d %H:%M:%S')
    datetime_stop = datetime.strptime(str_stop, '%Y-%m-%d %H:%M:%S')
    times_datetime = []
    values = []
    for row in data:
        if row[0] > datetime_start-timedelta(minutes=30) and row[0] < datetime_stop+timedelta(minutes=30):
            times_datetime.append(row[0])
            values.append(row[1])
    return times_datetime, values


def datetime_to_num(array):
    return [int(round(i.timestamp()*1000)) for i in array]

def interp_evaluate(data, start_time, stop_time, step_minutes, mode, decimals):
    
    times = create_time_vals_minutes(start_time, stop_time, step_minutes)
    data_times, data_values = extract_time_range_for_interp(data, start_time, stop_time)

    data_times_num = datetime_to_num(data_times)
    times_num = datetime_to_num(times)

    interp_funct = interp1d(data_times_num, data_values, kind=mode, fill_value='extrapolate')
    values = interp_funct(times_num)

    rounded_val = []

    for value in values:
        rounded_val.append(round(value, decimals))

    return times, rounded_val



if __name__ == "__main__":
    
    data = readcsv('inputs/flow_5_diciembre.csv')
    
    caudal, raw_times, raw_values = geohistoric_formatted_by_id(data, 86782, ['RecordTime','Id','ValueAsReal'], 2)

    times, values = interp_evaluate(caudal, '2020-06-01 00:00:00', '2021-02-10 23:59:59', 15, 'linear', 2)

    report = []

    for i in range(len(times)):
        report.append([times[i], values[i]])

    print(report[10])

    writecsv('outputs/report_caudal_5_diciembre_15.csv',report)

    output_file('report2.html')
    fig = figure(x_axis_type='datetime',plot_width=1200,plot_height=400)
    fig.line(raw_times,raw_values, line_width = 2,color="navy")
    fig.line(times,values, line_width = 4,color="orange")
    show(fig)