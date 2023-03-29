#!/bin/bash

#该脚本在linux上需要转换下换行符格式：dos2unix start_run.sh

#准备环境
#Windows导出依赖版本：
#  ./venv/Scripts/pip3.exe freeze > requirements.txt
#Linux安装项目依赖版本环境：
#  python3 -m venv /usr/local/python3/venv/ihome
#  pip3 install -r requirements.txt
#激活环境：
source /usr/local/python3/venv/ihome/bin/activate

# 启动程序
# 方式1：
# python3 app.py #旧启动方式-app.run
# manager启动方式-manager.run
  # 1、python3 app.py runserver --threaded --host=0.0.0.0 --port=8000
  # 2、manager.add_command('runserver', Server('0.0.0.0', port=8000, use_debugger=True))
python3 app.py runserver -h 0.0.0.0 -p 8080
# 方式2：
# uwsgi --ini uwsgi.ini
# 停止：uwsgi --stop uwsgi.pid