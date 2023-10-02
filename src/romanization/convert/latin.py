import json
import pathlib

PATH = pathlib.Path(__file__).parent


def jungsung() -> None:
    with open(PATH / "data/latin/JUNGSUNG", "r") as f:
        data = f.readlines()

    resp = {}

    for d in data:
        blocks = d.strip().split(" ")
        try:
            resp[blocks[1]] = blocks[2]
        except IndexError:
            resp[blocks[1]] = ""

    with open(PATH / "output/latin/jungsung.json", "w") as f:
        f.write(json.dumps(resp))


if __name__ == "__main__":
    jungsung()
