import itertools
import re
import typing as t
import unicodedata

from .const import CONSONANTS, DOUBLES, CHOSUNG, JUNGSEONG, JONGSUNG, PROVISIONS


def decompose_hangul(char: str) -> t.Tuple[str, str, str]:
    """
    Decomposes a single Hangul syllable into its constituent jamo (choseong, jungseong, jongseong).

    Parameters
    ----------
    char : str
        A single Hangul character.

    Returns
    -------
    Tuple[str, str, str]
        A tuple containing the choseong, jungseong, and jongseong of the character.

    Examples
    --------
    >>> decompose_hangul("가")
    ("ᄀ", "ᅡ", "")

    >>> decompose_hangul("각")
    ("ᄀ", "ᅡ", "ᆨ")
    """
    x = ord(char)
    if 44032 <= x <= 55203:
        a = x - 44032
        b = a % 28
        c = 1 + ((a - b) % 588) // 28
        d = 1 + a // 588
        q = [*map(sum, zip(*[[d, c, b], [4351, 4448, 4519]]))]
        if b:
            return (chr(q[0]), chr(q[1]), chr(q[2]))
        return (chr(q[0]), chr(q[1]), '')
    return ('', char, '')


def convert_hangul_to_jamo(syllables: str) -> str:
    """
    Converts a string of Hangul syllables into a string of jamo characters.

    Parameters
    ----------
    syllables : str
        A string of Hangul syllables.

    Returns
    -------
    str
        A string of jamo characters representing the input Hangul syllables.
    """
    output = []

    data = []
    for syllable in syllables:
        block = decompose_hangul(syllable)
        for index, char in enumerate(block):
            if char:
                if index == 0:
                    data.extend(CHOSUNG.get(ord(char)))
                elif index == 1:
                    data.append(JUNGSEONG.get(ord(char)))
                elif index == 2:
                    data.extend(JONGSUNG.get(ord(char)))
    data = [list(group) for _, group in itertools.groupby(data, key=lambda x: isinstance(x, int))]

    prefix = data[0]
    try:
        if len(prefix) == 1:
            output.append(CONSONANTS[prefix[0]][0])
        elif len(prefix) == 2:
            output.append(CONSONANTS[prefix[0]][1])
    except Exception:
        pass

    for d in data[1:-1]:
        if isinstance(d[0], str):
            output.append(d[0])
            continue

        if len(d) == 1:
            output.append(CONSONANTS[d[0]][0])
        elif len(d) == 2:
            output.append(CONSONANTS[d[0]][1] if d[0] == d[1] and d[0] in DOUBLES else PROVISIONS[tuple(d)])
        elif len(d) == 3:
            if d[0] == d[1]:
                output.append(CONSONANTS[d[0]][1] if d[2] == 0x3147 else PROVISIONS[(d[0], d[2])])
            else:
                output.append(CONSONANTS[d[0]][2])
                output.append(CONSONANTS[d[1]][1] if d[1] == d[2] else PROVISIONS[(d[1], d[2])])

    suffix = data[-1]
    try:
        output.append(CONSONANTS[suffix[0]][2])
    except Exception:
        output.append(suffix[0])

    return "".join(output)


def romanize(text: str) -> str:
    """
    Romanizes Korean Hangul text into the Latin alphabet according to the Revised Romanization of Korean.

    Parameters
    ----------
    text : str
        The input string containing Korean Hangul text to be romanized.

    Returns
    -------
    str
        The romanized string.

    Examples
    --------
    >>> romanize("좋아 첫 눈에 반해 버린")
    "joha cheot nune banhae beorin"

    References
    ----------
    https://en.wikipedia.org/w/index.php?title=Revised_Romanization_of_Korean&oldid=1064463473
    """
    output = ""

    # Regular expression to separate Korean words, spaces, punctuation, and non-Korean words
    pattern = r"([ㄱ-ㅎ가-힣]+)|(\s+)|([^\w\s])|([A-Za-z0-9]+)"
    matches = (match for match in re.split(pattern, text) if match)
    for match in matches:
        try:
            if all("HANGUL" in unicodedata.name(char) for char in match):
                output += convert_hangul_to_jamo(match)
            else:
                output += match
        except Exception:
            output += match

    return output
