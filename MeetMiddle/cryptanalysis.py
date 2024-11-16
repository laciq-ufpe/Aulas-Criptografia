from crypt_utils import generate_full_key, N_BITS_KEY
import time
import tqdm
from Crypto.Cipher import DES


# Brute-force single DES key
def brute_force_single_des(ciphertext, plaintext, known_bits=0x0000000000000000):
    start_time = time.time()
    for key_bit in range(2**N_BITS_KEY):  # 2^10 = 1024 possible keys
        full_key = generate_full_key(key_bit, known_bits)
        cipher = DES.new(full_key, DES.MODE_ECB)
        if cipher.encrypt(plaintext) == ciphertext:
            elapsed_time = time.time() - start_time
            print(key_bit, elapsed_time)
    return None, None

# Brute-force double DES without MITM
def brute_force_double_des(ciphertext, plaintext, known_bits=0x0000000000000000):
    start_time = time.time()
    for key1_bit in tqdm.tqdm(range(2**N_BITS_KEY)):  # Outer loop: 2^N_BITS for the first key
        full_key1 = generate_full_key(key1_bit, known_bits)
        cipher1 = DES.new(full_key1, DES.MODE_ECB)
        intermediate = cipher1.encrypt(plaintext)

        for key2_bit in range(2**N_BITS_KEY):  # Inner loop: 2^N_BITS_KEY for the second key
            full_key2 = generate_full_key(key2_bit, known_bits)
            cipher2 = DES.new(full_key2, DES.MODE_ECB)
            if cipher2.encrypt(intermediate) == ciphertext:
                elapsed_time = time.time() - start_time
                print( key1_bit, key2_bit, elapsed_time)
    return None, None, None


# Brute-force double DES using MITM
def mitm_double_des(ciphertext, plaintext, known_bits=0x0000000000000000):
    start_time = time.time()
    forward_map = {}

    # Forward encryption with all possible keys
    for key1_bit in tqdm.tqdm(range(2**N_BITS_KEY)):
        full_key1 = generate_full_key(key1_bit, known_bits)
        cipher1 = DES.new(full_key1, DES.MODE_ECB)
        intermediate = cipher1.encrypt(plaintext)
        if intermediate in forward_map:
            forward_map[intermediate].append(key1_bit)
            
        else:
            forward_map[intermediate] = [key1_bit]

    # Backward decryption with all possible keys
    for key2_bit in tqdm.tqdm(range(2**N_BITS_KEY)):
        full_key2 = generate_full_key(key2_bit, known_bits)
        cipher2 = DES.new(full_key2, DES.MODE_ECB)
        decrypted = cipher2.decrypt(ciphertext)
        if decrypted in forward_map:
            
            elapsed_time = time.time() - start_time
            keys1_bit = forward_map[decrypted]
            for key1_bit in keys1_bit:
                print(key1_bit, key2_bit, elapsed_time)

    return None, None, None