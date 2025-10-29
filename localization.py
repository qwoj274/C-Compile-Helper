from json import load
from os.path import exists
from enum import StrEnum
import prof

class Input(StrEnum):
    K_AVAILAVBLE_COMPILERS = "K_AVAILAVBLE_COMPILERS"
    K_WTU = "K_WTU"
    K_CHOOSEN_COMPILER = "K_CHOOSEN_COMPILER"
    K_INVALID_INPUT = "K_INVALID_INPUT"
    K_NO_COMPILERS = "K_NO_COMPILERS"
    K_NO_CPP = "K_NO_CPP"
    K_PRESS_ANY_KEY = "K_PRESS_ANY_KEY"
    K_COMPILER_TESTING = "K_COMPILER_TESTING"
    K_COMPILER_PASSED = "K_COMPILER_PASSED"
    K_COMPILER_FAILED = "K_COMPILER_FAILED"
    K_COMPILER_ARGS_CLARIFY = "K_COMPILER_ARGS_CLARIFY"
    K_CPP_FILES = "K_CPP_FILES"
    K_WFU = "K_WFU"
    K_CHOOSEN_CPP = "K_CHOOSEN_CPP"
    K_COMPILATION_PROCESS = "K_COMPILATION_PROCESS"
    K_EXITCODE = "K_EXITCODE"


if prof.PROFILE=="DEBUG":
    LANGPATH = "lang"
elif prof.PROFILE=="RELEASE":
    LANGPATH = "_internal\\lang"


if exists(f"{LANGPATH}/lang.cfg"):
    LANGUAGE: str = open(f"{LANGPATH}/lang.cfg").readline()
else:
    raise FileNotFoundError("Language file not found!")


locFile: dict = {}

LANFILEPATH = f"{LANGPATH}\\{LANGUAGE}.json"
if exists(LANFILEPATH):
    locFile: dict = load(open(LANFILEPATH, "r", encoding='utf-8'))
else:
    raise FileNotFoundError(f"{LANGUAGE}.json language not found in languages directory!")


class Sentence:
    def __init__(self, keyword):
        self.keyword = keyword
        if locFile == {}:
            self.languageInterpretation = keyword
            return
        
        try:
            self.languageInterpretation = locFile[keyword]
        except KeyError:
            self.languageInterpretation = keyword
    
    def __repr__(self) -> str:
        return self.languageInterpretation
