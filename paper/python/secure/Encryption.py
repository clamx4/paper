'''
Created on 2015年12月9日

@author: cdz
'''
import pyDes
from cryptography.hazmat.primitives.asymmetric import dsa 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class EncryptionAndDecryption:
    def __init__(self):
        self.private_key = dsa.generate_private_key(key_size=1024, backend=default_backend())
        
    def sign(self, data):
        signer = self.private_key.signer(hashes.SHA512())
        signer.update(data)
        signature = signer.finalize()
        return signature
    
    def authentic(self, signature, data):
        public_key = self.private_key.public_key()
        verifier = public_key.verifier(signature, hashes.SHA512())
        verifier.update(data)
        try:
            verifier.verify()
            return True
        except InvalidSignature:
            return False
        
    def encrypt(self, text):
        plains = splitMsg(text, 12)
        groups = []
        i = 0
        print('before encrypting')
        for splited_text in plains:
            digest = hash_sha512(splited_text)
            signature = self.sign(splited_text)
            sig_len = len(signature)
            group = bytearray(128)
            #group[0 : 64] = digest
            muti_assign(group, digest, 0)
            group[64] = sig_len
            #group[65 : sig_len] = signature
            muti_assign(group, signature, 65)
            group[113] = len(plains)
            group[114] = i
            #group[115 : len(plains[i])] = plains[i]
            group[115] = len(splited_text)
            muti_assign(group, plains[i], 116)
            print(splited_text)
            groups.append(group)
            i += 1
            
        ciphers = []
        for group in groups:
            cipher = dsa_encrypt(group)
            ciphers.append(cipher)
        return ciphers
    
    def decrypt(self, ciphers):
        plains = []
        for cipher in ciphers:
            plain = dsa_decrypt(cipher)
            plains.append(plain)
        datas = [None for i in range(0, len(ciphers))]
        print('after decrypting')
        for plain in plains:
            digest = plain[0 : 64]
            sig_len = int(plain[64])
            signature = plain[65 : 65 + sig_len]
            group_num = int(plain[113])
            curr_group = int(plain[114])
            data_len = int(plain[115])
            data = plain[116 : 116 + data_len]
            # check confidentiality and integrity
            if digest != hash_sha512(data) or \
                not self.authentic(signature, data) or \
                group_num != len(ciphers) or \
                curr_group < 0 or \
                curr_group >= group_num:
                raise Exception
            datas[curr_group] = data
            print(data)
        return b''.join(datas)
        
def splitMsg(msg, sub_msg_size_in_byte):
    i = 0
    msgs = []
    sub_msg_size = sub_msg_size_in_byte# << 3
    while i + sub_msg_size < len(msg):
        msgs.append(msg[i : i + sub_msg_size])
        i += sub_msg_size
    if i < len(msg):
        msgs.append(msg[i : len(msg)])
    return msgs

    
def dsa_encrypt(data):
    key = b'test-key'
    a = pyDes.des(key, pad=pyDes.PAD_PKCS5)
    cipher = a.encrypt(data, padmode=pyDes.PAD_PKCS5)
    return cipher

def dsa_decrypt(cipher):
    key = b'test-key'
    a = pyDes.des(key, pad=pyDes.PAD_PKCS5)
    data = a.decrypt(cipher, padmode=pyDes.PAD_PKCS5)
    return data
    
def hash_sha512(data):
    digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
    digest.update(data)
    return digest.finalize()

def muti_assign(dest, src, start):
    for i in src:
        dest[start] = i
        start += 1
        
if __name__ == '__main__':
    s = '软件21崔大壮，2121601009，就职于美团，后端开发工程师。python是世界上最好用的语言'
    crypt = EncryptionAndDecryption()
    ENCODING = 'utf-8'
    print(str(crypt.decrypt(crypt.encrypt(s.encode(encoding=ENCODING))), encoding=ENCODING))
