import requests
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from requests import exceptions

from src.ccms_constants import *
from src.db import *
from src.msg import *


class ProfileInfo(QWidget):
    """
    A class that can retrieve, show, and let edit profile information of the currently logged in user.
    """

    def __init__(self):
        super(ProfileInfo, self).__init__()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        forms_dir = os.path.join(base_dir, "forms")
        loadUi(os.path.join(forms_dir, "ui_profile.ui"), self)
        self.setup_elements()
        self.display_profile_info()
        # self.show()

    def setup_elements(self):
        self.btnSaveProfile.clicked.connect(self.update_profile)
        self.btnSaveNewPass.clicked.connect(self.change_password)
        pass

    def display_profile_info(self):
        """
        Sends a GET request to the server to retrieve profile information.
        :return: None
        """
        auth_token = None
        profile_response = None
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
        except Error as err:
            show_error(str(err))
        if auth_token is None:
            return
        profile_url = SERVER_URL + EP_USER
        headers = {"Authorization": "Token " + str(auth_token)}
        try:
            profile_response = requests.get(url=profile_url, headers=headers)
            profile_response.raise_for_status()
        except exceptions.ConnectTimeout:
            show_error('Connection Timeout')
        except exceptions.ConnectionError:
            show_error('Connection Error')
        except IOError as err:
            show_error(str(err))
        if profile_response is None or profile_response.status_code != 200:
            return
        profile_response = profile_response.json()
        self.idField.setText(str(profile_response["user_id"]))
        self.emailField.setText(profile_response["email"])
        self.nameField.setText(profile_response["name"])
        self.addressField.setText(profile_response["address"])

    def update_profile(self):
        """
        Sends a PATCH request to the server carrying modified profile information.
        :return: None
        """
        auth_token = None
        profile_response = None
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
        except Error as err:
            show_error(str(err))
        if auth_token is None:
            return
        profile_url = SERVER_URL + EP_USER
        headers = {"Authorization": "Token " + str(auth_token)}
        profile_update_data = {
            "name": self.nameField.text(),
            "address": self.addressField.text()
        }
        try:
            # using put caused 400 error, patch seems ok; we are sending partial data
            profile_response = requests.patch(url=profile_url, headers=headers, data=profile_update_data)
            profile_response.raise_for_status()
        except exceptions.ConnectTimeout:
            show_error('Connection Timeout')
            return
        except exceptions.ConnectionError:
            show_error('Connection Error')
            return
        except IOError as err:
            show_error(str(err))
            return
        if profile_response is None:
            return
        if profile_response.status_code != 200:
            show_error("Could not update")
            return
        profile_response = profile_response.json()
        self.idField.setText(str(profile_response["user_id"]))
        self.emailField.setText(profile_response["email"])
        self.nameField.setText(profile_response["name"])
        self.addressField.setText(profile_response["address"])
        show_success("Profile Information Updated")

    def change_password(self):
        """
        Sends a POST request to the server carrying old and new password in an attempt to change password.
        :return: None
        """
        auth_token = None
        pass_response = None
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
        except Error as err:
            show_error(str(err))
        if auth_token is None:
            return
        pass_url = SERVER_URL + EP_PASSWORD_CHANGE
        headers = {"Authorization": "Token " + str(auth_token)}
        old_pass = self.passFieldOld.text()
        new_pass_1 = self.passFieldNew1.text()
        new_pass_2 = self.passFieldNew2.text()
        if not (MIN_PASSWORD_LENGTH <= len(new_pass_1) <= MAX_PASSWORD_LENGTH):  # TODO more validity checks
            show_error(
                "Password length should be between " + str(MIN_PASSWORD_LENGTH) + " and " + str(MAX_PASSWORD_LENGTH))
            return
        if new_pass_1 != new_pass_2:
            show_error("Passwords don't match")
            return
        pass_change_data = {
            "new_password1": new_pass_1,
            "new_password2": new_pass_2,
            "old_password": old_pass
        }
        try:
            pass_response = requests.post(url=pass_url, headers=headers, data=pass_change_data)
            pass_response.raise_for_status()
        except exceptions.ConnectTimeout:
            show_error('Connection Timeout')
        except exceptions.ConnectionError:
            show_error('Connection Error')
        except IOError as err:
            # show_success(pass_response.json())
            show_error(str(err))
        if pass_response is None:
            show_error("Could not update")
            return
        if pass_response.status_code == 200:
            self.passFieldOld.clear()
            self.passFieldNew1.clear()
            self.passFieldNew2.clear()
            pass_response = pass_response.json()
            show_success(pass_response["detail"])
