import json
import pathlib

PATH = pathlib.Path(__file__).parent

LATIN = {
    "CHOSUNG": {
        "": "",
        "ㅇ": "",
        "ㄱ": "g",
        "ㄴ": "n",
        "ㄷ": "d",
        "ㄹ": "r",
        "ㅁ": "m",
        "ㅂ": "b",
        "ㅅ": "s",
        "ㅈ": "j",
        "ㅊ": "ch",
        "ㅋ": "k",
        "ㅌ": "t",
        "ㅍ": "p",
        "ㅎ": "h",
    },
    "JONGSUNG": {
        "ㄱ": "k",
        "ㄴ": "n",
        "ㄷ": "t",
        "ㄹ": "l",
        "ㅁ": "m",
        "ㅂ": "p",
        "ㅅ": "t",
        "ㅇ": "ng",
        "ㅈ": "t",
        "ㅊ": "t",
        "ㅌ": "t",
        "ㅎ": "t",
        "ㅋ": "k",
        "ㅍ": "p",
    }
}

TWIN_CASE_PROVISION = {
    "ㅂ": "pp",
    "ㅈ": "jj",
    "ㄷ": "tt",
    "ㄱ": "kk",
    "ㅅ": "ss"
}

with open(PATH / "convert/output/raw/chosung.json", "r") as f:
    CHOSUNG = json.load(f)

with open(PATH / "convert/output/latin/jungsung.json", "r") as f:
    JUNGSUNG = json.load(f)

with open(PATH / "convert/output/raw/jongsung.json", "r") as f:
    JONGSUNG = json.load(f)
