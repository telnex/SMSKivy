import json
import str_text as st
from kivy.properties import ObjectProperty
from functools import partial
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar


class AlertList(Screen):
    """ Редактирование списка оповещения и телефонной книги"""
    sms = ObjectProperty()
    data = ObjectProperty()
    float_btn = ObjectProperty()
    panel_num = ObjectProperty()
    input_json = ObjectProperty()
    label_info = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.LoadBtn()
        self.ClearDistList()
        self.float_btn.bind(minimum_height=self.float_btn.setter('height'))  # Важно!

    def LoadBtn(self):
        self.float_btn.clear_widgets()
        self.js_data = self.JSON()
        self.allName = []
        if len(self.js_data['data']['number']) == 0:
            self.float_btn.add_widget(Label(text=st.em_book,
                                            valign='top', halign='center',
                                            markup='1', color='black'))
        else:
            for i in self.js_data['data']['number']:
                self.allName.append(i)
            for f_name in self.allName:
                if len(f_name) > 20:
                    name = f_name[:20] + '...'
                else:
                    name = f_name
                btn = ToggleButton(text=name, size_hint_y=None, background_normal='',
                                   background_color=(0.05, 0.42, 0.24, 1), font_size=14)
                btn.size = (0, 35)
                # btn.size = (len(f_name) * 15, 35) # for StackLayout
                btn.bind(on_release=partial(self.AddNewTel, f_name))
                self.float_btn.add_widget(btn)

    def AddNewTel(self, name, j=False):
        number = self.js_data['data']['number'][name]
        with open('./data/dist_list.json', 'r') as f:
            dist_list = json.load(f)
        if dist_list.get(name) is not None:
            if dist_list[name] == number:
                dist_list.pop(name)
            else:
                dist_list[name] = number
        else:
            dist_list[name] = number
        self.UpdLabelInfo(dist_list)
        with open('./data/dist_list.json', 'w') as f:
            json.dump(dist_list, f)

    def UpdLabelInfo(self, dist_list):
        text = ''
        for name, tel in dist_list.items():
            text += f'[color=#0d576b][b]{name.upper()}[/b][/color] [size=12]{tel}[/size]\n'
        self.data.text = text

    def JSON(self) -> object:
        with open('./data/data.json', 'r') as f:
            data = json.load(f)
        return data

    def ClearDistList(self):
        w = {}
        with open('./data/dist_list.json', 'w') as f:
            json.dump(w, f)

    def LoadFromJSON(self):
        self.label_info.text = st.help
        if self.input_json.text == '':
            self.tel = self.js_data['data']['number']
            new_str = ''
            for name in self.allName:
                number = self.tel[name]
                new_str += f'{name.upper()} / {number}\n'
            self.input_json.text = new_str

    def EditData(self):
        error = False
        error_msg = ''
        t = self.input_json.text.split('\n')
        w = {"status": "ok", "data": {"number": {}}}
        for i in t:
            if i != '':
                if len(i.split('/')) == 2:
                    name = i.split('/')[0].strip()
                    tel = i.split('/')[1].strip()
                    if len(name) != 0 and len(tel) != 0:
                        tel = tel.replace(' ', '')
                        if tel[1:].isdigit():
                            w['data']['number'][name] = tel
                        else:
                            error = True
                            error_msg = f'[b]Ошибка![/b]\nПроверьте правильность ввода номера {tel}.'
                            break
                    else:
                        error = True
                        error_msg = f'[b]Ошибка![/b]\nПроверьте правильность ввода данных.'
                        break
                else:
                    error = True
                    error_msg = f'[b]Ошибка![/b]\nПроверьте правильность ввода данных.'
                    break
        if not error:
            with open('./data/data.json', 'w') as f:
                json.dump(w, f)
            self.LoadBtn()
            Snackbar(text="Данные сохранены!", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=.4, bg_color=(0.05, 0.42, 0.24, 1)).open()
        else:
            Snackbar(text=error_msg, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=.8,
                     bg_color=(0.64, 0.13, 0.13, 1)).open()

    def DelList(self):
        self.ClearDistList()
        self.LoadBtn()
        self.data.text = ''
