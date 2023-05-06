'''
###########################################################
Honors Project Part 1
Algorithm (main)
    open files to be used (observations file and twilight times file)
    skip the header lines for each file
    read the observations file gathering relevant information and put it in a 
list of dictionaries
    filter the info in the list to have just the observations between the 
months of March and November
    replace missing values for for temp, visibility, and low cloud ht in each 
dict with previous number + "*"
    remove data that does not satisfy modified VFR conditions and minimum 
temperatures
    replace missing values for peak wind gust, wind speed, and wind direction 
in each dict with previous number + "*"
    read the twilight times file and filter the data from the list to include
only times between sunrise and sunset
    sort the list based on time
    remove any duplicate times from the list
    generates csv file with the data from the filtered list
    display number of feasible datapoints
    close both files used
###########################################################
'''

import csv
import datetime
from operator import itemgetter


def skip_lines(n, fp):
    """
    skips n number of lines in the input file
    n: number of lines to be skipped (int)
    fp: file pointer (_io.TextIOWrapper)
    return: None
    """
    for i in range(0,n):
        next(fp)


def read_file(fp):
    """
    reads the file and returns a list of dictionaries with relevant information
    fp: file pointer (_io.TextIOWrapper)
    return: dict_list (list of dictionaries)
    """
    reader = csv.reader(fp)
    dict_list = []
    for line in reader:
        dictt = dict()
        
        dictt['date'] = line[0]
        dictt['time'] = line[1]
        dictt['temp'] = line[2]
        dictt['wind spd'] = line[5]
        dictt['wind direction'] = line[6]
        dictt['peak wind gust'] = line[7]
        dictt['ceiling'] = line[8]
        dictt['visibility'] = line[11]
        
        dict_list.append(dictt)
    return dict_list
         

def filter_by_date(dict_list):
    """
    converts date and time in the dictionary to datetime objects, and filters 
the list to include only data between the months of march and november
    dict_list: TEW observations data (list of dictionaries)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    for dictt in dict_list:
        try:
            time = dictt['time']
            time = [int(n) for n in time.split(':')]
            time = datetime.time(time[0],time[1])
            dictt['time'] = time
            
            date = dictt['date']
            date = [int(n) for n in date.split('/')]
            date = datetime.date(date[2],date[0], date[1])
            # if month is between march and november
            if date.month > 2 and date.month < 12:
                dictt['date'] = date
                new_list.append(dictt)
        except ValueError:
            continue
    return new_list


def replace_values_1(dict_list):
    """
    replaces missing values with the last value plus "*" for temp, visibility, 
and low cloud ht in each dict
    dict_list: TEW observations data (list of dictionaries)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    last_visibility = '0'
    last_temp = '0'
    last_ceiling = '0'
    
    for dictt in dict_list:
        if dictt['temp'] in 'Mm':
            dictt['temp'] = last_temp + '*'
        else:
            last_temp = dictt['temp']
        
        if dictt['visibility'] in 'Mm':
            dictt['visibility'] = last_visibility + '*'
        else:
            last_visibility = dictt['visibility']
            
        if dictt['ceiling'] in 'Mm':
            dictt['ceiling'] = last_ceiling + '*'
        else:
            last_ceiling = dictt['ceiling']
        
        new_list.append(dictt)
    return new_list
    

def check_validity(dict_list):
    """
    filters the data, keeping only the times in which the temperature is more
or equal to 35(F), low cloud ht is more or equal to 2000(ft), and visibility is
more or equal to 5(mi) 
    dict_list: TEW observations data (list of dictionaries)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    for dictt in dict_list:
        
        if int(dictt['temp'].strip('*')) < 35:
            continue
        if int(dictt['ceiling'].strip('*')) < 2000:
            continue
        if int(dictt['visibility'].strip('*')) < 5: 
            continue
        new_list.append(dictt)
            
    return new_list


def replace_values_2(dict_list):
    """
    replaces missing values with the last value plus "*" for peak wind gust, 
wind speed, and wind direction in each dict
    dict_list: TEW observations data (list of dictionaries)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    last_peak_wind_gust = '0'
    last_wind_speed = '0'
    last_wind_direction = '0'
    
    for dictt in dict_list:
        if dictt['peak wind gust'] in 'Mm':
            dictt['peak wind gust'] = last_peak_wind_gust + '*'
        else:
            last_peak_wind_gust = dictt['peak wind gust']
        
        if dictt['wind spd'] in 'Mm':
            dictt['wind spd'] = last_wind_speed + '*'
        else:
            last_wind_speed = dictt['wind spd']
            
        if dictt['wind direction'] in 'Mm':
            dictt['wind direction'] = last_wind_direction + '*'
        else:
            last_wind_direction = dictt['wind direction']
        
        new_list.append(dictt)
    return new_list


