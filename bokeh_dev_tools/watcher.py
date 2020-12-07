import time
from watchdog.observers.polling import PollingObserver
from watchdog.events import PatternMatchingEventHandler
from selenium import webdriver

driver = webdriver.Chrome()

class MyHandler(PatternMatchingEventHandler):
    def __init__(self, patterns):
        super(MyHandler, self).__init__(patterns=patterns)
        self.changed_flg = False

    def on_moved(self, event):
        self.changed_flg = True

    def on_created(self, event):
        self.changed_flg = True

    def on_deleted(self, event):
        self.changed_flg = True

    def on_modified(self, event):
        self.changed_flg = True


def watch(path, main_func, patterns=['*.py']):
    event_handler = MyHandler(patterns)
    main_func()
    observer = PollingObserver()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            if event_handler.changed_flg:
                try:
                    main_func()
                except Exception as e:
                    print(e)
                event_handler.changed_flg = False
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def watch_bokeh_app(path, update_bokeh, test, patterns=['*.py']):
    def main_func():
        update_bokeh()
        test(driver)
    watch(path, main_func, patterns)
