# Single String Replacement

given_string = "I think %s is a perfectly normal thing to do in public."
def sub1(s):
    return given_string % s

# Multiple String Replacements

given_string = "I think %s is a perfectly normal %s to do in public."
def sub1(s,b):
    return given_string % (s,b,)

# Advanced String Replacements

given_string2 = "I'm %(nickname)s. My real name is %(name)s, but my friends call me %(nickname)s."
def sub_m(name, nickname):
    return given_string2 % {'nickname' : nickname, 'name' : name}