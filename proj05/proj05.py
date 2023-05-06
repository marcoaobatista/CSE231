''' 
###########################################################
# Project #5
# Algorithm    
#     display banner
#     display and prompt user for options
#     until user does not enter 3 when prompt for option
#         if user entered 1 when prompted
#             get file
#             get episodes, scores, names, and average variables with 
#                 read_file() function
#             display the highest score and title(s) with that said score
#             display the highest number of episodes and title(s)
#             display the lowest score and title(s) with that score
#             close connection to file
#         if user entered 2 when prompted
#             get file
#             prompt for anime name to search for
#             get the number of anime matches and their names with 
#                search_anime() function
#             if there were no matches
#                 display No Animes Found message
#             otherwise
#                 display number matches and their names
#             close connection to file
#         if user entered unknown option
#             display invalid option message
#             display and re-prompt for options
#         prompt for option
#     display goodbye message
###########################################################
'''

def open_file():
    '''
    Repeatedly prompts user for file name until it is a valid name
    returns: file (io.TextIOWrapper)
    '''
    fp = ''
    while True:
        try:
            fp_name = input("\nEnter filename: ")
            fp = open(fp_name, "r", encoding="utf-8")
            break
        except FileNotFoundError:
            print("\nFile not found!")
    return fp


def find_max(value, name, max_value, max_name):
    '''
    finds the title(s) with the highest input value and formats it if necessary
    value: value of the title to be compared (float)
    name: title to be compared (string)
    max_value: current highest value (float)
    max_name: current title with the highest value (string)
    returns: max_value, max_name (float, string)
    '''
    if value < max_value:
        return max_value, max_name
    elif value > max_value:
        return value, "\n\t{}".format(name)
    else:
        return max_value, "{}\n\t{}".format(max_name, name)
    
    
def find_min(value, name, min_value, min_name):
    '''
    finds the title(s) with the lowest input value and formats it if necessary
    value: value of the title to be compared (float)
    name: title to be compared (string)
    min_value: current lowest value (float)
    min_name: current title with the lowest value (string)
    returns: min_value, min_name (float, string)
    '''
    if value > min_value:
        return min_value, min_name
    elif value < min_value:
        return value, "\n\t{}".format(name)
    else:
        return min_value, "{}\n\t{}".format(min_name, name)
    

def read_file(data_fp):
    '''
    Go through the file and get the titles with most and least scores, 
        episodes, their names and calculates the average score from all titles 
        in the file, always making sure that the inputs are valid
    data_fp: file (io.TextIOWrapper)
    returns:
        max_score: highest score in the file (float)
        max_score_name: title with the highest score in the file (string)
        max_episodes: highest number of episodes in the file (float)
        max_episode_name: title with the most number of episodes in the 
            file (string)
        min_score: lowest score in the file (float)
        min_score_name: title with the lowest score in the file (string)
        avg_score: average of all scores in the file (float)
    '''
    
    max_score = 0.0
    max_score_name = ''
    max_episodes = 0
    max_episode_name = ''
    min_score = 999.0
    min_score_name = ''
    avg_score = 0.0
    score_sum = 0.0
    score_count = 0
    
    for line in data_fp:
        # strip method to remove starting and ending whitespace
        title = line[0:100].strip()
        score = line[100:105].strip()
        episodes = line[105:110].strip()
        
        try:
            score = float(score)
            max_score, max_score_name = \
                find_max(score, title, max_score, max_score_name)
            min_score, min_score_name = \
                find_min(score, title, min_score, min_score_name)
            
            score_sum += score
            score_count += 1
        except:
            pass
        
        try:
            episodes = float(episodes)
            max_episodes, max_episode_name = find_max(episodes, title, \
                max_episodes, max_episode_name)
        except:
            pass
    if min_score > 10:
        min_score = 0.0
    avg_score = round(score_sum/score_count,2)
        
    return max_score, max_score_name, max_episodes, max_episode_name, \
        min_score, min_score_name, avg_score


def search_anime(data_fp, search_str):
    '''
    Searches for animes titles that have the search string in them and format
        the results to include the release season
    data_fp: file (io.TextIOWrapper)
    search_str: anime to be searched (string)
    returns:
        count: number of matches (int)
        out_str: title and release season of search matches
    '''
    out_str = ''
    count = 0
    for line in data_fp:
        # line = line.replace('\n','')
        title = line[0:100].strip()
        release_season = line[110:122].strip()
        if search_str.lower() in title.lower():
            entry = "\n\t{:100}{:12}".format(title, release_season)
            out_str += entry
            count += 1
    return count, out_str


def main():
    BANNER = "\nAnime-Planet.com Records" \
         "\nAnime data gathered in 2022"

    MENU ="Options" + \
          "\n\t1) Get max/min stats" + \
          "\n\t2) Search for an anime" + \
          "\n\t3) Stop the program!" + \
          "\n\tEnter option: "
    
    print(BANNER)
    
    answer = input(MENU)
    
    while answer != '3':
        if answer == '1':
            file = open_file()
            max_score, max_score_name, max_episodes, max_episode_name,\
                min_score, min_score_name, avg_score = read_file(file)
            
            print("\n\nAnime with the highest score of {:.2f}:"
                  .format(max_score))
            print(max_score_name)
            print("\n\nAnime with the highest episode count of {:,.0f}:"
                  .format(max_episodes))
            print(max_episode_name)
            print("\n\nAnime with the lowest score of {:.2f}:"
                  .format(min_score))
            print(min_score_name)
            print("\n\nAverage score for animes in file is {:.2f}"
                  .format(avg_score))
            
            file.close()
        elif answer == '2':
            file = open_file()
            search_str = input("\nEnter anime name: ")
            
            count, out_str = search_anime(file, search_str)
            if count == 0:
                print("\nNo anime with '{}' was found!".format(search_str))
            else:
                print("\nThere are {} anime titles with '{}'"
                      .format(count, search_str))
                print(out_str)
            file.close()
        
        else:
            print("\nInvalid menu option!!! Please try again!")
        answer = input(MENU)
    
    print("\nThank you using this program!")
    