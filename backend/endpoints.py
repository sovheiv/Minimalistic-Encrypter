from os import environ
from urllib.parse import parse_qsl
from flask import Blueprint, request

admin = Blueprint("admin", __name__)


@admin.route("/")
def index():
    return "main page"


@admin.route("/encrypt")
def encrypt():
    text = request.args.get("text")
    key = request.args.get("key")

    if not text or not key:
        qstr = environ.get("QUERY_STRING")
        text = dict(parse_qsl(qstr))["text"]
        key = dict(parse_qsl(qstr))["key"]

    result = {
        "success": False,
        "error_message": "",
        "result": [],
    }
    error_message = initial_error_check(text, key)

    if error_message:
        result["error_message"] = error_message
        return result

    key = int(key)

    key = limit_key(key)

    codes = [ord(code) for code in text]
    enc_codes = [lmit_code(code + key) for code in codes]
    enc_text = "".join([chr(code) for code in enc_codes])

    result["success"] = True
    result["result"] = enc_text

    return result


@admin.route("/decrypt")
def decrypt(in_text: str, key: int):
    return encrypt(in_text, key * -1)


def lmit_code(num, limits=[32, 126]):
    if num < limits[0]:
        num += limits[1] - limits[0] + 1
    if num > limits[1]:
        num -= limits[1] - limits[0] + 1
    return num


def limit_key(key, limit=94):
    div = key / (limit)
    # print(div)
    if div < -1 or div > 1:
        # print(int(div))
        key -= int(div) * limit
    return key


def initial_error_check(text: str, key: str, max_len=128):
    error_message = ""
    if not text:
        error_message = "empty string"
    elif len(text) > max_len:
        error_message = f"word is too long. Max {max_len} characters"
    elif not key.lstrip("-").isdigit():
        error_message = "Incorrect key"
    else:
        for character in text:
            if ord(character) > 126 or ord(character) < 32:
                error_message = f"unsupported character: {character}"
                break

    return error_message


@admin.app_errorhandler(404)
def handle_404(error):
    print(error)
    return "<center><b><mark> Page not found </mark></b></center>"
