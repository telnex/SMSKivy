from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class EventLog(Screen):
    label_log = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    def on_enter(self, *args):
        with open('./data/app.log', 'r') as f:
            self.label_log.text = f.read()

    def DelLog(self):
        with open('./data/app.log', 'w') as f:
            f.write('')
        self.label_log.text = ''
