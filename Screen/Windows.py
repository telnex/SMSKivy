# Скопировать «ru_RU.aff» и «ru_RU.dic» с https://github.com/LibreOffice/dictionaries/tree/master/ru_RU
# в C:\...\site-packages\enchant\data\mingw64\share\enchant\hunspell»

import json
import gammu
import threading
import time
import str_text as st
import pyperclip
import enchant
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from functools import partial
from kivy.clock import Clock
from main import AppLog


class Windows(Screen):
    """ ГЛАВНЫЙ ЭКРАН """
    info_label = ObjectProperty()
    input_sms = ObjectProperty()
    log = ObjectProperty()
    config_label = ObjectProperty()
    progress_bar = ObjectProperty()
    start_btn = ObjectProperty()
    stop_btn = ObjectProperty()
    sym_info = ObjectProperty()
    sms_info = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.UpdLog(st.wel)
        self.info_label.text = '[b]СТАТУС:[/b] РАССЫЛКА НЕ ЗАПУЩЕНА'
        self.progress_bar.value = 0
        self.stop = False
        self.dialog = None
        self.start_btn.disabled = True
        self.stop_btn.disabled = True
        Clock.schedule_interval(self.SymSMS_info, 0.3)
        self.config_label.text = f"[b]МОДЕМ:[/b] ИНИЦИАЛИЗАЦИЯ"
        self.LoadDataModem()

    def LoadDataModem(self):
        """ Запускаем инициализацию в отдельном потоке """
        threading.Thread(target=self.ConnectModem).start()

    def ConnectModem(self):
        """ Инициализация модема """
        sm = gammu.StateMachine()
        try:
            sm.ReadConfig()
        except gammu.GSMError as e:
            err = eval(str(e))
            msg = f'ОШИБКА: {err["Text"]}'
            Clock.schedule_once(partial(self.UpdLog, msg, err=True))
            self.config_label.text = f"[b]МОДЕМ:[/b] ОШИБКА ЗАПУСКА ПРОГРАММЫ"
        else:
            try:
                sm.Init()
            except gammu.GSMError:
                self.config_label.text = f"[b]МОДЕМ:[/b] НЕТ СВЯЗИ С МОДЕМОМ"
            else:
                modem = sm.GetModel()
                try:
                    signal = sm.GetSignalQuality()
                except gammu.GSMError as e:
                    err = eval(str(e))
                    msg = f'ОШИБКА: {err["Text"]}'
                    Clock.schedule_once(partial(self.UpdLog, msg, err=True))
                    self.config_label.text = f'[b]МОДЕМ:[/b] {err["Text"]}'
                else:
                    netinfo = sm.GetNetworkInfo()
                    network = gammu.GSMNetworks.get(netinfo['NetworkCode'], 'Unknown')
                    self.config_label.text = f"[b]МОДЕМ:[/b] {modem[1]} | " \
                                             f"[b]СИГНАЛ:[/b] {network.upper()} {signal['SignalPercent']}%"
                    self.start_btn.disabled = False
                    sm.Terminate()

    def UpdLog(self, msg, dt=0, err=False):  # dt means delta-time
        """ Обновить TextInput мониторинга """
        if err:
            mess = f'[color=#a60000]{time.strftime("%H:%M")} - {msg}[/color]\n'
        else:
            mess = f'[color=#616161]{time.strftime("%H:%M")}[/color] - {msg}\n'
        self.log.text += mess

    def StartSMS(self, *args):
        """ Запускаем отправку смс в отдельном потоке """
        self.close_alert()
        threading.Thread(target=self.GammuStart).start()

    def GammuStart(self):
        """ Отправка СМС """
        data_tel = self.LoadNum()
        allName = {}
        count = 0
        msg_log = ''
        error = False
        self.stop = False
        self.progress_bar.value = 0
        if len(data_tel) == 0:
            msg = 'Список рассылки пуст, укажите абонентов!'
            Clock.schedule_once(partial(self.UpdLog, msg, err=True))
        else:
            progress_count = 100 / len(data_tel)
            for i, j in data_tel.items():
                allName[j] = i
            if self.input_sms.text == '':
                msg = 'Введите текст сообщения!'
                Clock.schedule_once(partial(self.UpdLog, msg, err=True))
            else:
                self.stop_btn.disabled = False
                self.start_btn.disabled = True
                self.info_label.text = f'[b]СТАТУС:[/b] РАССЫЛКА ЗАПУЩЕНА | [b]ОПОВЕЩЕНО:[/b] {count} ИЗ {len(allName)}'
                msg = f'РАССЫЛКА ЗАПУЩЕНА. Абонентов - {len(allName)}'
                Clock.schedule_once(partial(self.UpdLog, msg))
                state_machine = gammu.StateMachine()
                state_machine.ReadConfig()
                try:
                    state_machine.Init()
                except gammu.GSMError as e:
                    err = eval(str(e))
                    msg = f'ОШИБКА: {err["Text"]}'
                    Clock.schedule_once(partial(self.UpdLog, msg, err=True))
                    self.info_label.text = f'[b]СТАТУС:[/b] ОШИБКА #{err["Code"]}'
                    self.stop_btn.disabled = True
                    self.start_btn.disabled = False

                else:
                    sms_text = self.input_sms.text.strip()
                    sms_info = {
                        "Class": -1,
                        "Unicode": True,
                        "Entries": [
                            {
                                "ID": "ConcatenatedTextLong",
                                "Buffer": f"{sms_text}",
                            }
                        ],
                    }
                    encoded = gammu.EncodeSMS(sms_info)
                    msg_log += self.LogStr(f'[b]ОТПРАВКА СМС[/b]\nТекст: {sms_text}')
                    for tel in allName:
                        if self.stop:
                            msg = '[b]РАССЫЛКА ОСТАНОВЛЕНА![/b]'
                            msg_log += self.LogStr(msg)
                            AppLog(msg_log)
                            Clock.schedule_once(partial(self.UpdLog, msg))
                            self.info_label.text = f'[b]СТАТУС:[/b] РАССЫЛКА ОСТАНОВЛЕНА | ' \
                                                   f'[b]ОПОВЕЩЕНО: {count} ИЗ {len(allName)}[/b]'
                            self.stop = False
                            self.start_btn.disabled = False
                            self.stop_btn.disabled = True
                            state_machine.Terminate()
                            return True
                        else:
                            for message in encoded:
                                message["SMSC"] = {"Location": 1}
                                message["Number"] = tel
                                try:
                                    state_machine.SendSMS(message)
                                except gammu.GSMError as e:
                                    err = eval(str(e))
                                    msg = f'ОШИБКА: {tel} -> {err["Text"]}'
                                    msg_log += self.LogStr(msg)
                                    Clock.schedule_once(partial(self.UpdLog, msg, err=True))
                                    error = True
                                    # state_machine.Terminate()
                            if not error:
                                msg = f'[b]{allName[tel]}[/b] - оповещён.'
                                msg_log += self.LogStr(msg)
                                self.progress_bar.value = self.progress_bar.value + progress_count
                                Clock.schedule_once(partial(self.UpdLog, msg))
                                count = count + 1
                                self.info_label.text = f'[b]СТАТУС:[/b] РАССЫЛКА ЗАПУЩЕНА | ' \
                                                       f'[b]ОПОВЕЩЕНО: {count} ИЗ {len(allName)}[/b]'
                            else:
                                error = False
                    # счетчик сообщений
                    with open('./data/config.json', 'r') as f:
                        count_mess = json.load(f)
                    count_mess = count_mess + 1
                    with open('./data/config.json', 'w') as f:
                        json.dump(count_mess, f)

                    msg = f'[b]РАССЫЛКА ЗАВЕРШЕНА.[/b] Оповещено: {count} из {len(allName)}\n'
                    msg_log += self.LogStr(msg)
                    AppLog(msg_log)
                    Clock.schedule_once(partial(self.UpdLog, msg))
                    self.info_label.text = f'[b]СТАТУС:[/b] РАССЫЛКА ЗАВЕРШЕНА | ' \
                                           f'[b]ОПОВЕЩЕНО:[/b] {count} ИЗ {len(allName)}'
                    self.start_btn.disabled = False
                    self.stop_btn.disabled = True
                    self.progress_bar.value = 100
                    state_machine.Terminate()

    def LoadNum(self):
        with open('./data/dist_list.json', 'r') as f:
            data = json.load(f)
        return data

    def LogStr(self, msg: str):
        j = f'[color=#616161]{time.strftime("%d.%m.%y %H:%M")}[/color] - {msg}\n'
        return j

    def stop_send(self):
        self.stop = True

    def SymSMS_info(self, dt=0):
        data_sms = gammu.SMSCounter(self.input_sms.text, UDH='NoUDH', Coding='Default')
        self.sym_info.text = f'Символов: {len(self.input_sms.text)}/{data_sms[1]}'
        if data_sms[0] > 2:
            self.sms_info.text = f"Кол-во СМС: [color=#ff0000]{data_sms[0]}[/color]"
        else:
            self.sms_info.text = f"Кол-во СМС: {data_sms[0]}"

    def check_spelling(self):
        """ Запускаем проверку в отдельном потоке """
        threading.Thread(target=self.spelling).start()

    def spelling(self):
        """  Проверка орфографии """
        text = self.input_sms.text.split()
        dictionary = enchant.Dict("ru_RU")
        if len(text) != 0:
            corrected = f'[b]Орфография:[/b] {self.input_sms.text}'
            for word in text:
                word = word.replace('.', '')
                word = word.replace(',', '')
                if word.isalpha():
                    if dictionary.check(word) is False:
                        if word.upper() not in ['ЕВСПД', 'РСПД', 'ПРС', 'ГРС', 'ГПУ', 'УТТИСТ', 'ИТЦ', 'УПЦ']:
                            if len(dictionary.suggest(word)) != 0:
                                corrected = corrected.replace(word, f'[color=#ff0000]{word}[/color] '
                                                                    f'({dictionary.suggest(word)[0]})')
                            else:
                                corrected = corrected.replace(word, f'[color=#ff0000]{word}[/color]')
            Clock.schedule_once(partial(self.UpdLog, corrected))

    def PasteText(self, instance, touch):
        """ Вставка текста ПКМ """
        if touch.button == 'right':
            self.input_sms.text += pyperclip.paste()

    def show_alert(self):
        """ Подтверждение запуска рассылки """
        self.dialog = MDDialog(
            title='Запустить рассылку?',
            text="[color=#1a1a1a][size=14]Проверьте содержимое СМС и список рассылки![/size][/color]",
            md_bg_color='white',
            buttons=[
                MDRaisedButton(
                    text="ОТМЕНА",
                    theme_text_color="Custom",
                    md_bg_color='#0d6b3d',
                    on_release=self.close_alert,
                ),
                MDRaisedButton(
                    text="ДА",
                    theme_text_color="Custom",
                    md_bg_color='#0d6b3d',
                    on_release=self.StartSMS,
                ),
            ],
        )
        self.dialog.open()

    def close_alert(self, *args):
        """ Закрыть подтверждение """
        self.dialog.dismiss()
