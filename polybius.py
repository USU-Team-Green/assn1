from pip._vendor.distlib.compat import raw_input
import pandas as pd


SQUARE = [
        ['e', '2', 'r', 'f', 'z', 'm'],
        ['y', 'h', '3', '0', 'b', '7'],
        ['o', 'q', 'a', 'n', 'u', 'k'],
        ['p', 'x', 'j', '4', 'v', 'w'],
        ['d', '1', '8', 'g', 'c', '6'],
        ['9', 'i', 's', '5', 't', 'l']
        ]

def polybius(numbers):
    # takes a string of numbers and runs them through the polybius square
    ret = ''
    for i in range(len(numbers))[::2]:
        ret = ret + SQUARE[int(numbers[i])][int(numbers[i + 1])]

    return ret

def get_one_time_pad(numbers):
    #takes the last 2 digits for the entry and
    # creates a one time pad key used for encryption
    numbers_length = len(numbers)
    one_time_pad = int(numbers[numbers_length -2] + numbers[numbers_length - 1])
    return(one_time_pad)


def dec_to_bin(x):
    #converts integers to decimal form
    start = '00'
    return start + str(bin(x)[2:])


def get_coordinates(trans_key):
    #takes the transposition key and gets the corrdinate value for each letter,
    # returned in an array
    rows = 6
    columns = 6

    coordinates = []

    for letter in trans_key:
        for i in range(rows):
            for j in range(columns):
                if letter == SQUARE[i][j]:
                    addition = str(i) + str(j)
                    coordinates.append(addition)
    return coordinates

def columnar_transposition_technique(key, message):
    #takes a key and a message, both strings.
    #returns the encrypted cipher

    #create a list of lists to organize the message into columns
    messagelist = [[] for i in key]
    for i in range(len(message)):
        messagelist[i%len(messagelist)].append(message[i])

    #put it into a dataframe for sorting and transposing
    transposed_matrix = pd.DataFrame(messagelist, index=[i for i in key])
    sorted_matrix = transposed_matrix.sort_index()

    #loop through the dataframe to add letters to cipher
    newcode = ''
    for i in range(len(sorted_matrix.index)):
        for j in sorted_matrix.iloc[i,:]:
            #don't use padding
            if pd.notna(j):
                newcode += j
    return newcode

def one_pad_crypto_technique(coordinates, one_time_key):

    one_time_binary = dec_to_bin(int(one_time_key))

    coordinates_in_binary = []

    for item in coordinates:
        new_item = dec_to_bin(int(item))
        coordinates_in_binary.append(new_item)

    #XOR Operation
    final_ciphertext = ''
    for item in coordinates_in_binary:
        new_binary = ''
        
        #keep binary at the same length
        item = '0' * (len(one_time_binary) - len(item)) + item
        one_time_binary = '0' * (len(item) - len(one_time_binary)) + one_time_binary

        for i in range(len(one_time_binary)):
            if item[i] != one_time_binary[i]:
                new_binary += '1'
            else:
                new_binary += '0'

        #make sure we have two digits for each character 
        temp_text = str(int(new_binary, 2))
        if len(temp_text) < 2:
            temp_text = '0' + temp_text
        final_ciphertext += temp_text


    return(final_ciphertext)



if __name__ == '__main__':

   comp_key = raw_input('Enter Composite Key: ')
   message = raw_input('Enter Secret Message: ')
   one_time = get_one_time_pad(comp_key)

   trans_key = polybius(comp_key[:-2])
   print('transposition key' , trans_key)
   print('one time pad key: ', one_time)

   cipher1 = columnar_transposition_technique(trans_key, message)
   coordinates = get_coordinates(cipher1)

   print('Cipher1: ', cipher1)
   print('Ciphertext: ', one_pad_crypto_technique(coordinates, one_time))
