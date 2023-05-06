'''
###########################################################
# Project #6
# Algorithm (main)
# Get file pointer
# Get relevant file content in a list
# Prompt for option
# While user does not enter 4 when prompted for option
# 	if option selected is 1 (find a book with a title)
# 		prompt for title
# 		get books based on input
# 		display matches
# 	if option selected is 2 (filter by criteria)
# 		while criteria index is not valid
# 			prompt for criteria index
# 		prompt for value/ search parameter
# 		if criterion is rating
# 			try to convert it to float, if not valid, re-prompt
# 		if criterion is number or pages
# 			try to convert it to int, if not possible, re-prompt
# 		get filtered books based on input criterion
# 		sort books based on author names
# 		display the first 30 books from the list
# 	if option selected is 3 (recommend a book)
# 		prompt for category
# 		prompt for rating, try to convert it to float, re-prompt if invalid
# 		prompt for page number, try to convert it to int, re-prompt if invalid
# 		prompt for a-z sorting
# 			if answer is 1, set it to True, False otherwise
# 		prompt for keywords and split it where there are whitespaces
# 		get recommended books based on input
# 		display recommended books
# 	prompt for option 
###########################################################
'''
import csv
from operator import itemgetter
import copy

TITLE = 1
CATEGORY = 3
YEAR = 5
RATING = 6
PAGES = 7

MENU = "\nWelcome to the Book Recommendation Engine\n\
        Choose one of below options:\n\
        1. Find a book with a title\n\
        2. Filter books by a certain criteria\n\
        3. Recommend a book \n\
        4. Quit the program\n\
        Enter option: "

CRITERIA_INPUT = "\nChoose the following criteria\n\
                 (3) Category\n\
                 (5) Year Published\n\
                 (6) Average Rating (or higher) \n\
                 (7) Page Number (within 50 pages) \n\
                 Enter criteria number: "

TITLE_FORMAT = "{:15s} {:35s} {:35s} {:6s} {:8s} {:15s} {:15s}"
TABLE_FORMAT = "{:15s} {:35s} {:35s} {:6s} {:<8.2f} {:<15d} {:<15d}"

def open_file():
    """
    prompts for file name and returns file pointer
    return: file pointer (_io.TextIOWrapper)
    """
    while True:
        try:
            file_name = input("Enter file name: ")
            fp = open(file_name, "r", encoding="utf-8")
            break
        except FileNotFoundError:
            print("\nError opening file. Please try again.")
    return fp

def read_file(fp):
    """
    Goes through the content of the input file and returns the relevant info
    fp: file pointer (_io.TextIOWrapper)
    return: books data (list of tuples)
    """
    reader = csv.reader(fp)
    books = [] # list of tuples
    next(reader) # skip the first line
    for line in reader:
        try:
            isbn13 = line[0]
            title = line[2]
            authors = line[4]
            categories = line[5].lower().split(',')
            description = line[7]
            year = line[8]
            rating = float(line[9])
            num_pages = int(line[10])
            rating_count = int(line[11])
           
            t = isbn13, title, authors, categories, description, year, rating,\
                num_pages, rating_count
        except ValueError:
            continue
        books.append(t)
    return books

def get_books_by_criterion(list_of_tuples, criterion, value):
    """
    filter books based on criterion and input value
    list_of_tuples: books data (list of tuples)
    criterion: search criterion (int)
    value: search parameter (string or float or int)
    return: matched books data (tuple or list of tuples)
    """
    output = []
    for book_data in list_of_tuples:
        
        if criterion == TITLE:
            title = book_data[TITLE]
            if title.lower() == value.lower():
                return book_data
            
        elif criterion == CATEGORY:
            for category in book_data[CATEGORY]:
                if category == value.lower():
                    output.append(book_data)
                    
        elif criterion == YEAR:
            year = book_data[YEAR]
            if year == value:
                output.append(book_data)
        
        elif criterion == RATING:
            rating = book_data[RATING]
            if rating >= value:
                output.append(book_data)
                
        elif criterion == PAGES:
            pages = book_data[PAGES]
            if pages in range(value-50,value+51): # +/- 50 pages margin 
                output.append(book_data)
    return output
                
                    

def get_books_by_criteria(list_of_tuples, category, rating, page_number):
    """
    return filtered list of books based on input arguments
    list_of_tuples: books data (list of tuples)
    category: search parameter, book(s) category (list of string)
    rating: search parameter, mininum book(s) rating (float)
    page_number: search parameter, number of pages (int)
    return: filtered list of books (list of tuples)
    """
    filtered1 = get_books_by_criterion(list_of_tuples, PAGES, page_number)
    filtered2 = get_books_by_criterion(filtered1, RATING, rating)
    filtered3 = get_books_by_criterion(filtered2, CATEGORY, category)
    
    return filtered3
    
    
