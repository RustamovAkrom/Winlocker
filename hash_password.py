import hashlib

def main():
    password = input("Enter password to hash: ")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    print(f"Hashed password: {hashed}")

if __name__ == "__main__":
    main()