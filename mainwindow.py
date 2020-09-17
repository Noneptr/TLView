from PySide2.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow
from TLTableModel import TLTableModel
from PySide2.QtCore import QTimer, Slot, Signal, QThread
from ithread_worker import IThreadWorker



TIMER_VALUES = (1000, 3000, 5000)


class MainWindow(QMainWindow):
    class ThWinDataUpdater(IThreadWorker):
        """
            Wraper for update window's data in separate thread
        """
        def __init__(self, window):
            super().__init__(window)
            self.window = window

        @Slot()
        def process(self):
            self.started.emit()
            self.window.updateData()
            self.finished.emit()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # link model with view
        self.tlTableModel = TLTableModel()
        self.ui.tableView.setModel(self.tlTableModel)

        self.updateData()

        # link model with timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDataInOtherThread)
        # self.timer.timeout.connect(self.updateData)
        self.timer.setInterval(TIMER_VALUES[0])
        self.timer.start()

    @Slot()
    def updateData(self):
        """ update info in down tool bar and update data model """
        self.tlTableModel.updateData()
        self.ui.actionEndpoints.setText(f'Endpoints: {self.tlTableModel.countEndpoints()}')
        self.ui.actionEstablished.setText(f'Established: {self.tlTableModel.countEstablished()}')
        self.ui.actionListen.setText(f'Listen: {self.tlTableModel.countListen()}')
        self.ui.actionTime_Wait.setText(f'Time wait: {self.tlTableModel.countTimeWait()}')
        self.ui.actionClose_Wait.setText(f'Close wait: {self.tlTableModel.countCloseWait()}')

    @Slot()
    def updateDataInOtherThread(self):
        """
            update data in separate thread
        """
        self.update_thread = QThread(self)
        self.update_worker = MainWindow.ThWinDataUpdater(self)
        self.update_thread.started.connect(self.update_worker.process)
        self.update_worker.finished.connect(self.update_thread.quit)
        self.update_thread.finished.connect(self.update_thread.deleteLater)
        self.update_thread.finished.connect(self.update_worker.deleteLater)
        self.update_worker.moveToThread(self.update_thread)
        self.update_thread.start()