from utils import read_plain_apply_cipher_save
import argparse


def get_args(): 
    # Argument parser
    parser = argparse.ArgumentParser(description="Cipher Tool")
    parser.add_argument("-i", "--input", help="Input text (file path or direct)", default= "Example/carta-general.txt")
    parser.add_argument("-f", "--file", help="Flag to specify if input is from file", action="store_true", default= False)
    parser.add_argument("-o", "--output", help="Output file to save the cipher text", default= "cipher_otp.txt")
    parser.add_argument("-k", "--key", help="otp key. In order to have perfect security, use a key as long as the plaintext", type=str, default= "!@#$%+=&*())_+{}[]?8796321684651331354413AFbaERgtheJHGBIGSWETRN" )
    parser.add_argument("-v", "--verbose", action="store_true",default= False)
    args = parser.parse_args()
    
    return args

def extend_key(text, key):
    return (key * (len(text) // len(key) + 1))[:len(text)]
def xor_byte_strs(b1, b2): 
    return bytes([b1_byte ^ b2_byte for b1_byte, b2_byte in zip(b1, b2)])

def otp_encrypt(plaintext, key):
    if type(key) == str: key = key.encode('utf-8')
    """If the key is shorter than the plaintext, it wraps around to match the plaintext length"""
    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')
    
    # Extend or wrap the key to match the length of the plaintext
    extended_key = extend_key(plaintext, key)
    
    # XOR each byte of plaintext with the corresponding byte in the extended key
    ciphertext = xor_byte_strs(plaintext_bytes, extended_key)
    
    return ciphertext

def otp_decrypt(ciphertext, key):
    """If the key is shorter than the ciphertext, it wraps around to match the ciphertext length"""
    NotImplemented

# Example usage
plaintext = "mensagem secreta"
# Example key (in bytes), shorter than the plaintext
key = b'!@#$%+=&*())_+{}[]?8796321684651331354413'

# Encrypt the plaintext with the provided key
ciphertext = otp_encrypt(plaintext, key)
print("Ciphertext (in bytes):", ciphertext.decode('utf-8'))


if __name__ == "__main__":
    args = get_args()
    read_plain_apply_cipher_save(args, cipher_algorithm= otp_encrypt, cipher_args=(args.key,))
