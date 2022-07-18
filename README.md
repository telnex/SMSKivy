# Программа создания СМС-рассылки через GSM-модем
**Версия:** 1.0.0 | **Python:** 3.9 | **Kivy:** 2.1 | **Gammu:** 3.2.4

![Иллюстрация к проекту](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjOQifOGxT15hvFsdkp1D8cri-QhD3z5VGk8d6UNqNvWyXcse-6-dtrrpgNvD4JI1ve8my5T6IZiFTl9SnuV4-aCuOwWUnYs-gaVe9e4We6LZQTEBohIBfqJrwDA0SN3-I5jAd-1vFY6ksDdDHRuTt9jOaXIkiIIRX5ScLOFA0j5FdlL0EPTZSI_mjMmA/s1600/photo_2022-07-14_01-38-19.jpg)
## Описание программы
Данное ПО позволяет производить рассылку СМС на указанный список адресатов, количество абонентов и символов в тексте СМС не имеет значения (рекомендуемый размер СМС: 250-300 символов = 2 СМС). Функционал программы обусловлен производственной необходимостью, т.е. программа создавалась под конкретные цели, с минимальным функционалом, необходимым для выполнения поставленных задач. В связи с чем, в программе отсутствует менеджер отправленных СМС и тд. Функционал Gammu и Kivy позволяют это реализовать без переписывания основного кода. При запуске программы происходит инициализация соединения с модемом. В случае, если возникают ошибки, необходимо перезапустить программу.

## Установка
Данная программа использует стороннюю библиотеку - **gammu**, её необходимо установить с оф. сайта https://ru.wammu.eu/download/gammu/

Саму программу можно скачать с репозитория -ссылка-

## Настройка
**Для  Windows:**  через штатный диспетчер задач необходимо выяснить номер com-порта вашего устройства, указать данный порт в настройка программы (только цифра).

**Для Ubuntu/Mac OS:** через команду ls /dev/ выяснить номер com-порта. Возможно, необходимо использовать дополнительное оборудование (переходник com->USB).
