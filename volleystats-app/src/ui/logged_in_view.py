from tkinter import ttk, constants

class LoggedInView:
    def __init__(self, root, user_service, handle_logout):
        self._root = root
        self._user_service = user_service
        self._handle_logout = handle_logout
        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _logout_handler(self):
        self._user_service.logout()
        self._handle_logout()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        
        user = self._user_service.get_current_user()
        welcome_text = f"Welcome {user.username}!"
        
        heading_label = ttk.Label(
            master=self._frame,
            text=welcome_text
        )

        logout_button = ttk.Button(
            master=self._frame,
            text="Logout",
            command=self._logout_handler
        )

        heading_label.grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)
        logout_button.grid(row=1, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)