def get_books_by_keyword(list_of_tuples, keywords):
    """
    return books with keywords in their description
    list_of_tuples: books data (list of tuples)
    keywords: search parameter, keywords (list of string)
    return: books with one of the keywords in the description (list of tuples)
    """
    output = []
    for book_data in list_of_tuples:
        description = book_data[4]
        for keyword in keywords:
            if keyword.lower() in description.lower():
                output.append(book_data)
                break
    return output

def sort_authors(list_of_tuples, a_z = True):
    """
    returns the input list sorted by author in alphabetical order
    a_z: sorting order, acending or descending (bool)
    list_of_tuples: books data (list of tuples)
    return: list of books sorted by author in alphabetical order 
        (list of tuples)
    """
    books = copy.deepcopy(list_of_tuples)
    books.sort(key=itemgetter(2), reverse = not a_z) # sort based on index 2
    return books

def recommend_books(list_of_tuples, keywords, category, rating, page_number,\
                    a_z):
    """
    filter and sorts books based on input
    list_of_tuples: books data (list of tuples)
    keywords: search parameter, keywords (list of string)
    category: search parameter, book(s) category (list of string)
    rating: search parameter, mininum book(s) rating (float)
    page_number: search parameter, number of pages (int)
    a_z: sorting order, acending or descending (bool)
    return: list of filtered books (list of tuples)
    """
    recommend_books = get_books_by_criteria(list_of_tuples, category, rating,\
                                            page_number)
    recommend_books = get_books_by_keyword(recommend_books, keywords)
    recommend_books = sort_authors(recommend_books, a_z)
    return recommend_books

def display_books(list_of_tuples):
    """
    prints header and books data from input
    list_of_tuples: books data (list of tuples)
    return: None
    """
    print("\nBook Details:")
    if not list_of_tuples: # if list is empty
        print("Nothing to print.")
    else:
        print(TITLE_FORMAT.format('ISBN-13', 'Title', 'Authors', 'Year',\
                                  'Rating', 'Number Pages', 'Number Ratings'))
        for book_data in list_of_tuples:
            title = book_data[TITLE]
            authors = book_data[2]
            # if title or authors has more than 35 characters do not print it
            if len(title) > 35 or len(authors) > 35:
                continue
            isbn_13 = str(int(float(book_data[0])))
            title = book_data[1]
            authors = book_data[2]
            year = book_data[5]
            rating = book_data[6]
            pages = book_data[7]
            rating_count = book_data[8]
            print(TABLE_FORMAT.format(isbn_13, title, authors, year, rating,\
                                      pages, rating_count))

def get_option():
    """
    prompts for a number from 1-4
    return: None or option (int)
    """
    option = input(MENU)
    if option.isdigit():
        option = int(option)
        if option in range(1,5):
            return option
    print("\nInvalid option")
    return None

def main():
    fp = open_file()
    books = read_file(fp)
    option = get_option()
    while option != 4:
        if option == 1:
            title = input("\nInput a book title: ")
            book = [get_books_by_criterion(books, TITLE, title)]
            display_books(book)
        elif option == 2:
            criterion = input(CRITERIA_INPUT)
            while criterion not in ['3', '5', '6', '7']:
                print("\nInvalid input")
                criterion = input(CRITERIA_INPUT)
            criterion = int(criterion)    
            
            value = input("\nEnter value: ")
            if criterion == RATING:
                while True:
                    try:
                        value = float(value)
                        break
                    except:
                        print("\nInvalid input")
                        value = input("\nEnter value: ")
            elif criterion == PAGES:
                while True:
                    try:
                        value = int(value)
                        break
                    except:
                        print("\nInvalid input")
                        value = input("\nEnter value: ")
            
            filtered_books = get_books_by_criterion(books, criterion, value)
            sorted_books = sort_authors(filtered_books)
            display_books(sorted_books[:30])
                
        elif option == 3:
            category = input("\nEnter the desired category: ")
            while True:
                try:
                    rating = float(input("\nEnter the desired rating: "))
                    break
                except:
                    pass
            while True:
                try:
                    page_number = int(input\
                                      ("\nEnter the desired page number: "))
                    break
                except:
                    pass
            a_z = input("\nEnter 1 for A-Z sorting, and 2 for Z-A sorting: ")
            a_z = True if a_z == '1' else False
            
            keywords = input("\nEnter keywords (space separated): ").split()
            
            recommended_books = recommend_books(books, keywords, category,\
                                                rating, page_number, a_z)
            display_books(recommended_books)
            
        option = get_option()

# DO NOT CHANGE THESE TWO LINES
# These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.
if __name__ == "__main__":
    main()
    
main()
