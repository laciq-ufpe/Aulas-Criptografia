import string
from collections import Counter
import argparse
from utils import read_file
import os
import json
import random
import matplotlib.pyplot as plt

# frequency order for English and Brazilian Portuguese
# https://en.wikipedia.org/wiki/Letter_frequency#Relative_frequencies_of_letters_in_other_languages
english_frequency_order = 'etaoinshrdlcumwfgypbvkjxqz'
portuguese_frequency_order = 'aeosrinmdutclpvghqbzfjxkwy'

def get_args():
    # Argument parser
    parser = argparse.ArgumentParser(description="Cryptanalysis Tool")
    parser.add_argument("-i", "--input", help="Input text (file path or direct)", default= "Example/cipher_substitution.txt")
    parser.add_argument("-o", "--output", help="Output file to save the plain text", default= "decoded.txt")
    parser.add_argument("-l", "--language", choices= ['en', 'pt'], default= 'pt')
    parser.add_argument("-v", "--verbose", action="store_true",default= False)
    parser.add_argument("-s", "--substitution_map", help="file where part of the substitution map is", default="Example/substitution_map.json")
    args = parser.parse_args()
    
    return args

# Function to plot the letter frequency distribution of the cipher text
def plot_letter_distribution(cipher_text):
    """
    Plot the letter frequency distribution of the cipher text.
    """
    # Clean text: remove non-alphabetic characters and convert to lowercase
    cleaned_text = ''.join(filter(str.isalpha, cipher_text.lower()))

    # Count the frequency of each letter in the cipher text
    letter_count = Counter(cleaned_text)
    
    # Sort the letter count by alphabet order
    letters = sorted(letter_count.keys())
    frequencies = [letter_count[letter] for letter in letters]

    # Plotting the distribution
    plt.figure(figsize=(10, 6))
    plt.bar(letters, frequencies, color='skyblue')
    plt.title('Letter Frequency Distribution in Cipher Text')
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


# frequency order for English and Brazilian Portuguese
english_frequency_order = 'etaoinshrdlcumwfgypbvkjxqz'
portuguese_frequency_order = 'aeosrinmdutclpvghqbzfjxkwy'

def frequency_analysis(cipher_text, language='pt',substitution_map = {}):
    print(substitution_map)
    """match the letters to the letter frequency in the chosen language (English or Brazilian Portuguese)"""
    # select the appropriate frequency order based on language
    if language == 'pt':
        target_frequency_order = portuguese_frequency_order
    else:
        target_frequency_order = english_frequency_order
    
    # clean text: remove non-alphabetic characters and convert to lowercase
    cleaned_text = ''.join(filter(str.isalpha, cipher_text.lower()))

    for cipher_letter, true_letter in substitution_map.items():
        target_frequency_order = target_frequency_order.replace(true_letter,'')
        cleaned_text =  cleaned_text.replace(cipher_letter, '')

    # count the frequency of each letter in the cipher text
    letter_count = Counter(cleaned_text)
    
    # get the letters in the cipher text, sorted by frequency (most to least)
    cipher_frequency_order = ''.join([item[0] for item in letter_count.most_common()])
    
    # create a substitution map from cipher letters to guessed letters (based on frequency)
    for i, letter in enumerate(cipher_frequency_order):
        if i < len(target_frequency_order):
            substitution_map[letter] = target_frequency_order[i]
        else:
            substitution_map[letter] = letter  # default to the same letter if we run out of guesses

    return substitution_map, target_frequency_order

# function to apply a small permutation to the target frequency order (adjacent swaps)
def permute_frequency_order(order):
    """
    Apply a small permutation by swapping two adjacent letters in the target frequency order.
    """
    order_list = list(order)
    
    # Choose a random index to swap with its next neighbor
    idx = random.randint(0, len(order_list) - 2)  # Ensure there's a next letter to swap with
    order_list[idx], order_list[idx + 1] = order_list[idx + 1], order_list[idx]
    
    return ''.join(order_list)

# Function to decipher the text using the substitution map
def apply_frequency_decoding(cipher_text, substitution_map):
    """
    Decipher the cipher text using the given substitution map.
    """
    deciphered_text = ""
    for char in cipher_text:
        if char.isalpha():
            if char.islower():
                deciphered_text += substitution_map.get(char, char)
            else:
                deciphered_text += substitution_map.get(char.lower(), char).upper()
        else:
            deciphered_text += char  # Non-alphabet characters remain unchanged
    return deciphered_text



if __name__ == "__main__":
    args = get_args()
    # Sample cipher text (from Caesar or Substitution Cipher)
    if os.path.exists(args.input):
        cipher_text = read_file(args.input)
    else:
        cipher_text = args.input
    
    if os.path.exists(args.substitution_map):
        with open(args.substitution_map) as sub_file:
            substitution_map = json.load(sub_file)
    else:
        substitution_map = {}

    # Perform frequency analysis and get the original substitution map and target frequency order
    substitution_map, target_frequency_order = frequency_analysis(cipher_text, language=args.language, substitution_map=substitution_map)

    # Generate and apply permutations to create 5 candidates
    for i in range(1):
        # a primeira ocorre sem substituicoes
        if i == 0:
            permuted_substitution_map = substitution_map
        else:
            # Create a new substitution map with a small permutation in the target frequency order
            permuted_order = permute_frequency_order(target_frequency_order)
            permuted_substitution_map = {}
            
            # Build the new substitution map based on the permuted order
            for j, letter in enumerate(permuted_order):
                if j < len(substitution_map):
                    cipher_letter = list(substitution_map.keys())[j]
                    permuted_substitution_map[cipher_letter] = letter
        
        # Decipher the text using the permuted substitution map
        deciphered_text = apply_frequency_decoding(cipher_text, permuted_substitution_map)

        # Output the result for this candidate
        print("---"*30)
        print(f"\nCandidate {i+1}:")
        print(deciphered_text)

    
