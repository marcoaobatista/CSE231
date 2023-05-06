"""
######################################################################
# Project 07
# Algorithm (main)
#
#     display welcome message
#     get file(s) pointers and cities names
#     read the file(s)
#     prompt for option
#     while option is not '7' (quit)
#         if selected option was '1'
#             prompt for starting and ending dates
#             prompt for category to be considered
#             filter data by timespan
#             get category column index
#             if category index is invalid, display error message
#             otherwise, get max values
#             display categories name, and the max values for each city
#
#         if selected option was '2'
#             prompt for starting and ending dates
#             prompt for category to be considered
#             filter data by timespan
#             get category column index
#             if category index is invalid, display error message
#             otherwise, get min values
#             display categories name, and the min values for each city
#
#         if selected option was '3'
#             prompt for starting and ending dates
#             prompt for category to be considered
#             filter data by timespan
#             get category column index
#             if category index is invalid, display error message
#             otherwise, get average values
#             display categories name, and the average values for each city
#  
#         if selected option was '4'
#             prompt for starting and ending dates
#             prompt for category to be considered
#             filter data by timespan
#             get category column index
#             if category index is invalid, display error message
#             otherwise
#                 get modes
#                 display categories name, then city name, modes values, and 
# their frequency for each city
#   
#         if selected option is '5'
#             prompt for starting and ending dates
#             prompt for category to be considered
#             filter data by timespan
#             get category column index
#             if category index is invalid, display error message, and 
# re-prompt
#             otherwise, display summary statistics
#  
#         if selected option is '6'
#             prompt for starting and ending dates
#             prompt for category to be considered
#             filter data by timespan
#             display high and low averages for each category across all data
#     
#         reprompt for option
#     display goodbye message
######################################################################
"""


import csv
from datetime import datetime
from operator import itemgetter

COLUMNS = ["date",  "average temp", "high temp", "low temp", "precipitation", \
           "snow", "snow depth"]

TOL = 0.02

BANNER = 'This program will take in csv files with weather data and compare \
the sets.\nThe data is available for high, low, and average temperatures,\
\nprecipitation, and snow and snow depth.'    

MENU = '''
        Menu Options:
        1. Highest value for a specific column for all cities
        2. Lowest value for a specific column for all cities
        3. Average value for a specific column for all cities
        4. Modes for a specific column for all cities
        5. Summary Statistics for a specific column for a specific city
        6. High and low averages for each category across all data
        7. Quit
        Menu Choice: '''
        
        
def open_files():
    ''' 
    prompts for file names and creates file pointers
    return: city names and file pointers (two lists, one with strings and 
another with file pointers)
    '''
    cities = input("Enter cities names: ")
    cities = cities.split(',')
    fp_list = []
    cities_list = []
    for city in cities:
        file_name = city + '.csv'
        try:
            fp = open(file_name)
            fp_list.append(fp)
            cities_list.append(city)
        except FileNotFoundError:
            print("\nError: File {} is not found".format(file_name))
            continue
    return cities_list, fp_list


def read_files(cities_fp):
    ''' 
    reads the input files
    cities_fp: list of file pointers
    return: files data (list of lists of tuples)
    '''
    files_data_list = []
    for fp in cities_fp:
        file_data = []
        reader = csv.reader(fp)
        next(reader)
        next(reader)
        for line in reader:
            Date = line[0]
            # None if cell is empty, convert to float otherwise
            TAVG = float(line[1]) if line[1] else None
            TMAX = float(line[2]) if line[2] else None
            TMIN = float(line[3]) if line[3] else None
            PRCP = float(line[4]) if line[4] else None
            SNOW = float(line[5]) if line[5] else None
            SNWD = float(line[6]) if line[6] else None
            file_data.append((Date, TAVG, TMAX, TMIN, PRCP, SNOW, SNWD))
        files_data_list.append(file_data)
    return files_data_list


def str_to_datetime(date_str):
    '''
    converts a string to a datetime object
    date_str: date in the format mm/dd/yy (string)
    return: converted date (datetime.date object)
    '''
    return datetime.strptime(date_str, "%m/%d/%Y").date()


def get_data_in_range(master_list, start_str, end_str):
    ''' 
    filters the data to include only dates that are between the input dates 
inclusive
    master_list: data originated from the file(s) (list of lists of tuples)
    start_str: date in the format mm/dd/yy (string)
    end_str: date in the format mm/dd/yy (string)
    return: filtered master_list (list of list of tuples)
    '''
    start_date = str_to_datetime(start_str)
    end_date = str_to_datetime(end_str)
    filtered_master_list = []
    
    for file_data in master_list:
        filtered_file_data = []
        for row in file_data:
            date_str = row[0]
            date = str_to_datetime(date_str)
           
            # if data is between the input dates (inclusive)
            if date >= start_date and date <= end_date:
                filtered_file_data.append(row)
        filtered_master_list.append(filtered_file_data)
    return filtered_master_list


