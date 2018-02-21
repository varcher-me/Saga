import hashlib


def calc_sha1(filepath):
    try:
        with open(filepath, 'rb') as f:
            sha1obj = hashlib.sha1()
            sha1obj.update(f.read())
            hash = sha1obj.hexdigest()
            return hash
    except:
        return 0


def calc_md5(filepath):
    try:
        with open(filepath, 'rb') as f:
            sha1obj = hashlib.md5()
            sha1obj.update(f.read())
            hash = sha1obj.hexdigest()
            return hash
    except:
        return 0


