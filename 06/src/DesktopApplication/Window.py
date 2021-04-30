from PySide2.QtCore import Slot

from PySide2.QtSql import QSqlDatabase, QSqlTableModel

from PySide2.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QTableView,
    QLabel, QWidget, QPushButton,
    QFileDialog,
)

from AddEntryDialog import AddEntryDialog


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Desktop application')

        self.__label = QLabel('Collection', self)

        self.__open_button = QPushButton('Open')
        self.__open_button.setToolTip('Choose the collection database')

        self.__add_button = QPushButton('Add')
        self.__add_button.setToolTip('Add a new entry into the collection')

        self.__model = None
        self.__view = QTableView(self)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.__label)
        horizontal_layout.addWidget(self.__open_button)
        horizontal_layout.addWidget(self.__add_button)

        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout)
        layout.addWidget(self.__view)

        self.setLayout(layout)

        self.__open_button.clicked.connect(self.__open_collection)
        self.__add_button.clicked.connect(self.__add_new_entry)

    @Slot()
    def __open_collection(self):
        collection = QFileDialog.getOpenFileName()[0]
        self._db = QSqlDatabase.addDatabase('QSQLITE')
        self._db.setDatabaseName(collection)
        self._db.open()

        self.__model: QSqlTableModel = QSqlTableModel(self, self._db)
        self.__model.setTable('objects')
        self.__model.select()

        self.__view.setModel(self.__model)

    @Slot()
    def __add_new_entry(self):
        dialog = AddEntryDialog(self)

        if dialog.exec_() == AddEntryDialog.Accepted:
            row = self.__model.rowCount()

            self.__model.insertRow(row)
            self.__model.setData(self.__model.index(row, 0), dialog.entry.original)
            self.__model.setData(self.__model.index(row, 1), dialog.entry.translation)
            self.__model.setData(self.__model.index(row, 2), dialog.entry.transcription)

            self.__model.submitAll()
