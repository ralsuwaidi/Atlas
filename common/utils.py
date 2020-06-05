import re
from passlib.hash import pbkdf2_sha512

numeral_map = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))

def int_to_roman(i):
    result = []
    for integer, numeral in numeral_map:
        count = i // integer
        result.append(numeral * count)
        i -= integer * count
    return ''.join(result)

def roman_to_int(n):
    i = result = 0
    for integer, numeral in numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return result

class Utils:
    @staticmethod
    def email_is_valid(email:str) ->bool:
        email_address_matcher = re.compile(r'[^@]+@[^@]+\.[^@]+')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password:str) ->str:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password: str, hashed_password:str)->bool:
        print(password, hashed_password)
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def hash_from_magnet(magnet:str)->str:
        if "btih:" in magnet:
            return magnet.split("btih:",1)[1]
        else:
            print("not magnet link")
        

if __name__ == "__main__":

    print(roman_to_int("LVII.VII"))

