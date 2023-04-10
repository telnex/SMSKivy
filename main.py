import str_text
from kivymd.app import MDApp as App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.config import Config
from Screen.Windows import *
from Screen.AlertList import *
from Screen.EventLog import *
from Screen.SetConfig import *

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '400')
Config.write()


def LoadConfig():
    with open('./data/config.json', 'r') as f:
        data = json.load(f)
    return data


def AppLog(msg):
    data = LoadConfig()
    if data.get('logging', 0) == 1:
        with open(f'./data/log/{time.strftime("%d_%m_%y_%H_%M")}.log', 'a+') as f:  # a+
            f.write(msg)


class MainApp(App):
    """ Запуск приложения """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        file_kv = ['Windows.kv', 'AlertList.kv', 'SetConfig.kv', 'EventLog.kv']
        for file in file_kv:
            with open(os.path.join(os.getcwd(), 'kvlang', file), encoding="utf-8") as KV:
                Builder.load_string(KV.read())

    def build(self):
        self.title = 'СМС-рассылка'
        self.theme_cls.theme_style = "Light"
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(Windows(name='main'))
        sm.add_widget(AlertList(name='alertlist'))
        sm.add_widget(SetConfig(name='setconfig'))
        sm.add_widget(EventLog(name='eventlog'))
        return sm

    def parse(self, msg):
        if msg == 'info':
            return str_text.info


if __name__ == "__main__":
    MainApp().run()
