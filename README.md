# :loudspeaker: СМС-рассылка через GSM-модем
### **Версия:** 1.0.2 
![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=appveyor) ![Kivy 2.1.0](https://img.shields.io/badge/Kivy-2.1.0-blue?style=flat-square&logo=appveyor) ![Kivymd 1.1.1](https://img.shields.io/badge/KivyMD-1.1.1-blue?style=flat-square&logo=appveyor) ![Gammu 3.2.4](https://img.shields.io/badge/Gammu-3.2.4-blue?style=flat-square&logo=appveyor) ![Pyserial 3.5](https://img.shields.io/badge/Pyserial-3.5-blue?style=flat-square&logo=appveyor)  ![Enchant 0.0.1](https://img.shields.io/badge/Enchant-0.0.1-blue?style=flat-square&logo=appveyor) ![Pyperclip 1.8.2](https://img.shields.io/badge/Pyperclip-1.8.2-blue?style=flat-square&logo=appveyor)

![Иллюстрация к проекту](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg3Bd2c4DdhYX0o529_qViF0wTVkM2JUlW6efTStmtZ8D99rHtWHTyuJDHruW0FUFf6XYIiGXprt55TbqYoH6ZvxJF1ZZekUfjOEFnFuBn5ZYmgS7CG2lOaq5K0t-PXZnusiWbHSAJlTjf3o1n_vq1f5Dp5CjykuVemez-kE1UVKH2huiZ9hBZ4rmmeww/s1600/img.png)
## Описание программы
Данная программа позволяет производить рассылку СМС через USB-модем, количество абонентов и символов в тексте СМС не имеет значения.
Программа поддерживает большинство модемов и gsm-модулей (полный список: [ru.wammu.eu/phones/](https://ru.wammu.eu/phones/)). Протестировано на модемах iRZ TU32 и Huawei Е352.

## Версии
### V1.0.1 - 11.2022
- [x] Реализована функция проверки орфографии (опечаток) в тексте (кнопка АВС).
### V1.0.2 - 04.2023
- [x] Изменен раздел меню **Журнал**: данные представлены в виде таблицы (использован kivymd).
- [x] Использованы иконки в меню **Список рассылки**.
- [x] Добавлен счетчик отправленных сообщений.

## Установка под ОС 
Скачать программу можно скачать с репозитория [telnex/SMSKivy/releases](https://github.com/telnex/SMSKivy/releases) (Windows x64). Распакуйте архив и запустите файл sms.exe.

## Настройка 
Откройте раздел **Настройки** и укажите COM-порт устройства. В данном разделе отображаются доступные для подключения устройства. Так же список доступных устройств можно получить штатными средствами ОС. **Для  Windows:**  через штатный диспетчер задач необходимо выяснить номер com-порта вашего устройства, указать данный порт в настройка программы (только цифра). **Для Ubuntu/Mac OS:** через команду ``` ls /dev/ ``` выяснить номер com-порта. Возможно, необходимо использовать дополнительное оборудование (переходник com->USB).

## Сборка программы под Windows 
Поместите исходный код программы в папку ``` test/src/```, в папку ``` test/``` добавьте файл single.spec и выполните команду ``` python -m PyInstaller single.spec```.
После сборки .exe файла скопируйте в ``` test/dist/``` папки data, kvlang и style, а также файл ``` gammurc```.

**Важно!** Протестированно на версии pyinstaller 5.6.2, на версии pyinstaller 5.9.0 возникает ошибка:
```buildoutcfg
Traceback (most recent call last):
  File "logging\__init__.py", line 1103, in emit
AttributeError: 'NoneType' object has no attribute 'write'
```

### Файл single.spec
```python
# -*- mode: python -*-
import sys
from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

app_name = 'SMS'
sys.path += ["src\\"]
a = Analysis(['src\\main.py'],
pathex=['C:\\Users\\Admin\\Desktop\\test'],
binaries=None,
datas=None,
hiddenimports=[
  'webbrowser',
  '__init__',
  'data.__init__',
  'data.screens.__init__',
  'data.screens.dbmanager',
  'data.screens.db_kv.__init__',
  'data.screens.db_kv.backupsd',
  ],
  hookspath=[kivymd_hooks_path],
  runtime_hooks=[],
  excludes=[],
  win_no_prefer_redirects=False,
  win_private_assemblies=False)
# exclusion list
from os.path import join
from fnmatch import fnmatch
exclusion_patterns = (
  join("kivy_install", "data", "images", "testpattern.png"),
  join("kivy_install", "data", "images", "image-loading.gif"),
  join("kivy_install", "data", "keyboards*"),
  join("kivy_install", "data", "settings_kivy.json"),
  join("kivy_install", "data", "logo*"),
  join("kivy_install", "data", "fonts", "DejaVuSans*"),
  join("sdl2-config"),
  # Filter app directory
  join(".idea*"),
  join("gammurc")
)
def can_exclude(fn):
    for pat in exclusion_patterns:
        if fnmatch(fn, pat):
            return True
a.datas = [x for x in a.datas if not can_exclude(x[0])]
a.binaries = [x for x in a.binaries if not can_exclude(x[0])]
# Filter app directory
appfolder = [x for x in Tree('src\\', excludes=['*.py','*.pyc']) if not can_exclude(x[0])]  
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(pyz,
  a.scripts,
  appfolder,
  a.binaries,
  a.zipfiles,
  a.datas,
  *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins )],
  name=app_name,
  debug=False,
  strip=False,
  upx=True,
  console=False)
  ```

## FAQ
### Драйвер
Данное приложение не имеет встроенного драйвера для USB-модема, в качестве решения необходимо установить стандартное приложение для модема. Например, huawei.mobzon.ru/huawei-modem-nano.

### Некорректная работа программы
Инициализация модема происходит при запуске программы и при отправке СМС. В случае некорректной работы, необходимо перезагрузить приложение.

### Не работает проверка орфографии
Необходимо скопировать «ru_RU.aff» и «ru_RU.dic» с [github.com/LibreOffice](https://github.com/LibreOffice/dictionaries/tree/master/ru_RU) в ``` C:\...\site-packages\enchant\data\mingw64\share\enchant\hunspell```.