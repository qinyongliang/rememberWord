from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from CustomAnimation import *
from WebEngineUrlRequestInterceptor import *
from ApplicationConfig import *


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

# 拦截器实例
interceptor = WebEngineUrlRequestInterceptor()
class TranslateWidget(CustomAnimation):
    def __init__(self, *args, **kwargs):
        self.word = kwargs.pop("text", "")
        super(TranslateWidget, self).__init__(*args, **kwargs)
        self.loadWidget = QSvgWidget(
            self, minimumHeight=self.height(), minimumWidth=self.height(), visible=False)
        self.loadWidget.move(self.width() / 4,
                             self.height() / 4)
        self.loadWidget.load(Svg_icon_loading)
        self.loadWidget.setVisible(True)

    def loadTranslation(self):
        self.browser = QWebEngineView(self)
        self.browser.resize(self.width(), self.height())
        self.browser.setZoomFactor(0.75)
        self.browser.page().profile().setRequestInterceptor(interceptor)
        if(ApplicationConfig.setting["engine"] == "google"):
            self.browser.load(
                QUrl("https://translate.google.cn/m/translate#en/zh-CN/" + self.word.lower()))
        elif ApplicationConfig.setting["engine"] == "baidu":
            self.browser.load(QUrl(
                "http://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh#en/zh/" + self.word.lower()))
        self.browser.loadFinished.connect(self.translationShow)

    # 显示翻译框，移除掉不用的div
    def translationShow(self):
        if(ApplicationConfig.setting['engine'] == 'baidu'):
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
        elif ApplicationConfig.setting['engine'] == 'google':
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
        QTimer.singleShot(500, self.browser.show)


    def stop(self):
        try:
            if(hasattr(self.mainWidget, "translateWidget")):
                del self.mainWidget.translateWidget
            self.outAnimation(nextAction=self._close)
        except:
            pass

    def _close(self):
        try:
            self.loadWidget.close()
            self.loadWidget.deleteLater()
            if(hasattr(self, "browser")):
                self.browser.close()
            self.close()
        except:
            pass
