import json
import gammu
import threading
import time
import str_text as st
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
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

    def StartSMS(self):
        """ Запускаем отправку смс в отдельном потоке """
        threading.Thread(target=self.GammuStart).start()

    def GammuStart(self):
        """ Отправка СМС """
        data_tel = self.LoadNum()
        allName = {}
        count = 0
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
                    msg = f'[b]ОТПРАВКА СМС[/b]\nТекст: [i]{sms_text}[/i]'
                    AppLog(msg)
                    for tel in allName:
                        if self.stop:
                            msg = 'РАССЫЛКА ОСТАНОВЛЕНА!'
                            AppLog(msg)
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
                                    AppLog(msg)
                                    Clock.schedule_once(partial(self.UpdLog, msg, err=True))
                                    error = True
                                    state_machine.Terminate()
                            if not error:
                                msg = f'[b]{allName[tel]}[/b] - оповещён.'
                                AppLog(msg)
                                self.progress_bar.value = self.progress_bar.value + progress_count
                                Clock.schedule_once(partial(self.UpdLog, msg))
                                count = count + 1
                                self.info_label.text = f'[b]СТАТУС:[/b] РАССЫЛКА ЗАПУЩЕНА | ' \
                                                       f'[b]ОПОВЕЩЕНО: {count} ИЗ {len(allName)}[/b]'
                            else:
                                error = False

                    msg = f'РАССЫЛКА ЗАВЕРШЕНА\nОПОВЕЩЕНО: {count} ИЗ {len(allName)}\n'
                    AppLog(msg)
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

    def stop_send(self):
        self.stop = True

    def SymSMS_info(self, dt=0):
        data_sms = gammu.SMSCounter(self.input_sms.text, UDH='NoUDH', Coding='Default')
        self.sym_info.text = f'Символов: {len(self.input_sms.text)}/{data_sms[1]}'
        self.sms_info.text = f"Кол-во СМС: {data_sms[0]}"