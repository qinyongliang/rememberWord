#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import linecache
import random
import math
import json
import platform
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *


# 全局设置
setting = {"engine": "baidu", "color": 0x00BFFF, "changeTime": 3.0, "fontSize": 12, "fontColor": 0xffffff,
           "wordPath": r"/home/administrator/world.txt", "opacity":80}
# 当前活跃视图
views = None
# 拦截器
class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)

    def interceptRequest(self, info):
        info.setHttpHeader(
            b"User-Agent", b"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
# 拦截器实例
interceptor = WebEngineUrlRequestInterceptor()
# 配置目录
configFilePath = os.environ['HOME'] + os.path.sep + ".remember.config"
def loadConfig():
    if(os.path.exists(configFilePath)):
        global setting
        setting = json.load(open(configFilePath))
def saveConfig():
    json.dump(setting, open(configFilePath, 'w'))
# 加载动画    
Svg_icon_loading = '''<svg width="100%" height="100%" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient x1="8.042%" y1="0%" x2="65.682%" y2="23.865%" id="a">
            <stop stop-color="#03a9f4" stop-opacity="0" offset="0%"/>
            <stop stop-color="#03a9f4" stop-opacity=".631" offset="63.146%"/>
            <stop stop-color="#03a9f4" offset="100%"/>
        </linearGradient>
    </defs>
    <g fill="none" fill-rule="evenodd">
        <g transform="translate(1 1)">
            <path d="M36 18c0-9.94-8.06-18-18-18" id="Oval-2" stroke="url(#a)" stroke-width="2">
                <animateTransform
                    attributeName="transform"
                    type="rotate"
                    from="0 18 18"
                    to="360 18 18"
                    dur="1.5s"
                    repeatCount="indefinite" />
            </path>
            <circle fill="#03a9f4" cx="36" cy="18" r="4">
                <animateTransform
                    attributeName="transform"
                    type="rotate"
                    from="0 18 18"
                    to="360 18 18"
                    dur="1.5s"
                    repeatCount="indefinite" />
            </circle>
        </g>
    </g>
</svg>'''.encode()


class CustomAnimation(QWidget):
    def inAnimation(self, startPos, endPos,nextAction=lambda : None):
        # 如果views不为空，就让它关闭
        global views
        if(views):
            views.stop()
        views = self
        # 透明度动画
        opacityAnimation = QPropertyAnimation(self, b"windowOpacity")
        opacityAnimation.setStartValue(0.0)
        opacityAnimation.setEndValue(setting["opacity"])
        # 设置动画曲线
        opacityAnimation.setEasingCurve(QEasingCurve.InQuad)
        opacityAnimation.setDuration(300)  # 在0.3秒的时间内完成
        # 变长动画
        heghtAnimation = QPropertyAnimation(self, b"geometry")
        heghtAnimation.setStartValue(QRect(startPos, QSize(self.width(),0)))
        heghtAnimation.setEndValue(
            QRect(endPos, QSize(self.width(), self.height())))
        heghtAnimation.setEasingCurve(QEasingCurve.InQuad)
        heghtAnimation.setDuration(300)  # 在0.3秒的时间内完成
        # 并行动画组（目的是让上面的两个动画同时进行）
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(heghtAnimation)
        self.animationGroup.finished.connect(nextAction)  # 动画结束时开始加载数据
        self.animationGroup.start()

    def outAnimation(self, nextAction=lambda: None):
        startPos = self.pos()
        endPos = QPoint(self.mainWidget.pos().x(),
                        self.mainWidget.pos().y() + self.mainWidget.height())
        # 透明度动画
        opacityAnimation = QPropertyAnimation(self, b"windowOpacity")
        opacityAnimation.setStartValue(setting["opacity"])
        opacityAnimation.setEndValue(0.0)
        heghtAnimation = QPropertyAnimation(self, b"geometry")
        heghtAnimation.setStartValue(
            QRect(self.pos(), QSize(self.width(), self.height())))
        heghtAnimation.setEndValue(
            QRect(self.mainWidget.pos(), QSize(self.width(), 0)))
        heghtAnimation.setEasingCurve(QEasingCurve.InQuad)
        heghtAnimation.setDuration(300)  # 在0.3秒的时间内完成
        # 设置动画曲线
        opacityAnimation.setEasingCurve(QEasingCurve.OutCubic)
        opacityAnimation.setDuration(200)  # 在0.2秒的时间内完成
        # 并行动画组（目的是让上面的两个动画同时进行）
        del self.animationGroup
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(heghtAnimation)
        self.animationGroup.finished.connect(nextAction)  # 动画结束时删除数据
        self.animationGroup.start()
        global views
        views=None
            
    def stop(self):
        self.outAnimation(self.close)


class MyQLineEdit(QLineEdit):
    clicked = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(MyQLineEdit, self).__init__(*args, **kwargs)
    def mousePressEvent(self,event):
        self.clicked.emit()

class SettionWidget(CustomAnimation):
    def __init__(self, *args, **kwargs):
        self.mainWidget = kwargs.pop("mainWidget", "")
        super(SettionWidget, self).__init__(*args, **kwargs)
        # 设置无边框置顶
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # 设置一下宽度
        self.resize(self.mainWidget.width(), 250)
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
        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.fontSize, self.fontColor)
        self.setTabOrder(self.fontColor, self.wordPathEdit)
        self.setTabOrder(self.wordPathEdit, self.baiduRadio)
        self.setTabOrder(self.baiduRadio, self.googleRedio)
        self.setTabOrder(self.googleRedio, self.changeTimeEdit)
        self.setTabOrder(self.changeTimeEdit, self.pushButton)
        

    def actionBind(self):
        self.pushButton.clicked.connect(lambda v: self.stop())
        self.fontSize.valueChanged.connect(
            lambda var: self.changeConfig("fontSize", var))
        self.changeTimeEdit.valueChanged.connect(
            lambda var: self.changeConfig("changeTime", var))
        self.baiduRadio.clicked.connect(lambda v: self.changeConfig("engine","baidu"))
        self.googleRedio.clicked.connect(
            lambda v: self.changeConfig("engine", "google"))
        self.wordPathEdit.clicked.connect(self.changeFilePath)
        self.fontColor.clicked.connect(lambda v: self.changeColor("fontColor"))
        self.backgroundColor.clicked.connect(
            lambda v: self.changeColor("color"))
        self.Opacityslider.valueChanged.connect(
            lambda value: self.changeConfig("opacity",value/100.0))
        # self.fontSize.changeEvent.connect(lambda var: self.changeConfig("fontSize",var))
        # self.fontSize.changeEvent.connect(lambda var: self.changeConfig("fontSize",var))


    def paintEvent(self, event):
        self.setWindowOpacity(setting["opacity"])  # 透明
        # 字体相关设置
        ft = QFont()
        ft.setPointSize(setting["fontSize"])
        self.label_7.setFont(ft)
        pa = QPalette()
        pa.setColor(QPalette.WindowText, QColor(setting["fontColor"]))
        self.label_7.setPalette(pa)
        # 头设置
        palette = self.label_7.palette()  # 调色板
        palette.setColor(self.label_7.backgroundRole(),
                         QColor(setting['color']))
        palette.setBrush(QPalette.Base, Qt.transparent)  # 父控件背景透明
        self.label_7.setAutoFillBackground(True)
        self.label_7.setPalette(palette)

 

        # 按钮设置
        palette = self.pushButton.palette()
        palette.setColor(self.label_7.backgroundRole(),
                         QColor(setting['color']))
        palette.setBrush(QPalette.Base, Qt.transparent)  # 父控件背景透明
        self.pushButton.setPalette(palette)
    def changeFilePath(self):
        fd = QFileDialog(self)
        fd.setWindowTitle("选择生词表")
        fd.setNameFilter("text(*.txt)")
        fd.setFileMode(QFileDialog.ExistingFile)
        fd.setViewMode(QFileDialog.Detail)
        fd.move(QApplication.instance().desktop().screenGeometry().width()/2-fd.width()/2,
                QApplication.instance().desktop().screenGeometry().height()/2-fd.height()/2)
        if(fd.exec()):
            ls =  fd.selectedFiles()
            self.changeConfig("wordPath", ls[0])
    def changeColor(self,key):
        color = QColorDialog.getColor(QColor(setting[key]))
        if(color.isValid()):
            # pass
            self.changeConfig(key, color.rgb())
    def changeConfig(self,key,value):
        setting[key] = value
        saveConfig()
        self.mainWidget.update()
        self.update()
    def show(self):
        super(SettionWidget, self).show()
        self.fontSize.setValue(setting["fontSize"])
        self.changeTimeEdit.setValue(setting["changeTime"])
        self.wordPathEdit.setText(setting["wordPath"])
        self.Opacityslider.setValue(setting["opacity"]*100)
        if(setting['engine']=='baidu'):
            self.baiduRadio.setChecked(True)
        elif setting['engine'] == 'google':
            self.googleRedio.setChecked(True)
        # 窗口开始位置
        startPos = QPoint(
            self.mainWidget.pos().x(),
            self.mainWidget.pos().y() + self.mainWidget.height())
        endPos = QPoint(
            self.mainWidget.pos().x(),
            self.mainWidget.pos().y() + self.mainWidget.height() + 10)
        self.move(startPos)
        # 初始化动画
        self.inAnimation(startPos, endPos)
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
        self.pushButton.setText(_translate("Form", "关闭"))
        

