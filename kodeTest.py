import sys
from PyQt5 import QtCore, QtWidgets

class Worker(QtCore.QThread):
    dataSent = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self._stopped = True
        self._mutex = QtCore.QMutex()

    def stop(self):
        self._mutex.lock()
        self._stopped = True
        self._mutex.unlock()

    def run(self):
        self._stopped = False
        for count in range(10):
            if self._stopped:
                break

            self.sleep(1)
            data = {
                'message':'running %d [%d]' % (
                    count, QtCore.QThread.currentThreadId()),
                'time': QtCore.QTime.currentTime(),
                'items': [1, 2, 3],
                }

            self.dataSent.emit(data)

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.edit = QtWidgets.QPlainTextEdit()
        self.edit.setReadOnly(True)
        self.button = QtWidgets.QPushButton('Start')
        self.button.clicked.connect(self.handleButton)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        self._worker = Worker()
        self._worker.started.connect(self.handleThreadStarted)
        self._worker.finished.connect(self.handleThreadFinished)
        self._worker.dataSent.connect(self.handleDataSent)

    def handleThreadStarted(self):
        self.edit.clear()
        self.button.setText('Stop')
        self.edit.appendPlainText('started')

    def handleThreadFinished(self):
        print("DONE")
        self.button.setText('Start')
        self.edit.appendPlainText('stopped')

    def handleDataSent(self, data):
        self.edit.appendPlainText('message [%d]' %
            QtCore.QThread.currentThreadId())
        self.edit.appendPlainText(data['message'])
        self.edit.appendPlainText(data['time'].toString())
        self.edit.appendPlainText(repr(data['items']))

    def handleButton(self):
        if self._worker.isRunning():
            self._worker.stop()
        else:
            self._worker.start()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 100, 400, 400)
    window.show()
    sys.exit(app.exec_())