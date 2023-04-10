import json
import serial.tools.list_ports
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar


class SetConfig(Screen):
    """ Окно настроек программы """
    com_port = ObjectProperty()
    logging = ObjectProperty()
    save_btn = ObjectProperty()
    port_lb = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.config = self.JSON()
        self.com_port.text = self.config['com_port']
        if self.config['logging'] == 1:
            self.logging.active = True
        else:
            self.logging.active = False
        ports = serial.tools.list_ports.comports()
        connected = []
        if len(ports) != 0:
            for element in ports:
                connected.append(element.description)
            self.port_lb.text = '[b]ДОСТУПНЫ ДЛЯ ПОДКЛЮЧЕНИЯ:[/b]\n'
            for port in connected:
                if port.find('3G PC UI') != -1:  # FOR iRZ/E3xx modem
                    self.port_lb.text += f'[b][size=12]{port}[/size][/b]\n'
                else:
                    self.port_lb.text += f'[size=12]{port}[/size]\n'


    def JSON(self) -> object:
        with open('./data/config.json', 'r') as f:
            data = json.load(f)
        return data

    def SaveConfig(self):
        """ Сохранить настройки """
        w = self.JSON()
        Error = False
        if not Error:
            w['com_port'] = self.com_port.text.strip()
            if self.logging.active:
                w['logging'] = 1
            else:
                w['logging'] = 0
            self.save_btn.disabled = True
            with open('./data/config.json', 'w') as f:
                json.dump(w, f)
            # Запись файла конфигурации GAMMU
            if w['com_port'].isdigit():
                gammuConfig = f"[gammu]\ndevice = COM{w['com_port']}\nconnection = at"
            else:
                gammuConfig = f"[gammu]\ndevice = {w['com_port']}\nconnection = at"
            with open('gammurc', 'w') as f:
                f.write(gammuConfig)
            Snackbar(text="Настройки сохранены!", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=.4,
                     bg_color=(0.05, 0.42, 0.24, 1)).open()
