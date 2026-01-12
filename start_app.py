import os
import sys
import threading
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def open_browser():
    webbrowser.open("http://127.0.0.1:8000/todolist")


os.chdir(BASE_DIR)

os.system(f"{sys.executable} manage.py migrate")
threading.Timer(2, open_browser).start()
os.system(f"{sys.executable} manage.py runserver")
