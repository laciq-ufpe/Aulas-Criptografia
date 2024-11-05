from utils import read_plain_apply_cipher_save
import argparse


def get_args():
    # Argument parser
    parser = argparse.ArgumentParser(description="Cipher Tool")
    parser.add_argument("-i", "--input", help="Input text (file path or direct)", default= "Example/carta-general.txt")
    parser.add_argument("-f", "--file", help="Flag to specify if input is from file", action="store_true", default= False)
    parser.add_argument("-o", "--output", help="Output file to save the cipher text", default= "cipher_substitution.txt")
    parser.add_argument("-k", "--key", help="should be a 26-character string where each letter represents the substitution.", type=str, default= 'zebrascdfghijklmnopqtuvwxy')
    parser.add_argument("-v", "--verbose", action="store_true",default= False)
    args = parser.parse_args()
    
    return args

def substitution_cipher(text, key):
    """ 'key' should be a 26-character string where each letter represents the substitution."""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    cipher_text = ""

    # create a mapping between each letter of the alphabet and the key
    key = key.lower()
    substitution_map = {alphabet[i]: key[i] for i in range(26)}

    for char in text:
        if char.isalpha():
            # preserve the case of the letter
            if char.islower():
                cipher_text += substitution_map[char]
            else:
                cipher_text += substitution_map[char.lower()].upper()
        else:
            cipher_text += char  # keep non-alphabet characters unchanged

    return cipher_text

def substitution_decipher():
    NotImplemented

    
if __name__ == "__main__":
    args = get_args()
    read_plain_apply_cipher_save(args, cipher_algorithm= substitution_cipher, cipher_args=(args.key,))
