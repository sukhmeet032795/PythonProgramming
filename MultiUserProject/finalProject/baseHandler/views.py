import hmac

#############Cookie Hash#############

secret_key = ",qLY5!RD06.w1onRFC$M8=w<-#M+DjvA,9<mB,*Yq#ZavEf.k`KZKP\2)V:(.,E"

def make_cookie_hash(userId):
    return ("%s|%s" % (str(userId), hmac.new( str(userId).encode("utf-8") + secret_key.encode("utf-8") ).hexdigest()))

def check_cookie_hash(hash):

    if not hash:
        return False

    userId = hash.split("|")[0]
    if hash == make_cookie_hash(userId):
        return True
    return False

#######################################
