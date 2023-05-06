"""
######################################################################
# Project 10
# Algorithm (main)
#     create new stock deck, tableau, and foundation
#     display rules
#     display menu options
#     display game table
#     loop until break
#         prompt and get option
#         while option is not valid, re-prompt
#         if option is D
#             deal to tableau
#         elif option is F
#             move top card from given column to foundation
#         elif option is T
#             move top card from given column to given target column
#         elif option is R
#             restart game, display restarting game message and display rules 
# and menu
#         elif option is H
#             display menu
#         elif option is Q
#             display quit message and break the loop
#      
#         if there are all and only aces on the tableau, display win message 
# and break loop
#
#         display game table
######################################################################
"""
import cards # required !!!

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():
    """ 
    set up stock, tableau, and foundation 
    return:
        stock: Deck of cards (Deck)
        tableau: list of lists of Cards
        Foundation: empty list of Cards
    """
    stock = cards.Deck()
    stock.shuffle()
    # deal one card to each column in the tableau
    tableau = [[stock.deal()] for n in range(4)]
    foundation = []
    return (stock, tableau, foundation)
    
def deal_to_tableau( tableau, stock ):
    """
    Add one card to each column of the tableau
    tableau: list of lists of Cards
    stock: Deck of cards (Deck)
    return: None
    """
    # for each column in the tableau
    for column in tableau:
        try:
            # deal from stock and add it to column
            column.append(stock.deal())
        except:
            break

def validate_move_to_foundation( tableau, from_col ):
    """
    check if move to foundation of top card from given column is valid and d
isplay error if it is not
    tableau: list of lists of Cards
    from_col: index of card to be moved
    return: whether move is valid (bool)
    """
    # if tableau column is empty, move is invalid
    if not tableau[from_col]:
        print("Error, empty column:", from_col)
        return False
    # get selected card
    selected_card = tableau[from_col][-1]
    # get list of cards on top of the tableau
    cards_top = [pile[-1] for pile in tableau if pile]
    # if card is an ace, move is invalid
    if selected_card.rank() == 1:
        print("\nError, cannot move {}.".format(selected_card))
        return False
    
    for card in cards_top:
        # if selected card suit and card from column suit are equal, and 
        #selected card rank is lower, move is valid
        if selected_card.suit() == card.suit() \
            and card.rank() > selected_card.rank():
            return True
        # if there is an ace in the tableau with the same suit as the selected 
        #card, move is valid
        elif card.rank() == 1 and selected_card.suit() == card.suit() \
            and card != selected_card:
            return True
    print("\nError, cannot move {}.".format(selected_card))
    return False

    
def move_to_foundation( tableau, foundation, from_col ):
    """
    removes card from tableau and adds it to foundation if the move is valid
    tableau: list of lists of Cards
    foundation: list of Cards
    from_col: column index of the Card to be moved
    return: None
    """
    # check if move to foundation is valid
    valid = validate_move_to_foundation( tableau, from_col )
    if valid:
        # get and remove card from tableau
        selected_card = tableau[from_col].pop()
        # add card to foundation
        foundation.append(selected_card)
        
        
def validate_move_within_tableau( tableau, from_col, to_col ):
    """
    check if there is an empty column in the tableau, display error message if 
there are no cards in selected column or if target column is not empty
    tableau: list of lists of Cards
    from_col: column index of the Card to be moved
    to_col: column index of the target column
    return: whether move is valid (bool)
    """
    # if there is a card on selected column and taget column is empty
    if tableau[from_col] and not tableau[to_col]:
        return True
    # if target column is not empty
    if tableau[to_col]:
        print("\nError, target column is not empty:", to_col+1)
    # if selected column is empty
    elif not tableau[from_col]:
        print("\nError, no card in column:", from_col+1)

    return False


def move_within_tableau( tableau, from_col, to_col ):
    """
    removes card from a column in the tableau and adds it to another column
    tableau: list of lists of Cards
    from_col: column index of the Card to be moved
    to_col: column index of the target column
    return: None
    """
    # check if move to another column is valid
    valid = validate_move_within_tableau( tableau, from_col, to_col ) 
    if valid:
        # get and remove card from given column
        selected_card = tableau[from_col].pop()
        # add card to target column
        tableau[to_col].append(selected_card)
        
    
def check_for_win( tableau, stock ):
    """
    checks if all Cards in the tableau are aces
    tableau: list of lists of Cards
    stock: Deck of cards (Deck)
    return: whether player won the game (bool)
    """
    # get tableau cards in a single list
    cards = [card for pile in tableau for card in pile]
    # if all items in tableau are aces, true, otherwise, false
    only_aces = all(card.rank() == 1 for card in cards)
    # if stock is empty and tableau only have aces
    if stock.is_empty() and only_aces:
        return True
    return False
    

def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():
    """
    prompts for options and checks if they are valid
    return: option and selected and target columns if applicable (list)
    """
    valid_options = ['d','f','t','r','h','q']
    # prompt user for option
    answer = input("\nInput an option (DFTRHQ): ")
    answer.strip()
    option_list = answer.split()
    # uppercase option letter and convert numbers strings to integers
    option_list = [int(item)-1 if item.isdigit() else item.upper() \
                   for item in option_list]
    for item in option_list:
        if type(item) == int:
            # if column's indexes are not within range
            if item < 0 or item > 3:
                print("\nError in option:", answer)
                return []
    # get option letter
    option = option_list[0]
    # check if user entered an valid option, print error if not
    if option.lower() in valid_options:
        if option.lower() == 'f' and len(option_list) == 2:
            if type(option_list[1]) == int:
                return option_list
            else:
                print("\nError in option:", answer)
                return []
        elif option.lower() == 't' and len(option_list) == 3:
            if type(option_list[1]) == int and type(option_list[2]) == int:
                return option_list
            else:
                print("\nError in option:", answer)
                return []
        elif len(option_list) > 1 or option.lower() == 'f'\
            or option.lower() == 't':
            print("\nError in option:", answer)
            return []
    else:
        print("\nError in option:", answer)
        return []
    return option_list


def main():
    stock, tableau, foundation = init_game()
    print(RULES)
    print(MENU)
    display(stock, tableau, foundation)
    while True:
        option = get_option()
        while not option:
            option = get_option()
        if option[0] == 'D':
            deal_to_tableau(tableau, stock)
            
        elif option[0] == 'F':
            from_col = option[1]
            move_to_foundation(tableau, foundation, from_col)
            
        elif option[0] == 'T':
            from_col = option[1]
            to_col = option[2]
            move_within_tableau(tableau, from_col, to_col)
            
        elif option[0] == 'R':
            stock, tableau, foundation = init_game()
            print("\n=========== Restarting: new game ============")
            print(RULES)
            print(MENU)
        elif option[0] == 'H':
            print(MENU)
        
        elif option[0] == 'Q':
            print("\nYou have chosen to quit.")
            break
        
        if check_for_win( tableau, stock ):
            print("\nYou won!")
            break
        display(stock, tableau, foundation)
        
if __name__ == '__main__':
     main()
