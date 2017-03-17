import hashlib
import string

#############Password Hash#############

def generate_salt():
    return "".join(random.choice(string.ascii_letters) for x in range(5))

def make_pw_hash(username, pwd, salt = None):

    if not salt:
        salt = generate_salt()
    return "%s,%s" % (salt, hashlib.sha256(salt.encode("utf-8") + username.encode("utf-8") + pwd.encode("utf-8")).hexdigest())

def check_pw_hash(username, pwd, hash):

    if not hash:
        return False

    salt = hash.split(",")[0]
    if make_pw_hash(username, pwd, salt) == hash:
        return True
    return False

#######################################