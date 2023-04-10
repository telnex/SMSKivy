# ВАЖНО: C:\..\Python39\Lib\site-packages\kivymd\uix\datatables\datatables.kv
# удалил tooltip | ну а как иначе :(

import os
import json
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.snackbar import Snackbar
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.dialog import MDDialog


class EventLog(Screen):
    table = ObjectProperty()
    count = ObjectProperty()

    def on_enter(self, *args):
        self.table_data()
        with open('./data/config.json', 'r') as f:
            j = json.load(f)
        self.count.text = f'Сообщений отправлено: {j["Count"]}'

    def table_data(self):
        """ Структура таблицы """
        self.table.clear_widgets()
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            row_data=self.sent_sms(),
            use_pagination=True,
            column_data=[
                ("Дата", dp(30), "DHTVZ"),
                ("Сообщение", dp(1000))
            ],
            elevation=0,
        )
        layout.add_widget(self.data_tables)
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.table.add_widget(layout)

    def DelLog(self):
        """ Удаление ЛОГА """
        folder = os.getcwd() + ".\data\log"
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
        Snackbar(
            text="История очищена!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.4,
            bg_color=(0.05, 0.42, 0.24, 1)
        ).open()

    def on_row_press(self, instance_table, instance_row):
        """ Обработка нажатия на строку таблицы """
        self.show_alert(instance_row.text)

    def sent_sms(self):
        """ Наполнение таблицы данными """
        row_data = []
        dir_log = ".\data\log"
        if len(os.listdir(os.getcwd() + dir_log)) == 0:
            row_data = [('', ("alert", [255 / 256, 165 / 256, 0, 1], 'Нет данных'))]
        else:
            for filelog in os.listdir(os.getcwd() + dir_log):
                with open(os.path.join(os.getcwd(), "data\log", filelog), 'r') as f:
                    text = f.read()
                    log = text.strip().split('\n\n')
                    for r in log:
                        dt = filelog[:-4].replace('_', '.', 2)
                        dt = dt.replace('_', ' ', 1)
                        dt = dt.replace('_', ':', 1)
                        a = ('[size=14]' + dt + '[/size]', '[size=14]' + r.split('\n')[1] + '[/size]')
                        row_data.append(a)
        return row_data

    def show_alert(self, text: str):
        """ Отображение полной информации СМС """
        dt = text[9:-7].replace('.', '_')
        dt = dt.replace(' ', '_')
        dt = dt.replace(':', '_')
        filelog = dt + '.log'
        if len(dt) != 14:
            msg = 'Кликните на дату, чтобы увидеть подробности.'
        else:
            with open(os.path.join(os.getcwd(), "data\log", filelog), 'r') as f:
                msg = f.read()
        self.dialog = MDDialog(
            title='Доп. информация',
            text='[color=#1a1a1a][size=14]' + msg + '[/size][/color]',
            md_bg_color='white',
            buttons=[
                MDRaisedButton(
                    text="ЗАКРЫТЬ",
                    theme_text_color="Custom",
                    md_bg_color='#0d6b3d',
                    on_release=self.close_alert,
                ),
            ],
        )
        self.dialog.open()

    def close_alert(self, *args):
        """ Закрыть окно """
        self.dialog.dismiss()
