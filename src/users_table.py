from sqlite3 import Error

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from requests import exceptions

from src.ccms_constants import *
from src.db import db_create_connection, db_select_auth_table
from src.msg import *


class UsersTable(QTableWidget):
    """
    Class representing the users table.
    """

    def __init__(self):
        super(UsersTable, self).__init__()
        self.header_list = ['ID', 'Email', 'Name', 'Type', 'Last Login']
        self.columns = len(self.header_list)
        self.url = SERVER_URL + EP_USERS
        self.setup_elements()
        self.fetch_n_show()

    def setup_elements(self):
        self.clearContents()
        self.clear()
        self.setRowCount(0)
        # self.verticalHeader().hide()
        self.setColumnCount(len(self.header_list))
        self.setHorizontalHeaderLabels(self.header_list)
        self.setAlternatingRowColors(True)
        table_header = self.horizontalHeader()
        table_header.setMinimumSectionSize(80)
        table_header.setDefaultSectionSize(200)
        table_header.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_header.setSectionResizeMode(QHeaderView.Interactive)
        table_header.setSortIndicatorShown(True)
        self.setSortingEnabled(True)
        self.setColumnWidth(0, 80)

    def fetch_n_show(self):
        """
        Retrieves list of all users from the server via GET request and displays them.
        :return: None
        """
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
            if auth_token is None:
                show_error("No login info")
                return
            headers = {"Authorization": "Token " + str(auth_token)}
            try:
                users_response = requests.get(url=self.url, headers=headers)
                users_response.raise_for_status()
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
                return
            except exceptions.ConnectionError:
                show_error('Connection Error')
                return
            except IOError as err:
                show_error(str(err))
                return
            users_response = users_response.json()
            total_users = len(users_response)
            self.setRowCount(total_users)
            for row in range(total_users):
                row_json = users_response[row]
                row_items = [
                    QTableWidgetItem(str(row_json['user_id'])),
                    QTableWidgetItem(row_json['email']),
                    QTableWidgetItem(str(row_json['name'])),
                    QTableWidgetItem(str(row_json['is_employee'])),
                    QTableWidgetItem(str(row_json['last_login']))
                ]
                for column in range(self.columns):
                    row_items[column].setFlags(row_items[column].flags() & ~Qt.ItemIsEditable)
                    self.setItem(row, column, row_items[column])
        except Error as err:
            show_error(str(err))


class CitizensTable(QTableWidget):
    """
    Class representing the citizens table.
    """

    def __init__(self):
        super(CitizensTable, self).__init__()
        self.header_list = ['ID', 'Email', 'Name', 'Last Login']
        self.columns = len(self.header_list)
        self.url = SERVER_URL + EP_CITIZENS
        self.setup_elements()
        self.fetch_n_show()

    def setup_elements(self):
        self.clearContents()
        self.clear()
        self.setRowCount(0)
        # self.verticalHeader().hide()
        self.setColumnCount(len(self.header_list))
        self.setHorizontalHeaderLabels(self.header_list)
        self.setAlternatingRowColors(True)
        table_header = self.horizontalHeader()
        table_header.setMinimumSectionSize(80)
        table_header.setDefaultSectionSize(200)
        table_header.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_header.setSectionResizeMode(QHeaderView.Interactive)
        table_header.setSortIndicatorShown(True)
        self.setSortingEnabled(True)
        self.setColumnWidth(0, 80)

    def fetch_n_show(self):
        """
        Retrieves list of citizens from the server via GET request and displays them.
        :return: None
        """
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
            if auth_token is None:
                show_error("No login info")
                return
            headers = {"Authorization": "Token " + str(auth_token)}
            try:
                users_response = requests.get(url=self.url, headers=headers)
                users_response.raise_for_status()
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
                return
            except exceptions.ConnectionError:
                show_error('Connection Error')
                return
            except IOError as err:
                show_error(str(err))
                return
            users_response = users_response.json()
            total_users = len(users_response)
            self.setRowCount(total_users)
            for row in range(total_users):
                row_json = users_response[row]
                row_items = [
                    QTableWidgetItem(str(row_json['user_id'])),
                    QTableWidgetItem(row_json['email']),
                    QTableWidgetItem(str(row_json['name'])),
                    QTableWidgetItem(str(row_json['last_login']))
                ]
                for column in range(self.columns):
                    row_items[column].setFlags(row_items[column].flags() & ~Qt.ItemIsEditable)
                    self.setItem(row, column, row_items[column])
        except Error as err:
            show_error(str(err))


class EmployeesTable(QTableWidget):
    """
    Class representing the employees table.
    """

    def __init__(self):
        super(EmployeesTable, self).__init__()
        self.header_list = ['ID', 'Email', 'Name', 'Last Login']
        self.columns = len(self.header_list)
        self.url = SERVER_URL + EP_EMPLOYEES
        self.setup_elements()
        self.fetch_n_show()

    def setup_elements(self):
        self.clearContents()
        self.clear()
        self.setRowCount(0)
        # self.verticalHeader().hide()
        self.setColumnCount(len(self.header_list))
        self.setHorizontalHeaderLabels(self.header_list)
        self.setAlternatingRowColors(True)
        table_header = self.horizontalHeader()
        table_header.setMinimumSectionSize(80)
        table_header.setDefaultSectionSize(200)
        table_header.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_header.setSectionResizeMode(QHeaderView.Interactive)
        table_header.setSortIndicatorShown(True)
        self.setSortingEnabled(True)
        self.setColumnWidth(0, 80)

    def fetch_n_show(self):
        """
        Retrieves list of employees from the server via GET request and displays them.
        :return: None
        """
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
            if auth_token is None:
                show_error("No login info")
                return
            headers = {"Authorization": "Token " + str(auth_token)}
            try:
                users_response = requests.get(url=self.url, headers=headers)
                users_response.raise_for_status()
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
                return
            except exceptions.ConnectionError:
                show_error('Connection Error')
                return
            except IOError as err:
                show_error(str(err))
                return
            users_response = users_response.json()
            total_users = len(users_response)
            self.setRowCount(total_users)
            for row in range(total_users):
                row_json = users_response[row]
                row_items = [
                    QTableWidgetItem(str(row_json['user_id'])),
                    QTableWidgetItem(row_json['email']),
                    QTableWidgetItem(str(row_json['name'])),
                    QTableWidgetItem(str(row_json['last_login']))
                ]
                for column in range(self.columns):
                    row_items[column].setFlags(row_items[column].flags() & ~Qt.ItemIsEditable)
                    self.setItem(row, column, row_items[column])
        except Error as err:
            show_error(str(err))
