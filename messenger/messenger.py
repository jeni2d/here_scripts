from PyQt6 import QtCore, QtGui, QtWidgets
from clientui import Ui_MainWindow
from entername import Ui_NameWindow
import requests
from datetime import datetime


class Namewin(QtWidgets.QMainWindow, Ui_NameWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		
		self.nextbtn.pressed.connect(self.secondscr)

	def secondscr(self):
		self.window = Messenger()
		self.window.show()
	
	def get_name(self):
		return self.nameEdit.text()


class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
		
        self.pushButton.pressed.connect(self.send_message)

        self.after = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messeges)
        self.timer.start(1000)
        self.name = window.get_name()

    def print_message(self, message):
        dt = datetime.fromtimestamp(message['time'])
        dt_str = dt.strftime('%d.%b %H:%M:%S')
        self.textBrowser.append(dt_str + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def get_messeges(self):
        try:
            r = requests.get('http://127.0.0.1:5000/messages',
                    params={'after': self.after}
            )
            messages = r.json()['messages']
        except:
            return

        for message in messages:
            self.print_message(message)
            self.after = message['time']

    def send_message(self):
        # name = self.lineEdit.text()
        name = self.name
        text = self.textEdit.toPlainText()
        try:
            r = requests.post('http://127.0.0.1:5000/send',
                        json={'name': name, 'text': text}
            )
        except:
            self.textBrowser.append('Server is down')
            self.textBrowser.append('Try one more time')
            self.textBrowser.append('')
            return

        if r.status_code != 200:
            self.textBrowser.append('Name and Text should be filled, text < 1000 simbols')
            self.textBrowser.append('')
            return

        self.textEdit.clear()

    

app = QtWidgets.QApplication([])	
# window = Messenger()
window = Namewin()
window.show()
app.exec()
