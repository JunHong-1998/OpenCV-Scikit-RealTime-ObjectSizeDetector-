import sys
import os
from ObjDetector_UI import *
from ObjDetector_CV import *

CV = OD_CV()
class Paint(QMainWindow):
    def __init__(self):
        self.col_fm = [(125, 0, 125), (0, 125, 125), (125, 125, 0)]
        self.col_lb = [(255, 255, 255), (255, 255, 255), (255, 255, 255)]
        self.lb_oprt = self.lb_msm = self.lb_bound = True
        self.oprt = [True, True, True]    # Canny, Sobel, Prewitt operators
        self.shape = [True, True, True, False]   #Tri, Rect, Cir
        self.CThres_auto = [True, True]     #Ref_Canny, Canny
        self.dil = [True, True, True]       # Canny, Sobel, Prewitt dilation
        self.ero = [True, True, True]  # Canny, Sobel, Prewitt erosion
        self.thin = [False, False, False]
        self.thinAUTO = [None, True, True]
        self.thres = [None, False, False]
        self.edgeDetect = 0
        self.display = 0
        self.zoom = 1
        self.targetREF = []
        self.canny_detect = []
        self.sobel_detect = []
        self.prewitt_detect = []
        self.EdgeDisplay = []
        self.ContDisplay = []
        self.CompareDisplay = False
        self.stream_live = self.flipH = self.flipV = self.stream_ref = False
        self.live_detect = self.overBIT = False
        self.live_ref = self.kar = True
        super(Paint,self).__init__()
        self.UI = WidgetUI()
        self.resize(1024, 768)
        self.setWindowIcon(QIcon("OD_assets/logo.png"))
        self.setWindowTitle("Object Size Detector by Low Jun Hong BS18110173")
        self.UI.SplashScreen()
        self.initUI()

    def initUI(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.UI.canvas)
        self.setCentralWidget(self.scrollArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.DockUI_settings())
        self.dock_LIST = self.DockUI_list()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_LIST)
        self.dock_STREAM = self.DockUI_stream()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_STREAM)
        self.zoom_slider = self.UI.SliderWidget(Qt.Horizontal, 100, 1, 500, 150, self.Zoom, False)
        self.zoom_percentage = self.UI.textLabel(" 100%", font=('Georgia', 11), width=50)
        self.mode = self.UI.textLabel("OBJECT", font=('Georgia', 10), width=110, align=Qt.AlignCenter)
        self.edgeOPRT = self.UI.textLabel("Edge:  CANNY", font=('Georgia', 10), width=150, align=Qt.AlignCenter)
        self.fileNAME = self.UI.textLabel("filename", font=('Georgia', 10), width=100, align=Qt.AlignCenter)
        status = self.statusBar()
        status.setStyleSheet('QStatusBar::item {border: none;}')
        status.addPermanentWidget(VLine())
        status.addPermanentWidget(self.fileNAME)
        status.addPermanentWidget(VLine())
        status.addPermanentWidget(self.edgeOPRT)
        status.addPermanentWidget(VLine())
        status.addPermanentWidget(self.mode)
        status.addPermanentWidget(VLine())
        status.addPermanentWidget(self.zoom_slider)
        status.addPermanentWidget(self.zoom_percentage)
        status.showMessage("1. Import an image")

    def Zoom(self):
        self.zoom = self.zoom_slider.value() / 100
        self.zoom_percentage.setText(" " + str(int(self.zoom* 100)) + "%")
        self.Render()

    def tab_detail(self):
        self.table_Canny.resizeRowsToContents()
        self.table_Sobel.resizeRowsToContents()
        self.table_Prewitt.resizeRowsToContents()

    def dockStream_btn(self, flag):
        if flag==1:
            self.stream_LISTupd.clear()
        elif flag==2:
            self.stream_LISTupd.clear()
            self.listTOOL.setChecked(False)
            self.dock_STREAM.hide()

    def DockUI_stream(self):
        dock = QDockWidget(self)
        self.stream_LISTupd = QListWidget(dock)
        head = QWidget(dock)
        head_lay = QHBoxLayout(head)
        head_lay.addWidget(self.UI.textLabel("LIVE stream update", font=('Georgia bold', 11), align=Qt.AlignLeft))
        head_lay.addStretch(1)
        head_lay.addWidget(self.UI.textBtn("Clear", lambda : self.dockStream_btn(1), font=('Georgia', 10), width=60))
        head_lay.addWidget(self.UI.textBtn("Close", lambda : self.dockStream_btn(2), font=('Georgia', 10), width=60))
        head_lay.setAlignment(Qt.AlignRight)
        head.setLayout(head_lay)
        dock.setTitleBarWidget(head)
        dock.setWidget(self.stream_LISTupd)
        dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        dock.hide()
        return dock

    def DockUI_list(self):
        dock = QDockWidget("Detection Detail", self)
        dock_widget = QWidget()
        dock_cont = QHBoxLayout()
        tabby = QTabWidget(dock)
        tab_Canny = QWidget()
        tab_Sobel= QWidget()
        tab_Prewitt = QWidget()
        tabby.addTab(tab_Canny, "Canny")
        tabby.addTab(tab_Sobel, "Sobel")
        tabby.addTab(tab_Prewitt, "Prewitt")
        tabby.setTabPosition(2)
        header = ["Image", "Shape", "Width", "Height", "Area", "DMNT_color"]
        CannyLay = QHBoxLayout(tab_Canny)
        self.table_Canny = self.UI.tableWIDGET(len(header), colHeader=header)
        CannyLay.addWidget(self.table_Canny)
        SobelLay = QHBoxLayout(tab_Sobel)
        self.table_Sobel = self.UI.tableWIDGET(len(header), colHeader=header)
        SobelLay.addWidget(self.table_Sobel)
        PrewittLay = QHBoxLayout(tab_Prewitt)
        self.table_Prewitt = self.UI.tableWIDGET(len(header), colHeader=header)
        PrewittLay.addWidget(self.table_Prewitt)
        tabby.tabBarClicked.connect(self.tab_detail)
        tabby.currentChanged.connect(self.tab_detail)
        dock_cont.addWidget(tabby, Qt.AlignTop)
        dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        dock_widget.setLayout(dock_cont)
        dock.setWidget(dock_widget)
        dock.hide()
        return dock

    def DockUI_settings(self):
        dock = QDockWidget("Settings", self)
        dock_widget = QWidget()
        dock_cont = QVBoxLayout()
        inner = QMainWindow(dock)
        inner.setWindowFlags(Qt.Widget)
        inner2 = QMainWindow(dock)
        inner2.setWindowFlags(Qt.Widget)
        toolbar_TOP = QToolBar(inner2)
        toolbar_TOP.setMovable(False)
        self.toolbar_BTM = QToolBar(inner)
        self.toolbar_BTM.setMovable(False)
        inner.addToolBar(Qt.TopToolBarArea, toolbar_TOP)
        inner2.addToolBar(Qt.BottomToolBarArea, self.toolbar_BTM)
        tabby = QTabWidget(dock)
        tab_Pref = QScrollArea()
        tab_Set = QScrollArea()
        tab_Edge = QScrollArea()
        tabby.addTab(tab_Pref, "Preferences")
        tabby.addTab(tab_Set, "Settings")
        tabby.addTab(tab_Edge, "Edge")
        content_Pref = QWidget()
        tab_Pref.setWidget(content_Pref)
        PrefLay = QVBoxLayout(content_Pref)
        tab_Pref.setWidgetResizable(True)
        self.preference(PrefLay)
        content_Set = QWidget()
        tab_Set.setWidget(content_Set)
        SetLay = QVBoxLayout(content_Set)
        tab_Set.setWidgetResizable(True)
        self.setting(SetLay, content_Set)
        content_Edge = QWidget()
        tab_Edge.setWidget(content_Edge)
        EdgeLay = QVBoxLayout(content_Edge)
        tab_Edge.setWidgetResizable(True)
        self.edge(EdgeLay)
        self.UI.ToolButton(toolbar_TOP, 1, 'OD_assets/import.png', 'Import image', self.importIMG)
        self.webcamTOOL = self.UI.ToolButton(toolbar_TOP, 2, 'OD_assets/webcam.png', 'Stream webcam', self.webcam_set)
        self.stopcamTOOL = self.UI.ToolButton(toolbar_TOP, 1, 'OD_assets/stop.png', 'Terminate stream', self.end_stream, enable=False)
        self.detectTOOL = self.UI.ToolButton(toolbar_TOP, 2, 'OD_assets/detect.png', 'Detect object', self.detectOBJ)
        self.switchTOOL = self.UI.ToolButton(toolbar_TOP, 1, 'OD_assets/switch.png', 'Switch detection', self.switchDetection, enable=False)
        self.compareTOOL = self.UI.ToolButton(toolbar_TOP, 2, 'OD_assets/compare.png', 'Detection Comparison', lambda : self.compareDisplay(check=True), enable=False)
        self.listTOOL = self.UI.ToolButton(toolbar_TOP, 2, 'OD_assets/list.png', 'List detection details', self.detail, enable=False)
        self.UI.ToolButton(toolbar_TOP, 1, 'OD_assets/hint.png', 'Hint/Guide', lambda : self.UI.about(self, 1))
        self.UI.ToolButton(toolbar_TOP, 1, 'OD_assets/info.png', 'About application', lambda : self.UI.about(self, 2))
        self.UI.ToolButton(self.toolbar_BTM, 2, None, 'Object detection', lambda : self.switchDisplay(0), AE=True, textOnly="OBJECT", font=('Georgia bold', 11), width=105, check=True)
        self.toolbar_BTM.addSeparator()
        self.UI.ToolButton(self.toolbar_BTM, 2, None, 'Contour detection', lambda : self.switchDisplay(1), AE=True, textOnly="CONTOUR", font=('Georgia bold', 11), width=105)
        self.toolbar_BTM.addSeparator()
        self.UI.ToolButton(self.toolbar_BTM, 2, None, 'Edge detection', lambda : self.switchDisplay(2), AE=True, textOnly="EDGE", font=('Georgia bold', 11), width=105)
        self.toolbar_BTM.setEnabled(False)
        dock_cont.addWidget(inner)
        dock_cont.addWidget(tabby, Qt.AlignTop)
        dock_cont.addWidget(inner2)
        dock.setTitleBarWidget(QWidget(dock))
        dock.setFixedWidth(370)
        dock_widget.setLayout(dock_cont)
        dock.setWidget(dock_widget)
        return dock

    def detail(self):
        if not self.listTOOL.isChecked():
            self.dockStream_btn(2)
            self.dock_LIST.hide()
            return
        if self.stream_live:
            if self.dock_STREAM.isHidden():
                self.dock_LIST.hide()
                self.dock_STREAM.show()
            if self.CompareDisplay:
                n1,n2 = 0,3
            else:
                n1,n2 = self.edgeDetect, self.edgeDetect+1
            for i in range(n1, n2):
                len_, infos = self.detailProcess(i)
                bg_col = self.col_fm[i]
                fg_col = self.col_lb[i]
                if len_==0:
                    continue
                else:
                    for info in infos:
                        if i==2:
                            tt = "\t"
                        else:
                            tt = "\t\t"
                        item = QListWidgetItem("{}{}Size: {} x {}\t\tArea: {}\t\tShape: {}".format(info[0], tt, info[2], info[3], info[4], info[1]))
                        item.setFont(QFont("Georgia", 11))
                        item.setBackground(QColor(bg_col[2], bg_col[1], bg_col[0]))
                        item.setForeground(QColor(fg_col[2], fg_col[1], fg_col[0]))
                        self.stream_LISTupd.addItem(item)
                        self.stream_LISTupd.scrollToBottom()
                        count = self.stream_LISTupd.count()
                        if count>350:
                            for i in range(10):
                                self.stream_LISTupd.takeItem(0)
        else:
            if self.dock_LIST.isHidden():
                self.dock_STREAM.hide()
                self.dock_LIST.show()
            for i in range(3):
                if i==0:
                    table = self.table_Canny
                elif i==1:
                    table = self.table_Sobel
                else:
                    table = self.table_Prewitt
                col, detail = self.detailProcess(i)
                if table.columnCount()<col:
                    while table.columnCount() < col:
                        table.insertColumn(table.columnCount())
                elif table.columnCount()>col:
                    while table.columnCount() > col:
                        table.removeColumn(table.columnCount() - 1)
                for col in range(table.columnCount()):
                    for row, info in enumerate(detail[col]):
                        if row==0:
                            lbl = self.UI.label(True, False, Qt.AlignCenter)
                            lbl.setPixmap(self.setPixmap_QtImg(info, 80, 80))
                            table.setCellWidget(row, col, lbl)
                        elif row==5:
                            if self.stream_live:
                                pass
                            lbl = self.UI.label(True, True, Qt.AlignCenter)
                            lbl.setPixmap(self.setPixmap_QtImg(info, 200, 40))
                            table.setCellWidget(row, col, lbl)
                        else:
                            item = QTableWidgetItem(info)
                            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                            table.setItem(row, col, item)
                table.resizeRowsToContents()

    def detailProcess(self, flag):
        detail = []
        if flag == 0:
            ED = self.canny_detect
            name = "CANNY"
        elif flag == 1:
            ED = self.sobel_detect
            name = "SOBEL"
        elif flag == 2:
            ED = self.prewitt_detect
            name = "PREWITT"
        if not self.stream_live:
            targetIMG, _ = self.targetREF[self.n]
        unit = self.comboUnit_obj.currentText()
        for obj in ED:
            if obj[0]==0:
                shape = "Triangular (3 vertices)"
            elif obj[0]==1:
                shape = "Rectangular (4 vertices)"
            elif obj[0]==2:
                shape = "Circular"
            elif obj[0]==3:
                shape = "Geometry ({} vertices)".format(len(obj[1]))
            w, h = obj[4]
            area = float(w)*float(h)
            width = "{} {}".format(w, unit)
            height = "{} {}".format(h, unit)
            size = "{} {}\u00b2".format(round(area, 2), unit)
            if not self.stream_live:
                image = CV.maskIMG(targetIMG.copy(), obj[3])
                image = CV.cropIMG(image.copy(), obj[2])
                palette = CV.dmntCOLOR(image.copy())
            else:
                image = name
                palette = 0
            detail.append((image, shape, width, height, size, palette))
        return len(detail), detail

    def webcam_set(self):
        if self.stream_live:
            self.webcamTOOL.setChecked(True)
            return
        self.stream_dlg = Dialog(self)
        self.stream_dlg.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.stream_dlg.setWindowTitle("Stream settings")
        dlg_lay = QVBoxLayout(self.stream_dlg)
        set_lay = QHBoxLayout()
        info_lay = QVBoxLayout()
        ref_lay = QVBoxLayout()
        resize_lay = QHBoxLayout()
        frame_lay = QHBoxLayout()
        flip_lay = QHBoxLayout()
        opt_lay = QHBoxLayout()
        btn_lay = QHBoxLayout()
        dev, res = CV.deviceList()
        self.stream_lbl = self.UI.label(False, False, Qt.AlignCenter)
        self.stream_REF_lbl = self.UI.label(True, True, Qt.AlignCenter)
        self.stream_lbl.setPixmap(self.setPixmap_QtImg(np.zeros((330,600,3), np.uint8), 600, 330))
        self.stream_REF_lbl.setPixmap(self.setPixmap_QtImg(np.zeros((330, 600, 3), np.uint8), 500, 250))
        self.comboDevice = self.UI.comboBox("Available devices", dev, minWidth=20, action=self.update_device, height=25)
        self.spinRES_W = self.UI.spinBox(True, 100, 4000, res[0][0], 100, maxWidth=100, action=lambda : self.update_res(True))
        self.spinRES_H = self.UI.spinBox(True, 100, 4000, res[0][1], 100, maxWidth=100, action=lambda : self.update_res(False))
        self.spinResize_W = self.UI.spinBox(True, 100, 4000, res[0][0], 100, maxWidth=100)
        self.spinResize_H = self.UI.spinBox(True, 100, 4000, res[0][1], 100, maxWidth=100)
        self.res_lbl = self.UI.textLabel("    RES: {} x {}".format(res[0][0], res[0][1]), ("Georgia", 10), align=Qt.AlignLeft)
        self.ref_opt1 = self.UI.textLabel("Background", font=('Georgia', 11), align=Qt.AlignCenter, border=1, color='#ffffff', height=25)
        self.ref_opt2 = self.UI.textLabel("Platform", font=('Georgia', 11), align=Qt.AlignCenter, border=1, color='#ffffff', height=25)
        ratio = self.UI.checkbox("Keep Aspect Ratio", lambda : self.check(25, ratio), True, font=('Georgia', 11))
        info_lay.addWidget(self.UI.textLabel("Device", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        info_lay.addWidget(self.comboDevice)
        info_lay.addWidget(self.UI.textLabel("Resolution", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        frame_lay.addWidget(self.spinRES_W)
        frame_lay.addWidget(self.UI.textLabel("x", ("Georgia", 11), align=Qt.AlignCenter, width=20))
        frame_lay.addWidget(self.spinRES_H)
        info_lay.addLayout(frame_lay)
        info_lay.addWidget(self.res_lbl)
        info_lay.addWidget(self.UI.textLabel("Resize", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        info_lay.addWidget(ratio)
        resize_lay.addWidget(self.spinResize_W)
        resize_lay.addWidget(self.UI.textLabel("x", ("Georgia", 11), align=Qt.AlignCenter, width=20))
        resize_lay.addWidget(self.spinResize_H)
        info_lay.addLayout(resize_lay)
        info_lay.addWidget(self.UI.textLabel("Invert", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        flip_lay.addWidget(self.UI.textBtn("Horizontal", lambda: self.stream_onChange(2), font=('Georgia', 10)))
        flip_lay.addWidget(self.UI.textBtn("Vertical", lambda: self.stream_onChange(3), font=('Georgia', 10)))
        info_lay.addLayout(flip_lay)
        opt_lay.addWidget(self.ref_opt1)
        opt_lay.addWidget(self.ref_opt2)
        btn_lay.addWidget(self.UI.textBtn("APPLY", self.apply_stream, font=('Georgia', 10)))
        btn_lay.addWidget(self.UI.textBtn("TERMINATE", self.close_stream_set, font=('Georgia', 10)))
        ref_lay.addWidget(self.UI.textLabel("Target Reference", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        ref_lay.addLayout(opt_lay)
        ref_lay.addWidget(self.UI.textLabel("Target Image", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        ref_lay.addWidget(self.stream_REF_lbl)
        ref_lay.addWidget(self.UI.textBtn("REFRESH", lambda : self.stream_onChange(1), font=('Georgia', 10)))
        ref_lay.addLayout(btn_lay)
        set_lay.addLayout(info_lay)
        set_lay.addLayout(ref_lay)
        dlg_lay.addWidget(self.UI.textLabel("Live Stream", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        dlg_lay.addWidget(self.stream_lbl)
        dlg_lay.addWidget(self.UI.textLabel("Settings", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        dlg_lay.addLayout(set_lay)
        dlg_lay.setAlignment(Qt.AlignTop)
        self.stream_dlg.setLayout(dlg_lay)
        self.stream_ref = True
        self.streaming()
        self.stream_dlg.exec_()

    def apply_stream(self):
        self.stopcamTOOL.setEnabled(True)
        self.stream_dlg.close()
        self.stream_live = True
        self.detectTOOL.setCheckable(True)
        self.compareTOOL.setChecked(False)
        self.compareTOOL.setEnabled(False)
        self.CompareDisplay = False
        if not self.zoom_slider.isEnabled():
            self.zoom_slider.setEnabled(True)
        self.getTarget_REF()
        self.targetREF_list.setCurrentRow(0)
        self.fileNAME.setText("LIVE")
        self.statusBar().showMessage("2. Please adjust settings before detection")
        self.live_ref1.setEnabled(True)
        self.live_ref2.setEnabled(True)

    def end_stream(self):
        self.webcamTOOL.setChecked(False)
        self.stopcamTOOL.setEnabled(False)
        self.detectTOOL.setCheckable(False)
        self.thread.stop()
        self.stream_live = self.live_detect = False
        self.fileNAME.setText("filename")
        self.UI.infoDialog(self, 1)
        self.statusBar().showMessage("INFO: LIVE stream terminated")
        self.live_ref1.setEnabled(False)
        self.live_ref2.setEnabled(False)

    def close_stream_set(self):
        self.webcamTOOL.setChecked(False)
        self.stream_dlg.close()
        self.thread.stop()

    def update_stream(self, image):
        if self.flipH:
            image = cv2.flip(image, 1)
        if self.flipV:
            image = cv2.flip(image, 0)
        if not self.stream_live:
            self.stream_lbl.setPixmap(self.setPixmap_QtImg(image, 600, 330))
            if self.stream_ref:
                self.stream_REF_lbl.setPixmap(self.setPixmap_QtImg(image, 600, 330))
                self.image = image.copy()
                self.detect_img_lb.setPixmap(self.setPixmap_QtImg(self.image.copy(), 200, 150))
                self.getTarget_REF()
                self.stream_ref = False
        else:
            image = CV.resizeImage(image.copy(), self.kar, self.spinResize_W.value(), self.spinResize_H.value())
            self.image = image.copy()
            self.renderIMG = self.image.copy()
            if self.live_detect:
                self.detectOBJ()
            else:
                self.Render()

    def streaming(self, res=None):
        self.thread = VideoThread(int(self.comboDevice.currentText()), res)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_stream)
        # start the thread
        self.thread.start()

    def update_device(self):
        self.thread.stop()
        self.streaming()

    def update_res(self, flag):
        if flag:
            w,h = self.thread.resolution(width=self.spinRES_W.value())
        else:
            w, h = self.thread.resolution(height=self.spinRES_H.value())
        self.res_lbl.setText("RES: {} x {}".format(w, h))
        self.spinResize_W.setValue(w)
        self.spinResize_H.setValue(h)
        self.thread.stop()
        self.streaming(res=(w,h))

    def stream_onChange(self, flag):
        if flag==1:
            self.stream_ref = True
        elif flag==2:
            self.flipH = True if not self.flipH else False
        elif flag==3:
            self.flipV = True if not self.flipV else False

    def live_REF(self):
        if self.live_ref1.isChecked():
            self.live_ref = True       # Background
        elif self.live_ref2.isChecked():
            self.live_ref = False      # Platform
            self.UI.infoDialog(self, 2)
            self.statusBar().showMessage("Info: Override might occurred")

    def edge(self, mainlay):
        gau_lay = QHBoxLayout()
        canny_lay1 = QHBoxLayout()
        canny_lay2 = QHBoxLayout()
        canny_lay3 = QHBoxLayout()
        sobel_lay1 = QHBoxLayout()
        sobel_lay2 = QHBoxLayout()
        sobel_lay3 = QHBoxLayout()
        sobel_lay4 = QHBoxLayout()
        prewitt_lay1 = QHBoxLayout()
        prewitt_lay2 = QHBoxLayout()
        prewitt_lay3 = QHBoxLayout()
        self.spinG_Filter = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinSigma = self.UI.spinBox(True, 0, 99, 0, 1)
        self.spinCThres_low = self.UI.spinBox(True, 0, 255, 150, 1)
        self.spinCThres_high = self.UI.spinBox(True, 0, 255, 200, 1)
        self.spinCDil_k = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinCDil_i = self.UI.spinBox(True, 1, 99, 3, 1)
        self.spinCEro_k = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinCEro_i = self.UI.spinBox(True, 1, 99, 2, 1)
        self.spinSobel_k = self.UI.spinBox(True, 1, 99, 3, 2, odd=True)
        self.spinSDil_k = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinSDil_i = self.UI.spinBox(True, 1, 99, 3, 1)
        self.spinSEro_k = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinSEro_i = self.UI.spinBox(True, 1, 99, 2, 1)
        self.spinPDil_k = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinPDil_i = self.UI.spinBox(True, 1, 99, 3, 1)
        self.spinPEro_k = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinPEro_i = self.UI.spinBox(True, 1, 99, 2, 1)
        self.spinSThres_low = self.UI.spinBox(True, 0, 255, 110, 1)
        self.spinSThres_high = self.UI.spinBox(True, 0, 255, 255, 1)
        self.spinPThres_low = self.UI.spinBox(True, 0, 255, 110, 1)
        self.spinPThres_high = self.UI.spinBox(True, 0, 255, 255, 1)
        CThres_auto = self.UI.checkbox('Auto', lambda : self.check(10, CThres_auto), True, font=('Georgia', 11))
        CDil = self.UI.checkbox('Dilation', lambda : self.check(11, CDil), True, font=('Georgia', 11))
        SDil = self.UI.checkbox('Dilation', lambda : self.check(12, SDil), True, font=('Georgia', 11))
        PDil = self.UI.checkbox('Dilation', lambda : self.check(13, PDil), True, font=('Georgia', 11))
        CEro = self.UI.checkbox('Erosion', lambda : self.check(14, CEro), True, font=('Georgia', 11))
        SEro = self.UI.checkbox('Erosion', lambda : self.check(15, SEro), True, font=('Georgia', 11))
        PEro = self.UI.checkbox('Erosion', lambda : self.check(16, PEro), True, font=('Georgia', 11))
        CThin = self.UI.checkbox('Thinning', lambda: self.check(18, CThin), False, font=('Georgia', 11))
        SThin = self.UI.checkbox('Thinning', lambda : self.check(19, SThin), False, font=('Georgia', 11))
        PThin = self.UI.checkbox('Thinning', lambda : self.check(20, PThin), False, font=('Georgia', 11))
        SThres_auto = self.UI.checkbox('Auto', lambda: self.check(21, SThres_auto), True, font=('Georgia', 11))
        PThres_auto = self.UI.checkbox('Auto', lambda: self.check(22, PThres_auto), True, font=('Georgia', 11))
        SThres = self.UI.checkbox('Thresholding', lambda: self.check(23, SThres), False, font=('Georgia', 11))
        PThres = self.UI.checkbox('Thresholding', lambda: self.check(24, PThres), False, font=('Georgia', 11))
        mainlay.addWidget(self.UI.textLabel("Gaussian Filtering", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        gau_lay.addStretch(1)
        gau_lay.addWidget(self.UI.textLabel("Kernel size", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        gau_lay.addWidget(self.spinG_Filter)
        gau_lay.addStretch(1)
        gau_lay.addWidget(self.UI.textLabel("SigmaX", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        gau_lay.addWidget(self.spinSigma)
        mainlay.addLayout(gau_lay)
        canny_lay1.addWidget(CThres_auto)
        canny_lay1.addStretch(1)
        canny_lay1.addWidget(self.spinCThres_low)
        canny_lay1.addWidget(self.UI.textLabel("< Threshold <", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        canny_lay1.addWidget(self.spinCThres_high)
        canny_lay1.addStretch(1)
        canny_lay2.addWidget(CDil)
        canny_lay2.addStretch(2)
        canny_lay2.addWidget(self.UI.textLabel("Kernel", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        canny_lay2.addWidget(self.spinCDil_k)
        canny_lay2.addStretch(1)
        canny_lay2.addWidget(self.UI.textLabel("Iterate", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        canny_lay2.addWidget(self.spinCDil_i)
        canny_lay3.addWidget(CEro)
        canny_lay3.addStretch(2)
        canny_lay3.addWidget(self.UI.textLabel("Kernel", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        canny_lay3.addWidget(self.spinCEro_k)
        canny_lay3.addStretch(1)
        canny_lay3.addWidget(self.UI.textLabel("Iterate", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        canny_lay3.addWidget(self.spinCEro_i)
        sobel_lay1.addStretch(1)
        sobel_lay1.addWidget(self.UI.textLabel("Kernel size", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        sobel_lay1.addStretch(1)
        sobel_lay1.addWidget(self.spinSobel_k)
        sobel_lay1.addStretch(1)
        sobel_lay2.addWidget(SDil)
        sobel_lay2.addStretch(2)
        sobel_lay2.addWidget(self.UI.textLabel("Kernel", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        sobel_lay2.addWidget(self.spinSDil_k)
        sobel_lay2.addStretch(1)
        sobel_lay2.addWidget(self.UI.textLabel("Iterate", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        sobel_lay2.addWidget(self.spinSDil_i)
        sobel_lay3.addWidget(SEro)
        sobel_lay3.addStretch(2)
        sobel_lay3.addWidget(self.UI.textLabel("Kernel", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        sobel_lay3.addWidget(self.spinSEro_k)
        sobel_lay3.addStretch(1)
        sobel_lay3.addWidget(self.UI.textLabel("Iterate", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        sobel_lay3.addWidget(self.spinSEro_i)
        sobel_lay4.addWidget(SThres_auto)
        sobel_lay4.addStretch(1)
        sobel_lay4.addWidget(self.spinSThres_low)
        sobel_lay4.addWidget(self.UI.textLabel("< Threshold <", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        sobel_lay4.addWidget(self.spinSThres_high)
        prewitt_lay1.addWidget(PDil)
        prewitt_lay1.addStretch(2)
        prewitt_lay1.addWidget(self.UI.textLabel("Kernel", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        prewitt_lay1.addWidget(self.spinPDil_k)
        prewitt_lay1.addStretch(1)
        prewitt_lay1.addWidget(self.UI.textLabel("Iterate", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        prewitt_lay1.addWidget(self.spinPDil_i)
        prewitt_lay2.addWidget(PEro)
        prewitt_lay2.addStretch(2)
        prewitt_lay2.addWidget(self.UI.textLabel("Kernel", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        prewitt_lay2.addWidget(self.spinPEro_k)
        prewitt_lay2.addStretch(1)
        prewitt_lay2.addWidget(self.UI.textLabel("Iterate", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        prewitt_lay2.addWidget(self.spinPEro_i)
        prewitt_lay3.addWidget(PThres_auto)
        prewitt_lay3.addStretch(1)
        prewitt_lay3.addWidget(self.spinPThres_low)
        prewitt_lay3.addWidget(self.UI.textLabel("< Threshold <", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        prewitt_lay3.addWidget(self.spinPThres_high)
        mainlay.addWidget(self.UI.textLabel("Canny Edge Detector", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        mainlay.addLayout(canny_lay1)
        mainlay.addWidget(self.UI.textLabel("Thinning", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addWidget(CThin)
        mainlay.addWidget(self.UI.textLabel("Morphology", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addLayout(canny_lay2)
        mainlay.addLayout(canny_lay3)
        mainlay.addWidget(self.UI.textLabel("Sobel Edge Detector", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        mainlay.addLayout(sobel_lay1)
        mainlay.addWidget(self.UI.textLabel("Thresholding", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addWidget(SThres)
        mainlay.addLayout(sobel_lay4)
        mainlay.addWidget(self.UI.textLabel("Thinning", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addWidget(SThin)
        mainlay.addWidget(self.UI.textLabel("Morphology", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addLayout(sobel_lay2)
        mainlay.addLayout(sobel_lay3)
        mainlay.addWidget(self.UI.textLabel("Prewitt Edge Detector", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        mainlay.addWidget(self.UI.textLabel("Thresholding", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addWidget(PThres)
        mainlay.addLayout(prewitt_lay3)
        mainlay.addWidget(self.UI.textLabel("Thinning", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addWidget(PThin)
        mainlay.addWidget(self.UI.textLabel("Morphology", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addLayout(prewitt_lay1)
        mainlay.addLayout(prewitt_lay2)
        mainlay.setAlignment(Qt.AlignTop)

    def setting(self, mainlay, content):
        optH_Lay = QHBoxLayout()
        edge_Lay = QVBoxLayout()
        shape_Lay = QVBoxLayout()
        lim_lay = QVBoxLayout()
        cond_lay = QVBoxLayout()
        msm_lay = QHBoxLayout()
        unit_lay = QHBoxLayout()
        gau_lay = QHBoxLayout()
        dil_lay = QHBoxLayout()
        ero_lay = QHBoxLayout()
        canny_lay = QHBoxLayout()
        btn_lay = QHBoxLayout()
        radio_lay = QHBoxLayout()
        self.targetREF_list = QListWidget(content)
        self.targetREF_list.setResizeMode(QListView.Adjust)
        self.targetREF_list.setLayout(QHBoxLayout())
        self.targetREF_list.setViewMode(QListView.IconMode)
        self.targetREF_list.setIconSize(QSize(90, 90))
        self.targetREF_list.setMinimumHeight(100)
        self.detect_img_lb = self.UI.label(False, False, Qt.AlignHCenter)
        self.detect_img_lb.setPixmap(self.setPixmap_QtImg(CV.loadImage("OD_assets/image.png"), 200, 150))
        self.detect_img_lb.resize(200, 150)
        edge_Lay.addWidget(self.UI.textLabel("Edge Operator", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        canny_oprt = self.UI.checkbox('Canny', lambda : self.check(3, canny_oprt), True, font=('Georgia', 11))
        sobel_oprt = self.UI.checkbox('Sobel', lambda : self.check(4, sobel_oprt), True, font=('Georgia', 11))
        prewitt_oprt = self.UI.checkbox('Prewitt', lambda : self.check(5, prewitt_oprt), True, font=('Georgia', 11))
        tri_shape = self.UI.checkbox('Triangular', lambda : self.check(6, tri_shape), True, font=('Georgia', 11))
        rect_shape = self.UI.checkbox('Rectangular', lambda : self.check(7, rect_shape), True, font=('Georgia', 11))
        cir_shape = self.UI.checkbox('Circular', lambda : self.check(8, cir_shape), True, font=('Georgia', 11))
        other_shape = self.UI.checkbox('Others', lambda: self.check(26, other_shape), True, font=('Georgia', 11))
        CThres_autoREF = self.UI.checkbox('Auto', lambda : self.check(9, CThres_autoREF), True, font=('Georgia', 11))
        edge_Lay.addWidget(canny_oprt)
        edge_Lay.addWidget(sobel_oprt)
        edge_Lay.addWidget(prewitt_oprt)
        edge_Lay.setAlignment(Qt.AlignTop)
        shape_Lay.addWidget(self.UI.textLabel("Shape Detection", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        shape_Lay.addWidget(tri_shape)
        shape_Lay.addWidget(rect_shape)
        shape_Lay.addWidget(cir_shape)
        shape_Lay.addWidget(other_shape)
        self.spinLIM_ref = self.UI.spinBox(True, 1, 1000000, 50000, 5, minWidth=80)
        self.spinLIM_tri = self.UI.spinBox(True, 1, 100000, 2000, 5, minWidth=80)
        self.spinLIM_rect = self.UI.spinBox(True, 1, 100000, 2000, 5, minWidth=80)
        self.spinLIM_cir = self.UI.spinBox(True, 1, 100000, 2000, 5, minWidth=80)
        self.spinLIM_other = self.UI.spinBox(True, 1, 100000, 2000, 5, minWidth=80)
        self.spinCir_Min = self.UI.spinBox(False, 0.1, 2.0, 0.7, 0.1)
        self.spinCir_Max = self.UI.spinBox(False, 0.1, 2.0, 1.2, 0.1)
        self.spinWidth_ref = self.UI.spinBox(True, 1, 10000, 210, 1)
        self.spinHeight_ref = self.UI.spinBox(True, 1, 10000, 297, 1)
        self.comboUnit_ref = self.UI.comboBox("unit measurement", ["mm", "cm", "m"])
        self.spinG_Filter_ref = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinSigma_ref = self.UI.spinBox(True, 0, 99, 1, 1)
        self.spinREF_Dil_k = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinREF_Dil_i = self.UI.spinBox(True, 1, 99, 3, 1)
        self.spinREF_Ero_k = self.UI.spinBox(True, 1, 99, 5, 2, odd=True)
        self.spinREF_Ero_i = self.UI.spinBox(True, 1, 99, 2, 1)
        self.spinREFCThres_low = self.UI.spinBox(True, 0, 255, 150, 1)
        self.spinREFCThres_high = self.UI.spinBox(True, 0, 255, 200, 1)
        lim_lay.addWidget(self.UI.textLabel("Minimum Area", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        lim_ref_lay = QHBoxLayout()
        lim_ref_lay.addWidget(self.UI.textLabel("Reference", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_ref_lay.addStretch(1)
        lim_ref_lay.addWidget(self.spinLIM_ref)
        lim_ref_lay.addWidget(self.UI.textLabel("pixel", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_lay.addLayout(lim_ref_lay)
        lim_tri_lay = QHBoxLayout()
        lim_tri_lay.addWidget(self.UI.textLabel("Triangular", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_tri_lay.addStretch(1)
        lim_tri_lay.addWidget(self.spinLIM_tri)
        lim_tri_lay.addWidget(self.UI.textLabel("pixel", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_lay.addLayout(lim_tri_lay)
        lim_rect_lay = QHBoxLayout()
        lim_rect_lay.addWidget(self.UI.textLabel("Rectangular", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_rect_lay.addStretch(1)
        lim_rect_lay.addWidget(self.spinLIM_rect)
        lim_rect_lay.addWidget(self.UI.textLabel("pixel", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_lay.addLayout(lim_rect_lay)
        lim_cir_lay = QHBoxLayout()
        lim_cir_lay.addWidget(self.UI.textLabel("Circular", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_cir_lay.addStretch(1)
        lim_cir_lay.addWidget(self.spinLIM_cir)
        lim_cir_lay.addWidget(self.UI.textLabel("pixel", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_lay.addLayout(lim_cir_lay)
        lim_other_lay = QHBoxLayout()
        lim_other_lay.addWidget(self.UI.textLabel("Others", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_other_lay.addStretch(1)
        lim_other_lay.addWidget(self.spinLIM_other)
        lim_other_lay.addWidget(self.UI.textLabel("pixel", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        lim_lay.addLayout(lim_other_lay)
        cond_lay.addWidget(self.UI.textLabel("Approximation", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        tri_lay = QHBoxLayout()
        rect_lay = QHBoxLayout()
        tri_lay.addWidget(self.UI.textLabel("Triangular", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        tri_lay.addWidget(self.UI.textLabel("3 vertices", font=('Georgia', 10), align=Qt.AlignRight, border=0))
        rect_lay.addWidget(self.UI.textLabel("Rectangular", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        rect_lay.addWidget(self.UI.textLabel("4 vertices", font=('Georgia', 10), align=Qt.AlignRight, border=0))
        cond_lay.addLayout(tri_lay)
        cond_lay.addLayout(rect_lay)
        cir_min_lay = QHBoxLayout()
        cir_min_lay.addWidget(self.UI.textLabel("Circularity MIN", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        cir_min_lay.addStretch(1)
        cir_min_lay.addWidget(self.spinCir_Min)
        cond_lay.addLayout(cir_min_lay)
        cir_max_lay = QHBoxLayout()
        cir_max_lay.addWidget(self.UI.textLabel("Circularity MAX", font=('Georgia', 10), align=Qt.AlignLeft, border=0))
        cir_max_lay.addStretch(1)
        cir_max_lay.addWidget(self.spinCir_Max)
        cond_lay.addLayout(cir_max_lay)
        msm_lay.addWidget(self.UI.textLabel("Width", font=('Georgia', 10), align=Qt.AlignCenter, border=0))
        msm_lay.addWidget(self.spinWidth_ref)
        msm_lay.addStretch(1)
        msm_lay.addWidget(self.UI.textLabel("Height", font=('Georgia', 10), align=Qt.AlignCenter, border=0))
        msm_lay.addWidget(self.spinHeight_ref)
        unit_lay.addWidget(self.UI.textLabel("Unit    ", font=('Georgia', 10), align=Qt.AlignCenter, border=0))
        unit_lay.addWidget(self.comboUnit_ref)
        unit_lay.addStretch(2)
        mainlay.addWidget(self.UI.textLabel("Target Image", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        mainlay.addWidget(self.detect_img_lb)
        optH_Lay.addLayout(edge_Lay)
        optH_Lay.addLayout(shape_Lay)
        mainlay.addLayout(optH_Lay)
        mainlay.addLayout(lim_lay)
        mainlay.addLayout(cond_lay)
        mainlay.addWidget(self.UI.textLabel("Target Reference", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        mainlay.addWidget(self.UI.textLabel("Gaussian Filtering", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        gau_lay.addStretch(1)
        gau_lay.addWidget(self.UI.textLabel("Kernel size", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        gau_lay.addWidget(self.spinG_Filter_ref)
        gau_lay.addStretch(1)
        gau_lay.addWidget(self.UI.textLabel("SigmaX", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        gau_lay.addWidget(self.spinSigma_ref)
        mainlay.addLayout(gau_lay)
        mainlay.addWidget(self.UI.textLabel("Canny Edge Detector", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        canny_lay.addWidget(CThres_autoREF)
        canny_lay.addStretch(1)
        canny_lay.addWidget(self.spinREFCThres_low)
        canny_lay.addWidget(self.UI.textLabel("< Threshold <", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        canny_lay.addWidget(self.spinREFCThres_high)
        canny_lay.addStretch(1)
        mainlay.addLayout(canny_lay)
        mainlay.addWidget(self.UI.textLabel("Dilation", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        dil_lay.addStretch(1)
        dil_lay.addWidget(self.UI.textLabel("Kernel", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        dil_lay.addWidget(self.spinREF_Dil_k)
        dil_lay.addStretch(1)
        dil_lay.addWidget(self.UI.textLabel("Iterate", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        dil_lay.addWidget(self.spinREF_Dil_i)
        dil_lay.addStretch(1)
        mainlay.addLayout(dil_lay)
        mainlay.addWidget(self.UI.textLabel("Erosion", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        ero_lay.addStretch(1)
        ero_lay.addWidget(self.UI.textLabel("Kernel", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        ero_lay.addWidget(self.spinREF_Ero_k)
        ero_lay.addStretch(1)
        ero_lay.addWidget(self.UI.textLabel("Iterate", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        ero_lay.addWidget(self.spinREF_Ero_i)
        ero_lay.addStretch(1)
        mainlay.addLayout(ero_lay)
        mainlay.addWidget(self.UI.textLabel("Target image", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addWidget(self.UI.textLabel("* Please select a target image below", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        mainlay.addWidget(self.targetREF_list)
        mainlay.addWidget(self.UI.textLabel("Measurement", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addLayout(msm_lay)
        mainlay.addLayout(unit_lay)
        self.live_ref1 = self.UI.radioButton("Background", font=('Georgia', 10), AE=True, enable=False, check=True)
        self.live_ref2 = self.UI.radioButton("Platform", font=('Georgia', 10), AE=True, enable=False)
        self.live_ref2.toggled.connect(self.live_REF)
        radio_lay.addStretch(1)
        radio_lay.addWidget(self.live_ref1)
        radio_lay.addStretch(1)
        radio_lay.addWidget(self.live_ref2)
        radio_lay.addStretch(1)
        mainlay.addWidget(self.UI.textLabel("LIVE stream Reference", font=('Georgia', 12), color='#bae998', align=Qt.AlignCenter, border=0, height=30))
        mainlay.addLayout(radio_lay)
        btn_lay.addStretch(1)
        btn_lay.addWidget(self.UI.textBtn("Refresh", self.getTarget_REF, font=('Georgia', 10)))
        mainlay.addLayout(btn_lay)
        mainlay.setAlignment(Qt.AlignTop)
        
    def preference(self, mainLay):
        unit_lay = QHBoxLayout()
        font_lay = QHBoxLayout()
        font_lay1 = QVBoxLayout()
        font_lay2 = QVBoxLayout()
        font_lay3 = QVBoxLayout()
        col_lay = QHBoxLayout()
        oprt_lay = QVBoxLayout()
        fm_lay = QVBoxLayout()
        lb_lay = QVBoxLayout()
        bound_lay = QHBoxLayout()
        bound_lay1 = QVBoxLayout()
        bound_lay2 = QVBoxLayout()
        bound_lay3 = QVBoxLayout()
        size_lay1 = QHBoxLayout()
        size_lay2 = QHBoxLayout()
        self.spinDeci = self.UI.spinBox(True, 0, 5, 1, 1)
        oprt = self.UI.checkbox('Operator', lambda : self.check(1, oprt), True, font=('Georgia', 11))
        msm = self.UI.checkbox('Measurement', lambda : self.check(2, msm), True, font=('Georgia', 11))
        bound = self.UI.checkbox('Bounding', lambda: self.check(17, bound), True, font=('Georgia', 11))
        mainLay.addWidget(self.UI.textLabel("Labelling", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        mainLay.addWidget(oprt)
        mainLay.addWidget(bound)
        mainLay.addWidget(msm)
        self.comboUnit_obj = self.UI.comboBox("unit measurement",["mm", "cm", "m"])
        unit_lay.addWidget(self.UI.textLabel("      Decimal:", font=('Georgia', 10), align=Qt.AlignCenter, border=0))
        unit_lay.addWidget(self.spinDeci)
        unit_lay.addStretch(1)
        unit_lay.addWidget(self.UI.textLabel("Unit:", font=('Georgia', 10), align=Qt.AlignCenter, border=0))
        unit_lay.addWidget(self.comboUnit_obj)
        mainLay.addLayout(unit_lay)
        mainLay.addWidget(self.UI.textLabel("Font", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        font_lay1.addWidget(self.UI.textLabel("Operator", font=('Georgia', 11), align=Qt.AlignLeft, border=0))
        font_lay1.addWidget(self.UI.textLabel("Measurement", font=('Georgia', 11), align=Qt.AlignLeft, border=0))
        self.comboFont_Oprt = self.UI.comboBox("font_Operator", ["Hershey Complex", "Hershey Cmplx(S)", "Hershey Duplex", "Hershey Plain", "Hershey Script(C)", "Hershey Script(S)", "Hershey Triplex", "Italic"], minWidth=100)
        self.spinFSize_Oprt = self.UI.spinBox(False, 0.1, 30, 0.8, 0.5, maxWidth=80, minWidth=50)
        self.comboFont_Msm = self.UI.comboBox("font_Measurement", ["Hershey Complex", "Hershey Cmplx(S)", "Hershey Duplex", "Hershey Plain", "Hershey Script(C)", "Hershey Script(S)", "Hershey Triplex", "Italic"], minWidth=100)
        self.spinFSize_Msm = self.UI.spinBox(False, 0.1, 30, 0.65, 0.5, maxWidth=80, minWidth=50)
        self.spinBoundOBJSize = self.UI.spinBox(True, 1, 99, 3, 1)
        self.spinBoundCONTSize = self.UI.spinBox(True, 0, 99, 0, 1)
        self.spinWidth_Oprt = self.UI.spinBox(True, 1, 1000, 120, 1)
        self.spinHeight_Oprt = self.UI.spinBox(True, 1, 1000, 35, 1)
        self.spinWidth_Msm = self.UI.spinBox(True, 0, 1000, 0, 1)
        self.spinHeight_Msm = self.UI.spinBox(True, 1, 1000, 30, 1)
        font_lay2.addWidget(self.comboFont_Oprt)
        font_lay2.addWidget(self.comboFont_Msm)
        font_lay3.addWidget(self.spinFSize_Oprt)
        font_lay3.addWidget(self.spinFSize_Msm)
        font_lay.addLayout(font_lay1)
        font_lay.addLayout(font_lay2)
        font_lay.addLayout(font_lay3)
        mainLay.addLayout(font_lay)
        mainLay.addLayout(font_lay2)
        mainLay.addWidget(self.UI.textLabel("Colour", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        oprt_lay.addWidget(self.UI.textLabel("Operator", font=('Georgia bold', 11), align=Qt.AlignCenter, border=0))
        oprt_lay.addWidget(self.UI.textLabel("Canny", font=('Georgia', 11), align=Qt.AlignLeft, border=0, height=25))
        oprt_lay.addWidget(self.UI.textLabel("Sobel", font=('Georgia', 11), align=Qt.AlignLeft, border=0, height=25))
        oprt_lay.addWidget(self.UI.textLabel("Prewitt", font=('Georgia', 11), align=Qt.AlignLeft, border=0, height=25))
        fm_lay.addWidget(self.UI.textLabel("Frame", font=('Georgia bold', 11), align=Qt.AlignCenter, border=0))
        self.pref_col_fm = [self.UI.colorBtn(self.col_fm[0], lambda : self.colorDialog((1,0)), height=25), self.UI.colorBtn(self.col_fm[1], lambda : self.colorDialog((1, 1)), height=25), self.UI.colorBtn(self.col_fm[2], lambda : self.colorDialog((1, 2)), height=25)]
        for pref in self.pref_col_fm:
            fm_lay.addWidget(pref)
        lb_lay.addWidget(self.UI.textLabel("Label", font=('Georgia bold', 11), align=Qt.AlignCenter, border=0))
        self.pref_col_lb = [self.UI.colorBtn(self.col_lb[0], lambda : self.colorDialog((2, 0)), height=25), self.UI.colorBtn(self.col_lb[1], lambda : self.colorDialog((2, 1)), height=25), self.UI.colorBtn(self.col_lb[2], lambda : self.colorDialog((2, 2)), height=25)]
        for pref in self.pref_col_lb:
            lb_lay.addWidget(pref)
        col_lay.addLayout(oprt_lay)
        col_lay.addLayout(fm_lay)
        col_lay.addLayout(lb_lay)
        mainLay.addLayout(col_lay)
        size_lay1.addWidget(self.UI.textLabel("Operator", font=('Georgia', 11), align=Qt.AlignLeft, border=0))
        size_lay1.addStretch(1)
        size_lay1.addWidget(self.spinWidth_Oprt)
        size_lay1.addWidget(self.UI.textLabel("x", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        size_lay1.addWidget(self.spinHeight_Oprt)
        size_lay2.addWidget(self.UI.textLabel("Measurement", font=('Georgia', 11), align=Qt.AlignLeft, border=0))
        size_lay2.addStretch(1)
        size_lay2.addWidget(self.spinWidth_Msm)
        size_lay2.addWidget(self.UI.textLabel("x", font=('Georgia', 11), align=Qt.AlignCenter, border=0))
        size_lay2.addWidget(self.spinHeight_Msm)
        mainLay.addWidget(self.UI.textLabel("Size (w x h)", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        mainLay.addLayout(size_lay1)
        mainLay.addLayout(size_lay2)
        self.bound_color = [(203,255,0), (0,0,255)]
        self.pref_col_bound = []
        self.pref_col_bound.append(self.UI.colorBtn(self.bound_color[0], lambda : self.colorDialog(0), height=25))
        self.pref_col_bound.append(self.UI.colorBtn(self.bound_color[1], lambda: self.colorDialog(1), height=25))
        bound_lay1.addWidget(self.UI.textLabel("Bound", font=('Georgia bold', 11), align=Qt.AlignCenter, border=0))
        bound_lay1.addWidget(self.UI.textLabel("Object", font=('Georgia', 11), align=Qt.AlignLeft, border=0, height=25))
        bound_lay1.addWidget(self.UI.textLabel("Contour", font=('Georgia', 11), align=Qt.AlignLeft, border=0, height=25))
        bound_lay2.addWidget(self.UI.textLabel("Colour", font=('Georgia bold', 11), align=Qt.AlignCenter, border=0))
        bound_lay2.addWidget(self.pref_col_bound[0])
        bound_lay2.addWidget(self.pref_col_bound[1])
        bound_lay3.addWidget(self.UI.textLabel("Thick", font=('Georgia bold', 11), align=Qt.AlignCenter, border=0))
        bound_lay3.addWidget(self.spinBoundOBJSize)
        bound_lay3.addWidget(self.spinBoundCONTSize)
        bound_lay.addLayout(bound_lay1)
        bound_lay.addLayout(bound_lay2)
        bound_lay.addLayout(bound_lay3)
        mainLay.addWidget(self.UI.textLabel("Bounding", font=('Georgia', 12), color='#4ad09b', align=Qt.AlignCenter, border=2, height=30))
        mainLay.addLayout(bound_lay)
        mainLay.setAlignment(Qt.AlignTop)

    def compareDisplay(self, check=False):
        if check:
            if self.CompareDisplay:
                self.CompareDisplay = False
            else:
                self.CompareDisplay = True
        if self.CompareDisplay:
            self.renderIMG = CV.compareIMG(self.finalRes(compare=True))
            self.Render()
            self.edgeOPRT.setText("Edge: COMPARE")
        else:
            self.finalRes()

    def switchDisplay(self, flag):
        self.display = flag
        if flag==0:
            self.mode.setText("OBJECT")
        elif flag==1:
            self.mode.setText("CONTOUR")
        elif flag==2:
            self.mode.setText("EDGE")
        self.compareDisplay()

    def switchDetection(self):
        if self.CompareDisplay:
            return
        self.edgeDetect += 1
        if self.edgeDetect>2:
            self.edgeDetect = 0
        self.finalRes()

    def detectOBJ(self):
        if not self.stream_live:
            self.detectTOOL.setCheckable(False)
            if self.targetREF_list.currentRow()==-1 or not self.targetREF:
                if not self.targetREF:
                    self.UI.warnDialog(self, 2)
                    self.statusBar().showMessage("Warning: Image not found")
                else:
                    self.UI.warnDialog(self, 3)
                    self.statusBar().showMessage("Warning: Target not selected")
                return
        if not self.toolbar_BTM.isEnabled():
            self.toolbar_BTM.setEnabled(True)
        if not self.compareTOOL.isEnabled():
            self.compareTOOL.setEnabled(True)
        if not self.switchTOOL.isEnabled():
            self.switchTOOL.setEnabled(True)
        if not self.listTOOL.isEnabled():
            self.listTOOL.setEnabled(True)
        if self.stream_live:
            self.getTarget_REF()
            self.live_detect = True if self.detectTOOL.isChecked() else False
            if self.live_ref or not self.live_ref and len(self.targetREF)!=2:
                self.n = 0
            else:
                self.n = 1
        else:
            self.n = self.targetREF_list.currentRow()
        targetIMG, scale = self.targetREF[self.n]
        self.canny_detect.clear()
        self.sobel_detect.clear()
        self.prewitt_detect.clear()
        self.EdgeDisplay.clear()
        self.ContDisplay.clear()
        for i in range(3):
            if i == 0:
                edgeIMG, edge = CV.canny(targetIMG.copy(), self.spinG_Filter.value(), self.spinSigma.value(), self.spinCDil_k.value(), self.spinCDil_i.value(),
                                   self.spinCEro_k.value(), self.spinCEro_i.value(), self.CThres_auto[1], self.spinCThres_low.value(), self.spinCThres_high.value(), self.dil[i], self.ero[i], self.thin[i])
                detect_LISt = self.canny_detect
            elif i == 1:
                edgeIMG, edge = CV.sobel(targetIMG.copy(), self.spinG_Filter.value(), self.spinSigma.value(), self.spinSDil_k.value(), self.spinSDil_i.value(),
                                    self.spinSEro_k.value(), self.spinSEro_i.value(), self.spinSobel_k.value(), self.dil[i], self.ero[i], self.thin[i], self.thinAUTO[i],
                                    self.spinSThres_low.value(), self.spinSThres_high.value(), self.thres[i], self.stream_live)
                detect_LISt = self.sobel_detect
            elif i == 2:
                edgeIMG, edge = CV.prewitt(targetIMG.copy(), self.spinG_Filter.value(), self.spinSigma.value(), self.spinPDil_k.value(), self.spinPDil_i.value(),
                                    self.spinPEro_k.value(), self.spinPEro_i.value(), self.dil[i], self.ero[i], self.thin[i], self.thinAUTO[i], self.spinPThres_low.value(),
                                    self.spinPThres_high.value(), self.thres[i], self.stream_live)
                detect_LISt = self.prewitt_detect
            self.EdgeDisplay.append(edge)
            contIMG, image = CV.getTarget_Contour(targetIMG.copy(), edgeIMG.copy(), (self.spinLIM_tri.value(), self.spinLIM_rect.value(), self.spinLIM_cir.value(), self.spinLIM_other.value()), self.shape, (self.spinCir_Min.value(), self.spinCir_Max.value()), self.bound_color[1], self.spinBoundCONTSize.value())
            self.ContDisplay.append(image)
            if self.oprt[i]:
                for c in contIMG:
                    if c[3] == 1:  # Rect
                        coords = c[0]  # approx
                    else:
                        coords = c[4]  # rotatedbox
                    dim = CV.findDist(c[3], coords, scale, (self.comboUnit_ref.currentIndex(), self.comboUnit_obj.currentIndex()), self.spinDeci.value())
                    detect_LISt.append((c[3], c[0], c[1], c[2], dim))
        if self.stream_live:
            self.statusBar().showMessage("LIVE detection ...")
        else:
            self.statusBar().showMessage("Object detection completed")
        self.compareDisplay()
        if self.listTOOL.isChecked():
            self.detail()

    def finalRes(self, compare=False):
        flag = self.edgeDetect
        if compare:
            compareList = []
            targetIMG, _ = self.targetREF[self.n]
            compareList.append(targetIMG.copy())
            for i in range(3):
                if self.display == 0:
                    image = targetIMG.copy()
                elif self.display == 1:
                    image = self.ContDisplay[i]
                    image = image.copy()
                elif self.display == 2:
                    image = self.EdgeDisplay[i]
                    image = CV.color_CVT(image.copy(), 2)
                if not self.oprt[i]:
                    h, w = image.shape[:2]
                    renderedIMG = np.zeros((h, w, 3), np.uint8)
                else:
                    if i==0:
                        ED = self.canny_detect
                        oprt_name = 'Canny'
                    elif i==1:
                        ED = self.sobel_detect
                        oprt_name = 'Sobel'
                    elif i==2:
                        ED = self.prewitt_detect
                        oprt_name = 'Prewitt'
                    renderedIMG = self.finalRender(image.copy(), ED, oprt_name, i)
                compareList.append(renderedIMG)
            return compareList
        else:
            if self.display == 0:
                targetIMG, _ = self.targetREF[self.n]
                image = targetIMG.copy()
            elif self.display == 1:
                image = self.ContDisplay[flag]
                image = image.copy()
            elif self.display == 2:
                image = self.EdgeDisplay[flag]
                image = CV.color_CVT(image.copy(), 2)
            if flag==0:
                ED = self.canny_detect
                oprt_name = 'Canny'
                self.edgeOPRT.setText("Edge:  CANNY")
            elif flag==1:
                ED = self.sobel_detect
                oprt_name = 'Sobel'
                self.edgeOPRT.setText("Edge:  SOBEL")
            elif flag==2:
                ED = self.prewitt_detect
                oprt_name = 'Prewitt'
                self.edgeOPRT.setText("Edge:  PREWITT")
            self.renderIMG = self.finalRender(image, ED, oprt_name, flag)
            self.Render()

    def finalRender(self, image, edgeDtc, oprt_name, flag):
        for obj in edgeDtc:
            CV.drawPrimitives(image, 2, obj[2], self.col_fm[flag], 2)  # frame
            if self.lb_bound:
                if obj[0]==2 or obj[0]==3:   #circle / others
                    pts = [obj[3]]  # contour
                else:
                    pts = [obj[1]]  # approx
                CV.drawPrimitives(image, 1, pts, self.bound_color[0], self.spinBoundOBJSize.value())     #bounding
            if self.lb_oprt:
                CV.drawPrimitives(image, 3, obj[2], self.col_fm[flag], -1, width=self.spinWidth_Oprt.value(), height=self.spinHeight_Oprt.value())        #label bg
                CV.drawText(1, image, oprt_name, obj[2], self.comboFont_Oprt.currentIndex(), self.col_lb[flag], self.spinFSize_Oprt.value())                   #label text
            if self.lb_msm:
                CV.drawPrimitives(image, 4, obj[2], self.col_fm[flag], -1, width=self.spinWidth_Msm.value(), height=self.spinHeight_Msm.value())  # label msm
                CV.drawText(2, image, "{} x {} {}".format(obj[4][0], obj[4][1], self.comboUnit_obj.currentText()), obj[2], self.comboFont_Msm.currentIndex(), self.col_lb[flag], self.spinFSize_Msm.value(), height=self.spinHeight_Msm.value())  # label text msm
        return image

    def check(self, flag, opt):
        if flag==1:
            self.lb_oprt = True if opt.isChecked() else False
        elif flag==2:
            self.lb_msm = True if opt.isChecked() else False
        elif flag==3:
            self.oprt[0] = True if opt.isChecked() else False
        elif flag==4:
            self.oprt[1] = True if opt.isChecked() else False
        elif flag==5:
            self.oprt[2] = True if opt.isChecked() else False
        elif flag==6:
            self.shape[0] = True if opt.isChecked() else False
        elif flag==7:
            self.shape[1] = True if opt.isChecked() else False
        elif flag==8:
            self.shape[2] = True if opt.isChecked() else False
        elif flag==9:
            self.CThres_auto[0] = True if opt.isChecked() else False    # Ref
        elif flag==10:
            self.CThres_auto[1] = True if opt.isChecked() else False    # Oprt
        elif flag==11:
            self.dil[0] = True if opt.isChecked() else False    #Canny
        elif flag==12:
            self.dil[1] = True if opt.isChecked() else False    #Sobel
        elif flag==13:
            self.dil[2] = True if opt.isChecked() else False    #Prewitt
        elif flag==14:
            self.ero[0] = True if opt.isChecked() else False    #Canny
        elif flag==15:
            self.ero[1] = True if opt.isChecked() else False    #Sobel
        elif flag==16:
            self.ero[2] = True if opt.isChecked() else False    #Prewitt
        elif flag==17:
            self.lb_bound = True if opt.isChecked() else False
        elif flag==18:
            self.thin[0] = True if opt.isChecked() else False
        elif flag==19:
            self.thin[1] = True if opt.isChecked() else False
        elif flag == 20:
            self.thin[2] = True if opt.isChecked() else False
        elif flag==21:
            self.thinAUTO[1] = True if opt.isChecked() else False
        elif flag == 22:
            self.thinAUTO[2] = True if opt.isChecked() else False
        elif flag == 23:
            self.thres[1] = True if opt.isChecked() else False
        elif flag == 24:
            self.thres[2] = True if opt.isChecked() else False
        elif flag == 25:
            self.kar = True if opt.isChecked() else False
        elif flag == 26:
            self.shape[3] = True if opt.isChecked() else False

    def getTarget_REF(self):
        canny,_ = CV.canny(self.image.copy(), self.spinG_Filter_ref.value(), self.spinSigma_ref.value(), self.spinREF_Dil_k.value(), self.spinREF_Dil_i.value(),
                         self.spinREF_Ero_k.value(), self.spinREF_Ero_i.value(), self.CThres_auto[0], self.spinREFCThres_low.value(), self.spinREFCThres_high.value(), True, True)
        contREF, _ = CV.getTarget_Contour(self.image.copy(), canny, (0, self.spinLIM_ref.value(), 0, 0), (False, True, False, False), (0,0), self.bound_color[1], self.spinBoundCONTSize.value())
        if self.stream_ref:
            color = '#7bff47', '#ff4747'
            if len(contREF)==0:
                self.ref_opt1.setStyleSheet("background-color: {}".format(color[0])+"; border: 1px solid black")
                self.ref_opt2.setStyleSheet("background-color: {}".format(color[1]) + "; border: 1px solid black")
            else:
                self.ref_opt1.setStyleSheet("background-color: {}".format(color[1]) + "; border: 1px solid black")
                self.ref_opt2.setStyleSheet("background-color: {}".format(color[0]) + "; border: 1px solid black")
        if len(contREF)==0 and not self.stream_ref and not self.stream_live:
            self.statusBar().showMessage("Warning: Target reference not found")
            self.UI.warnDialog(self, 1)
        self.targetREF_list.clear()
        self.targetREF.clear()
        image = self.image.copy()    # set ori image as one reference
        self.targetREF.append((image, (image.shape[1]/self.spinWidth_ref.value(), image.shape[0]/self.spinHeight_ref.value())))
        if not self.stream_live:
            item = QListWidgetItem()
            item.setIcon(QIcon(self.setPixmap_QtImg(image, 90, 90)))
            self.targetREF_list.addItem(item)
        for c in contREF:
            image, scale = CV.warpImg(self.image.copy(), c[0], (self.spinWidth_ref.value(), self.spinHeight_ref.value()))
            h,w = image.shape[:2]
            self.targetREF.append((image, scale))
            if not self.stream_live:
                item = QListWidgetItem()
                if h>90 or w>90:
                    h = w = 90
                item.setIcon(QIcon(self.setPixmap_QtImg(image, w, h)))
                self.targetREF_list.addItem(item)

    def importIMG(self):
        if self.stream_live:
            return
        self.statusBar().showMessage("Open File")
        file = self.UI.fileDialog(True)
        if file:
            self.fileNAME.setText(os.path.basename(file))
            self.image = CV.loadImage(file)
            self.renderIMG = self.image.copy()
            self.Render()
            if not self.zoom_slider.isEnabled():
                self.zoom_slider.setEnabled(True)
            self.detect_img_lb.setPixmap(self.setPixmap_QtImg(self.image.copy(), 200, 150))
            self.getTarget_REF()
            self.targetREF_list.setCurrentRow(0)
            self.n = 0
            self.statusBar().showMessage("2. Please adjust settings before detection")

    def colorDialog(self, flag):
        self.stream_dlg = QColorDialog(self)
        self.stream_dlg.setWindowModality(Qt.ApplicationModal)
        col = QColorDialog.getColor()
        if col.isValid():
            color = tuple(reversed(col.getRgb()[:3]))
            if type(flag)==int:
                self.bound_color[flag] = color
                btn = self.pref_col_bound[flag]
            elif flag[0]==1:
                btn = self.pref_col_fm[flag[1]]
                self.col_fm[flag[1]] = color
            elif flag[0]==2:
                btn = self.pref_col_lb[flag[1]]
                self.col_lb[flag[1]] = color
            btn.setStyleSheet("background-color:rgb({},{},{})".format(color[2], color[1], color[0]))

    def setPixmap_QtImg(self, image, width, height, Keep=True):
        image_RGBA = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2BGRA)
        QtImg = QImage(image_RGBA.data, image_RGBA.shape[1], image_RGBA.shape[0], QImage.Format_ARGB32)
        if Keep:
            KAR = Qt.KeepAspectRatio
        else:
            KAR = Qt.IgnoreAspectRatio
        return QPixmap.scaled(QPixmap.fromImage(QtImg), width, height, KAR, Qt.SmoothTransformation)

    def Render(self):
        self.UI.canvas.setPixmap(self.setPixmap_QtImg(self.renderIMG, int(self.renderIMG.shape[1]*self.zoom), int(self.renderIMG.shape[0]*self.zoom)))
        self.UI.canvas.adjustSize()

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self, id, res):
        super().__init__()
        self._run_flag = True
        self.webcam_id = id
        self.res = res

    def resolution(self, width=None, height=None):
        cap = cv2.VideoCapture(self.webcam_id)
        if width:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height:
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        width, height = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        cap.release()
        return width, height

    def run(self):
        cap = cv2.VideoCapture(self.webcam_id)
        if self.res:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.res[0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.res[1])
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

def main():
    app = QApplication(sys.argv)
    win = Paint()
    win.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
