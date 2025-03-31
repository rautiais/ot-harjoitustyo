from tkinter import ttk, constants, StringVar
from services.user_service import UserService

class LoginView:
    def __init__(self, root, handle_register, handle_logged_in, user_service):
        self._root = root
        self._handle_register = handle_register
        self._handle_logged_in = handle_logged_in
        self._user_service = user_service
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _login_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        if self._user_service.login(username, password):
            self._handle_logged_in()
        else:
            self._error_variable.set("Invalid username or password")

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._error_variable = StringVar(self._frame)

        heading_label = ttk.Label(
            master=self._frame, text="Login")

        username_label = ttk.Label(master=self._frame, text="Username")
        self._username_entry = ttk.Entry(master=self._frame)

        password_label = ttk.Label(master=self._frame, text="Password")
        self._password_entry = ttk.Entry(master=self._frame, show="*")

        login_button = ttk.Button(
            master=self._frame,
            text="Login",
            command=self._login_handler
        )

        register_button = ttk.Button(
            master=self._frame,
            text="Create new user",
            command=self._handle_register
        )

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground='red'
        )

        heading_label.grid(row=0, column=0, columnspan=3, sticky=constants.W, padx=8, pady=8)
        username_label.grid(row=1, column=0, padx=8, pady=8)
        self._username_entry.grid(row=1, column=1, sticky=(constants.E, constants.W), padx=8, pady=8)
        password_label.grid(row=2, column=0, padx=8, pady=8)
        self._password_entry.grid(row=2, column=1, sticky=(constants.E, constants.W), padx=8, pady=8)
        login_button.grid(row=3, column=0, columnspan=2, sticky=(constants.E, constants.W), padx=8, pady=8)
        register_button.grid(row=4, column=0, columnspan=2, sticky=(constants.E, constants.W), padx=8, pady=8)
        self._error_label.grid(row=5, column=0, columnspan=2, padx=8, pady=8)