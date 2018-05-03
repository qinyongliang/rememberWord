from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ApplicationConfig import *

class CustomAnimation(QWidget):
    def __init__(self, *args, **kwargs):
        self.mainWidget = kwargs.pop("mainWidget", "")
        super(CustomAnimation, self).__init__(*args, **kwargs)
        # 设置无边框置顶
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # 设置一下宽度
        self.resize(self.mainWidget.width(), 250)
        self.setWindowOpacity(ApplicationConfig.setting["opacity"])  # 透明
        # 定时关闭
        self.closeTimer = QTimer(self, timeout=self.stop)

    def inAnimation(self, startPos, endPos, nextAction=lambda: None):
        # 如果views不为空，就让它关闭
        if(ApplicationConfig.views != None):
            ApplicationConfig.views.stop()
        ApplicationConfig.views = self
        # 透明度动画
        opacityAnimation = QPropertyAnimation(self, b"windowOpacity")
        opacityAnimation.setStartValue(0.0)
        opacityAnimation.setEndValue(ApplicationConfig.setting["opacity"])
        # 设置动画曲线
        opacityAnimation.setEasingCurve(QEasingCurve.InQuad)
        opacityAnimation.setDuration(300)  # 在0.3秒的时间内完成
        # 变长动画
        heghtAnimation = QPropertyAnimation(self, b"geometry")
        heghtAnimation.setStartValue(QRect(startPos, QSize(self.width(), 0)))
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
        # 透明度动画
        opacityAnimation = QPropertyAnimation(self, b"windowOpacity")
        opacityAnimation.setStartValue(ApplicationConfig.setting["opacity"])
        opacityAnimation.setEndValue(0.0)
        heghtAnimation = QPropertyAnimation(self, b"geometry")
        heghtAnimation.setStartValue(
            QRect(self.pos(), QSize(self.width(), self.height())))
        heghtAnimation.setEndValue(
            QRect(QPoint(self.mainWidget.pos().x(), self.mainWidget.pos().y()+self.mainWidget.height()), QSize(self.width(), 0)))
        heghtAnimation.setEasingCurve(QEasingCurve.InQuad)
        heghtAnimation.setDuration(300)  # 在0.3秒的时间内完成
        # 设置动画曲线
        opacityAnimation.setEasingCurve(QEasingCurve.OutCubic)
        opacityAnimation.setDuration(300)  # 在0.2秒的时间内完成
        # 并行动画组（目的是让上面的两个动画同时进行）
        del self.animationGroup
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(heghtAnimation)
        self.animationGroup.finished.connect(nextAction)  # 动画结束时删除数据
        self.animationGroup.start()
        ApplicationConfig.views = None

    def paintEvent(self, event):
        super(CustomAnimation, self).paintEvent(event)

    def stop(self):
        self.outAnimation(self.close)

    def close(self):
        try:
            self.closeTimer.stop()
            self.closeTimer.deleteLater()
            self.hide()
            self.animationGroup.stop()
            self.close()
            self.deleteLater()
        except:
            pass

    def show(self, nextAction=lambda: None,closeTime = 1000*10):
        """
        @closeTime10秒后自动关闭
        """
        super(CustomAnimation, self).show()
        # 窗口开始位置
        startPos = QPoint(
            self.mainWidget.pos().x(),
            self.mainWidget.pos().y() + self.mainWidget.height())
        endPos = QPoint(
            self.mainWidget.pos().x(),
            self.mainWidget.pos().y() + self.mainWidget.height() + 10)
        self.move(startPos)
        # 初始化动画
        self.inAnimation(startPos, endPos, nextAction=nextAction)
        self.closeTimer.start(closeTime)

    def attentionIn(self):
        self.closeTimer.stop()

    def attentionOut(self):
        self.closeTimer.start(1000*1.5)