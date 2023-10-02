from romanization import romanize


def test_romanize():
    assert romanize("안녕") == "annyeong"