def filter_by_daylight(dict_list, twilight_fp):
    """
    reads the twilight file to gather sunrise and sunset times, and filters the
list of dictionaries to contain just the data between sunrise and sunset of 
each day
    dict_list: TEW observations data (list of dictionaries)
    twilight_fp: file pointer to file with twilight times (_io.TextIOWrapper)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    twilight_list = [] # list of tuples (date, sunrise, sunset)
    for line in twilight_fp:
        line = line.strip()
        day = line[:3]
        # split the line in 11 characters at a time, skipping the first 3
        line = [line[i*11+4:(i+1)*11+4].strip() for i in \
                range(0,int(len(line[3:])/11)+1)]
        try:
            day = int(day)
        except ValueError:
            continue
        
        for i in range(0,len(line)):
            month = i+1
            month_times = line[i].strip().split(' ')
            sunrise_time = datetime.time()
            sunset_time = datetime.time()
            try:
                sunrise_time = datetime.time(int(month_times[0][:2]),\
                                             int(month_times[0][2:]))
                sunset_time = datetime.time(int(month_times[1][:2]),\
                                            int(month_times[1][2:]))
                
                date = datetime.date(2021, month, day)
                twilight_list.append((date,sunrise_time,sunset_time))
            except:
                continue

    for dictt in dict_list:
        for twilight in twilight_list:
            if twilight[0] == dictt['date']:
                # if time in dictionary is between sunrise and sunset
                if dictt['time'] > twilight[1] and dictt['time'] < twilight[2]:
                    new_list.append(dictt)
                break
    return new_list
    

def remove_duplicates(dict_list):
    """
    removes dictionaries that have the same date and time
    dict_list: TEW observations data (list of dictionaries)
    return: dict_list (filtered list of dictionaries)
    """
    for i in range(0,len(dict_list)):
        try:
            if dict_list[i-1]['date'] == dict_list[i]['date'] and \
                dict_list[i-1]['time'] == dict_list[i]['time']:
                dict_list.pop(i)
        except:
            pass
    return dict_list
        

def sort_by_time(dict_list):
    """
    sorts the input dictionary list by date and time
    dict_list: TEW observations data (list of dictionaries)
    return: dict_list (sorted list of dictionaries)
    """
    dict_list = sorted(dict_list, key=itemgetter('time'))
    dict_list = sorted(dict_list, key=itemgetter('date'))
    return dict_list
    

def generate_file(dict_list):
    """
    generates a comma separated value (csv) file with the date from the input
list of dictionaries
    dict_list: TEW observations data (list of dictionaries)
    return: None
    """
    daylight_weather_fp = open('daylight_weather.csv', 'w')
    list_of_tuple_list = []
    # populate tuple list
    for dictt in dict_list:
        tuple_list = []
        for key, value in dictt.items():
            t = key, value
            tuple_list.append(t)
        list_of_tuple_list.append(tuple_list)
        
    # print file header
    print('JEWETT FLD AP (MI),54822,,Lat: 42.5658,\
Lon: -84.4331,Elev: 922 ft,,,', file = daylight_weather_fp)
    print('Date,Hr,Min,Temp (F),Wind Spd (mph),Wind Direction (deg),Peak Wind\
Gust(mph),Low Cloud Ht (ft),Visibility (mi)', file = daylight_weather_fp)
    for line in list_of_tuple_list:
        date = line[0][1].strftime("%m/%d/%y")
        hour = '{:2d}'.format(line[1][1].hour)
        minute = '{:2d}'.format(line[1][1].minute)
        temp = line[2][1]
        wind_spd = line[3][1]
        wind_dir = line[4][1]
        gust = line[5][1]
        ceiling = line[6][1]
        visibility = line[7][1]
        print(date+','+hour+','+minute+','+temp+','+wind_spd+','+wind_dir+','\
              +gust+','+ceiling+','+visibility+',', file = daylight_weather_fp)
    
    daylight_weather_fp.close()
    
    
def main():
    dict_list = []
    
    twilight_fp = open('civil_twilight.txt', 'r')
    TEW_fp = open('TEW_2021_Observations.csv', 'r')
    
    skip_lines(9, twilight_fp)
    skip_lines(6, TEW_fp)
    
    dict_list = read_file(TEW_fp)
    dict_list = filter_by_date(dict_list)
    dict_list = replace_values_1(dict_list)
    dict_list = check_validity(dict_list)
    dict_list = replace_values_2(dict_list)
    dict_list = filter_by_daylight(dict_list, twilight_fp)
    dict_list = sort_by_time(dict_list)
    dict_list = remove_duplicates(dict_list)
    
    generate_file(dict_list)
    
    print('Total feasible data points:',len(dict_list))
    
    twilight_fp.close()
    TEW_fp.close()

main()