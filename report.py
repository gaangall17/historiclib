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

def extract_by_id(rows, id):
    result = []
    for row in rows:
        if row[1] == str(id):
            timestamp = datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S')
            timestamp.replace(tzinfo=pytz.timezone('America/Lima'))
            value = float(row[2])
            result.append([timestamp,value])
    return result

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

def plot_bokeh(name, vals):
    output_file(name + '.html')
    fig = figure(x_axis_type='datetime')
    x_vals = []
    y_vals = []
    for row in vals:
        x_vals.append(row[0])
        y_vals.append(row[1])  
    fig.line(x_vals, y_vals, line_width = 2)
    show(fig)


def create_time_vals_minutes(str_start, str_stop, step_minutes):
    datetime_start = datetime.strptime(str_start, '%Y/%m/%d %H:%M:%S')
    datetime_stop = datetime.strptime(str_stop, '%Y/%m/%d %H:%M:%S')
    step = timedelta(minutes=step_minutes)

    time_vals = [datetime_start]
    
    if datetime_stop > datetime_start:
        while (time_vals[-1] + step) < datetime_stop:
            time_vals.append(time_vals[-1] + step)
    
    return time_vals


def get_report_minutes(vals, str_start, str_stop, step_minutes):
    #time_vals = create_time_vals_minutes(str_start, str_stop, step_minutes)
    pass


if __name__ == "__main__":
    
    option = int(input("Opcion Ejemplo: [1] Temporizado, [2] Horometro y Energía, [3] Reporte directo:"))
    
    if option == 1:

        result_flow = readcsv('documents/flow.csv')  
        flow_84339 = extract_by_id(result_flow,84339)

        time_vals_min = create_time_vals_minutes('2020/08/01 00:00:00','2020/08/01 23:59:59',5)
        time_vals_15min = create_time_vals_minutes('2020/08/01 00:00:00','2020/08/01 23:59:59',15)
        times_num, times_datetime, values = extract_from_time_range(flow_84339,'2020/08/01 00:00:00','2020/08/01 23:59:59')
        
        print(flow_84339[1])
        print(time_vals_min[1])

        #x_np = numpy.linspace(0, 10, num=51, endpoint=True)
        #print(x_np)
        #print(type(x_np))
        #pn2 = numpy.polynomial.polynomial.polyfit(times_num, values, 2)
        #pn3 = numpy.polynomial.polynomial.polyfit(times_num, values, 5)
        interpolated_cubic = interp1d(times_num,values,kind='linear',fill_value='extrapolate')
        #print(pn2)
        #print(pn3)
        #print(numpy.polynomial.polynomial.polyval(int(round(time_vals_min[4].timestamp())),pn3,tensor=False))
        #print(numpy.polynomial.polynomial.polyval(int(round(time_vals_min[4].timestamp())),pn2,tensor=False))

        output_file('report.html')
        fig = figure(x_axis_type='datetime',plot_width=1200,plot_height=400)
        x1_vals = []
        y1_vals = []
        #x2_vals = []
        x2_nums = []
        y2_vals = []
        x3_nums = []
        y3_vals = []
        for row in flow_84339:
            x1_vals.append(row[0])
            y1_vals.append(row[1])
        for row in time_vals_min:
            #x2_vals.append(row)
            x2_nums.append(int(round(row.timestamp()*1000)))
            #y2_vals.append(numpy.polynomial.polynomial.polyval(int(round(row.timestamp()*1000)),pn2,tensor=True))
        #for row in time_vals_min:
            #x3_vals.append(row)
            #y3_vals.append(numpy.polynomial.polynomial.polyval(int(round(row.timestamp()*1000)),pn3,tensor=False))
        y2_vals = interpolated_cubic(x2_nums)
        for row in time_vals_15min:
            #x2_vals.append(row)
            x3_nums.append(int(round(row.timestamp()*1000)))
        y3_vals = interpolated_cubic(x3_nums)   


        fig.line(x1_vals,y1_vals, line_width = 2,color="navy")
        fig.circle(x1_vals,y1_vals, size = 7,fill_color="navy")
        #fig.line(times_datetime,values, line_width = 3,color="brown")
        #fig.line(times_num,values, line_width = 3,color="yellow")
        fig.circle(time_vals_min,y2_vals,size = 10,fill_color="green")
        #fig.line(x2_vals,y2_vals, line_width = 2,color="black")
        #fig.circle(x2_vals,y2_vals,size = 5,fill_color="black")
        #fig.line(x3_vals,y3_vals, line_width = 2,color="red")
        #fig.circle(x3_vals,y3_vals,size = 3,fill_color="red")
        fig.circle(time_vals_15min,y3_vals,size = 10,fill_color="orange")
        show(fig)
        #[2:len(x2_nums)-2]

        for_export =[]
        for i in range(len(time_vals_min)):
            for_export.append([time_vals_min[i],y2_vals[i]])
        
        writecsv('documents/report.csv',for_export)
    
    elif option == 2:
        result_hour = readcsv('documents/op_g1h.csv')  
        result_power = readcsv('documents/power_g1h.csv')  

        