import requests
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.uic import loadUi
from requests import exceptions
from validate_email import validate_email as validate_email

from src.ccms_constants import *
from src.dashboard import QDashboard
from src.db import *
from src.msg import show_error, show_success


class CCMSMain(QWidget):
    """
    Class representing the starting window for logged out user.
    """

    def __init__(self):
        super(CCMSMain, self).__init__()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        forms_dir = os.path.join(base_dir, "forms")
        loadUi(os.path.join(forms_dir, "ui_main.ui"), self)
        self.setup_elements()

    def setup_elements(self):
        self.btnRegister.clicked.connect(self.show_register_window)
        self.btnLogin.clicked.connect(self.show_login_window)

    def show_register_window(self):
        """
        Replaces the current window with registration window.
        :return: None
        """
        new_widget = Register()
        self.parentWidget().addWidget(new_widget)
        self.parentWidget().removeWidget(self)

    def show_login_window(self):
        """
        Replaces the current window with login window.
        :return: None
        """
        new_widget = Login()
        self.parentWidget().addWidget(new_widget)
        self.parentWidget().removeWidget(self)


class Register(QWidget):
    """
    Class representing the registration window.
    """

    def __init__(self):
        super(Register, self).__init__()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        forms_dir = os.path.join(base_dir, "forms")
        loadUi(os.path.join(forms_dir, "ui_register.ui"), self)
        self.setup_elements()

    def setup_elements(self):
        self.passField2.returnPressed.connect(self.try_to_register)
        self.registerButton.clicked.connect(self.try_to_register)
        self.btnSignInPrompt.clicked.connect(self.show_login_window)

    def show_login_window(self):
        """
        Replaces the current window with login window.
        :return: None
        """
        new_widget = Login()
        self.parentWidget().addWidget(new_widget)
        self.parentWidget().removeWidget(self)

    def try_to_register(self):
        """
        Reads data from the 'form' and sends a POST request to the server to create a new account.
        :return: None
        """
        reg_email = self.emailField.text().strip().lower()
        password1 = self.passField1.text()
        password2 = self.passField2.text()
        is_valid = True
        if not validate_email(email=reg_email):
            show_error("Invalid email address!")
            is_valid = False
        if not (MIN_PASSWORD_LENGTH <= len(password1) <= MAX_PASSWORD_LENGTH):  # TODO more validity checks
            show_error(
                "Password length should be between " + str(MIN_PASSWORD_LENGTH) + " and " + str(MAX_PASSWORD_LENGTH))
            is_valid = False
        if not (password1 == password2 and MIN_PASSWORD_LENGTH <= len(password2) <= MAX_PASSWORD_LENGTH):
            show_error("Passwords don't match")
            is_valid = False
        if not is_valid:
            return
        register_url = SERVER_URL + EP_REGISTER
        register_data = {"email": reg_email, "password1": password1, "password2": password2}
        try:
            reg_response = requests.post(url=register_url, data=register_data)  # data, json both seems ok
            reg_response.raise_for_status()
            if reg_response.status_code == 201:
                self.emailField.setText("")
                self.passField1.setText("")
                self.passField2.setText("")
                show_success("Registration successful, check email!")
            else:
                show_error("Registration failed, try again!")
        except exceptions.ConnectTimeout:
            show_error('Connection Timeout')
        except exceptions.ConnectionError:
            show_error('Connection Error')
        except IOError:
            show_error('Error')


class Login(QWidget):
    """
    Class representing the login window.
    """

    def __init__(self):
        super(Login, self).__init__()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        forms_dir = os.path.join(base_dir, "forms")
        loadUi(os.path.join(forms_dir, "ui_signin.ui"), self)
        self.setup_elements()

    def setup_elements(self):
        self.passField.returnPressed.connect(self.try_to_login)
        self.loginButton.clicked.connect(self.try_to_login)
        self.btnRegisterPrompt.clicked.connect(self.show_register_window)

    def show_register_window(self):
        """
        Replaces the current window with registration window.
        :return: None
        """
        new_widget = Register()
        self.parentWidget().addWidget(new_widget)
        self.parentWidget().removeWidget(self)

    def try_to_login(self):
        """
        Reads data from the 'form' and sends a POST request to the server to let the user log in.
        :return: None
        """
        login_email = self.emailField.text().strip().lower()
        password = self.passField.text()
        is_valid = True
        if not validate_email(email=login_email):
            show_error("Invalid email address!")
            is_valid = False
        if not (MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH):  # TODO more validity checks
            show_error(
                "Password length should be between " + str(MIN_PASSWORD_LENGTH) + " and " + str(MAX_PASSWORD_LENGTH))
            is_valid = False
        if not is_valid:
            return
        login_url = SERVER_URL + EP_LOGIN
        login_data = {"email": login_email, "password": password}
        try:
            login_response = requests.post(url=login_url, json=login_data)
            if login_response.status_code == 200:
                auth_token = login_response.json()["key"]
                conn = db_create_connection()
                db_create_auth_table(conn)
                db_delete_auth_table(conn)
                db_insert_auth_table(conn, "token", auth_token)
                conn.close()
                self.emailField.setText("")
                self.passField.setText("")
                show_success("Successfully signed in")
                pw = self.parentWidget()
                pw.addWidget(QDashboard())
                pw.addWidget(QDashboard())
                pw.removeWidget(self)
                pw.setMinimumSize(800, 600)
                pw.setMaximumSize(16777215, 16777215)
                fg = pw.frameGeometry()
                cp = QDesktopWidget().availableGeometry().center()
                fg.moveCenter(cp)
                pw.move(fg.topLeft())
            else:
                show_error("Failed, try again!")
        except exceptions.ConnectTimeout:
            show_error('Connection Timeout')
        except exceptions.ConnectionError:
            show_error('Connection Error')
        except IOError:
            show_error('Error')
