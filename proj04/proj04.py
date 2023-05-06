'''
###########################################################
#	Project #4
#
#	Algorithm (main)
#		display welcome message and menu options
#		prompt for option
#		while user does not input ‘x’ when prompted
#			if user input ‘a’ when prompted
#				prompt for decimal number
#				check if it is a valid input. Re-prompt if not
#				prompt for new base
#				check if it is a valid input. Re-prompt if not
#				display  number in new base
#			if user input ‘b’ when prompted
#				prompt for number in base b
#				prompt for base
#				check if base is a valid input. Re-prompt if not
#				display number in decimal base
#			if user input ‘c’ when prompted
#				prompt user for base 1
#				check if it is a valid input. Re-prompt if not
#				prompt for base 2
#				check if it is a valid input. Re-prompt if not
#				prompt for number in base 1
#				display number in base 2
#			if user input ‘e’
#				prompt for image in binary
#				prompt for integer number of bits in each pixel
#				prompt for text to be embedded in to image
#				display error message if image is not big enough
#				display original image and the encoded image
#			if user input ‘d’
#				prompt for encoded image
#				prompt for number of bits in each color
#				decode image
#				display the text encoded in image
#			if user input ‘m’
#				display menu
#			if user input unrecognized input
#				display error message and display menu
#			Re-prompt for option
#		print goodbye message
###########################################################
'''

import math

MENU = '''\nPlease choose one of the options below:
             A. Convert a decimal number to another base system         
             B. Convert decimal number from another base.
             C. Convert from one representation system to another.
             E. Encode an image with a text.
             D. Decode an image.
             M. Display the menu of options.
             X. Exit from the program.'''
    
def numtobase( N, B ):
    '''
    Converts the input decimal number to another input base with algorithm
    N: decimal number (int)
    B: base number (int)
    Returns: the number N in base B
    '''
    if N == 0:
        return ''
    
    converted_num = ''
    converted_num = str(N%B) + converted_num
    quotient = N//B
    converted_num = str(quotient % B) + converted_num
    
    while quotient != 0:
        quotient = quotient//B
        converted_num = str(quotient % B) + converted_num
    
    converted_num = '{:0>8s}'.format(converted_num)
    return converted_num


def basetonum( S, B ):
    '''
    Converts the input number S in base B to decimal
    S: number in base B to be converted (string)
    B: base of the number to be converted (int)
    return: S in decimal number (int)
    '''
    num = 0
    for index, ch in enumerate(S[::-1]):
        ch = int(ch)
        column_num = ch * (B**index)
        num += column_num
    return num


def basetobase(B1,B2,s_in_B1):
    '''
    Converts one number in base B1 to base B2
    B1: Base of input number (int)
    B2: new base of number (int)
    s_in_B1: number in base B1 (string)
    return: s_in_B1 in base B2 (string)
    '''
    new_base = numtobase(basetonum(s_in_B1, B1),B2)
    width = str(math.ceil(len(new_base)/8)*8)
    placeholder = '{:0>'+width+'s}'
    return placeholder.format(new_base)


 
def encode_image(image,text,N):
    '''
    Takes an image and encodes an input text into it
    image: input image in binary with N bits per pixel (string)
    text: message to be encoded into the image (string)
    N: number of bits per pixel (int)
    return: image with binary text encoded in the LSB of each pixel (string)
    '''
    if image == '':
        return ''
    if text == '':
        return image
    
    text_binary = ''
    #convert text to binary
    for ch in text:
        text_binary += numtobase(ord(ch), 2)
    
    N = int(N)
    # check if image can hold text
    if len(image)/N < len(text_binary):
        return None
    
    encoded_image = ''
    counter = 0
    # insert binary text in least significant bit positions
    for index, ch in enumerate(image):
        if (index + 1) % N == 0 and counter < len(text_binary) and index != 0:
            encoded_image += text_binary[counter]
            counter += 1
        else:
            encoded_image += ch
    return encoded_image