def get_min(col, data, cities): 
    ''' 
    gets the minimum value from a certain column (category)
    col: column to be considered (int)
    data: data originated from the files (list of lists of tuples)
    cities: list of the cities in the data list (list of strings)
    return: tuples with city name, and minimum value in the column (list of 
tuples: [(city, min_value)])
    '''
    min_value_list = []
    for file_data, city in zip(data, cities):
        min_value = 10**9
        for row in file_data:
            try:
                min_value = min(row[col], min_value)
            except TypeError:
                continue
        min_value_list.append((city, min_value))
    return min_value_list
        
    
def get_max(col, data, cities): 
    ''' 
    gets the minimum value from a certain column (category)
    col: column to be considered (int)
    data: data originated from the files (list of lists of tuples)
    cities: list of the cities in the data list (list of strings)
    return: tuples with city name, and maximum value in the column ( list of 
    tuples: [(city, max_value)] )
    '''
    max_value_list = []
    for file_data, city in zip(data, cities):
        max_value = 0
        for row in file_data:
            try:
                max_value = max(row[col], max_value)
            except TypeError:
                continue
        max_value_list.append((city, max_value))
    return max_value_list


def get_average(col, data, cities): 
    ''' 
    calculates the average value of a certain column (category)
    col: column to be considered (int)
    data: data originated from the files (list of lists of tuples)
    cities: list of the cities in the data list (list of strings)
    return: tuples with city name, and column's average value ( list of tuples: 
[(city, average_value)] )
    '''
    average_value_list = []
    for file_data, city in zip(data, cities):
        sum_value = 0
        count = 0
        
        for row in file_data:
            try:
                sum_value += row[col]
                count += 1
            except:
                continue
        avg = round(sum_value/count,2)
        average_value_list.append((city, avg))
    return average_value_list


def get_modes(col, data, cities):
    ''' 
    calculates the mode from a certain column (category), considering a 
tolerance 
    col: column to be considered (int)
    data: data originated from the files (list of lists of tuples)
    cities: list of the cities in the data list (list of strings)
    return: tuples with city name, list of column's mode value(s), and it's
frequency ( list of tuples: [(city, [list of values], frequency)] )
    '''
    modes_list = []
    for file_data, city in zip(data, cities):
        column = []
        for row in file_data:
            if row[col]:
                column.append(row[col])
        column.sort()
        
        streaks = []
        count = 0
        n1 = column[0]

        for i in range(0,len(column)):
            try:
                # absolute relative difference between the previous value and
                #the current
                abs_rel_dif = abs((n1-column[i])/n1)
                
                # if the absolute relative difference is less or equal to TOL
                if abs_rel_dif <= TOL:
                    count += 1 # add one to the count
                else:
                    count = 1 # reset count 
                    n1 = column[i] # set n1 to current iteration value
                streaks.append((count, n1))
                
            except IndexError:
                continue
        # sort in decreasing order and get the highest frequency
        streaks.sort(reverse = True)
        higher_mode = streaks[0][0] 
        modes = []
        # add to modes list the tuples with highest counts
        for t in streaks:
            if t[0] == higher_mode and higher_mode != 1:
                modes.append(t)
        
        modes_list.append((city, sorted([i[1] for i in modes]), higher_mode))
    return modes_list

        
def high_low_averages(data, cities, categories):
    ''' 
    gets the highest and lowest averages from the data (column) of given cities
    data: data originated from the files (list of lists of tuples)
    cities: list of the cities in the data list (list of strings)
    return: city with the lowest and the city with the highest average ( list 
of tuples [(city, lowest_average), (city, highest_average)] )
    '''
    high_low_averages =  []
    for category in categories:
        try:
            col = COLUMNS.index(category) # get category index
            averages_list = sorted(get_average(col, data, cities), \
                                   key=itemgetter(1))
            
            lowest_tuple = averages_list[0]
            highest_tuple = averages_list[-1]
            for average in averages_list:
                if average[1] == averages_list[-1][1]: 
                    highest_tuple = average
                    break
                    
            # if lowest and highest averages tuples are the same, append just
            # one instance of it
            averages = [lowest_tuple,highest_tuple if lowest_tuple \
                        != highest_tuple else averages_list[0]]
            high_low_averages.append(averages)
        except ValueError:
            high_low_averages.append(None)
    return high_low_averages
    

def display_statistics(col, data, cities):
    ''' 
    prints a summary of the statistics of the data in the list from given 
column: max value, min value, average value, and mode
    col: column to be considered (int)
    data: data originated from the files (list of lists of tuples)
    cities: list of the cities in the data list (list of strings)
    return: None
    '''
    min_values = get_min(col, data, cities)
    max_values = get_max(col, data, cities)
    averages = get_average(col, data, cities)
    modes = get_modes(col, data, cities)
    
    for min_value, max_value, average, city, mode in zip(min_values, \
max_values, averages, cities, modes):
        
        # get mode values in list form
        values = [str(f) for f in mode[1]]
        values = ','.join(values)
        
        frequency =  mode[2]
        
        print("\t{}: ".format(city))
        print("\tMin: {:.2f} Max: {:.2f} Avg: {:.2f}"
              .format(min_value[1], max_value[1], average[1]))
        if mode[1]:
            print("\tMost common repeated values ({:d} occurrences): {:s}\n"
                  .format(frequency,values))
        else:
            print("\tNo modes.")
             
