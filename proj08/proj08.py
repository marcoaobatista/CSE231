'''
############################################################
# Project 8
# Algorithm (main)
# get discount and games files
# read files
# prompt for option
# while option input is not 7:
#     if option is 1
#         prompt for year. If invalid, reprompt
#         get games published in year
#         display games names or nothing to print message
#     elif option is 2
#         prompt for developer
#         get games by developer
#         display games names or nothing to print message
#     elif option is 3
#         prompt for genre
#         get games by genre
#         display games names or nothing to print message
#     elif option is 4
#         prompt for developer
#         prompt for year. If invalid, display error message
#         display games names or nothing to print message
#     elif option is 5
#         prompt for genre
#         get games titles by genre and no discount
#         display games names or nothing to print message
#     elif option is 6
#         prompt for developer
#         get games by developer that have discount
#         display games names or nothing to print message
#     else display invalid option message
#     reprompt for option
# display goodbye message
############################################################
'''
import csv
from operator import itemgetter
from datetime import datetime 

MENU = '''\nSelect from the option: 
        1.Games in a certain year 
        2. Games by a Developer 
        3. Games of a Genre 
        4. Games by a developer in a year 
        5. Games of a Genre with no discount 
        6. Games by a developer with discount 
        7. Exit 
        Option: '''
        
      
        
def open_file(s):
    ''' 
    prompts for a file name and re-prompts if file does not exist
    s: type of file to prompt for (string)
    return: file pointer (_io.TextIOWrapper)
    '''
    # re-prompt until file name is valid
    while True:
        try:
            file_name = input(f'\nEnter {s} file: ')
            fp = open(file_name, 'r', encoding='UTF-8')
            break
        except FileNotFoundError:
            print('\nNo Such file')
            pass
    return fp

def read_file(fp_games):
    ''' 
    reads the information from the file and adds it to a dictionary by name
    fp_games: file pointer (_io.TextIOWrapper)
    return: a dictionary with the games and its data as value (dictionary)
    '''
    reader = csv.reader(fp_games)
    # skip header
    next(reader)
    games_data = {}
    
    for line in reader:
        
        name = line[0]
        release_date = line[1]
        developers = line[2].split(';')
        genres = line[3].split(';')
        # if first mode multiplayer, mode is 0 otherwise it is 1
        player_mode = 0 if line[4].split(';')[0].lower() == \
            'multi-player' else 1
        
        price_str = line[5].replace(',','')
        # convert price from dollars to rupees if it is not free to play
        price = float(price_str)*0.012 if price_str.isdigit() else 0.0
        
        overall_reviews = line[6]
        reviews = int(line[7].strip())
        percent_positive = int(line[8].strip('%'))
        
        support = []
        if int(line[9]):
            support.append('win_support')
        if int(line[10]):
            support.append('mac_support')
        if int(line[11]):
            support.append('lin_support')

        games_data[name] = [release_date, developers, genres, player_mode, \
                           price, overall_reviews, reviews, percent_positive,\
                               support]
    return games_data


def read_discount(fp_discount):
    ''' 
    reads the information from the file and adds it to a dictionary by name
    fp_discount: file pointer (_io.TextIOWrapper)
    return: a dictionary with the games and its dicount % as value (dict)
    '''
    reader = csv.reader(fp_discount)
    # skip header
    next(reader)
    discounts_data = {}
    
    # go through the file and add data to dict
    for line in reader:
        name = line[0]
        discount = round(float(line[1]),2)
        discounts_data[name] = discount
    return discounts_data


def in_year(master_D, year):
    ''' 
    gets the names of the games that where published in the input year and sort
them by alphabetical order
    master_D: dictionary of the data originated from the file (dict)
    year: year to be considered when filtering (int)
    return: list of games' titles published in given year (list of strings)
    '''
    games_list = []
    for name, data in master_D.items():
        # convert data to datetime object for sorting purposes
        date = datetime.strptime(data[0], "%d/%m/%Y")
        if date.year == year:
            games_list.append(name)
    # sort alphabetically
    games_list.sort()
    return games_list


def by_genre(master_D,genre): 
    ''' 
    gets the names of the games that have the input genre and sorts them by
positive percentage review from highest to lowest
    master_D: dictionary of the data originated from the file (dict)
    genre: genre to be considerd when filtering (str)
    return: list of games' titles of given genre (list of strings)
    '''
    games_list = []
    for name, data in master_D.items():
        genre_list = data[2]
        positive_percentage = data[7]
        # if the input genre is one of the game's genre
        if genre in genre_list:
            games_list.append((name, positive_percentage))
    
    # sort by positive reviews percentage from highest to lowest
    games_list.sort(key=itemgetter(1), reverse = True)
    games_list = [name for name,percentage in games_list]
    return games_list
        

def by_dev(master_D,developer): 
    ''' 
    get the names of the games that have the input developer as devs and sorts 
them by latest to oldest release date
    master_D: dictionary of the data originated from the file (dict)
    developer: developer to be considered when filtering (str)
    return: list of games by given dev (list of strings)
    '''
    games_list = []
    for name,data in master_D.items():
        developers = data[1]
        if developer in developers:
            # convert data to datetime object for sorting purposes
            year = datetime.strptime(data[0], "%d/%m/%Y").year
            games_list.append((name, year))
    # sort by release year from latest to oldest
    games_list.sort(key=itemgetter(1), reverse = True)
    games_list = [name for name,year in games_list]
    return games_list


