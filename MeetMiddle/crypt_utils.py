from Crypto.Cipher import DES

N_BITS_KEY = 14

# Helper function to generate a full 64-bit DES key from a shorter key
def generate_full_key(short_key, known_bits=0x0000000000000000):    
    # if type(short_key) == bytes:
    #     short_key = int.from_bytes(short_key, byteorder="big")
    # result_int = short_key | known_bits
    return short_key.to_bytes(8, byteorder="big")
    

# Encrypt using single DES with a 5-bit key
def single_des_encrypt(key_bit, plaintext, known_bits=0x0000000000000000):
    full_key = generate_full_key(key_bit, known_bits)
    cipher = DES.new(full_key, DES.MODE_ECB)

    return cipher.encrypt(plaintext)

# Encrypt using double DES with two 10-bit keys
def double_des_encrypt(key1_bit, key2_bit, plaintext, known_bits=0x0000000000000000):
    full_key1 = generate_full_key(key1_bit, known_bits)
    full_key2 = generate_full_key(key2_bit, known_bits)
    
    cipher1 = DES.new(full_key1, DES.MODE_ECB)
    cipher2 = DES.new(full_key2, DES.MODE_ECB)
    intermediate = cipher1.encrypt(plaintext)
    return cipher2.encrypt(intermediate)

if __name__ =="__main__":
    # considere que se sabe o comeco de uma mensagem criptografada,
    # a mensagem comeca com GENERAL AUGUSTO, os primeiros 8-bytes sao GENERAL 
    plaintext = b"GENERAL "  # 8-byte plaintext (DES block size)
    print(str(plaintext)+":", plaintext)

    # Single DES test
    single_key = 1234
    single_ciphertext = single_des_encrypt(single_key, plaintext)
    print("single_ciphertext = ", single_ciphertext)

    # Double DES test
    double_key1 = 3210
    double_key2 = 1234
    
    double_ciphertext = double_des_encrypt(double_key1, double_key2, plaintext)
    print("double_ciphertext = ", double_ciphertext)

