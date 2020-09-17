from PySide2.QtCore import QObject, Slot, Signal

"""
    Interface of an object executable in a separate thread. 
    Designed for use with QThread
"""

class IThreadWorker(QObject):
    started = Signal()
    finished = Signal()
    def __init__(self, parent = None):
        super().__init__(parent)

    @Slot()
    def process(self):
        self.started.emit()
        pass
        self.finished.emit()