def per_discount(master_D,games,discount_D): 
    ''' 
    gets the discounted price of games in the input list
    master_D: dictionary of the data originated from the file (dict)
    games: games to be considered when calculating the price (list of strings)
    discount_D: dictionary of the data originated from the discount file (dict)
    return: list of dicounted prices (list of float)
    '''
    discounted_list = []
    for game in games:
        price = master_D[game][4]
        try:
            discount = discount_D[game]
            # calculate price with discount
            price = round(price*(1-discount/100), 6)
        except KeyError:
            pass
        discounted_list.append(price)
    return discounted_list


def by_dev_year(master_D,discount_D,developer,year):
    ''' 
    gets the names of the games that have the input developer, input release 
year and sorts them by the price before any discount
    master_D: dictionary of the data originated from the file (dict)
    discount_D: dictionary of the data originated from the discount file (dict)
    developer: developer to be considered when filtering (str)
    year: year to be considered when filtering (int)
    return: list of games filtered by year and developer (list of strings)
    '''
    
    games_by_year = set(in_year(master_D, year))
    games_by_dev = set(by_dev(master_D,developer))
    # get games that have given release year and given developer
    games_filtered = games_by_year & games_by_dev
    
    #get prices with discount of the games 
    prices = per_discount(master_D,games_filtered,discount_D)
    
    games = [(game, price) for game, price in zip(games_filtered, prices)]
    
    # sort by price
    games.sort(key=itemgetter(1))
    games = [name for name,price in games]
    return games
        
          
def by_genre_no_disc(master_D,discount_D,genre):
    '''
    gets the names of the games that have a given genre and don't have discount
and sorts them by percent of positive reviews from higher to lowest and then
sort them by price before discount
    master_D: dictionary of the data originated from the file (dict)
    discount_D: dictionary of the data originated from the discount file (dict)
    genre: genre to be considerd when filtering (str)
    return: list of games filtered by genre and no discount (list of strings)
    '''
    games_filtered = by_genre(master_D, genre) # filter by genre
    
    #filter by games not in discount list
    games_filtered = [game for game in games_filtered \
                      if game not in discount_D]
    # tuple list with name, price and positive percentage
    games_filtered = [(game, master_D[game][4], master_D[game][7]) \
                      for game in games_filtered]
    # sort by positive review percentage high to low
    games_filtered.sort(key=itemgetter(2), reverse = True)
    #sort by price
    games_filtered.sort(key=itemgetter(1))
    games = [name for name,price,percentage in games_filtered]
    return games

def by_dev_with_disc(master_D,discount_D,developer):
    ''' 
    gets the names of the games that have a given dev and have discount and 
sorts them by release year and then by price before discount
    master_D: dictionary of the data originated from the file (dict)
    discount_D: dictionary of the data originated from the discount file (dict)
    developer: developer to be considered when filtering (str)
    return: games filtered by dev and if they have discount (list of str)
    '''
    # filter by dev
    games_filtered = by_dev(master_D, developer)
    # filter by games that have discount
    games_filtered = [game for game in games_filtered if game in discount_D]
    # tuples list with name, price and release year
    games_filtered = [(game, master_D[game][4], \
                       datetime.strptime(master_D[game][0], "%d/%m/%Y").year) \
                       for game in games_filtered]
    # sort by release year
    games_filtered.sort(key=itemgetter(2))
    # sort by price
    games_filtered.sort(key=itemgetter(1))
    games = [name for name,price,year in games_filtered]
    return games
    
def main():
    fp_games = open_file('games')
    fp_discount = open_file('discount')
    
    master_D = read_file(fp_games)
    discount_D = read_discount(fp_discount)
    
    option = input(MENU)
    while option != '7':
        if option == '1':
            while True:
                try:
                    year = int(input('\nWhich year: '))
                    break
                except ValueError:
                    print("\nPlease enter a valid year")
            
            games = in_year(master_D, year)
            games = ', '.join(games)
            
            if games:
                print("\nGames released in {}:".format(year))
                print(games)
            else:
                print("\nNothing to print")
        
        elif option == '2':
            developer = input('\nWhich developer: ')
            games = by_dev(master_D, developer)
            games = ', '.join(games)
            
            if games:
                print("\nGames made by {}:".format(developer))
                print(games)
            else:
                print("\nNothing to print")
        
        elif option == '3':
            genre = input('\nWhich genre: ')
            games = by_genre(master_D, genre)
            games = ', '.join(games)
            
            if games:
                print("\nGames with {} genre:".format(genre))
                print(games)
            else:
                print("\nNothing to print")
                
        elif option == '4':
            developer = input('\nWhich developer: ')
            try:
                year = int(input('\nWhich year: '))
            except TypeError:
                print("\nPlease enter a valid year")
                
            games = by_dev_year(master_D, discount_D, developer, year)
            games = ', '.join(games)
            
            if games:
                print("\nGames made by {} and released in {}:"
                      .format(developer, year))
                print(games)
            else:
                print("\nNothing to print")
        
        elif option == '5':
            genre = input('\nWhich genre: ')
            
            games = by_genre_no_disc(master_D, discount_D, genre)
            games = ', '.join(games)
            
            if games:
                print("\nGames with {} genre and without a discount:"
                      .format(genre))
                print(games)
            else:
                print("\nNothing to print")
                
        elif option == '6':
            developer = input('\nWhich developer: ')
            games = by_dev_with_disc(master_D,discount_D,developer)
            games = ', '.join(games)
            
            if games:
                print("\nGames made by {} which offer discount:"
                      .format(developer))
                print(games)
            else:
                print("\nNothing to print")
                
        else:
            print("\nInvalid option")
        option = input(MENU)
    print("\nThank you.")
    

if __name__ == "__main__":
    main()