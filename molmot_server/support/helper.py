import random
import string


def qrcode_selfie_num():
    LENGTH = 5
    string_pool = string.ascii_letters + string.digits
    auth_num = ""
    for i in range(LENGTH):
        auth_num += random.choice(string_pool)
    return auth_num