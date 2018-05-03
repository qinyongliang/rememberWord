from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from CustomAnimation import *
from ApplicationConfig import *
from TranslateWidget import *


class MyQLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MyQLineEdit, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        self.clicked.emit()


class SettionWidget(CustomAnimation):
    def __init__(self, *args, **kwargs):
        super(SettionWidget, self).__init__(*args, **kwargs)
        # 创建窗体元素
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setGeometry(
            QRect(0, 0, self.mainWidget.width(), 250))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QVBoxLayout(
            self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        # 字体大小
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(
            2, QFormLayout.LabelRole, self.label)
        self.fontSize = QSpinBox(self.verticalLayoutWidget)
        self.fontSize.setObjectName("fontSize")
        self.formLayout.setWidget(
            2, QFormLayout.FieldRole, self.fontSize)

        # 字体颜色
        self.fontColorLabel = QLabel(self.verticalLayoutWidget)
        self.fontColorLabel.setText("字体颜色")
        self.fontColor = QPushButton(self.verticalLayoutWidget)
        self.fontColor.setObjectName("fontColor")
        self.formLayout.setWidget(
            3, QFormLayout.FieldRole, self.fontColor)
        self.formLayout.setWidget(
            3, QFormLayout.LabelRole, self.fontColorLabel)

        # 单词表地址
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(
            4, QFormLayout.LabelRole, self.label_3)
        self.wordPathEdit = MyQLineEdit(self.verticalLayoutWidget)
        self.wordPathEdit.setAutoFillBackground(False)
        self.wordPathEdit.setObjectName("wordPathEdit")
        self.formLayout.setWidget(
            4, QFormLayout.FieldRole, self.wordPathEdit)
        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")

        # 翻译引擎
        self.formLayout.setWidget(
            5, QFormLayout.LabelRole, self.label_4)
        self.groupBox = QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setTitle("")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.baiduRadio = QRadioButton(self.groupBox)
        self.baiduRadio.setGeometry(QRect(0, 5, 99, 23))
        self.baiduRadio.setObjectName("baiduRadio")
        self.googleRedio = QRadioButton(self.groupBox)
        self.googleRedio.setGeometry(QRect(50, 5, 99, 23))
        self.googleRedio.setObjectName("googleRedio")
        self.formLayout.setWidget(
            5, QFormLayout.FieldRole, self.groupBox)

        # 切换时间设置
        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(
            6, QFormLayout.LabelRole, self.label_5)
        self.changeTimeEdit = QDoubleSpinBox(
            self.verticalLayoutWidget)
        self.changeTimeEdit.setSingleStep(0.5)
        self.changeTimeEdit.setSuffix(" 分钟")
        self.changeTimeEdit.setObjectName("changeTimeEdit")
        self.formLayout.setWidget(
            6, QFormLayout.FieldRole, self.changeTimeEdit)

        # 背景颜色
        self.backgroundLabel = QLabel(self.verticalLayoutWidget)
        self.backgroundLabel.setObjectName("backgroundLabel")
        self.formLayout.setWidget(
            7, QFormLayout.LabelRole, self.backgroundLabel)
        self.backgroundColor = QPushButton(self.verticalLayoutWidget)
        self.backgroundColor.setObjectName("fontColor")
        self.formLayout.setWidget(
            7, QFormLayout.FieldRole, self.backgroundColor)

        # 透明度
        self.Opacitylabel = QLabel(self.verticalLayoutWidget)
        self.Opacitylabel.setText("透明度")
        self.Opacitylabel.setObjectName("Opacitylabel")
        self.formLayout.setWidget(
            8, QFormLayout.LabelRole, self.Opacitylabel)

        self.Opacityslider = QSlider(
            self.verticalLayoutWidget)
        self.Opacityslider.setOrientation(Qt.Horizontal)
        self.Opacityslider.setMaximum(100)
        self.Opacityslider.setMinimum(20)
        self.Opacityslider.setSingleStep(1)
        self.formLayout.setWidget(
            8, QFormLayout.FieldRole, self.Opacityslider)

        spacerItem = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(0, QFormLayout.FieldRole, spacerItem)
        spacerItem1 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(
            1, QFormLayout.FieldRole, spacerItem1)
        self.verticalLayout_2.addLayout(self.formLayout)
        # self.pushButton = QPushButton(self.verticalLayoutWidget)
        # self.pushButton.setObjectName("pushButton")
        # self.verticalLayout_2.addWidget(self.pushButton)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.fontSize, self.fontColor)
        self.setTabOrder(self.fontColor, self.wordPathEdit)
        self.setTabOrder(self.wordPathEdit, self.baiduRadio)
        self.setTabOrder(self.baiduRadio, self.googleRedio)
        self.setTabOrder(self.googleRedio, self.changeTimeEdit)
        # self.setTabOrder(self.changeTimeEdit, self.pushButton)

    def actionBind(self):
        # self.pushButton.clicked.connect(lambda v: self.stop())
        self.fontSize.valueChanged.connect(
            lambda var: self.changeConfig("fontSize", var))
        self.changeTimeEdit.valueChanged.connect(
            lambda var: self.changeConfig("changeTime", var))
        self.baiduRadio.clicked.connect(
            lambda v: self.changeConfig("engine", "baidu"))
        self.googleRedio.clicked.connect(
            lambda v: self.changeConfig("engine", "google"))
        self.wordPathEdit.clicked.connect(self.changeFilePath)
        self.fontColor.clicked.connect(lambda v: self.changeColor("fontColor"))
        self.backgroundColor.clicked.connect(
            lambda v: self.changeColor("color"))
        self.Opacityslider.valueChanged.connect(
            lambda value: self.changeConfig("opacity", value / 100.0))
        # self.fontSize.changeEvent.connect(lambda var: self.changeConfig("fontSize",var))
        # self.fontSize.changeEvent.connect(lambda var: self.changeConfig("fontSize",var))

    def paintEvent(self, event):
        super(SettionWidget, self).paintEvent(event)
        self.setWindowOpacity(ApplicationConfig.setting["opacity"])  # 透明
        # 字体相关设置
        ft = QFont()
        ft.setPointSize(ApplicationConfig.setting["fontSize"])
        self.label_7.setFont(ft)
        pa = QPalette()
        pa.setColor(QPalette.WindowText, QColor(
            ApplicationConfig.setting["fontColor"]))
        self.label_7.setPalette(pa)
        # 头设置
        palette = self.label_7.palette()  # 调色板
        palette.setColor(self.label_7.backgroundRole(),
                         QColor(ApplicationConfig.setting['color']))
        palette.setBrush(QPalette.Base, Qt.transparent)  # 父控件背景透明
        self.label_7.setAutoFillBackground(True)
        self.label_7.setPalette(palette)

        # 按钮设置
        # palette = self.pushButton.palette()
        # palette.setColor(self.label_7.backgroundRole(),
        #                  QColor(ApplicationConfig.setting['color']))
        # palette.setBrush(QPalette.Base, Qt.transparent)  # 父控件背景透明
        # self.pushButton.setPalette(palette)

    def changeFilePath(self):
        fd = QFileDialog(self)
        fd.setWindowTitle("选择生词表")
        fd.setNameFilter("text(*.txt)")
        fd.setFileMode(QFileDialog.ExistingFile)
        fd.setViewMode(QFileDialog.Detail)
        fd.move(QApplication.instance().desktop().screenGeometry().width() / 2 - fd.width() / 2,
                QApplication.instance().desktop().screenGeometry().height() / 2 - fd.height() / 2)
        if(fd.exec()):
            ls = fd.selectedFiles()
            self.changeConfig("wordPath", ls[0])

    def changeColor(self, key):
        color = QColorDialog.getColor(QColor(ApplicationConfig.setting[key]))
        if(color.isValid()):
            # pass
            self.changeConfig(key, color.rgb())

    def changeConfig(self, key, value):
        ApplicationConfig.setting[key] = value
        ApplicationConfig.saveConfig()
        self.mainWidget.update()
        self.update()

    def show(self):
        self.fontSize.setValue(ApplicationConfig.setting["fontSize"])
        self.changeTimeEdit.setValue(ApplicationConfig.setting["changeTime"])
        self.wordPathEdit.setText(ApplicationConfig.setting["wordPath"])
        self.Opacityslider.setValue(ApplicationConfig.setting["opacity"] * 100)
        if(ApplicationConfig.setting['engine'] == 'baidu'):
            self.baiduRadio.setChecked(True)
        elif ApplicationConfig.setting['engine'] == 'google':
            self.googleRedio.setChecked(True)
        super(SettionWidget, self).show()
        self.actionBind()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label_7.setText(_translate("Form", "设置"))
        self.label.setText(_translate("Form", "字体大小"))
        self.backgroundLabel.setText(_translate("Form", "背景颜色"))
        self.fontColor.setText(_translate("Form", "选择"))
        self.backgroundColor.setText(_translate("Form", "选择"))
        self.label_3.setText(_translate("Form", "生词表"))
        self.label_4.setText(_translate("Form", "翻译引擎"))
        self.baiduRadio.setText(_translate("Form", "百度"))
        self.googleRedio.setText(_translate("Form", "谷歌"))
        self.label_5.setText(_translate("Form", "切换时间"))
        # self.pushButton.setText(_translate("Form", "关闭"))
