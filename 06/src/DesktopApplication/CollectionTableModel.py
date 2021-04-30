from PySide2.QtCore import Slot, Qt, QAbstractTableModel, QModelIndex, QTimer

from ReminderApiProvider import ReminderApiProvider


class CollectionTableModel(QAbstractTableModel):
    __update_timeout = 10_000
    __columns = ['original', 'translation', 'transcription']

    def __init__(self, provider, collection: str, parent=None):
        super(CollectionTableModel, self).__init__(parent)
        self.__api: ReminderApiProvider = provider
        self.__collection = collection
        self.__objects = []
        self.__timer = QTimer(self)

        self.__timer.timeout.connect(self.update_model)

        self.__timer.start(self.__update_timeout)
        self.update_model()

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.__columns)

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__objects)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row, column = index.row(), index.column()

            if row < self.rowCount() and column < self.columnCount():
                return self.__get_display_data(row, column)

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        return self.__columns[section] \
                if orientation == Qt.Horizontal and role == Qt.DisplayRole \
                else None

    def object(self, row):
        return self.__objects[row]

    @Slot()
    def update_model(self):
        objects = self.__api.get_objects(self.__collection)

        if objects != self.__objects:
            self.beginResetModel()
            self.__objects = objects
            self.endResetModel()

    def __get_display_data(self, row: int, column: int) -> str:
        try:
            return self.__objects[row][self.__columns[column]]
        except KeyError:
            return 'NULL'
