import hashlib, random, string

# randomly pick 5 letters
def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(4)])

def make_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    hash = hashlib.sha256(password + salt).hexdigest()
    return '{0},{1}'.format(hash, salt)

def check_hash(password, hash):
    salt = hash.split(',')[1]
    if make_hash(password, salt) == hash:
        return True
    return False