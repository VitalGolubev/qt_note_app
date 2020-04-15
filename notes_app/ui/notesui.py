from PyQt5 import QtWidgets, QtCore
from notes_app.models import Note
from notes_app.services import NotesService


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, notes_service: NotesService, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.notes_service = notes_service

        self.cur_note = None
        self.setupUi()
        self.update_notes()
        self.set_active(0)
        self.show()

    def setupUi(self):
        """ Setup User Inteface """
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.notesTitleListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.notesTitleListWidget.setObjectName("notesTitleListWidget")
        self.horizontalLayout.addWidget(self.notesTitleListWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.noteTitleLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.noteTitleLineEdit.setObjectName("noteTitleLineEdit")
        self.verticalLayout.addWidget(self.noteTitleLineEdit)
        self.noteTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.noteTextEdit.setObjectName("noteTextEdit")
        self.verticalLayout.addWidget(self.noteTextEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.infoPushButton = QtWidgets.QPushButton("Info", self.centralwidget)
        self.infoPushButton.setObjectName("infoPushButton")
        self.horizontalLayout_3.addWidget(self.infoPushButton)
        self.createPushButton = QtWidgets.QPushButton("Create", self.centralwidget)
        self.createPushButton.setObjectName("createPushButton")
        self.horizontalLayout_3.addWidget(self.createPushButton)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.deletePushButton = QtWidgets.QPushButton("Delete", self.centralwidget)
        self.deletePushButton.setObjectName("deletePushButton")
        self.horizontalLayout_2.addWidget(self.deletePushButton)
        self.savePushButton = QtWidgets.QPushButton("Save", self.centralwidget, )
        self.savePushButton.setObjectName("savePushButton")
        self.horizontalLayout_2.addWidget(self.savePushButton)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.notesTitleListWidget.currentItemChanged.connect(self.onCurrentItemChangedInNotesTitleList)
        self.createPushButton.clicked.connect(self.onCreateClicked)
        self.infoPushButton.clicked.connect(self.onInfoClicked)
        self.deletePushButton.clicked.connect(self.onDeleteClicked)
        self.savePushButton.clicked.connect(self.onSaveClicked)
        QtCore.QMetaObject.connectSlotsByName(self)

    def update_notes(self):
        """ Fill the ListWidget with notes titles """
        self.notesTitleListWidget.clear()
        self.notesTitleListWidget.addItems(self.notes_service.get_titles())
        self.repaint()

    def set_active(self, idx: int):
        """ Set active ListWidget item by index """
        self.cur_note = self.notes_service.notes[idx]
        self.notesTitleListWidget.setCurrentRow(idx)
        self.noteTitleLineEdit.setText(self.notes_service.notes[idx].title)
        self.noteTextEdit.setText(self.notes_service.notes[idx].content)
        self.repaint()

    def onInfoClicked(self):
        """ Show the Info Window """
        print("Info button..")
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "Info",
                              "The first Note App written in PyQt5",
                              QtWidgets.QMessageBox.Ok).exec_()

    def onCurrentItemChangedInNotesTitleList(self):
        """
        Select another Note in ListWidget
        and repaint window with selected Note content
        """
        self.set_active(self.notesTitleListWidget.currentRow())

    def onSaveClicked(self):
        """ Save selected Note """
        self.cur_note.title = self.noteTitleLineEdit.text()
        self.cur_note.content = self.noteTextEdit.toPlainText()
        if not self.cur_note.title or not self.cur_note.content:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Warning", "Can't be empty!",
                                  QtWidgets.QMessageBox.Ok).exec_()
            return
        cur_row = None
        if self.cur_note.id is None:
            self.notes_service.create(self.cur_note)
        else:
            self.notes_service.update(self.cur_note)
            cur_row = self.notesTitleListWidget.currentRow()

        self.update_notes()
        if cur_row is not None:
            self.set_active(cur_row)

    def onDeleteClicked(self):
        """ Delete selected Note """
        self.notes_service.delete(self.cur_note)
        self.update_notes()
        self.set_active(0)

    def onCreateClicked(self):
        """ Create new Note """
        self.cur_note = Note()
        self.onSaveClicked()
        self.set_active(len(self.notes_service.notes) - 1)
