'''
Created on 2015年12月9日

@author: cdz
'''

def initial(s, key, length):
    tmp = [0 for i in range(0, 256)]
    for i in range(0, 256):
        s[i] = i
        tmp[i] = key[i % length]
    j = 0
    for i in range(0, 256):
        j = (j + s[i] + tmp[i]) & 0xFF
        s[i], s[j] = s[j], s[i]
    
def crypt(plain, s):
    i = j = 0
    for k in range(0, len(plain)):
        i = (i + 1) & 0xFF
        j = (j + 1) & 0xFF
        s[i], s[j] = s[j], s[i]
        t = (s[i] + s[j]) & 0xFF
        plain[k] ^= s[t]    

if __name__ == '__main__':
    string = '软件21崔大壮，就职于美团，后端开发工程师'
    modifiedstring = '软件20崔大壮，就职于美团，后端开发工程师'
    ENCODING = 'gbk'
    encryped1 = None
    encryped2 = None
    s = [i for i in range(0, 256)]
    key = b'test key test key test key'
    initial(s, key, len(key))
    
    text = bytearray(string.encode(encoding=ENCODING))
    # plain text
    print('明文：', str(text, encoding=ENCODING))
    
    # encrypte
    crypt(text, s)
    encryped1 = bytearray(text)
    
    # decrypte
    crypt(text, s)
    print('解密：', str(text, encoding=ENCODING))
    
    #-----------modified text-------------
    text = bytearray(modifiedstring.encode(encoding=ENCODING))
    # plain text
    print('明文：', str(text, encoding=ENCODING))
    
    # encrypte
    crypt(text, s)
    encryped2 = bytearray(text)
    
    # decrypte
    crypt(text, s)
    print('解密：', str(text, encoding=ENCODING))
    
    #--------compare 2 encrypted text------------
    print('original ciphertext:', bytes(encryped1))
    print('modified ciphertext:', bytes(encryped2))
