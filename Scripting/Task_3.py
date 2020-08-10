import socket
import sys
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def AES_GCM_decrypt(key, iv, cipher, tag):
    # https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#module-cryptography.hazmat.primitives.ciphers.modes
    decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()).decryptor()
    return decryptor.update(cipher) + decryptor.finalize()
    

def SHA256_hash(plaintext):
    sha_signature = hashlib.sha256(plaintext).hexdigest()
    return sha_signature

def run():
    HOST = sys.argv[1]
    PORT = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((HOST, PORT))

    payload = "hello"
    s.send(payload.encode())
    response = s.recv(4096)
    # You've connected to the super secret server, send a packet with the payload ready to receive more information
    
    payload = "ready"
    s.send(payload.encode())
    response = s.recv(4096)
    key = b'thisisaverysecretkeyl337'
    iv = b'secureivl337'
    checksum = response[104:136]
    while True:
        payload = "final" 
        s.send(payload.encode())
        flag = s.recv(4096)

        s.send(payload.encode())
        tag = s.recv(4096)
        
        plaintext = AES_GCM_decrypt(key, iv, flag, tag)
    
        hash_text = SHA256_hash(plaintext)
        if hash_text == checksum.hex():
            print(plaintext)
            break
        else:
            continue
  
    s.close()


if __name__ == "__main__":
    run()