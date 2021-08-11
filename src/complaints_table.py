from sqlite3 import Error

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from requests import exceptions

from src.ccms_constants import *
from src.db import db_create_connection, db_select_auth_table
from src.msg import *


class ComplaintsTable(QTableWidget):
    """
    Class representing the complaints table.
    """

    def __init__(self):
        super(ComplaintsTable, self).__init__()
        self.complaints_status = None
        self.header_list = ['id', 'Complaint Text', 'Category', 'Status', 'Submitted by', 'Submission Time']
        self.columns = len(self.header_list)
        self.setup_elements()
        # self.fetch_n_show()

    def setup_elements(self):
        self.clearContents()  # clears all data excluding header
        self.clear()  # clears all data items including header
        self.setRowCount(0)  # deletes blank rows, must required
        # self.verticalHeader().hide()
        self.setColumnCount(len(self.header_list))
        self.setHorizontalHeaderLabels(self.header_list)
        self.setAlternatingRowColors(True)
        table_header = self.horizontalHeader()
        table_header.setMinimumSectionSize(150)
        table_header.setDefaultSectionSize(150)
        table_header.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_header.setSectionResizeMode(QHeaderView.Interactive)  # InterActive, Fixed, ResizeToContents, Stretch
        table_header.setSortIndicatorShown(True)

    def set_complaints_status(self, complaints_status):
        self.complaints_status = complaints_status

    def fetch_n_show(self):
        """
        Retrieves list of complaints from the server via GET request and displays them.
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
            complaints_url = SERVER_URL + EP_COMPLAINTS
            complaints_param = {
                "cs": self.complaints_status
            }
            try:
                complaints_response = requests.get(url=complaints_url, headers=headers, params=complaints_param)
                complaints_response.raise_for_status()
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
                return
            except exceptions.ConnectionError:
                show_error('Connection Error')
                return
            except IOError as err:
                show_error(str(err))
                return
            complaints_response = complaints_response.json()
            total_complaints = len(complaints_response)
            self.setRowCount(total_complaints)
            for row in range(total_complaints):
                row_json = complaints_response[row]
                row_items = [
                    QTableWidgetItem(str(row_json['complaints_id'])),
                    QTableWidgetItem(row_json['description']),
                    QTableWidgetItem(str(row_json['category_id'])),
                    QTableWidgetItem(str(row_json['status'])),
                    QTableWidgetItem(str(row_json['citizen_id'])),
                    QTableWidgetItem(row_json['time_submitted'])
                ]
                for column in range(self.columns):
                    row_items[column].setFlags(row_items[column].flags() & ~Qt.ItemIsEditable)
                    self.setItem(row, column, row_items[column])
        except Error as err:
            show_error(str(err))
