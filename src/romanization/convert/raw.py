import json
import pathlib

PATH = pathlib.Path(__file__).parent


def chosung() -> None:
    with open(PATH / "data/raw/CHOSUNG", "r") as f:
        data = f.readlines()

    resp = {}

    for d in data:
        blocks = d.strip().split(" ")
        try:
            resp[blocks[1]] = list(blocks[2])
        except IndexError:
            resp[blocks[1]] = []

    with open(PATH / "output/raw/chosung.json", "w") as f:
        f.write(json.dumps(resp))


def jongsung() -> None:
    with open(PATH / "data/raw/JONGSUNG", "r") as f:
        data = f.readlines()

    resp = {}

    for d in data:
        blocks = d.strip().split(" ")
        try:
            resp[blocks[1]] = list(blocks[2])
        except IndexError:
            resp[blocks[1]] = []

    with open(PATH / "output/raw/jongsung.json", "w") as f:
        f.write(json.dumps(resp))


if __name__ == "__main__":
    chosung()
    jongsung()
