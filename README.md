# C++ Compile Helper
**EN:**
This script makes it easy to compile C/C++ files without fiddling with build systems or searching for compilers. It automatically finds potential compilers, checks their functionality, and then offers you a convenient list of compilers to compile your files with. This project may be useless to experienced users (or even to everyone). I created it simply because I need programming practice. I'd be happy if this simple utility helps C++ beginners.
##
**RU:**
Этот скрипт позволяет легко компилировать C/C++ файлы, не возясь с системами сборки и поиском компиляторов. Он автоматически находит потенциальные компиляторы, проверяет их на работоспособность, а затем предлагает вам скомпилировать свои файлы с помощью него, выводя удобный список.

Возможно, этот проект не будет бесполезен опытным пользователям (а может даже и всем). Я сделал его лишь потому, что мне нужна практика в программировании. Я буду рад, если новичкам в C++ поможет эта простая утилита. 
# Usage / Использование
**EN:**
Download archive from [release](https://github.com/qwoj274/C-Compile-Helper/releases/tag/release). Unzip it into the same folder as your cpp file, then run `build.exe`.  The compilation result will be displayed in the console. If anything goes wrong, you can check `./debug/log.txt`. 

You can change the language in the _internal/lang/lang.cfg file. Available languages:
 - Russian `ru`
 - English `en` 
 
 You can add your own language by copying one of the language JSON files and entering your own values ​​for the options. 

>  This program searches for compiler executables based on the PATH environment variable. You can expand the list of available compiler by editing `_intertal/compilers.json`.

You can also customize the compilation arguments by editing `_intertal/compiler_args.json`. Simply remove or add arguments to the "args" array:

    {
        "args" : [
            "-std=c++23",
            "-Wall",
            "-another-arg",
            "-another-arg"
        ]
    }
##
**RU:**
Скачайте архив из [релизов](https://github.com/qwoj274/C-Compile-Helper/releases/tag/release). Распакуйте его в ту же папку, где находится ваш cpp-файл, а затем запустите `build.exe`. Результат компиляции будет в консоли. Если что-то пойдет не так, вы можете проверить `./debug/log.txt`.

Вы можете поменять язык в файле `_internal/lang/lang.cfg`. Доступные языки:

 - `ru` Русский
 - `en` Английский
 
 Вы можете добавить свой язык, скопировав какой-нибудь из json-файлов с языками и прописав свои значения для предложений.
 

> Данная программа ищет исполняемые файлы компиляторов, основываясь на переменной окружения PATH. Вы можете пополнить список доступных программе компиляторов, редактируя `_intertal/compilers.json`.

Также вы можете настраивать аргументы для компиляции, редактируя файл `_intertal/compiler_args.json`. Просто удалите или добавьте в массив "args" аргументы:

    {
        "args" : [
            "-std=c++23",
            "-Wall",
            "-another-arg",
            "-another-arg"
        ]
    }

# Building from source code / Самостоятельная сборка проекта
**EN:**
You need to install Python. Download my repository, unzip it somewhere, open a terminal in it and enter the following lines:

    pip install pyinstaller
    pyinstaller build.spec

Builded project will be in `dist/C++ Compile Helper` directory.
##
**RU:**
У вас должен быть установлен Python. Скачайте мой репозиторий, распакуйте куда-нибудь, откройте там терминал и введите следующее:

    pip install pyinstaller
    pyinstaller build.spec
В папке `dist/C++ Compile Helper` будет собранный проект.

