# :loudspeaker: СМС-рассылка через GSM-модем / SMS sending
**Версия:** 1.0.1 | **Python:** 3.9 | **Kivy:** 2.1 | **Gammu:** 3.2.4

![Иллюстрация к проекту](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg3Bd2c4DdhYX0o529_qViF0wTVkM2JUlW6efTStmtZ8D99rHtWHTyuJDHruW0FUFf6XYIiGXprt55TbqYoH6ZvxJF1ZZekUfjOEFnFuBn5ZYmgS7CG2lOaq5K0t-PXZnusiWbHSAJlTjf3o1n_vq1f5Dp5CjykuVemez-kE1UVKH2huiZ9hBZ4rmmeww/s1600/img.png)
## Описание программы / Program description
Данное ПО позволяет производить рассылку СМС на указанный список адресатов, количество абонентов и символов в тексте СМС не имеет значения *(рекомендуемый размер СМС: 250-300 символов = 2 СМС)*. Программа поддерживает большинство модемов и gsm-модулей (полный список: [ru.wammu.eu/phones/](https://ru.wammu.eu/phones/)). Функционал программы обусловлен производственной необходимостью, т.е. программа создавалась под конкретные цели, с минимальным функционалом, необходимым для выполнения поставленных задач. 
При запуске программы происходит инициализация соединения с модемом. В случае, если возникают ошибки, необходимо перезапустить программу.

:speaking_head: This software allows you to send SMS to a specified list of recipients, the number of subscribers and characters in the SMS text does not matter *(recommended SMS size: 250-300 characters = 2 SMS)*. The program supports most modems and gsm modules (full list: [en.wammu.eu/phones/](https://en.wammu.eu/phones/)).
When the program starts, the connection with the modem is initialized. If errors occur, you must restart the program.

### V1.0.1
- [x] Реализована функция проверки орфографии (опечаток) в тексте (кнопка АВС).

## Установка под ОС / OS installation
Скачать программу можно скачать с репозитория [telnex/SMSKivy/releases](https://github.com/telnex/SMSKivy/releases) (Windows x64). Распакуйте архив и запустите файл sms.exe.

:speaking_head: You can download the program from the repository [telnex/SMSKivy/releases](https://github.com/telnex/SMSKivy/releases/tag/v1.0.1_En) (Windows x64 English). Unzip the archive and run the sms.exe file

## Настройка / Setting
Откройте раздел **Настройки** и укажите COM-порт устройства. В данном разделе отображаются доступные для подключения устройства. Так же список доступных устройств можно получить штатными средствами ОС. **Для  Windows:**  через штатный диспетчер задач необходимо выяснить номер com-порта вашего устройства, указать данный порт в настройка программы (только цифра). **Для Ubuntu/Mac OS:** через команду ``` ls /dev/ ``` выяснить номер com-порта. Возможно, необходимо использовать дополнительное оборудование (переходник com->USB).

:speaking_head: Open the **Settings** section and specify the COM port of the device. This section displays the devices available for connection. You can also get a list of available devices using regular OS tools. **For Windows:** through the regular task manager, you need to find out the com-port number of your device, specify this port in the program settings (only a number). **For Ubuntu/Mac OS:** use the command ``` ls /dev/ ``` to find out the com port number. You may need to use additional equipment (com->USB adapter).

## Сборка программы под Windows / Building a program for Windows
Поместите исходный код программы в папку ``` test/src/```, в папку ``` test/``` добавьте файл single.spec и выполните команду ``` python -m PyInstaller single.spec```.
После сборки .exe файла скопируйте в ``` test/dist/``` папки data, kvlang и style, а также файл ``` gammurc```.

:speaking_head: Place the source code of the program in the folder ``` test/src/```, in the folder ``` test/``` add the file single.spec and run the command ``` python -m PyInstaller single.spec```.
After building the .exe file, copy the data, kvlang and style folders to ``` test/dist/```, as well as the ``` gammurc``` file.

### Файл single.spec
```python
# -*- mode: python -*-
from kivy_deps import sdl2, glew
import sys
app_name = 'SMS'
sys.path += ["src\\"]
a = Analysis(['src\\main.py'],
  pathex=['C:\\Users\\Admin\\Desktop\\test\\'],
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
  hookspath=[],
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