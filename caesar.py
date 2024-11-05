from utils import read_plain_apply_cipher_save
import argparse


def get_args(): 
    # Argument parser
    parser = argparse.ArgumentParser(description="Cipher Tool")
    parser.add_argument("-i", "--input", help="Input text (file path or direct)", default= "Example/carta-general.txt")
    parser.add_argument("-f", "--file", help="Flag to specify if input is from file", action="store_true", default= True)
    parser.add_argument("-o", "--output", help="Output file to save the cipher text", default= "cipher_caesar.txt")
    parser.add_argument("-k", "--key", help="Shift value for Caesar Cipher", type=int, default= 10)
    parser.add_argument("-v", "--verbose", action="store_true",default= False)
    args = parser.parse_args()
    
    return args

# Function to apply Caesar Cipher
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_decipher(cipher_text, shift):
    NotImplemented

if __name__ == "__main__":
    args = get_args()
    read_plain_apply_cipher_save(args, cipher_algorithm= caesar_cipher, cipher_args=(args.key,))
