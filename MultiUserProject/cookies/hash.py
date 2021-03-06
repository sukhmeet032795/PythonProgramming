import hashlib
import hmac

def hash_str(s):
    return hashlib.md5(s).hexdigest()

def hash_str_better(s):
    return hmac.new("unique".encode('utf-8'), "sss".encode('utf-8')).hexdigest()

def make_secure_val(s):
    return "%s,%s" % (s, hash_str(s))

def check_secure_val(h):
    strs = h.split(",")
    if strs[1] == hash_str(strs[0]):
        return strs[0]
    else:
        return None

print(check_secure_val("udacity,1497d98baea787eb6a8a676145c44212"))




