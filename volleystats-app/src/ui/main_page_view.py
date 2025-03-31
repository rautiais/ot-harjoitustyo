from tkinter import ttk

class MainPageView():
    def __init__(self, root, handle_logout):
        self._handle_logout = handle_logout

    def delete_process(self):
        self._handle_logout()