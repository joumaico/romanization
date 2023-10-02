import itertools
import numpy as np
import re
import typing as t

from .const import CHOSUNG
from .const import JONGSUNG
from .const import JUNGSUNG
from .const import LATIN
from .const import PATH


class Locator:
    """
    A class used to represent a Locator that reads provision data and stores it
    in a table, along with column and row labels.

    Attributes
    ----------
    TABLE : np.ndarray
        A 2D numpy array containing the provision data read from the file "convert/data/provisions".
    COL_LABELS : np.ndarray
        A 1D numpy array containing column labels derived from the keys of the "CHOSUNG" dictionary in LATIN.
    ROW_LABELS : np.ndarray
        A 1D numpy array containing row labels derived from the keys of the "JONGSUNG" dictionary in LATIN.

    Methods
    -------
    None
    """

    with open(PATH / "convert/data/provisions", "r") as f:
        TABLE = np.array([i.strip().split(" ") for i in f.readlines()])

    COL_LABELS = np.array(list(LATIN["CHOSUNG"].keys()))
    ROW_LABELS = np.array(list(LATIN["JONGSUNG"].keys()))


def custom_split(text: str) -> t.List[str]:
    """
    Splits a given text into a list of strings, separating by whitespace and non-whitespace sequences.
    Consecutive whitespace characters are split into individual space characters.

    Parameters
    ----------
    text : str
        The input text to be split.

    Returns
    -------
    List[str]
        A list of substrings, where each substring is either a single non-whitespace sequence 
        or a single whitespace character.

    Examples
    --------
    >>> custom_split("Hello   world")
    ["Hello", " ", " ", " ", "world"]

    >>> custom_split("a\nb\tc")
    ["a", "\n", "b", "\t", "c"]
    """
    pattern = re.compile(r"(\s+|[^\s]+)")
    matches = pattern.findall(text)
    result = []
    for match in matches:
        if len(match) > 1 and match.isspace():
            result.extend(list(match))
        else:
            result.append(match)
    return result


def decompose_hangul(char: str) -> t.Tuple[str, str, str]:
    """
    Decomposes a Hangul syllable character into its constituent Jamo components.

    Parameters
    ----------
    char : str
        A single Hangul syllable character.

    Returns
    -------
    Tuple[str, str, str]
        A tuple containing three strings:
        - The leading consonant (choseong)
        - The vowel (jungseong)
        - The trailing consonant (jongseong), or an empty string if there is no trailing consonant.

    Raises
    ------
    ValueError
        If the input character is not a Hangul syllable character.

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
        return (chr(q[0]), chr(q[1]), "")
    return ("", char, "")


def get_chosung(char: str) -> t.List[str]:
    """
    Retrieves the Chosung (initial consonant) candidates for a given character.

    Parameters
    ----------
    char : str
        A single character to look up in the CHOSUNG dictionary.

    Returns
    -------
    List[str]
        A list of Chosung candidates corresponding to the input character. 
        Returns an empty list if the character is not found in the CHOSUNG dictionary.

    Examples
    --------
    >>> get_chosung("ㄱ")
    ["ᄀ", "ᄁ"]

    >>> get_chosung("x")
    []
    """
    try:
        return CHOSUNG[f"'{char}'"]
    except KeyError:
        return []


def get_jongsung(char: str) -> t.List[str]:
    """
    Retrieves the Jongsung (final consonant) candidates for a given character.

    Parameters
    ----------
    char : str
        A single character to look up in the JONGSUNG dictionary.

    Returns
    -------
    List[str]
        A list of Jongsung candidates corresponding to the input character.
        Returns an empty list if the character is not found in the JONGSUNG dictionary.

    Examples
    --------
    >>> get_jongsung("ㄱ")
    ["ᆨ", "ᆩ"]

    >>> get_jongsung("x")
    []
    """
    try:
        return JONGSUNG[f"'{char}'"]
    except KeyError:
        return []


def get_jungsung(char: str) -> str:
    """
    Retrieves the Jungsung (medial vowel) for a given character.

    Parameters
    ----------
    char : str
        A single character to look up in the JUNGSUNG dictionary.

    Returns
    -------
    str
        The corresponding Jungsung for the input character.
        Returns an empty string if the character is not found in the JUNGSUNG dictionary.

    Examples
    --------
    >>> get_jungsung("ㅏ")
    "ᅡ"

    >>> get_jungsung("x")
    ""
    """
    try:
        return JUNGSUNG[f"'{char}'"]
    except KeyError:
        return ""


def split_into_chunks(data: t.Iterable[t.Any], size: int) -> t.Iterator[t.List[str]]:
    """
    Splits an iterable into chunks of a specified size.

    Parameters
    ----------
    data : iterable
        The iterable to be split into chunks.
    size : int
        The size of each chunk.

    Returns
    -------
    Iterator[List[str]]
        An iterator where each item is a list containing a chunk of the original data.

    Examples
    --------
    >>> list(split_into_chunks([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]

    >>> list(split_into_chunks("abcdef", 3))
    [["a", "b", "c"], ["d", "e", "f"]]
    """
    def slize_size(g):
        return lambda: tuple(itertools.islice(g, size))
    return iter(slize_size(iter(data)), ())


def split_jamo(text: str) -> t.List[t.Tuple[str]]:
    """
    Splits a string of Hangul characters into their constituent Jamo components.

    Parameters
    ----------
    text : str
        The string of Hangul characters to be split.

    Returns
    -------
    List[Tuple[str]]
        A list of strings where each item is a tuple containing the Jamo components of the corresponding Hangul character.

    Examples
    --------
    >>> split_jamo("한글")
    [("ᄒ", "ᅡ", "ᆫ"), ("ᄀ", "ᅳ", "ᆯ")]

    >>> split_jamo("가")
    [("ᄀ", "ᅡ", "")]
    """
    result = []
    for i, char in enumerate(text):
        jamo_components = decompose_hangul(char)
        if i == 0:
            result.append(("", *jamo_components))
        elif i == len(text) - 1:
            result.append((*jamo_components, "", ""))
        else:
            result.append(jamo_components)
    return result
