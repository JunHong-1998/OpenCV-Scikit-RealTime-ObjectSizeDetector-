from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time


class WidgetUI(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = self.label(True, True, Qt.AlignCenter)
        self.next = 0

    def label(self, SizeIgnore, Scale, Align):
        canvas = QLabel(self)
        if SizeIgnore:
            canvas.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        canvas.setScaledContents(Scale)
        canvas.setAlignment(Align)
        return canvas

    def textLabel(self, text, font=None, color=None, align=None, border=None, height=None, width=None):
        label_Text = QLabel(self)
        label_Text.setText(text)
        if font:
            label_Text.setFont(QFont(font[0], font[1]))
        if height:
            label_Text.setFixedHeight(height)
        if width:
            label_Text.setFixedWidth(width)
        if align:
            label_Text.setAlignment(align)
        if color and border:
            label_Text.setStyleSheet("background-color: {}".format(color)+"; border: {}px solid black".format(border))
        elif color:
            label_Text.setStyleSheet("background-color: {}".format(color))
        return label_Text

    def radioButton(self, text, action=None, AE=False, font=None, check=False, enable=True):
        radio = QRadioButton(self)
        radio.setText(text)
        if font:
            radio.setFont(QFont(font[0], font[1]))
        radio.setChecked(check)
        radio.setEnabled(enable)
        if action:
            radio.toggled.connect(action)
        radio.setAutoExclusive(AE)
        return radio

    def ToolButton(self, toolbar, flag, icon, name, action, AE=False, textOnly=None, font=None, width=None, check=False, enable=True):
        if flag==1:
            ToolBtn = QAction(QIcon(icon), name, self)
            ToolBtn.triggered.connect(action)
            ToolBtn.setEnabled(enable)
            toolbar.addAction(ToolBtn)
        elif flag==2:
            ToolBtn = QToolButton(self)
            if textOnly:
                ToolBtn.setText(textOnly)
            else:
                ToolBtn.setIcon(QIcon(icon))
            if font:
                ToolBtn.setFont(QFont(font[0], font[1]))
            if width:
                ToolBtn.setMinimumWidth(width)
            ToolBtn.setToolTip(name)
            ToolBtn.setCheckable(True)
            ToolBtn.setAutoExclusive(AE)
            if check:
                ToolBtn.setChecked(True)
            ToolBtn.setEnabled(enable)
            toolbar.addWidget(ToolBtn)
            ToolBtn.clicked.connect(action)
        return ToolBtn

    def tableWIDGET(self, row, colHeader=None, col=None):
        Table = QTableWidget()
        Table.setRowCount(row)
        if col:
            Table.setColumnCount(col)
        if colHeader:
            Table.setVerticalHeaderLabels(colHeader)
        Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        Table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return Table

    def textBtn(self, text, action, font=None, width=None, height=None):
        btn = QPushButton(self)
        btn.setText(text)
        if font:
            btn.setFont(QFont(font[0], font[1]))
        if width:
            btn.setFixedWidth(width)
        if height:
            btn.setFixedHeight(height)
        btn.clicked.connect(action)
        return btn

    def colorBtn(self, color, action, height=None):
        btn = QPushButton(self)
        btn.setStyleSheet("background-color:rgb({},{},{})".format(color[2], color[1], color[0]))
        if height:
            btn.setFixedHeight(height)
        if action:
            btn.clicked.connect(action)
        return btn

    def checkbox(self, name, action, checked, font=None):
        checkbox = QCheckBox(self)
        if name:
            checkbox.setText(name)
        checkbox.setChecked(checked)
        if font:
            checkbox.setFont(QFont(font[0], font[1]))
        if action:
            checkbox.clicked.connect(action)
        return checkbox

    def spinBox(self, flag, min, max, value, step, action=None, maxWidth=None, minWidth=None, odd=None):
        if flag:
            if odd:
                spin = OddSpinBox()
            else:
                spin = QSpinBox()
        else:
            spin = QDoubleSpinBox()
        if odd:
            spin.setSingleStep(2)
        else:
            spin.setSingleStep(step)
        if maxWidth:
            spin.setMaximumWidth(maxWidth)
        if minWidth:
            spin.setMinimumWidth(minWidth)
        spin.setMinimum(min)
        spin.setMaximum(max)
        spin.setValue(value)

        if action:
            spin.valueChanged.connect(action)
        return spin

    def comboBox(self, name, combo_str, action=None, minWidth=None, height=None):
        combo = QComboBox(self)
        combo.setToolTip(name)
        if minWidth:
            combo.setMinimumWidth(minWidth)
        if height:
            combo.setFixedHeight(height)
        for f in combo_str:
            combo.addItem(f)
        if action:
            combo.currentIndexChanged.connect(action)
        return combo

    def SliderWidget(self, ott, default, min, max, width, action, enable):
        slider = QSlider(self)
        slider.setOrientation(ott)
        slider.setValue(default)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setFixedWidth(width)
        slider.setEnabled(enable)
        slider.setStyleSheet("QSlider::groove:horizontal {border: 1px solid #bbb;background: white;height: 10px;border-radius: 4px;}"
                             "QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,stop: 0 #66e, stop: 1 #bbf);background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,stop: 0 #bbf, stop: 1 #55f);border: 1px solid #777;height: 10px;border-radius: 4px;}"
                             "QSlider::add-page:horizontal {background: #fff;border: 1px solid #777;height: 10px;border-radius: 4px;}"
                             "QSlider::handle:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #eee, stop:1 #ccc);border: 1px solid #777;width: 13px;margin-top: -2px;margin-bottom: -2px;border-radius: 4px;}"
                             "QSlider::handle:horizontal:hover {background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #fff, stop:1 #ddd);border: 1px solid #444;border-radius: 4px;}"
                             "QSlider::sub-page:horizontal:disabled {background: #bbb;border-color: #999;}"
                             "QSlider::add-page:horizontal:disabled {background: #eee;border-color: #999;}"
                             "QSlider::handle:horizontal:disabled {background: #eee;border: 1px solid #aaa;border-radius: 4px;}")
        slider.valueChanged.connect(action)
        return slider

    def fileDialog(self, flag):
        filter = "Images (*.png *.jpg)"
        if flag:
            file, _ = QFileDialog.getOpenFileName(self, "File Directory", QDir.currentPath(), filter)
        else:
            file, _ = QFileDialog.getSaveFileName(self, "Save File", QDir.currentPath(), "PNG(*.png);;JPEG(*.jpg *.jpeg)")
        if file == (""):
            return
        else:
            return file

    def warnDialog(self, parent, flag):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        if flag==1:
            msg.setText("Target reference not found !")
            msg.setDetailedText("You may proceed with original image else follow the instructions below: \n1. Please adjust the target reference in settings \n2. Please import an image with good quality")
        elif flag==2:
            msg.setText("Image not found !")
            msg.setDetailedText("Please import an image to continue")
        elif flag==3:
            msg.setText("Target image unselected !")
            msg.setDetailedText("Please choose an image as target in settings")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def infoDialog(self, parent, flag):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information")
        if flag == 1:
            msg.setText("Live stream terminated !")
        elif flag==2:
            msg.setText("Override might occurred !")
            msg.setDetailedText("System auto switch to background format whenever platform not detected")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def about(self, parent, flag):
        msg = QDialog(parent)
        if flag==1:
            image = "OD_assets/guide.png"
            title = "Quick Guide"
        elif flag==2:
            image = "OD_assets/about.png"
            title = "ABOUT OSD_2021(64-bit)"
        msg.setWindowTitle(title)
        about_label = QLabel(msg)
        about_label.setPixmap(QPixmap(image))
        layout = QVBoxLayout(msg)
        layout.addWidget(about_label)
        def nextFunc():
            if self.next==0:
                about_label.setPixmap(QPixmap("OD_assets/instruction.png"))
                about_label.setAlignment(Qt.AlignCenter)
                self.next = 1
            elif self.next == 1:
                about_label.setPixmap(QPixmap("OD_assets/guide.png"))
                self.next = 0
        if flag==1:
            layout.addWidget(self.textBtn("NEXT", nextFunc))
        msg.setLayout(layout)
        msg.exec_()


    def SplashScreen(self):
        splash = QSplashScreen(QPixmap("OD_assets/splash.png"), Qt.WindowStaysOnTopHint)
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.show()
        for i in range(1,15):
            splash.setPixmap(QPixmap("OD_assets/splash{}.png".format(i)))
            t = time.time()
            while time.time() < t + 0.2:
                QApplication.processEvents()
        time.sleep(1)

class VLine(QFrame):
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)

class OddSpinBox(QSpinBox):
    # Replaces the valueChanged signal
    newValueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(OddSpinBox, self).__init__(parent=parent)

        self.valueChanged.connect(self.onValueChanged)
        self.before_value = self.value()

    def onValueChanged(self, i):
        if not self.isValid(i):
            self.setValue(self.before_value)
        else:
            self.newValueChanged.emit(i)
            self.before_value = i

    def isValid(self, value):
        if (value % self.singleStep()) == 0:
            return False
        return True

class Dialog(QDialog):
    def __init__(self, parent):
        super(Dialog, self).__init__(parent=parent)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        pass


