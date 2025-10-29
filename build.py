import os
from localization import Sentence, Input

import prof
import subprocess
from enum import Enum
from datetime import datetime
from sys import exit as exitScript
import json

from termcolor.termcolor import colored
import glob


def time() -> str:
    now = datetime.now()
    return now.strftime("%H:%M:%S")


class DebugTypes(Enum):
    DEBUG = 0
    WARN = 1
    ERR = 2


class DebugLogger:
    LOGTYPES: dict = {
        DebugTypes.DEBUG : "DEBUG",
        DebugTypes.WARN : "WARN",
        DebugTypes.ERR : "ERR"
    }
    
    DEBUGFILE = "log.txt"
    DEBUGFILEPATH = "debug/" + DEBUGFILE
    debugFile = None
    
    @staticmethod
    def init():
        DebugLogger.createDebugDir()
        DebugLogger.rawLog("======== BUILD SCRIPT ========")

    @staticmethod
    def log(value: str, debugType: DebugTypes = DebugTypes.DEBUG):
        if DebugLogger.debugFile:
            DebugLogger.debugFile.write(f"[{time()}] {DebugLogger.LOGTYPES[debugType]}: {value}\n")
            return
        raise FileNotFoundError()

    @staticmethod
    def rawLog(value: str):
        if DebugLogger.debugFile:
            DebugLogger.debugFile.write(value + "\n")
            return
        raise FileNotFoundError()
    
    @staticmethod
    def createDebugDir():
        debugDirExists: bool = os.path.isdir("debug")
        if not debugDirExists:
            os.makedirs("debug")
            
        debugFileExists = os.path.isfile(DebugLogger.DEBUGFILEPATH)
        
        DebugLogger.debugFile = open(file=DebugLogger.DEBUGFILEPATH, mode="a")
        # file opening after file existing checking
        # its needed for correct \n inserting
        # if file is not exist before file opening then we dont need to insert \n
        if debugFileExists:
            DebugLogger.debugFile.write("\n")


