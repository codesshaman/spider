import base64
import cryptocode


# For BASE-64
def get_encode_64(text):
    string = text.encode("UTF-8")
    result = base64.b64encode(string)
    return result.decode("UTF-8")


def get_decode_64(text):
    decode = base64.b64decode(text)
    return decode.decode("UTF-8")


# For AES
def get_encode(text, password):
    return cryptocode.encrypt(text, password)


def get_decode(text, password):
    return cryptocode.decrypt(text, password)