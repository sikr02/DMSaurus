# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QHBoxLayout, QHeaderView,
    QLayout, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QToolButton, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from src.ui.file_tree import FileTree

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(907, 592)
        self.actionVerzeichnisbaum = QAction(MainWindow)
        self.actionVerzeichnisbaum.setObjectName(u"actionVerzeichnisbaum")
        self.actionVerzeichnisbaum.setCheckable(True)
        self.actionVerzeichnisbaum.setChecked(True)
        icon = QIcon(QIcon.fromTheme(u"folder"))
        self.actionVerzeichnisbaum.setIcon(icon)
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditUndo))
        self.actionUndo.setIcon(icon1)
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditRedo))
        self.actionRedo.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout.addWidget(self.toolButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 907, 33))
        self.menuAnsicht = QMenu(self.menubar)
        self.menuAnsicht.setObjectName(u"menuAnsicht")
        self.menuBearbeiten = QMenu(self.menubar)
        self.menuBearbeiten.setObjectName(u"menuBearbeiten")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.explorerWidget = QDockWidget(MainWindow)
        self.explorerWidget.setObjectName(u"explorerWidget")
        self.explorerWidget.setFloating(False)
        self.explorerWidget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.explorerWidget.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.treeWidget = FileTree(self.dockWidgetContents)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1")
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setAnimated(True)
        self.treeWidget.setHeaderHidden(True)

        self.verticalLayout.addWidget(self.treeWidget)

        self.explorerWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.explorerWidget)

        self.menubar.addAction(self.menuBearbeiten.menuAction())
        self.menubar.addAction(self.menuAnsicht.menuAction())
        self.menuAnsicht.addAction(self.actionVerzeichnisbaum)
        self.menuBearbeiten.addAction(self.actionUndo)
        self.menuBearbeiten.addAction(self.actionRedo)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"DMSaurus", None))
        self.actionVerzeichnisbaum.setText(QCoreApplication.translate("MainWindow", u"Verzeichnisbaum", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"R\u00fcckg\u00e4ngig", None))
#if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Wiederherstellen", None))
#if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Y", None))
#endif // QT_CONFIG(shortcut)
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.menuAnsicht.setTitle(QCoreApplication.translate("MainWindow", u"Ansicht", None))
        self.menuBearbeiten.setTitle(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.explorerWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Dateien", None))
    # retranslateUi

