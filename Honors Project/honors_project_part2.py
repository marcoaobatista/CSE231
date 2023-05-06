'''
###########################################################
Honors Project Part 2
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
    close file handlers
    get safe take off and landing data for proposed and current runway
    get number of shared take off and landing times
    generates csv file with the data from the filtered list, safe take off and 
landing data for proposed runway and current runway
    display number of feasible datapoints, safe datapoints for proposed runway,
safe datapoints for current runway, and shared datapoints between runways
###########################################################
'''

import csv
import datetime
from operator import itemgetter
from math import sin, radians
from copy import deepcopy

def skip_lines(n, fp):
    """
    skips n number of lines in the input file
    n: number of lines to be skipped (int)
    fp: file pointer (_io.TextIOWrapper)
    return: None
    """
    for i in range(n):
        next(fp)


def read_file(fp):
    """
    reads the file and returns a list of dictionaries with relevant information
    fp: file pointer (_io.TextIOWrapper)
    return: weather_list (list of dictionaries)
    """
    reader = csv.reader(fp)
    weather_list = []
    for line in reader:
        weather_data = {
            'date': line[0],
            'time': line[1],
            'temp': line[2],
            'wind spd': line[5],
            'wind direction': line[6],
            'peak wind gust': line[7],
            'ceiling': line[8],
            'visibility': line[11]
        }
        
        weather_list.append(weather_data)
    return weather_list
         

def filter_by_date(weather_list):
    """
    converts date and time in the dictionary to datetime objects, and filters 
the list to include only data between the months of march and november
    weather_data: TEW observations data (list of dictionaries)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    for weather_data in weather_list:
        try:
            time = weather_data['time']
            time = [int(n) for n in time.split(':')]
            time = datetime.time(time[0],time[1])
            weather_data['time'] = time
            
            date = weather_data['date']
            date = [int(n) for n in date.split('/')]
            date = datetime.date(date[2],date[0], date[1])
            # if month is between march and november
            if date.month > 2 and date.month < 12:
                weather_data['date'] = date
                new_list.append(weather_data)
        except ValueError:
            continue
    return new_list


def replace_values_1(weather_list):
    """
    replaces missing values with the last value plus "*" for temp, visibility, 
and low cloud ht in each dict
    weather_list: TEW observations data (list of dictionaries)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    last_visibility = '0'
    last_temp = '0'
    last_ceiling = '0'
    
    for weather_data in weather_list:
        if weather_data['temp'] in 'Mm':
            weather_data['temp'] = last_temp + '*'
        else:
            last_temp = weather_data['temp']
        
        if weather_data['visibility'] in 'Mm':
            weather_data['visibility'] = last_visibility + '*'
        else:
            last_visibility = weather_data['visibility']
            
        if weather_data['ceiling'] in 'Mm':
            weather_data['ceiling'] = last_ceiling + '*'
        else:
            last_ceiling = weather_data['ceiling']
        
        new_list.append(weather_data)
    return new_list
    

def check_validity(weather_list):
    """
    filters the data, keeping only the times in which the temperature is more
or equal to 35(F), low cloud ht is more or equal to 2000(ft), and visibility is
more or equal to 5(mi) 
    weather_list: TEW observations data (list of dictionaries)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    for weather_data in weather_list:
        
        if int(weather_data['temp'].strip('*')) < 35:
            continue
        if int(weather_data['ceiling'].strip('*')) < 2000:
            continue
        if int(weather_data['visibility'].strip('*')) < 5: 
            continue
        new_list.append(weather_data)
            
    return new_list


def replace_values_2(weather_list):
    """
    replaces missing values with the last value plus "*" for peak wind gust, 
wind speed, and wind direction in each dict
    weather_list: TEW observations data (list of dictionaries)
    returns: new_list (filtered list of dictionaries)
    """
    new_list = []
    last_peak_wind_gust = '0'
    last_wind_speed = '0'
    last_wind_direction = '0'
    
    for weather_data in weather_list:
        if weather_data['peak wind gust'] in 'Mm':
            weather_data['peak wind gust'] = last_peak_wind_gust + '*'
        else:
            last_peak_wind_gust = weather_data['peak wind gust']
        
        if weather_data['wind spd'] in 'Mm':
            weather_data['wind spd'] = last_wind_speed + '*'
        else:
            last_wind_speed = weather_data['wind spd']
            
        if weather_data['wind direction'] in 'Mm':
            weather_data['wind direction'] = last_wind_direction + '*'
        else:
            last_wind_direction = weather_data['wind direction']
        
        new_list.append(weather_data)
    return new_list


def filter_by_daylight(weather_list, twilight_fp):
    """
    reads the twilight file to gather sunrise and sunset times, and filters the