class Compiler:
    BUILDDIR = "build"
    if prof.PROFILE=="RELEASE":
        ARGSFILEPATH = "_internal\\compiler_args.json"
    elif prof.PROFILE=="DEBUG":
        ARGSFILEPATH = "compiler_args.json"
    PATH_ENV = os.environ.get('PATH')
    path_dirs = set(PATH_ENV.split(os.pathsep))
    
    compilersDescriptionDict = dict()
    availableCompilers = []
    availableCppFiles = []
    compilersCount: int = 0
    compilerArgs = ()
    
    currentCompiler: Compiler
    
    cppToCompile: str
    outputFile: str
    
    
    def __init__(self, name: str, fullpath: str):
        self.name = name
        self.isValid = True
        self.fullpath = fullpath
    
    
    @staticmethod
    def init() -> int:
        Compiler.compilersDescriptionDict = Compiler.setupAvaliableCompilers()
        Compiler.createBuildDir()
        
        if not os.path.exists(Compiler.ARGSFILEPATH):
            DebugLogger.log("args file not found! compiling will be without args", DebugTypes.WARN)
        else:
            args = json.load(open(Compiler.ARGSFILEPATH))
            Compiler.compilerArgs = args["args"]

        
        if not Compiler.searchForCompilers():
            DebugLogger.log("no compilers! exiting...", DebugTypes.ERR)
            return 1
        
        if not Compiler.searchForCppFiles():
            DebugLogger.log("no CPP files! exiting...", DebugTypes.ERR)
            return 2
        
        return 0
    
    
    @staticmethod
    def createBuildDir():
        if os.path.isdir(Compiler.BUILDDIR):
            DebugLogger.log("build dir already exists!", DebugTypes.WARN)
            return
        DebugLogger.log("created build dir!")
        os.makedirs(Compiler.BUILDDIR)
    
    
    @staticmethod
    def setupAvaliableCompilers() -> dict:
        if prof.PROFILE=="RELEASE":
            COMPILERSPATH="_internal\\compilers.json"
        elif prof.PROFILE=="DEBUG":
            COMPILERSPATH="compilers.json"
        
        if os.path.exists(COMPILERSPATH):
            jsonWithAvaliableCompilers = json.load(open(COMPILERSPATH))
        else:
            DebugLogger.log("compilers.json not found!", DebugTypes.ERR)
            raise FileNotFoundError("compilers.json not found!")
        return jsonWithAvaliableCompilers
        
        
    @staticmethod
    def searchForCompiler(compilerName: str):
        foundPaths = list()
        for path in Compiler.path_dirs:
            if path == '':
                continue
            
            if path in foundPaths:
                continue
            
            fullpath = path + compilerName if path[-1]=="\\" else path + "\\" + compilerName 
            if os.path.exists(fullpath):
                _compiler = Compiler(compilerName, fullpath)
                if _compiler in Compiler.availableCompilers:
                    return
                Compiler.availableCompilers.append(_compiler)
                _compiler.isValid =  Compiler.validate(_compiler)
                Compiler.compilersCount+=1
        return foundPaths
    
    
    @staticmethod
    def searchForCppFiles() -> bool:
        cppFiles = glob.glob("*.cpp")
        # deleting ".cpp" from names
        cppFiles = list(map(lambda s: s[:-4], cppFiles))
        if len(cppFiles) == 0:
            return False
        Compiler.availableCppFiles = cppFiles
        return True
    
    
    @staticmethod
    def searchForCompilers():
        for compiler in list(Compiler.compilersDescriptionDict.keys()):
            paths = Compiler.searchForCompiler(compiler)
            if len(paths) == 0:
                continue
            DebugLogger.log(f"found {compiler} in:\n\t{"\n\t".join(paths)}")
            Compiler.availableCompilers.append(compiler)
            continue
        
        if Compiler.compilersCount == 0:
            return False
        return True


    @staticmethod
    def setCompiler(choice):
        try:
            choice = int(choice)
        except ValueError:
            return False
        
        if choice<=0:
            return False
        
        if choice>len(Compiler.availableCompilers):
            return False
        
        Compiler.currentCompiler = Compiler.availableCompilers[choice-1]
        if not Compiler.currentCompiler.isValid:
            DebugLogger.log(f"choosen compiler is not valid!")
            return False
        
        DebugLogger.log(f"choosen compiler: {Compiler.currentCompiler}")
        return True

    
    @staticmethod
    def setCppFile(choice) -> False:
        try:
            choice = int(choice)
        except ValueError:
            return False
        
        if choice<=0:
            return False
        
        if choice>len(Compiler.availableCppFiles):
            return False

        Compiler.cppToCompile = Compiler.availableCppFiles[choice-1]
        
        return True
        

    @staticmethod
    def validate(compiler: Compiler) -> bool:
        if prof.PROFILE=="RELEASE":
            TESTDIR = "_internal\\compiler_test"
        elif prof.PROFILE=="DEBUG":
            TESTDIR = "compiler_test"
        
        if not os.path.isdir(TESTDIR):
            DebugLogger.log("dir for compiler testing is not found!", DebugTypes.ERR)
            raise NotADirectoryError("dir for compiler testing is not found!")
        
        print(f"{Sentence(Input.K_COMPILER_TESTING)}{compiler.name} . . .")
        compiledSuccessfully = compiler.compile(inputCppPath=f"{TESTDIR}\\test", outputPath=TESTDIR)
        
        testFile = open(f"{TESTDIR}\\test.txt", mode="w")
        
        
        if compiledSuccessfully:
            subprocess.run(f"{TESTDIR}\\test.exe", stdout=testFile)
        else:
            DebugLogger.log(f"output file not received!", DebugTypes.ERR)
            print(colored(f"{Sentence(Input.K_COMPILER_FAILED)}", "red"))
            return False
            
        testFile = open(f"{TESTDIR}\\test.txt", mode="r")
        
        isValid: bool = testFile.readline() == "TEST STRING"
        
        testFile.close()
        os.remove(f"{TESTDIR}\\test.txt")
        os.remove(f"{TESTDIR}\\test.exe")
        
        if isValid:
            DebugLogger.log(f"{compiler.name} passed!")
            print(colored(f"{Sentence(Input.K_COMPILER_PASSED)}", "green"))
            return True
        DebugLogger.Log(f"{compiler.name} failed!", DebugTypes.ERR)
        print(colored(f"{Sentence(Input.K_COMPILER_FAILED)}", "red"))
        
        
    def compile(self, inputCppPath: str, outputPath: str, outputFileName: str = "", outputExtension: str=".exe", args: list = []) -> bool:
        if not self in Compiler.availableCompilers:
            DebugLogger.log("compiler not found in list!", DebugTypes.ERR)
            return False

        if not self.isValid:
            DebugLogger.log("compiler is not valid!", DebugTypes.ERR)
            return False

        if not os.path.isfile(inputCppPath + ".cpp"):
            DebugLogger.log(f"{inputCppPath}.cpp is not exist!", DebugTypes.ERR)
            return False
        
        if not os.path.isdir(outputPath):
            DebugLogger.log("output dir is not exist!", DebugTypes.ERR)
            return False

        INPUTFILE = inputCppPath.split('\\')[-1]
        
        if outputFileName == "":
            outputFileName = INPUTFILE
            
        
        OUTPUTFILE = outputFileName + outputExtension

        DebugLogger.log(f"compiling {INPUTFILE} with {self.fullpath} . . .")
        DebugLogger.log(f"output file: {OUTPUTFILE}")
        command: list = [self.name] + args + [inputCppPath+".cpp", '-o', outputPath + "\\" + OUTPUTFILE]
        subprocess.call(command)
        
        if os.path.isfile(outputPath + "\\" + OUTPUTFILE):
            Compiler.outputFile = outputPath + "\\" + OUTPUTFILE
            return True

        return False


