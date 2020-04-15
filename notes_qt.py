import sys
from PyQt5.QtWidgets import QApplication
from notes_app import MainWindow, NotesService

if __name__ == "__main__":
    database = None
    if len(sys.argv)>1:
        database = sys.argv[1]

    notes_service = NotesService(database)
    notes_service.load_notes()

    app = QApplication(sys.argv)
    window = MainWindow(notes_service)
    app.exec_()