list of dictionaries to contain just the data between sunrise and sunset of 
each day
    weather_list: TEW observations data (list of dictionaries)
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

    for weather_data in weather_list:
        for twilight in twilight_list:
            if twilight[0] == weather_data['date']:
                # if time in dictionary is between sunrise and sunset
                if weather_data['time'] > twilight[1] \
                    and weather_data['time'] < twilight[2]:
                    new_list.append(weather_data)
                break
    return new_list
    

def remove_duplicates(weather_list):
    """
    removes dictionaries that have the same date and time
    weather_list: TEW observations data (list of dictionaries)
    return: weather_list (filtered list of dictionaries)
    """
    for i in range(0,len(weather_list)):
        try:
            if weather_list[i-1]['date'] == weather_list[i]['date'] \
                and \
                weather_list[i-1]['time'] == weather_list[i]['time']:
                weather_list.pop(i)
        except:
            pass
    return weather_list
        

def sort_by_time(weather_list):
    """
    sorts the input dictionary list by date and time
    weather_list: TEW observations data (list of dictionaries)
    return: weather_list (sorted list of dictionaries)
    """
    weather_list = sorted(weather_list, key=itemgetter('time'))
    weather_list = sorted(weather_list, key=itemgetter('date'))
    return weather_list
    

def generate_file(weather_list, file_name):
    """
    generates a comma separated value (csv) file with the date from the input
list of dictionaries
    weather_list: observations data (list of dictionaries)
    file_name: name of the file to be generated (string)
    return: None
    """
    fp = open(file_name, 'w')
    list_of_tuple_list = []
    # populate tuple list
    for weather_data in weather_list:
        tuple_list = []
        for key, value in weather_data.items():
            t = key, value
            tuple_list.append(t)
        list_of_tuple_list.append(tuple_list)
        
    # print file header
    print('JEWETT FLD AP (MI),54822,,Lat: 42.5658,\
Lon: -84.4331,Elev: 922 ft,,,', file = fp)
    print('Date,Hr,Min,Temp (F),Wind Spd (mph),Wind Direction (deg),Peak Wind\
Gust(mph),Low Cloud Ht (ft),Visibility (mi)', file = fp)
    
    # print rows
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
        try:
            either = line[8][1]
        except IndexError:
            either = ''
        print(date+','+hour+','+minute+','+temp+','+wind_spd+','+wind_dir+','\
              +gust+','+ceiling+','+visibility+','+either, file = fp)
    
    fp.close()


def shared_data_count(cur_safe, prop_safe):
    """
    gets the number of shared data between current runway and proposed runway
    cur_safe: current runway safe flying data (list of dict)
    prop_safe: proposed runway safe flying data  (list of dict)
    return: shared data count (int)
    """
    def dict_list_to_set(weather_list):
        """
        converts a list of dictionaries to set of tuples
        weather_list: weather data list (list of dictionaries)
        return: converted data (set of tuples)
        """
        # define an empty set to store the converted data
        converted_data = set()
        
        # iterate over the list of dictionaries
        for weather_data in weather_list: 
            
            # extract the relevant data from the dictionary 
            date = weather_data['date']
            time = weather_data['time']
            temp = weather_data['temp']
            wind_spd = weather_data['wind spd']
            wind_dir = weather_data['wind direction']
            wind_gust = weather_data['peak wind gust']
            ceiling = weather_data['ceiling']
            visibility = weather_data['visibility']
            either = weather_data['either']
             
            # convert the data to a tuple
            converted_tuple = (date, time, temp, wind_spd, wind_dir, \
                               wind_gust, ceiling, visibility, either)
            
            # add the tuple to the set
            converted_data.add(converted_tuple)
        return converted_data

    # convert proposed runway data to a set
    set_prop_safe = dict_list_to_set(prop_safe)
    # convert current runway data to a set
    set_cur_safe = dict_list_to_set(cur_safe)
    # get number of shared data
    shared_data_count = len(set_prop_safe & set_cur_safe)
    
    return shared_data_count


