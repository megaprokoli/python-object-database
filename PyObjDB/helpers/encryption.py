from cryptography.fernet import Fernet


def generate_key() -> bytes:
    return Fernet.generate_key()


def encrypt(key: bytes, string: str) -> bytes:
    cipher = Fernet(key)
    return cipher.encrypt(string.encode())


def decrypt(key: bytes, encrypted: bytes) -> str:
    cipher = Fernet(key)
    return cipher.decrypt(encrypted).decode("utf-8")


if __name__ == "__main__":
    key = generate_key()
    s = "test"
    print(key)

    s = encrypt(key, s)
    print(s)

    s = decrypt(key, s)
    print(s)
