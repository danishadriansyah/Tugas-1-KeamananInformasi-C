import binascii

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

S_BOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

KEY_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def permute(block, table):
    """Melakukan permutasi pada blok berdasarkan tabel."""
    return [block[x - 1] for x in table]

def string_to_bits(text):
    """Mengubah string menjadi list bit."""
    return [int(bit) for char in text for bit in bin(char)[2:].zfill(8)]

def bits_to_string(bits):
    """Mengubah list bit menjadi string."""
    chars = []
    for i in range(len(bits) // 8):
        byte = bits[i*8:(i+1)*8]
        chars.append(chr(int("".join(map(str, byte)), 2)))
    return "".join(chars)

def xor(bits1, bits2):
    """Melakukan operasi XOR pada dua list bit."""
    return [bit1 ^ bit2 for bit1, bit2 in zip(bits1, bits2)]

def left_shift(bits, n):
    """Melakukan pergeseran kiri sirkular."""
    return bits[n:] + bits[:n]

def pad(data):
    """
    Menambahkan padding PKCS7.
    Sesuai materi KI-04 (Message Padding), ini diperlukan untuk menangani
    blok data terakhir yang ukurannya mungkin kurang dari 8 byte.
    """
    block_size = 8
    padding_len = block_size - len(data) % block_size
    padding = bytes([padding_len] * padding_len)
    return data + padding

def unpad(data):
    """Menghapus padding PKCS7."""
    padding_len = data[-1]
    return data[:-padding_len]

def generate_subkeys(key_bits):
    """Menghasilkan 16 subkunci dari kunci utama."""
    key_permuted = permute(key_bits, PC1)
    left_key = key_permuted[:28]
    right_key = key_permuted[28:]
    subkeys = []

    for i in range(16):
        left_key = left_shift(left_key, KEY_SHIFTS[i])
        right_key = left_shift(right_key, KEY_SHIFTS[i])
        combined_key = left_key + right_key
        subkeys.append(permute(combined_key, PC2))

    return subkeys

def feistel_function(block_32_bits, subkey_48_bits):
    """Fungsi Feistel (F) dalam DES."""
    expanded_bits = permute(block_32_bits, E)
    xor_result = xor(expanded_bits, subkey_48_bits)
    sbox_output = []
    for i in range(8):
        chunk = xor_result[i*6:(i+1)*6]
        row = int(str(chunk[0]) + str(chunk[5]), 2)
        col = int("".join(map(str, chunk[1:5])), 2)
        val = S_BOX[i][row][col]
        sbox_output.extend([int(b) for b in bin(val)[2:].zfill(4)])
    return permute(sbox_output, P)

def process_block(block_64_bits, subkeys, mode):
    """Memproses satu blok 64-bit untuk enkripsi atau dekripsi."""
    block = permute(block_64_bits, IP)
    left, right = block[:32], block[32:]

    if mode == 'decrypt':
        subkeys = subkeys[::-1]

    for i in range(16):
        f_result = feistel_function(right, subkeys[i])
        new_right = xor(left, f_result)
        left = right
        right = new_right

    final_block = right + left
    return permute(final_block, FP)

def des_algorithm(data_bits, subkeys, mode):
    """
    Menjalankan algoritma DES pada seluruh data.
    Fungsi ini memproses data blok per blok secara independen,
    yang merupakan implementasi dari mode ECB (Electronic Codebook)
    seperti yang dijelaskan dalam materi KI-04.
    """
    processed_data = []
    for i in range(len(data_bits) // 64):
        block = data_bits[i*64:(i+1)*64]
        processed_block = process_block(block, subkeys, mode)
        processed_data.extend(processed_block)
    return processed_data

def encrypt_text(plain_text, key):
    key_bytes = key.encode('utf-8')
    key_bits = string_to_bits(key_bytes)
    subkeys = generate_subkeys(key_bits)

    plain_bytes = plain_text.encode('utf-8')
    padded_bytes = pad(plain_bytes)
    data_bits = string_to_bits(padded_bytes)
    
    encrypted_bits = des_algorithm(data_bits, subkeys, 'encrypt')
    
    encrypted_bytes = int("".join(map(str, encrypted_bits)), 2).to_bytes(len(encrypted_bits) // 8, byteorder='big')
    return binascii.hexlify(encrypted_bytes)

def decrypt_text(encrypted_text_hex, key):
    key_bytes = key.encode('utf-8')
    key_bits = string_to_bits(key_bytes)
    subkeys = generate_subkeys(key_bits)

    encrypted_bytes = binascii.unhexlify(encrypted_text_hex)
    data_bits = string_to_bits(encrypted_bytes)

    decrypted_bits = des_algorithm(data_bits, subkeys, 'decrypt')
    
    decrypted_bytes = int("".join(map(str, decrypted_bits)), 2).to_bytes(len(decrypted_bits) // 8, byteorder='big')
    unpadded_bytes = unpad(decrypted_bytes)
    
    return unpadded_bytes.decode('utf-8')

def main():
    """Fungsi utama untuk interaksi dengan pengguna."""
    print("=" * 45)
    print("Implementasi Manual Enkripsi & Dekripsi DES")
    print("=" * 45)

    key = 'mysecret'
    print(f"Kunci yang digunakan: {key}\n")

    while True:
        print("Pilih Aksi:")
        print("1. Enkripsi Teks")
        print("2. Dekripsi Teks")
        print("3. Keluar")
        
        choice = input("Masukkan pilihan (1/2/3): ")

        if choice == '1':
            plain_text = input("Masukkan teks yang ingin dienkripsi: ")
            encrypted = encrypt_text(plain_text, key)
            print("\n--- Hasil Enkripsi ---")
            print(f"Ciphertext (hex): {encrypted.decode('utf-8')}")
            print("-" * 22 + "\n")
        
        elif choice == '2':
            encrypted_text_hex = input("Masukkan ciphertext (format hex): ").encode('utf-8')
            try:
                decrypted = decrypt_text(encrypted_text_hex, key)
                print("\n--- Hasil Dekripsi ---")
                print(f"Plaintext: {decrypted}")
                print("-" * 22 + "\n")
            except Exception as e:
                print(f"\nGagal mendekripsi. Pastikan kunci dan ciphertext benar. Error: {e}\n")

        elif choice == '3':
            print("Terima kasih telah menggunakan program ini.")
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.\n")

if __name__ == "__main__":
    main()

