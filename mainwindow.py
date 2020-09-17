from PySide2.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow
from TLTableModel import TLTableModel
from PySide2.QtCore import QTimer, Slot, Signal, QThread


TIMER_VALUES = (1000, 3000, 5000)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # link model with view
        self.tlTableModel = TLTableModel()
        self.ui.tableView.setModel(self.tlTableModel)

        self.updateInfoInDownToolBar()

        # link model with timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tlTableModel.updateData)
        self.timer.timeout.connect(self.updateInfoInDownToolBar)
        self.timer.setInterval(TIMER_VALUES[0])
        self.timer.start()

    @Slot()
    def updateInfoInDownToolBar(self):
        """ update info in down tool bar """
        self.ui.actionEndpoints.setText(f'Endpoints: {self.tlTableModel.countEndpoints()}')
        self.ui.actionEstablished.setText(f'Established: {self.tlTableModel.countEstablished()}')
        self.ui.actionListen.setText(f'Listen: {self.tlTableModel.countListen()}')
        self.ui.actionTime_Wait.setText(f'Time wait: {self.tlTableModel.countTimeWait()}')
        self.ui.actionClose_Wait.setText(f'Close wait: {self.tlTableModel.countCloseWait()}')