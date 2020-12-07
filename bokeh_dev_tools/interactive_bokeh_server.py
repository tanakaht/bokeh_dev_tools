import subprocess, sys, json, os, time
from bokeh.server.server import Server
import threading
from IPython import get_ipython

class InteractiveBokehServer:
    _instance = None
    _exist = False

    def __init__(self, app_dict=None):
        if InteractiveBokehServer._exist:
            print('server already exists')
            print(f'server running at {self.url}')
            return
        self.app_dict = app_dict if app_dict is not None else{}
        if str(get_ipython()).find('colab')!=-1:
            self.env = 'colab'
        elif get_ipython() is None:
            self.env = 'script'
        else:
            self.env = 'jupyter'
        if self.env == 'colab':
            self.prepare_ngrok()
        self.url = self.get_base_url()
        self.server_thread = None
        self.server = None
        self.get_server()
        self.start_server()
        print(f'server running at {self.url}')
        InteractiveBokehServer._exist = True

    def __del__(self):
        print(self.server)
        # self.stop_server()

    def __new__(cls, app_dict=None, jupyter='colab'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start_server(self):
        if self.env == 'script':
            self.server.start()
            self.server_thread = threading.Thread(target=self.server.io_loop.start)
            self.server_thread.start()
        else:
            self.server.start()

    def stop_server(self):
        if self.env == 'script':
            if self.server_thread:
                ioloop = self.server.io_loop
                ioloop.add_callback(ioloop.stop)
                self.server_thread.join()
            self.server.stop()
        else:
            self.server.stop()

    def get_server(self, allow_websocket_origin=['*']):
        if self.env != 'colab':
            self.server = Server(self.app_dict, port=6006)
        else:
            self.server = Server(self.app_dict, port=6006, allow_websocket_origin=['*'])
        return self.server

    def prepare_ngrok(self):
        if os.path.exists('/content/ngrok'):
            return
        os.system('cd /content')
        os.system('wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip')
        os.system('unzip ngrok-stable-linux-amd64.zip')
        os.system('rm ngrok-stable-linux-amd64.zip')

    def get_base_url(self):
        if self.env=='colab':
            get_ipython().system_raw('/content/ngrok http 6006 &')
            time.sleep(2)
            res = subprocess.check_output('curl -s http://localhost:4040/api/tunnels | cat', shell=True)
            res_json = json.loads(res.decode('utf-8'))
            self.url = res_json['tunnels'][0]['public_url']
        else:
            self.url = 'http://localhost:6006'
        return self.url

    def restart_server(self):
        self.stop_server()
        self.get_server()
        self.start_server()
        for url in self.get_apps_urls():
            print(url)

    def add_app_dict(self, app_dict):
        app_dict_modified = {'/'*(not k.startswith('/'))+k: v for k, v in app_dict.items()}
        self.app_dict.update(app_dict_modified)
        self.restart_server()

    def remove_apps(self, app_keys):
        self.app_dict.pop(*app_keys)
        self.restart_server()

    def get_apps_urls(self):
        ret = []
        for k in self.app_dict.keys():
            ret.append(f'{self.url}{k}')
        return ret