def decode_image(stego,N):
    '''
    Decodes the text encoded into the image
    stego: encoded image (string)
    N: number of bits per pixel (int)
    return: text encoded into the image (string)
    '''
    decoded_image = ''
    N = int(N)
    # add every LSB character from the image to decoded image string
    for i in range(N-1,len(stego),N):
        decoded_image += stego[i]
    
    # remove excess characters
    decoded_image = decoded_image[:(len(decoded_image)//8)*8]
    
    converted = ''
    # group by 8 characters, convert to decimal, then alphabetic characters
    for i in range(0,len(decoded_image)//8):
        char_binary = decoded_image[i*8:(i+1)*8]
        char_decimal = basetonum(char_binary, 2)
        char = chr(char_decimal)
        converted += char
    return converted
    


def base_within_range(base):
    '''
    Checks if input argument is a digit and within the range 2 to 10 inclusive
    base: (string)
    return: True only if base is a digit and within the range 2 to 10 inclusive
    '''
    if base.isdigit():
        if int(base) in range(2,11):
            return True
    return False



def main():
    BANNER = '''
               A long time ago in a galaxy far, far away...   
              A terrible civil war burns throughout the galaxy.      
  ~~ Your mission: Tatooine planet is under attack from stormtroopers,
                   and there is only one line of defense remaining        
                   It is up to you to stop the invasion and save the planet~~
    '''

    print(BANNER)
    print(MENU)
    
    answer = input("\n\tEnter option: ")
    while answer.lower() != 'x':
        if answer.lower() == 'a':

            N = input("\n\tEnter N: ")
            while N.isdigit() == False:
                print("\n\tError: {} was not a valid non-negative integer." \
                      .format(N))
                N = input("\n\tEnter N: ")
            N = int(N)

            B = input("\n\tEnter Base: ")
            while base_within_range(B) == False:
                print("\n\tError: {} was not a valid integer between 2 and 10 \
inclusive.".format(B))
                B = input("\n\tEnter Base: ")
            B = int(B)
            
            print("\n\t {} in base {}: {}".format(N, B, numtobase(N, B)))
        
        
        elif answer.lower() == 'b':
            S = input("\n\tEnter string number S: ")
            
            B = input("\n\tEnter Base: ")
            while base_within_range(B) == False:
                print("\n\tError: {} was not a valid integer between 2 and 10 \
inclusive.".format(B))
                B = input("\n\tEnter Base: ")
            B = int(B)
            
            print("\n\t {} in base {}: {}".format(S, B, basetonum(S, B)))
            
            
        elif answer.lower() == 'c':
            B1 = input("\n\tEnter base B1: ")
            while base_within_range(B1) == False:
                print("\n\tError: {} was not a valid integer between 2 and 10 \
inclusive.".format(B1))
                B1 = input("\n\tEnter base B1: ")
            B1 = int(B1)
            
            
            B2 = input("\n\tEnter base B2: ")
            while base_within_range(B2) == False:
                print("\n\tError: {} was not a valid integer between 2 and 10 \
inclusive.".format(B2))
                B2 = input("\n\tEnter base B2: ")
            B2 = int(B2)
            
            S_B1 = input("\n\tEnter string number: ")
            
            print("\n\t {} in base {} is {} in base {}..."\
                  .format(S_B1, B1, basetobase(B1, B2, S_B1), B2))
            
            
        elif answer.lower() == 'e':
            image = input("\n\tEnter a binary string of an image: ")
            N = input("\n\tEnter number of bits used for pixels: ")
            text = input("\n\tEnter a text to hide in the image: ")
            encoded_image = encode_image(image, text, N)
            
            if encoded_image == None or encoded_image == '':
                print("\n\tImage not big enough to hold all the text to \
steganography")
            else:
                print("\n\t Original image: {}".format(image))
                print("\n\t Encoded image: {}".format(encoded_image))
            

        elif answer.lower() == 'd':
            encoded_image = input("\n\tEnter an encoded string of an image: ")
            N = input("\n\tEnter number of bits used for pixels: ")
            decoded_image = decode_image(encoded_image, N)
            print("\n\t Original text: {}".format(decoded_image))
        elif answer.lower() == 'm':
            print(MENU)
        else:
            print("\nError:  unrecognized option [{}]".format(answer.upper()))
            print(MENU)
        answer = input("\n\tEnter option: ")
    print('\nMay the force be with you.')

main()
    