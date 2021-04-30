from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow

from CollectionsModel import CollectionsModel
from CollectionTableModel import CollectionTableModel
from ReminderApiProvider import ReminderApiProvider

from Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__provider = ReminderApiProvider('http://localhost:8080')
        self.__collections_model = CollectionsModel(self.__provider)
        self.__table_model = None

        self.__ui.comboBox.setModel(self.__collections_model)
        self.__ui.comboBox.currentTextChanged.connect(self._set_collection)

        self.__collections_model.update_model()
        self._set_collection(self.__ui.comboBox.currentText())

    @Slot()
    def _set_collection(self, collection: str):
        self.__table_model = CollectionTableModel(self.__provider, collection)
        self.__table_model.update_model()
        self.__ui.tableView.setModel(self.__table_model)
