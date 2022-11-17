import str_text
import os
from kivy.app import App
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
        msg_LOG = f'[color=#616161]{time.strftime("%d.%m.%y %H:%M")}[/color] - {msg}\n'
        with open('./data/app.log', 'a+') as f:  # a+
            f.write(msg_LOG)


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
