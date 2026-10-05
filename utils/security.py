import os
import hashlib

def hash_password(password: str, salt: str = None) -> str:

    if not salt:
        salt = os.urandom(16).hex()  # random 32-character hex salt
        
    salted_password = (password + salt).encode('utf-8')
    password_hash = hashlib.sha256(salted_password).hexdigest()
    
    return f"$sha256${salt}${password_hash}"

def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        algorithm, salt, password_hash = stored_hash.split('$')[1:]
        if algorithm != 'sha256':
            print(f"❌ Algorithm mismatch: got '{algorithm}' instead of 'sha256'")
            return False
            
        salted_password = (plain_password + salt).encode('utf-8')
        computed_hash = hashlib.sha256(salted_password).hexdigest()

        return computed_hash == password_hash
    
    except (ValueError, AttributeError):
        return False