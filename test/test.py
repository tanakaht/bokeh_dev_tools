import sys, os, time
from bokeh_dev_tools import watcher
import sample_bokeh_app
import importlib


if __name__=='__main__':
    from bokeh_dev_tools.interactive_bokeh_server import InteractiveBokehServer
    server = InteractiveBokehServer()
    path = '/Users/ht/googledrive/PycharmProjects/bokeh_dev_tools/test'
    # 呼び出されたら、sample_bokeh_appを読み込み直して、serverを更新する関数
    modules_reload = [sample_bokeh_app]
    def update_bokeh():
        for mod in modules_reload:
            importlib.reload(mod)
        app_dict = {'/test': sample_bokeh_app.mod_doc}
        server.add_app_dict(app_dict)
    # 開くだけのtest
    def test(driver):
        driver.get('http://localhost:6006' + '/test')
    # path以下の*.pyの変更を監視, 変更があったらupdate_bokeh(), test(driver)を実行する
    watcher.watch_bokeh_app(path, update_bokeh, test, patterns=['*.py'])