def exitDialogCaused(cause: str):
    print(cause)
    input(Sentence(Input.K_PRESS_ANY_KEY))
    exitScript()


if __name__ == "__main__":
    DebugLogger.init()
    
    tryToInitCompilers = Compiler.init()
    
    if tryToInitCompilers == 1:
        exitDialogCaused(Sentence(Input.K_NO_COMPILERS))
    elif tryToInitCompilers == 2:
        exitDialogCaused(Sentence(Input.K_NO_CPP))
        
    
    print(colored(Sentence(Input.K_AVAILAVBLE_COMPILERS), "blue"))
    for index, compiler in enumerate(Compiler.availableCompilers):
        validStatus: str = colored("VALID", "green") if compiler.isValid else colored("INVALID", "red")
        print(f"{index+1}) {Compiler.compilersDescriptionDict[compiler.name]} ({compiler.fullpath}) : {validStatus}")
    
    choice = input(f"{Sentence(Input.K_WTU)} (1-{len(Compiler.availableCompilers)}): ")
    
    if not Compiler.setCompiler(choice):
        exitDialogCaused(Sentence(Input.K_INVALID_INPUT))
        
    print(f"{colored(Sentence(Input.K_CHOOSEN_COMPILER), "blue")} {Compiler.currentCompiler.name} ({Compiler.currentCompiler.fullpath})\n")
    print(f"{colored(Sentence(Input.K_COMPILER_ARGS_CLARIFY), "red", "on_white")} {Compiler.compilerArgs}")
    input(Sentence(Input.K_PRESS_ANY_KEY))
    
    os.system('cls')
    
    print(colored(Sentence(Input.K_CPP_FILES), "blue"))
    for index, cppFile in enumerate(Compiler.availableCppFiles):
        print(f"{index+1}) {cppFile}.cpp")
    
    choice = input(f"{Sentence(Input.K_WFU)} (1-{len(Compiler.availableCppFiles)}): ")
    
    if not Compiler.setCppFile(choice):
        exitDialogCaused(Sentence(Input.K_INVALID_INPUT))
    
    print(f"{colored(Sentence(Input.K_CHOOSEN_CPP), "blue")}{Compiler.cppToCompile}.cpp")
    print(f"{Sentence(Input.K_COMPILATION_PROCESS)}")
    input(Sentence(Input.K_PRESS_ANY_KEY))
    
    os.system('cls')
    
    compiledSuccessfully = Compiler.currentCompiler.compile(
        Compiler.cppToCompile,
        f"{Compiler.BUILDDIR}",
        args=Compiler.compilerArgs
    )
    
    if compiledSuccessfully:
        exitCode = subprocess.run([Compiler.outputFile])
        DebugLogger.log(f"exit code: {exitCode.returncode}")
        print(f"{colored(Sentence(Input.K_EXITCODE), "green")} {exitCode.returncode}")
        input(Sentence(Input.K_PRESS_ANY_KEY))