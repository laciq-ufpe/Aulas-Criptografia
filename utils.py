import argparse
import os

def get_io_args(): 
    # Argument parser
    parser = argparse.ArgumentParser(description="Cipher Tool")
    parser.add_argument("-i", "--input", help="Input text (file path or direct)", required=True)
    parser.add_argument("-f", "--file", help="Flag to specify if input is from file", action="store_true", default= False)
    parser.add_argument("-o", "--output", help="Output file to save the cipher text", default= "cipher.txt")
    parser.add_argument("-k", "--chave", help="secret key", type=int, default= 10)
    parser.add_argument("-v", "--verbose", action="store_true",default= False)
    args = parser.parse_args()
    
    return args

def read_file(file_path):
    # Read the input text
    with open(file_path, 'r') as f:
        text = f.read()
    return text

def apply_cipher(cipher_text,output_path) :  
    
    # Save the cipher text to a file
    if type(cipher_text) ==str:
        with open(output_path, 'w') as f:
            f.write(cipher_text)
    else:
        with open(output_path, 'wb') as f:
            f.write(cipher_text)

def read_plain_apply_cipher_save(args, cipher_algorithm, cipher_args):
    
    text = args.input
    if os.path.exists(args.input) == False:
        print(f"\n\nWarning: could not find file {args.input}, treating it as plain_text")
        
    elif args.file:
        text = read_file(args.input)
    
    if args.verbose: print("leu a entrada\naplicando algoritmo de cifragem")

    cipher_text = cipher_algorithm(text,*cipher_args)

    if args.verbose: print("salvando cifro texto")

    apply_cipher(cipher_text, output_path= args.output)
    print(f"Cifro text salvo em: {args.output}")