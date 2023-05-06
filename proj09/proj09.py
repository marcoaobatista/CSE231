"""
############################################################
# Project 09
# Algorithm (main)
#   prompt for file name and get file pointer
#   read file and get set of words in it
#   get dictionary of tuples of letter and its index in the words in value
#   prompt for prefix to be analized
#   while prefix/ answer is not #
#       get completions
#       if completions is not empty
#           sort it, join it and display it
#       otherwise print no completions message
#       reprompt for prefix
#   display goodbye message
############################################################
"""

import string

def open_file():
    """ 
    prompts for file name until it is valid and return its file pointer
    return: file pointer (_io.TextIOWrapper)
    """
    while True:
        try:
            file_name = input("\nInput a file name: ")
            fp = open(file_name, encoding='UTF-8')
            break
        except FileNotFoundError:
            print("\n[Error]: no such file") 
    return fp


def read_file(fp):
    """ 
    reads the file to get the words in it
    fp: txt file pointer (_io.TextIOWrapper)
    return: set of words in file (set)
    """
    words = set()
    for line in fp:
        # split the line between spaces and remove any punctuation
        words_list = [word.strip(string.punctuation).lower() 
                      for word in line.split()]
        for word in words_list:
            # add to set if it has more than one letter and it's all letters
            if len(word) != 1 and word.isalpha() == True:
                words.add(word)
    return words


def fill_completions(words):
    """ 
    creates a dictionary with sets of words as values and tuples as keys in the
format (i,a) i for index and a the letter at index
    words: set of words originated from a file (set)
    return: dictionary in the format {(i,n): set(words)}
    """
    dictt = {}
    for word in words:
        for i, ch in enumerate(word):
            # if key is in the dictionary, add word to value set
            if (i,ch) in dictt:
                dictt[(i,ch)].add(word)
            # otherwise create key value pair
            else:
                dictt[(i,ch)] = {word}
    return dictt


def find_completions(prefix,word_dic):
    """ 
    finds words in the input dictionary that have the same prefix as the input
    prefix: prefix to be considered (string)
    word_dic: dictionary in the format {(i,n): set(words)}
    return: valid completions (set)
    """
    completions = set()
    # handle empty string
    if not prefix:
        return completions
    # add all words from dict to completions set
    for s in word_dic.values():
        completions.update(s)
    
    # get words with the same input prefix
    for i, ch in enumerate(prefix):
        if (i, ch) in word_dic:
            completions = completions & word_dic[(i, ch)]
        else:
            return set()
        
    return completions
    
    
def main():       
    fp = open_file()
    words = read_file(fp)
    word_dic = fill_completions(words)
    
    prefix = input("\nEnter a prefix (# to quit): ")
    while prefix != '#':
        completions = find_completions(prefix,word_dic)
        if completions:
            completions = sorted(list(completions))
            completions = ', '.join(completions)
            print("\nThe words that completes {} are: {}"
                  .format(prefix, completions))
        else:
            print("\nThere are no completions.")
            
        prefix = input("\nEnter a prefix (# to quit): ")
    print("\nBye")
    
    
if __name__ == '__main__':
    main()