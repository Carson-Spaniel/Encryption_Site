from Crypto.Random import get_random_bytes

aes_key = get_random_bytes(32)

with open(f"key.bin", "wb") as f:
    f.write(aes_key)