class TranslateWidget(CustomAnimation):
    def __init__(self, *args, **kwargs):
        self.word = kwargs.pop("text", "")
        self.mainWidget = kwargs.pop("mainWidget", "")
        super(TranslateWidget, self).__init__(*args, **kwargs)
        # 设置无边框置顶
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # 设置一下宽度
        self.resize(self.mainWidget.width(),250)
        self.setWindowOpacity(setting["opacity"])  # 透明
        #创建关闭翻译控件的定时器
        self.closeTimer = QTimer(self, timeout=self.stop)
        self.loadWidget = QSvgWidget(
            self, minimumHeight=self.height(), minimumWidth=self.height(), visible=False)
        self.loadWidget.move(self.width()/4,
                             self.height()/4)
        self.loadWidget.load(Svg_icon_loading)
        self.loadWidget.setVisible(True)

    def loadTranslation(self):
        self.browser = QWebEngineView(self)
        self.browser.resize(self.width(),self.height())
        self.browser.setZoomFactor(0.75)
        self.browser.page().profile().setRequestInterceptor(interceptor)
        if(setting["engine"]=="google"):
            self.browser.load(QUrl("https://translate.google.cn/m/translate#en/zh-CN/" + self.word.lower()))
        elif setting["engine"] == "baidu":
            self.browser.load(QUrl(
                "http://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh#en/zh/" + self.word.lower()))
        self.browser.loadFinished.connect(self.translationShow)

    # 显示翻译框，移除掉不用的div
    def translationShow(self):
        if(setting['engine'] == 'baidu'):
            self.browser.page().runJavaScript(
                '''document.getElementById("shoubai-header").remove();
                document.getElementsByClassName("app-bar")[0].remove();
                document.getElementsByClassName("bottom-intro")[0].remove();
                document.getElementsByClassName("trans-input")[0].remove();
                document.getElementsByClassName("mach-trans")[0].remove();
                document.getElementsByClassName("translang")[0].remove()
                document.getElementsByClassName("translatein")[0].remove()
                '''
            )
        elif setting['engine'] == 'google':
            self.browser.page().runJavaScript(
                '''document.getElementsByTagName("header")[0].remove();
                document.getElementsByClassName("tlid-input input")[0].remove();
                document.getElementsByClassName("gp-footer")[0].remove();
                '''
            )
        # 隐藏滚动条
        self.browser.page().settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, False)
        self.loadWidget.hide()
        self.browser.show()
    def show(self):
        super(TranslateWidget, self).show()
        # 窗口开始位置
        startPos = QPoint(
            self.mainWidget.pos().x(),
                  self.mainWidget.pos().y() + self.mainWidget.height())
        endPos = QPoint(
            self.mainWidget.pos().x(),
            self.mainWidget.pos().y() + self.mainWidget.height() + 10)
        self.move(startPos)
        # 初始化动画
        self.inAnimation(startPos, endPos, self.loadTranslation)
        self.closeTimer.start(10000)

    def stop(self):
        try:
            if(hasattr(self.mainWidget,"translateWidget")):
                del self.mainWidget.translateWidget
            self.closeTimer.stop()
            self.closeTimer.deleteLater()
            self.outAnimation(nextAction=self._close)
        except:
            pass

    def _close(self):
        try:
            self.loadWidget.close()
            self.loadWidget.deleteLater()
            if(hasattr(self, "browser")):
                self.browser.close()
            self.hide()
            self.animationGroup.stop()
            self.close()
            self.deleteLater()
        except:
            pass



