from PySide2.QtCore import Slot, Qt, QAbstractListModel, QModelIndex

from ReminderApiProvider import ReminderApiProvider


class CollectionsModel(QAbstractListModel):
    def __init__(self, provider: ReminderApiProvider, parent=None):
        super(CollectionsModel, self).__init__(parent)
        self.__api: ReminderApiProvider = provider
        self.__collections = []

        self.update_model()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__collections)

    def data(self, index, role=Qt.DisplayRole):
        return self.__collections[index.row()] \
            if role == Qt.DisplayRole and index.row() < self.rowCount() else None

    @Slot()
    def update_model(self):
        collections = self.__api.get_collections()

        if collections != self.__collections:
            self.beginResetModel()
            self.__collections = collections
            self.endResetModel()
