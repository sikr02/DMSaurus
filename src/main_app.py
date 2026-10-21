import shutil

from PySide6.QtWidgets import QMainWindow, QWidget

from src.core.protocol import Protocol
from src.ui.main_window import Ui_MainWindow
from src.config import DOCUMENT_PATH, CACHE_PATH

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        CACHE_PATH.mkdir(exist_ok=True, parents=True)

        self.ui.actionVerzeichnisbaum.toggled.connect(self.ui.explorerWidget.setVisible)

        self.ui.explorerWidget.setTitleBarWidget(QWidget())

        self.ui.treeWidget.populate_file_tree_widget(root=DOCUMENT_PATH)

        self.protocol = Protocol(self)

    def closeEvent(self, event):
        try:
            shutil.rmtree(CACHE_PATH.as_posix(), ignore_errors=False)
        except FileNotFoundError:
            pass
        except OSError as exc:
            print(f"Failed to clean cache: {exc}")

        event.accept()