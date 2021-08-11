import requests
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.uic import loadUi
from requests import exceptions
from validate_email import validate_email as validate_email

from src.ccms_constants import *
from src.dashboard import QDashboard
from src.db import *


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
        if validate_email(email=reg_email):
            self.labelMsgEmail.setStyleSheet("color:green;")
            self.labelMsgEmail.setText("Email address seems ok")
        else:
            self.labelMsgEmail.setStyleSheet("color:red;")
            self.labelMsgEmail.setText("Invalid email address!")
            is_valid = False
        if MIN_PASSWORD_LENGTH <= len(password1) <= MAX_PASSWORD_LENGTH:  # TODO more validity checks
            self.labelMsgPass1.setStyleSheet("color:green;")
            self.labelMsgPass1.setText("Password seems ok")
        else:
            self.labelMsgPass1.setStyleSheet("color:red;")
            self.labelMsgPass1.setText(
                "Password length should be between " + str(MIN_PASSWORD_LENGTH) + " and " + str(MAX_PASSWORD_LENGTH))
            is_valid = False
        if password1 == password2 and MIN_PASSWORD_LENGTH <= len(password2) <= MAX_PASSWORD_LENGTH:
            self.labelMsgPass2.setStyleSheet("color:green;")
            self.labelMsgPass2.setText("Passwords matched")
        else:
            self.labelMsgPass2.setStyleSheet("color:red;")
            self.labelMsgPass2.setText("Passwords don't match")
            is_valid = False
        if not is_valid:
            return
        register_url = SERVER_URL + EP_REGISTER
        register_data = {"email": reg_email, "password1": password1, "password2": password2}
        self.labelMsgRegister.setStyleSheet("color:red;")
        try:
            reg_response = requests.post(url=register_url, data=register_data)  # data, json both seems ok
            reg_response.raise_for_status()
            if reg_response.status_code == 201:
                self.labelMsgRegister.setStyleSheet("color:green;")
                self.labelMsgRegister.setText("Registration successful, check email!")
            else:
                self.labelMsgRegister.setText("Registration failed, try again!")
        except exceptions.ConnectTimeout:
            self.labelMsgRegister.setText('Connection Timeout')
        except exceptions.ConnectionError:
            self.labelMsgRegister.setText('Connection Error')
        except IOError:
            self.labelMsgRegister.setText('Error')


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
        if validate_email(email=login_email):
            self.labelMsgEmail.setStyleSheet("color:green;")
            self.labelMsgEmail.setText("Email address seems ok")
        else:
            self.labelMsgEmail.setStyleSheet("color:red;")
            self.labelMsgEmail.setText("Invalid email address!")
            is_valid = False
        if MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:  # TODO more validity checks
            self.labelMsgPass.setStyleSheet("color:green;")
            self.labelMsgPass.setText("Password seems ok")
        else:
            self.labelMsgPass.setStyleSheet("color:red;")
            self.labelMsgPass.setText(
                "Password length should be between " + str(MIN_PASSWORD_LENGTH) + " and " + str(MAX_PASSWORD_LENGTH))
            is_valid = False
        if not is_valid:
            return
        login_url = SERVER_URL + EP_LOGIN
        login_data = {"email": login_email, "password": password}
        self.labelMsgLogin.setStyleSheet("color:red;")
        try:
            login_response = requests.post(url=login_url, json=login_data)
            if login_response.status_code == 200:
                auth_token = login_response.json()["key"]
                conn = db_create_connection()
                db_create_auth_table(conn)
                db_delete_auth_table(conn)
                db_insert_auth_table(conn, "token", auth_token)
                conn.close()
                self.labelMsgLogin.setStyleSheet("color:green;")
                self.labelMsgLogin.setText("Successfully signed in")
                pw = self.parentWidget()
                pw.addWidget(QDashboard())
                pw.removeWidget(self)
                pw.setMinimumSize(800, 600)
                pw.setMaximumSize(16777215, 16777215)
                fg = pw.frameGeometry()
                cp = QDesktopWidget().availableGeometry().center()
                fg.moveCenter(cp)
                pw.move(fg.topLeft())
            else:
                self.labelMsgLogin.setText("Failed, try again!")
        except exceptions.ConnectTimeout:
            self.labelMsgLogin.setText('Connection Timeout')
        except exceptions.ConnectionError:
            self.labelMsgLogin.setText('Connection Error')
        except IOError:
            self.labelMsgLogin.setText('Error')
