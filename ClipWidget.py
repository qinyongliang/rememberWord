from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from CustomAnimation import *
from ApplicationConfig import *
import platform
try:
    import pykeyboard
    keyboard = pykeyboard.PyKeyboard()
except:
    pass

class ClipWidget(CustomAnimation):
    def __init__(self, *args, **kwargs):
        super(ClipWidget, self).__init__(*args, **kwargs)
        self.list = QListWidget(self)
        self.list.resize(self.mainWidget.width(), 250)
        for itemText in ApplicationConfig.clips:
            itemText = itemText.replace("\n", "")
            item = QListWidgetItem()
            item.setSizeHint(QSize(self.mainWidget.width(), self.list.height()/10))
            if(len(itemText) > 30):
                item.setText(itemText[0:30] + "...")
            else:
                item.setText(itemText)
            self.list.addItem(item)
        self.list.itemClicked.connect(self.itemClicked)
        self.list.setFrameShape(QListWidget.NoFrame)
        self.list.setSpacing(2)
        self.list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def itemClicked(self,event):
        index = self.list.selectedIndexes()[0].row()
        if(keyboard!=None and ApplicationConfig.key.match(ApplicationConfig.clips[index])):
            keyboard.type_string(ApplicationConfig.clips[index])
        QApplication.clipboard().setText(ApplicationConfig.clips[index])
        self.stop()
