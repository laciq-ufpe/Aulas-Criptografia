from cryptanalysis import brute_force_double_des, brute_force_single_des, mitm_double_des
if __name__ == "__main__":
    plaintext = plaintext = b"GENERAL "
    single_ciphertext =  b'\x90zu%+O\xff\xd2'
    double_ciphertext =  b'\xf0\x82B\xec\xf7\x0c|%'

    print("BRUTE FORCE DES")
    recovered_key, single_time = brute_force_single_des(single_ciphertext, plaintext)
    #print(f"Single DES key: {recovered_key} (Time taken: {1e3*single_time:.6f} ms)")

    print('-'*100)


    # Brute-force Double DES without MITM
    # print("BRUTE FORCE 2DES")
    # bf_key1, bf_key2, bf_time = brute_force_double_des(double_ciphertext, plaintext)
    # print(
    #     f"Brute-force Double DES keys: Key1={bf_key1}, Key2={bf_key2} "
    #     f"(Time taken: {1e3*bf_time:.6f} ms)"
    # )

    print('-'*100)



    print("MEET IN THE MIDDLE DOUBLE DES:")
    # Brute-force Double DES with MITM
    mitm_key1, mitm_key2, mitm_time = mitm_double_des(double_ciphertext, plaintext)

    # print(
    #     f"MITM Double DES keys: Key1={mitm_key1}, Key2={mitm_key2} "
    #     f"(Time taken: {1e3*mitm_time:.6f} ms)"
    # )