class MainWidget( QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)

        # 获取桌面信息
        self._desktop = QApplication.instance().desktop()
        self.resize(200, 24)
        
        # 位置设置
        LeftTopPos = QPoint(setting["pos"]["x"],setting["pos"]["y"])
        self.lastPos = LeftTopPos
        self.move(LeftTopPos)

        # 单词设置
        self.label = QLabel(self)

       
        self.label.setFixedWidth(self.width())
        self.label.setFixedHeight(self.height())
        self.label.setAlignment(Qt.AlignCenter) # 居中
        self.label.setWordWrap(False) # 不允许换行
        self.label.setText("start...")
        self.changeWord()

        # 菜单设置
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QMenu(self)
        self.settingAction = self.contextMenu.addAction(u"设置")
        self.nextAction = self.contextMenu.addAction(u"下一个单词")
        self.exitAction = self.contextMenu.addAction(u"退出")
    

        self.settingAction.triggered.connect(
            lambda v: SettionWidget(mainWidget=self).show())
        self.exitAction.triggered.connect(lambda v: QApplication.exit())
        self.nextAction.triggered.connect(lambda v: self.changeWord())


        # Windows 和linux使用的全局热键实现不一样。
        # Windows 使用keyboard包，linux使用PyUserInput
        if(platform.system() == "Windows" or os.geteuid() == 0):
            import keyboard
            keyboard.add_hotkey('ctrl+shift+v', self.showClipBoard, suppress=False)
        else:
            import pykeyboard
            self.keyboard = pykeyboard.PyKeyboard()
            class GlobalKeyHotEvent(pykeyboard.PyKeyboardEvent, QObject):
                press = pyqtSignal()
                # 按钮改变事件
                change = pyqtSignal(set)
                def __init__(self,hotKey):
                    QObject.__init__(self)
                    pykeyboard.PyKeyboardEvent.__init__(self)
                    self.HotKey = hotKey
                    self.nowPressKey = set()

                def tap(self, keycode, character, press):
                    if(character==None):
                        return
                    if(press==True):
                        self.nowPressKey.add(character.replace("_L", "").replace("_R", ""))
                    else:
                        self.nowPressKey.remove(
                            character.replace("_L", "").replace("_R", ""))
                    if(len(self.nowPressKey)>1):
                        self.change.emit(self.nowPressKey)
                        self.change.emit(self.nowPressKey)
                    if(self.HotKey == self.nowPressKey):
                        self.press.emit()
            g = GlobalKeyHotEvent(set(["Control","Shift","V"]))
            g.press.connect(self.showClipBoard)
            g.change.connect(lambda v: None)
            threading.Thread(target = lambda: g.run()).start()
        
    def paintEvent(self, event):
        self.setWindowOpacity(setting["opacity"])  # 透明
        ft = QFont()
        ft.setPointSize(setting["fontSize"])
        pa = QPalette()
        pa.setColor(QPalette.WindowText, QColor(setting["fontColor"]))
        self.label.setFont(ft)
        self.label.setPalette(pa)

        palette = self.palette()  # 调色板
        palette.setColor(self.backgroundRole(), QColor(setting['color']))
        palette.setBrush(QPalette.Base, Qt.transparent)  # 父控件背景透明
        self.setPalette(palette)
        pass
    def set(self,key,value):
        setting[key] = value
    # 显示右键菜单
    def showContextMenu(self, pos):
        self.contextMenu.move(self.pos()+pos)
        self.contextMenu.show()

    # 双击切换下一个单词
    def mouseDoubleClickEvent(self,event):
        if(hasattr(self, "clickTimer")):
            self.clickTimer.stop()
            del self.clickTimer
        self.changeWord()
        self.isDoubleClick = True
        
    # 鼠标按下
    def mousePressEvent(self,event):
        self.isClick = True
        self.pressPos = event.pos()
        self.pressGlobalPos = event.globalPos()

    def translation(self):
        if(hasattr(self, "clickTimer")):
            self.clickTimer.stop()
            del self.clickTimer
        self.translateWidget = TranslateWidget(
            text=self.word, mainWidget=self)
        self.translateWidget.show()
    
    # 鼠标抬起
    def mouseReleaseEvent(self,event):
        # 判断上一次是否是双击，如果是那么此次的鼠标释放不生效
        if(hasattr(self, "isDoubleClick")):
            del self.isDoubleClick
            return
        # 如果是鼠标右键，就展开菜单
        if(event.button() == Qt.RightButton):
            pass 
            return
            
        if(self.pressGlobalPos == event.globalPos()):
            if(self.isClick==True):
                self.clickTimer = QTimer(self, timeout=self.translation)
                # 150毫秒后才是单击
                self.clickTimer.start(150)
        else:
            # 移动操作
            return

    def getFileLength(self,fileName):
        count = 0
        thefile = open(fileName)
        while True:
            buffer = thefile.read(1024 * 8192)
            if not buffer:
                break
            count += buffer.count('\n')
        thefile.close()
        return count
    def changeWord(self,text=None):
        if(hasattr(self, "translateWidget")):
            self.translateWidget._close()
        if(text==None):
            # 从文件中加载
            fileName = setting['wordPath']
            if(os.path.exists(fileName)):
                length = self.getFileLength(fileName)
                # 越靠后的单词出现的频率越高。以下写法很骚
                lineNumber = int(math.sqrt(random.randrange(1, length * length)))+1
                self.word = linecache.getline(
                    fileName, lineNumber)
            else:
                self.word = u"请指定生词表！"
        else:
            self.word = text
        self.label.setText(self.word)
        # 为了让每次切换单词后都会等待3分钟
        QTimer.singleShot(60 * 1000 * setting['changeTime'], self.changeWord)

    # 移动
    def mouseMoveEvent(self,event):
        self.isClick = False
        last = self.pos()
        nowPos = event.pos()
        movePos = QPoint(last.x() + (nowPos.x() - self.pressPos.x()), last.y() + (nowPos.y() - self.pressPos.y()))
        self.move(movePos)
        global views
        if(views!=None):
            last = views.pos()
            views.move(QPoint(last.x() + (nowPos.x() - self.pressPos.x()),
                              last.y() + (nowPos.y() - self.pressPos.y())))
        global setting
        setting["pos"] = {"x":movePos.x(),"y":movePos.y()}
        saveConfig()

    def eventFilter(self,  source,  event):
        try:
            # if event.type() == QEvent.QKeyEvent:
            #     print("按下按钮")
            # if event.type() == QEvent.QShortcutEvent:
            #     print("快捷键处理")
            # if event.type() == QEvent.NonClientAreaMouseButtonPress:
            #     print("鼠标按钮按下发生在客户端区域外")
            # 鼠标进入窗体
            global views
            if event.type() == QEvent.Enter:
                if(views!=None and hasattr(self, "translateWidget") and hasattr(self.translateWidget, "closeTimer")):
                    # 停止定时任务
                    self.translateWidget.closeTimer.stop()
            # 鼠标移除窗体
            if event.type() == QEvent.Leave:
                if(views != None and hasattr(self, "translateWidget") and hasattr(self.translateWidget, "closeTimer")):
                    # 开始定时任务
                    self.translateWidget.closeTimer.start(1500)
        except:
            pass
        return QMainWindow.eventFilter(self,  source,  event)
        
    # 设置要显示的单词
    def setWord(self,word):
        self.word = word
        self._wordLable.setText(self.word)

    # 显示粘贴板
    def showClipBoard(self):
        print("调用粘贴办")
        pass
    # 监控粘贴班变化
    def onClipboradChanged(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        # 如果是一个单词就直接弹出翻译
        if(self.word != text and  text.lower().strip().isalpha()):
            self.changeWord(text)
            self.translation()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loadConfig()
    if('pos' not in setting):
        setting["pos"]={"x": QApplication.instance().desktop().screenGeometry().width() * 0.8, "y": QApplication.instance().desktop().availableGeometry().height() *0.027}
    w = MainWidget()
    w.show()
    app.installEventFilter(w)
    clipboard = QApplication.clipboard()
    clipboard.dataChanged.connect(w.onClipboradChanged)
    sys.exit(app.exec_())
