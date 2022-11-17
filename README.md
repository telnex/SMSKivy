# СМС-рассылка через GSM-модем
**Версия:** 1.0.0 | **Python:** 3.9 | **Kivy:** 2.1 | **Gammu:** 3.2.4

![Иллюстрация к проекту](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjOQifOGxT15hvFsdkp1D8cri-QhD3z5VGk8d6UNqNvWyXcse-6-dtrrpgNvD4JI1ve8my5T6IZiFTl9SnuV4-aCuOwWUnYs-gaVe9e4We6LZQTEBohIBfqJrwDA0SN3-I5jAd-1vFY6ksDdDHRuTt9jOaXIkiIIRX5ScLOFA0j5FdlL0EPTZSI_mjMmA/s1600/photo_2022-07-14_01-38-19.jpg)
## Описание программы
Данное ПО позволяет производить рассылку СМС на указанный список адресатов, количество абонентов и символов в тексте СМС не имеет значения *(рекомендуемый размер СМС: 250-300 символов = 2 СМС)*. Программа поддерживает большинство модемов и gsm-модулей (полный список: [ru.wammu.eu/phones/](https://ru.wammu.eu/phones/)). Функционал программы обусловлен производственной необходимостью, т.е. программа создавалась под конкретные цели, с минимальным функционалом, необходимым для выполнения поставленных задач. 
При запуске программы происходит инициализация соединения с модемом. В случае, если возникают ошибки, необходимо перезапустить программу.

## Установка под ОС
Скачать программу можно скачать с репозитория [telnex/SMSKivy/releases](https://github.com/telnex/SMSKivy/releases) (Windows x64). Распакуйте архив и запустите файл sms.exe.

## Настройка
Откройте раздел **Настройки** и укажите COM-порт устройства. В данном разделе отображаются доступные для подключения устройства. Так же список доступных устройств можно получить штатными средствами ОС. **Для  Windows:**  через штатный диспетчер задач необходимо выяснить номер com-порта вашего устройства, указать данный порт в настройка программы (только цифра). **Для Ubuntu/Mac OS:** через команду ``` ls /dev/ ``` выяснить номер com-порта. Возможно, необходимо использовать дополнительное оборудование (переходник com->USB).

## Сборка программы под Windows
Поместите исходный код программы в папку ``` test/src/```, в папку ``` test/``` добавьте файл single.spec и выполните команду ``` python -m PyInstaller single.spec```.
После сборки .exe файла скопируйте в ``` test/src/``` папки data, kvlang и style.

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
