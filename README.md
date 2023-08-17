# py_miner
Python Minecraft miner for Excalibur-Craft

EN:  
Needed libraries:  
I'll do that later. For now, look at the errors, and use `pip install`

How to use:  
I'll translate later, just use Google Translate for now, thx :BASED:

RU:  
Как запустить:  
  
Windows:  
1. Установить Python:  
    a. Перейти по ссылке: https://www.python.org/downloads/, и скачать установщик  
    b. Запустить установку, обязательно не забыв поставить галочку добавления в PATH, а то придется ставить самому  
    c. Запустить новую (обязательно новую) командную строку, и проверить установку командой `python --version`  
2. Проверить наличие pip'a:  
    a. Ввести в командную строку команду `pip --version`. Если выводится версия, то все хорошо. Если нет,  
    b. Установить pip. Вот туториал: https://pythonru.com/baza-znanij/ustanovka-pip-dlja-python-i-bazovye-komandy  
3. Поставить необходимые библиотеки следющими командами:  
    a. `pip install pywin32`  
    b. `pip install pynput`  
4. Пробовать запустить скрипт  
  
Linux:  
Если у тебя Линукс, можно разобраться и самому (мне лень)  
  
MacOS:  
Ваще хз, не буду туда лезть  
  
Как какать:  
Способ работы скрипта основан на наличии статуса DELUXE для флая и супер-кирки.

Начнем:  
1. Поменять константу `PLAYER_NAME` на свой ник  
2. Поменять константу `TO_MINE_LENGTH` на длину слоя, которую нужно выкопать (расстояние, короче)  
3. Прожать в игре F3+P, чтобы убрать паузу при сворачивании  
4. Расположить персонажа:  
    a. Включить режим полета командой `/dfly`  
    b. Включить супер-кирку командой `/spa`  
    с. Встать в начало первого блока слоя (ниже скрин)  
    d. Взять в руки кирку  
5. Выйти из полноэкранного режима  
6. Не нажимая паузу и не открывая чат, свернуть окно (Alt + Tab, например)  
7. Запустить скрипт в терминале командой `python ./main.py`  

![Alignment example](alignment.png)

PS:  
Иногда по какой-то причине (непонятной) выходит так, что игрок пролетает за слой больше, чем нужно. Можно подкорректировать самому или же просто перезапустить скрипт.

Как корректировать движение во время работы скрипта:  
Если скрипт летает вперед больше, чем нужно, недолго прожать кнопку движения назад, но ТОЛЬКО ТОГДА, когда игрок уже движется вперед, иначе игрок встанет, и нужно будет перезапускать скрипт. В обратную сторону (назад) работает так же, но наоборот.