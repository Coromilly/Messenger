from datetime import datetime
import clientui
from PyQt5 import QtWidgets
import requests
import time


class MessengerApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_clicked)
        self.pushButton_2.pressed.connect(self.update_messages)
        self.last_time = 0

    def send_message(self, username, password, text):
        response = requests.post(
            'http://127.0.0.1:5000/auth',
            json={'username': username, 'password': password}
        )
        if not response.json()['ok']:
            self.add_to_chat('Сообщение не отправлено')
            return

        response = requests.post(
            'http://127.0.0.1:5000/send',
            json={'username': username, 'password': password, 'text': text}
        )
        if not response.json()['ok']:
            self.add_to_chat('Сообщение не отправлено')

    def update_messages(self):
        response = requests.get('http://127.0.0.1:5000/messages',
                                params={'after': self.last_time})
        messages = response.json()['messages']

        for message in messages:
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
            self.add_to_chat(message['username'] + ' ' + beauty_time)
            self.add_to_chat(message['text'])
            self.add_to_chat('')

            self.last_time = message['time']

            time.sleep(1)

    def button_clicked(self):
        try:
            self.send_message(
                self.textEdit_2.toPlainText(),
                self.textEdit_3.toPlainText(),
                self.textEdit.toPlainText()
            )
        except:
            self.add_to_chat('Произошла ошибка')

        self.textEdit.setText('')
        self.textEdit.repaint()
        self.update_messages()

    def add_to_chat(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()


app = QtWidgets.QApplication([])
window = MessengerApp()
window.show()
app.exec_()