def main():
    print(BANNER)
    
    cities_list, cities_fp = open_files()
    master_list = read_files(cities_fp)
    
    option = input(MENU)
    while option != '7':
        if option == '1':
            start_str = input("\nEnter a starting date (in mm/dd/yyyy \
format): ")
            end_str = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
            
            filtered_data = get_data_in_range(master_list, start_str, end_str)
            
            try:
                col = COLUMNS.index(category)
                max_values = get_max(col, filtered_data, cities_list)
                print('\n\t{}: '.format(category))
                
                for max_value in max_values:
                    city = max_value[0]
                    value = max_value[1]
                    print("\tMax for {:s}: {:.2f}".format(city, value))
            except:
                print("\n\t{} category is not found.".format(category))

            
        if option == '2':
            start_str = input("\nEnter a starting date (in mm/dd/yyyy \
format): ")
            end_str = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
           
            filtered_data = get_data_in_range(master_list, start_str, end_str)
            
            try:
                col = COLUMNS.index(category)
                min_values = get_min(col, filtered_data, cities_list)
                print('\n\t{}: '.format(category))
                
                for min_value in min_values:
                    city = min_value[0]
                    value = min_value[1]
                    print("\tMin for {:s}: {:.2f}".format(city, value))
            except:
                print("\n\t{} category is not found.".format(category))
               
                
        if option == '3':
            start_str = input("\nEnter a starting date (in mm/dd/yyyy \
format): ")
            end_str = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
            
            filtered_data = get_data_in_range(master_list, start_str, end_str)
            
            try:
                col = COLUMNS.index(category)
                average_values = get_average(col, filtered_data, cities_list)
                print('\n\t{}: '.format(category))
                
                for average_value in average_values:
                    city = average_value[0]
                    value = average_value[1]
                    print("\tAverage for {:s}: {:.2f}".format(city, value))
            except:
                print("\n\t{} category is not found.".format(category))
        
        
        if option == '4':
            start_str = input("\nEnter a starting date (in mm/dd/yyyy \
format): ")
            end_str = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
            
            filtered_data = get_data_in_range(master_list, start_str, end_str)
            
            try:
                col = COLUMNS.index(category)
                modes_values = get_modes(col, filtered_data, cities_list)
                print('\n\t{}: '.format(category))
                
                for modes_value in modes_values:
                    city = modes_value[0]
                    values = [str(f) for f in  modes_value[1]]
                    values = ','.join(values)
                    frequency = modes_value[2]
                    
                    print("\tMost common repeated values for {:s} ({:d} \
occurrences): {:s}\n".format(city, frequency, values))
            except:
                print("\n\t{} category is not found.".format(category))
                
                
        if option == '5':
            start_str = input("\nEnter a starting date (in mm/dd/yyyy \
format): ")
            end_str = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
            
            filtered_data = get_data_in_range(master_list, start_str, end_str)
            
            while True:
                try:
                    col = COLUMNS.index(category)
                    break
                except:
                    print("\n\t{} category is not found.".format(category))
                    category = input("\nEnter desired category: ").lower()
            
            print('\n\t{}: '.format(category))
            
            display_statistics(col, filtered_data, cities_list)
               
            
        if option == '6':
            start_str = input("\nEnter a starting date (in mm/dd/yyyy \
format): ")
            end_str = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            categories = input("\nEnter desired categories seperated by \
comma: ").lower().split(',')

            filtered_data = get_data_in_range(master_list, start_str, end_str)
            high_low_averages_list = high_low_averages(filtered_data, \
                                                       cities_list, categories)
                
            print("\nHigh and low averages for each category across all data.")
            for category, category_list in zip(categories, \
                                               high_low_averages_list):
                if category_list == None:
                    print("\n\t{} category is not found.".format(category))
                    continue
                
                low_city = category_list[0][0]
                low_avg = category_list[0][1]
                high_city = category_list[1][0]
                high_avg = category_list[1][1]
                
                print('\n\t'+category+': ')
                print("\tLowest Average: {:s} = {:.2f} Highest Average: {:s} \
= {:.2f}".format(low_city, low_avg, high_city, high_avg))
                
        option = input(MENU)
        
    print("\nThank you using this program!")
    
    
#DO NOT CHANGE THE FOLLOWING TWO LINES OR ADD TO THEM
#ALL USER INTERACTIONS SHOULD BE IMPLEMENTED IN THE MAIN FUNCTION
if __name__ == "__main__":
    main()
    