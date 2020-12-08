import sys, os, time
from bokeh_dev_tools import watcher
import sample_bokeh_app
import importlib


if __name__=='__main__':
    path = '/Users/ht/googledrive/PycharmProjects/bokeh_dev_tools/test'
    # 呼び出されたら、sample_bokeh_appを読み込み直して、serverを更新する関数
    app_getter = lambda: sample_bokeh_app.mod_doc
    modules_reload = [sample_bokeh_app]
    # path以下の*.pyの変更を監視, 変更があったらmoduleをreloadしてbokeh_appを更新, appを開く
    watcher.watch_bokeh_app(path, app_getter, modules_reload, watcher.just_open_test, patterns=['*.py'])
