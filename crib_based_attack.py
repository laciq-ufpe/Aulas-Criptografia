import string
from collections import Counter
import argparse
from utils import read_file
import os
import json
import random
import matplotlib.pyplot as plt


def slide_crib(texts, crib_bytes):
    crib_length = len(crib_bytes)
    results = []

    # Slide the crib across the XORed ciphertext
    for i in range(len(texts) - crib_length + 1):
        # XOR the crib with the section of XORed ciphertext to guess plaintext fragment
        possible_plaintext1 = xor_bytes(texts[i:i + crib_length], crib_bytes)
        
        # Decode to see if we have readable text
        try:
            possible_plaintext1_text = possible_plaintext1.decode('utf-8')
            results.append((i, possible_plaintext1_text))
        except UnicodeDecodeError:
            # If decoding fails, skip this position
            print("decode fails at position", i)
            pass
    return results

def xor_bytes(b1, b2):
    """XOR two byte strings of equal length."""
    return bytes([x ^ y for x, y in zip(b1, b2)])

def crib_drag(ciphertext1, ciphertext2, crib):
    """
    Attempt a crib-based attack on two ciphertexts encrypted with the same OTP key.
    """
    # XOR the two ciphertexts
    xor_ciphertexts = xor_bytes(ciphertext1, ciphertext2)
    
    crib_bytes = crib.encode('utf-8')
    
    results = slide_crib(xor_ciphertexts, crib_bytes)
    
    return results

def get_args():
    # Argument parser
    parser = argparse.ArgumentParser(description="Cryptanalysis Tool")
    parser.add_argument("-i", "--input", help="Input text (folder path or direct)", default= "Example/Crib/Mensagens")
    parser.add_argument("-o", "--output", help="Output file to save the plain text", default= "decoded.txt")
    parser.add_argument("-l", "--language", choices= ['en', 'pt'], default= 'pt')
    parser.add_argument("-v", "--verbose", action="store_true",default= False)
    parser.add_argument("-d", "--dictionary", help="file with good cribs", default="Example/Crib/dicionario.json")
    parser.add_argument("-s", "--strong_filter", default= False, action= 'store_true')
    args = parser.parse_args()
    
    return args



if __name__ == "__main__":

    args = get_args()
    # get cipher texts from folder
    cipher_texts = []
    if os.path.exists(args.input):
        for message_file in os.listdir(args.input):
            with open(os.path.join(args.input, message_file), 'rb') as f:
                cipher_texts.append((message_file, f.read()))
    else:
        raise FileNotFoundError("could not find the folder with the messages")

    if os.path.exists(args.dictionary):
        with open(args.dictionary) as dict_file:
            dicionario = json.load(dict_file)
    else:
        raise FileNotFoundError
    
    if args.strong_filter:
        with open("Example/General/fila.json") as dict_file:
            fila = json.load(dict_file)

    confirmed_matches = {}
    for crib in dicionario:
        print("---"*10)
        print("crib:", crib)
        # Run crib-dragging attack
        for i in range(len(cipher_texts)-1):
            for message_path, cipher_text in cipher_texts[i+1:]:
                matches = crib_drag(cipher_texts[i][1], cipher_text, crib)

                for position, match in matches:
                    if match in confirmed_matches:
                        continue
                    if args.strong_filter:
                        for i,(remetente,frase ) in enumerate(fila.items()):
                            if match in frase:
                                confirmed_matches[match] = True
                                print(remetente, end=": ")
                                pos = frase.find(match)
                                print("_"*pos + match + "_"*(len(frase)-len(match)-pos))
                
