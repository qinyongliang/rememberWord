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
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from ApplicationConfig import *
from TranslateWidget import *
from SettionWidget import *
from ClipWidget import *

class MainWidget( QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)

        # 获取桌面信息
        self._desktop = QApplication.instance().desktop()
        self.resize(200, 24)
        
        # 位置设置
        LeftTopPos = QPoint(ApplicationConfig.setting["pos"]["x"],ApplicationConfig.setting["pos"]["y"])
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
        self.clipAction = self.contextMenu.addAction(u"粘贴板")
        self.settingAction = self.contextMenu.addAction(u"设置")
        self.nextAction = self.contextMenu.addAction(u"下一个单词")
        self.exitAction = self.contextMenu.addAction(u"退出")
    

        self.settingAction.triggered.connect(
            lambda v: SettionWidget(mainWidget=self).show())
        self.clipAction.triggered.connect(self.showClipBoard)
        self.exitAction.triggered.connect(lambda v: QApplication.exit() or sys.exit())
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
                    try:
                        value = character.replace("_L", "").replace("_R", "")
                        if(press==True):
                            self.nowPressKey.add(value)
                        else:
                            if(value in self.nowPressKey):
                                self.nowPressKey.remove(value)
                        if(len(self.nowPressKey)>1):
                            self.change.emit(self.nowPressKey)
                        if(self.HotKey == self.nowPressKey):
                            self.press.emit()
                    except:
                        self.nowPressKey = set()
            g = GlobalKeyHotEvent(set(["Control","Shift","V"]))
            g.press.connect(self.showClipBoard)
            g.change.connect(lambda v: None)
            threading.Thread(target = lambda: g.run()).start()
        
    def paintEvent(self, event):
        self.setWindowOpacity(ApplicationConfig.setting["opacity"])  # 透明
        ft = QFont()
        ft.setPointSize(ApplicationConfig.setting["fontSize"])
        pa = QPalette()
        pa.setColor(QPalette.WindowText, QColor(ApplicationConfig.setting["fontColor"]))
        self.label.setFont(ft)
        self.label.setPalette(pa)

        palette = self.palette()  # 调色板
        palette.setColor(self.backgroundRole(), QColor(ApplicationConfig.setting['color']))
        palette.setBrush(QPalette.Base, Qt.transparent)  # 父控件背景透明
        self.setPalette(palette)
        pass
    def set(self,key,value):
        ApplicationConfig.setting[key] = value
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
            fileName = ApplicationConfig.setting['wordPath']
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
        # 为了让每次切换单词后都会等待
        QTimer.singleShot(60 * 1000 * ApplicationConfig.setting['changeTime'], self.changeWord)

    # 移动
    def mouseMoveEvent(self,event):
        self.isClick = False
        last = self.pos()
        nowPos = event.pos()
        movePos = QPoint(last.x() + (nowPos.x() - self.pressPos.x()), last.y() + (nowPos.y() - self.pressPos.y()))
        self.move(movePos)
        if(ApplicationConfig.views!=None):
            # ApplicationConfig.views.update()
            last = ApplicationConfig.views.pos()
            ApplicationConfig.views.move(QPoint(last+ (nowPos - self.pressPos)))
        ApplicationConfig.setting["pos"] = {"x": movePos.x(), "y": movePos.y()}
        ApplicationConfig.saveConfig()

    def eventFilter(self,  source,  event):
        try:
            # if event.type() == QEvent.QKeyEvent:
            #     print("按下按钮")
            # if event.type() == QEvent.QShortcutEvent:
            #     print("快捷键处理")
            # if event.type() == QEvent.NonClientAreaMouseButtonPress:
            #     print("鼠标按钮按下发生在客户端区域外")
            # 鼠标进入窗体
            if event.type() == QEvent.Enter:
                if(ApplicationConfig.views != None):
                    # 关注
                    ApplicationConfig.views.attentionIn()
            # 鼠标移除窗体
            if event.type() == QEvent.Leave:
                if(ApplicationConfig.views != None):
                    # 关注移除
                    ApplicationConfig.views.attentionOut()
        except:
            pass
        return QMainWindow.eventFilter(self,  source,  event)
        
    # 设置要显示的单词
    def setWord(self,word):
        self.word = word
        self._wordLable.setText(self.word)

    # 显示粘贴板
    def showClipBoard(self):
        ClipWidget(mainWidget=self).show()
        pass
    # 监控粘贴班变化
    def onClipboradChanged(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if(text == ""):
            return
        if(text in ApplicationConfig.clips):
            ApplicationConfig.clips.remove(text)
        ApplicationConfig.clips.insert(0,text)
        
        # 如果是一个单词就直接弹出翻译
        if(self.word != text and text.lower().strip().isalpha() and ApplicationConfig.checkWord.match(text)):
            self.changeWord(text)
            self.translation()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ApplicationConfig.loadConfig()
    if('pos' not in ApplicationConfig.setting):
        ApplicationConfig.setting["pos"]={"x": QApplication.instance().desktop().screenGeometry().width() * 0.8, "y": QApplication.instance().desktop().availableGeometry().height() *0.027}
    w = MainWidget()
    w.show()
    app.installEventFilter(w)
    clipboard = QApplication.clipboard()
    clipboard.dataChanged.connect(w.onClipboradChanged)
    sys.exit(app.exec_())