def get_safe_times(master_list):
    """
    analizes the data from master_list to determine if it is safe to fly from
the proposed and current runway
    master_list: filtered weather data according to VFR
    return:
        cur_safe: safe flying conditions on current runway (list of dict)
        prop_safe: safe flying conditions on proposed runway (list of dict)
    """
    master_list = deepcopy(master_list)
    # list of safe weather for flying on proposed runway
    prop_safe = []
    # list of safe weather for flying on current runway
    cur_safe = []

    for weather_data in master_list:
        # runways angle
        proposed_angle = 10
        existing_angle = 100
        
        wind_direction = int(weather_data['wind direction'].strip('*'))
        
        # get wind velocities and convert it to knots from mph
        wind_spd = int(weather_data['wind spd'].strip('*')) / 1.151
        wind_gust = int(weather_data['peak wind gust'].strip('*')) / 1.151
        weather_data['either'] = ''
        
        # if gust is bigger than 20 knots, consider it not safe
        if wind_gust > 20:
            continue

        # if wind speed is less or equal than 5 knots, consider it safe
        if wind_spd <= 5:
            prop_safe.append(weather_data)
            cur_safe.append(weather_data)
            weather_data['either'] = 'either'
            continue
        
        # get crosswind velocity vector magnitude
        angular_dif_prop = radians(wind_direction - proposed_angle)
        angular_dif_exist = radians(wind_direction - existing_angle)
        prop_xwc = abs(wind_spd * sin(angular_dif_prop))
        exist_xwc = abs(wind_spd * sin(angular_dif_exist))
        
        # analize if safe for each runway
        proposed = False
        current = False
        if prop_xwc >= 5 and prop_xwc <= 8 and wind_gust <= 12:
            prop_safe.append(weather_data)
            proposed = True
        elif prop_xwc > 8 and prop_xwc <= 12 and wind_gust <= 15:
            prop_safe.append(weather_data)
            proposed = True
        elif prop_xwc > 12 and prop_xwc <= 15 and wind_gust <= 20:
            prop_safe.append(weather_data)
            proposed = True
        
        if exist_xwc >= 5 and exist_xwc <= 8 and wind_gust <= 12:
            cur_safe.append(weather_data)
            current = True
        elif exist_xwc > 8 and exist_xwc <= 12 and wind_gust <= 15:
            cur_safe.append(weather_data)
            current = True
        elif exist_xwc > 12 and exist_xwc <= 15 and wind_gust <= 20:
            cur_safe.append(weather_data)
            current = True
        
        # if both are same add either to dictionary value
        if current and proposed:
            weather_data['either'] = 'either'
    return cur_safe, prop_safe


def main():
    # load data files    
    twilight_fp = open('civil_twilight.txt', 'r')
    TEW_fp = open('TEW_2021_Observations.csv', 'r')
    
    # skip header lines
    skip_lines(9, twilight_fp)
    skip_lines(6, TEW_fp)
    
    # filter observations data based on VFR
    master_list = read_file(TEW_fp)
    master_list = filter_by_date(master_list)
    master_list = replace_values_1(master_list)
    master_list = check_validity(master_list)
    master_list = replace_values_2(master_list)
    master_list = filter_by_daylight(master_list, twilight_fp)
    master_list = sort_by_time(master_list)
    master_list = remove_duplicates(master_list)
    
    # close file handlers
    twilight_fp.close()
    TEW_fp.close()
    
    # get safe take off and landing data for proposed and current runway
    cur_safe, prop_safe = get_safe_times(master_list)
    
    # get shared take off and landing times
    common_data_count = shared_data_count(cur_safe, prop_safe)
    
    # generate files
    generate_file(master_list, 'daylight_weather.csv')
    generate_file(prop_safe, 'proposed_runway_safe.csv')
    generate_file(cur_safe, 'current_runway_safe.csv')
    
    # display number of data points
    print('Total feasible data points:',len(master_list))
    print("Data points that are safe for the current runway:",len(cur_safe))
    print("Data points that are safe for the proposed runway:",len(prop_safe))
    print("Data points that are safe for both runways:", common_data_count)
    
    
main()