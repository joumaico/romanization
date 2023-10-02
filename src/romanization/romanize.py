import numpy as np
import unicodedata

from .const import LATIN
from .const import TWIN_CASE_PROVISION

from .utils import Locator
from .utils import custom_split
from .utils import get_chosung
from .utils import get_jongsung
from .utils import get_jungsung
from .utils import split_into_chunks
from .utils import split_jamo


locator = Locator()


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
    result = []

    for word in custom_split(text):
        process = False
        for i in word:
            if unicodedata.category(i) == "Lo":  # checks if a word has Hangul syllable
                process = True
                break
        if process:
            dump = []
            for index, block in enumerate(split_into_chunks((j for i in split_jamo(word) for j in i), 3)):
                if len(block) == 1:  # for standalone syllable "책"
                    block = (block[0], "", "")

                chosung = get_chosung(block[1])
                jungsung = get_jungsung(block[2])
                jongsung = get_jongsung(block[0])

                if chosung:
                    if len(chosung) > 1 and len(set(chosung)) == 1:
                        if jongsung:  # "올까"
                            for i in jongsung:
                                dump.append(LATIN["JONGSUNG"][i])
                        if ord(chosung[0]) == 12593:  # ㄲ: "깐다"
                            dump.append(TWIN_CASE_PROVISION[chosung[0]])
                        else:
                            if index == 0:  # "뚜두"
                                dump.append(LATIN["CHOSUNG"][chosung[0]] * 2)
                            else:  # "오빠"
                                dump.append(TWIN_CASE_PROVISION[chosung[0]])
                    else:
                        if jongsung:
                            if len(jongsung) > 1 and len(set(jongsung)) == 1 and ord(chosung[0]) == 12615:  # ㅇ: "있을까"
                                dump.append(TWIN_CASE_PROVISION[jongsung[0]])
                            else:
                                if len(jongsung) > 1 and len(set(jongsung)) >= 2:  # "없어요"
                                    for i in jongsung[:-1]:
                                        dump.append(LATIN["JONGSUNG"][i])
                                col_index = np.where(locator.COL_LABELS == chosung[0])[0][0]
                                row_index = np.where(locator.ROW_LABELS == jongsung[-1])[0][0]
                                dump.append(locator.TABLE[row_index, col_index])
                        else:
                            dump.append(LATIN["CHOSUNG"][chosung[0]])
                else:
                    if jongsung:
                        dump.append(LATIN["JONGSUNG"][jongsung[0]])
                if jungsung:
                    dump.append(jungsung.lower())
                else:
                    dump.append(block[2])
            result.append("".join(dump))
        else:
            result.append(word)

    return "".join(result)
