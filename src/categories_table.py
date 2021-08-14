from sqlite3 import Error

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QPushButton, QWidget, \
    QHBoxLayout, QVBoxLayout
from requests import exceptions

from src.ccms_constants import *
from src.db import db_create_connection, db_select_auth_table
from src.msg import *


class CategoriesWidget(QWidget):
    """
    Class representing the categories table and related tasks.
    """

    def __init__(self):
        super(CategoriesWidget, self).__init__()
        self.table = CategoriesTableWidget()
        self.v_box = QVBoxLayout()
        h_box = QHBoxLayout()
        btn_add = QPushButton("Add")
        btn_add.setMinimumSize(80, 30)
        btn_add.setMaximumSize(80, 30)
        btn_add.clicked.connect(self.add_new_row)
        btn_save = QPushButton("Save")
        btn_save.setMinimumSize(80, 30)
        btn_save.setMaximumSize(80, 30)
        btn_save.clicked.connect(self.save_current_category)
        btn_delete = QPushButton("Delete")
        btn_delete.setMinimumSize(80, 30)
        btn_delete.setMaximumSize(80, 30)
        btn_delete.clicked.connect(self.delete_current_category)
        h_box.addWidget(btn_add)
        h_box.addWidget(btn_save)
        h_box.addWidget(btn_delete)
        h_box.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        h_box.setSpacing(6)
        self.v_box.addWidget(self.table)
        self.v_box.addLayout(h_box)
        self.setLayout(self.v_box)

    def add_new_row(self):
        """
        Adds a new row to the categories table so that the employee can add new data.
        :return: None
        """
        current_row = self.table.rowCount()
        if current_row > 0 and self.table.item(current_row - 1, 0).text() == "-1":
            return
        self.table.insertRow(current_row)
        current_item = QTableWidgetItem("-1")
        current_item.setFlags(current_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(current_row, 0, current_item)

    def save_current_category(self):
        """
        If the selected row is new calls necessary method to create a new category. Otherwise saves the changes in current category.
        :return: None
        """
        current_row = self.table.currentRow()
        current_item = self.table.item(current_row, 0)
        if current_item is None:
            show_error("Empty item")
            return
        cat_id = current_item.text()
        if cat_id is None:
            show_error("Empty id")
            return
        if cat_id == "-1":
            self.create_new_category(current_row)
            return
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
            headers = {"Authorization": "Token " + str(auth_token)}
            categories_url = SERVER_URL + EP_CATEGORY + cat_id
            new_cat_data = {
                "keyword": self.table.item(current_row, 1).text(),
                "category": self.table.item(current_row, 2).text()
            }
            try:
                cat_response = requests.put(url=categories_url, headers=headers, json=new_cat_data)  # put & json works
                cat_response.raise_for_status()
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
                return
            except exceptions.ConnectionError:
                show_error('Connection Error')
                return
            except IOError as err:
                show_error(str(err))
                return
        except Error as err:
            show_error(str(err))

    def create_new_category(self, current_row):
        """
        Creates a new entry in the categories table in the server database.
        :param current_row: Current row
        :return: None
        """
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
            headers = {"Authorization": "Token " + str(auth_token)}
            categories_url = SERVER_URL + EP_CATEGORIES
            try:
                new_cat_data = {
                    "keyword": self.table.item(current_row, 1).text(),
                    "category": self.table.item(current_row, 2).text()
                }
                categories_response = requests.post(url=categories_url, headers=headers, json=new_cat_data)
                categories_response.raise_for_status()
                if categories_response.status_code == 201:
                    categories_response = categories_response.json()
                    current_item = QTableWidgetItem(str(categories_response['category_id']))
                    current_item.setFlags(current_item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(current_row, 0, current_item)
            except AttributeError:
                show_error('Attribute Error')
                return
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
                return
            except exceptions.ConnectionError:
                show_error('Connection Error')
                return
            except IOError as err:
                show_error(str(err))
                return
        except Error as err:
            show_error(str(err))
        pass

    def delete_current_category(self):
        """
        Deletes selected row from the categories table and related data from server.
        :return: None
        """
        row = self.table.currentRow()
        current_item = self.table.item(row, 0)
        if current_item is None:
            show_error("Empty item")
            self.table.removeRow(row)
            return
        if current_item.text() == "-1":
            self.table.removeRow(row)
            return
        cat_id = current_item.text()
        if cat_id is None:
            show_error("Empty id")
            self.table.removeRow(row)
            return
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
            headers = {"Authorization": "Token " + str(auth_token)}
            categories_url = SERVER_URL + EP_CATEGORIES + "/" + cat_id
            try:
                categories_response = requests.delete(url=categories_url, headers=headers)
                categories_response.raise_for_status()
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
                return
            except exceptions.ConnectionError:
                show_error('Connection Error')
                return
            except IOError as err:
                show_error(str(err))
                return
            self.table.removeRow(row)
        except Error as err:
            show_error(str(err))


class CategoriesTableWidget(QTableWidget):
    """
    Class representing the categories table.
    """

    def __init__(self):
        super(CategoriesTableWidget, self).__init__()
        self.header_list = ['ID', 'Key Word', 'Category']
        self.columns = len(self.header_list)
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
        table_header.setMinimumSectionSize(150)
        table_header.setDefaultSectionSize(150)
        table_header.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_header.setSectionResizeMode(QHeaderView.Stretch)
        table_header.setSortIndicatorShown(True)
        self.setSortingEnabled(True)

    def fetch_n_show(self):
        """
        Retrieves list of categories from the server via GET request and displays them.
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
            categories_url = SERVER_URL + EP_CATEGORIES
            try:
                categories_response = requests.get(url=categories_url, headers=headers)
                categories_response.raise_for_status()
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
                return
            except exceptions.ConnectionError:
                show_error('Connection Error')
                return
            except IOError as err:
                show_error(str(err))
                return
            categories_response = categories_response.json()
            total_categories = len(categories_response)
            self.setRowCount(total_categories)
            for row in range(total_categories):
                row_json = categories_response[row]
                row_items = [
                    QTableWidgetItem(str(row_json['category_id'])),
                    QTableWidgetItem(str(row_json['keyword'])),
                    QTableWidgetItem(str(row_json['category']))
                ]
                row_items[0].setFlags(row_items[0].flags() & ~Qt.ItemIsEditable)
                self.setItem(row, 0, row_items[0])
                self.setItem(row, 1, row_items[1])
                self.setItem(row, 2, row_items[2])
        except Error as err:
            show_error(str(err))
