from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeView, QHeaderView, QStyledItemDelegate
from PyQt6.QtCore import Qt

class TreeView:
    def __init__(self, treeview):
        self.treeview = treeview
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Num', 'Image', 'Size', 'Prediction'])

        self.treeview.setModel(self.model)
        self.treeview.setHeaderHidden(False)

        self.header = self.treeview.header()
        self.header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header.setFont(self.setfont())

        # Set column width
        self.treeview.setColumnWidth(0, 50)   # Adjust the width for 'Num' column
        self.treeview.setColumnWidth(1, 90)  # Adjust the width for 'Image' column
        self.treeview.setColumnWidth(2, 130)  # Adjust the width for 'Size' column
        self.treeview.setColumnWidth(3, 130)  # Adjust the width for 'Prediction' column

        # You can also enable stretch on specific columns if needed
        self.header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)

        self.treeview.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        self.treeview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.treeview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.treeview.setSelectionMode(QTreeView.SelectionMode.NoSelection)
        self.treeview.setStyleSheet(
            "QTreeView { background-color: #D9D9D9; }"
            "QHeaderView::section { background-color: #228B22;}"
            "QTreeView::item { color: black; text-align: center;}"
        )

        delegate = CustomItemDelegate(row_height=90)
        self.treeview.setItemDelegate(delegate)

    def setfont(self):
        font = self.treeview.header().font()
        font.setBold(True)
        font.setPointSize(font.pointSize() - 2)
        return font

    def add(self, image, num, size, prediction):
        image_item = QStandardItem()
        image_item.setData(image, Qt.ItemDataRole.DecorationRole)
        num_item = StandardItem(num, True)
        size_item = StandardItem(size, True)
        prediction_item = StandardItem(prediction, True)
        self.model.appendRow([num_item, image_item, size_item, prediction_item])

    def clear(self):
        self.model.removeRows(0, self.model.rowCount())

class StandardItem(QStandardItem):
    def __init__(self, text = None, Bold = False):
        super().__init__()
        if text is not None:
            self.setText(text)
        if Bold == True:
            font = self.font()
            font.setBold(True)
            self.setFont(font)
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

class CustomItemDelegate(QStyledItemDelegate):
    def __init__(self, row_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_height = row_height

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(self.row_height)
        return size