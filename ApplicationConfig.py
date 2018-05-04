import os
import json
import re

# 配置目录
configFilePath = os.environ['HOME'] + os.path.sep + ".remember.config"

class ApplicationConfig(object):
    # 全局设置
    setting = {"engine": "baidu", "color": '#00BFFF', "changeTime": 3.0, "fontSize": 12, "fontColor": '#ffffff',
            "wordPath": r"/home/administrator/world.txt", "opacity": 80}
    # 当前活跃视图
    views = None

    clips = []

    checkWord = re.compile("^[a-z]*$", re.I)
    key = re.compile("^[a-z1-9 ~!@#$%^&*()_+-=,.\/;'\\\[\]{}:\"\|\<\>\?        ]*$", re.I)

    def loadConfig():
        if(os.path.exists(configFilePath)):
            ApplicationConfig.setting = json.load(open(configFilePath))


    def saveConfig():
        json.dump(ApplicationConfig.setting, open(configFilePath, 'w'))
