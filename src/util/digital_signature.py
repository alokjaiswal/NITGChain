import ecdsa

def generate_key_pair():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    vk = sk.get_verifying_key()
    return sk,vk
    
def get_sk_from_string(str_sk):
    return ecdsa.SigningKey.from_string(str_sk.encode('utf-8'),curve=ecdsa.SECP256k1)

def get_string_of_sk(str_sk):
    return ecdsa.SigningKey.to_string(str_sk)

def get_pk_from_string(str_pk):
    return ecdsa.VerifyingKey.from_string(str_pk.encode('utf-8'),curve=ecdsa.SECP256k1)

def get_string_of_pk(str_pk):
    return ecdsa.VerifyingKey.to_string(str_pk)

def sign(sk,msg):    
    sig = sk.sign(msg.encode('utf-8'))
    return sig


def verification(sign,msg,vk):
    return vk.verify(sign, msg.encode('utf-8'))












