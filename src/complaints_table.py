from sqlite3 import Error

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton
from requests import exceptions

from src.ccms_constants import *
from src.db import db_create_connection, db_select_auth_table
from src.msg import *


class ComplaintsWidget(QWidget):
    """
    Class representing the complaints tables and related tasks.
    """

    def __init__(self):
        super(ComplaintsWidget, self).__init__()
        self.table = ComplaintsTable()
        self.v_box = QVBoxLayout()
        self.h_box = QHBoxLayout()
        self.btn_op = QPushButton()
        self.btn_op.setMinimumSize(180, 30)
        self.btn_op.setMaximumSize(180, 30)
        self.btn_op.clicked.connect(self.change_status)
        self.h_box.addWidget(self.btn_op)
        self.h_box.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.h_box.setSpacing(6)
        self.v_box.addWidget(self.table)
        self.v_box.addLayout(self.h_box)
        self.setLayout(self.v_box)

    def set_complaints_status(self, complaints_status):
        self.change_layout(complaints_status)
        self.table.complaints_status = complaints_status

    def change_layout(self, complaints_status):
        if complaints_status == "Resolved":
            self.btn_op.setFixedSize(0, 0)
        else:
            if complaints_status == "Submitted":
                self.btn_op.setText("Mark as assigned")
                self.btn_op.setFixedSize(180, 30)
            else:
                self.btn_op.setText("Mark as resolved")
                self.btn_op.setFixedSize(180, 30)

    def fetch_n_show(self):
        self.table.fetch_n_show()

    def change_status(self):
        if not self.table.selectionModel().hasSelection():
            return
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        complaints_id = self.table.item(current_row, 0).text()
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            conn.close()
            headers = {"Authorization": "Token " + str(auth_token)}
            comp_url = SERVER_URL + EP_COMPLAINTS + "/" + complaints_id
            if self.table.complaints_status == "Submitted":
                new_comp_data = {
                    "status": "Assigned"
                }
            elif self.table.complaints_status == "Assigned":
                new_comp_data = {
                    "status": "Resolved"
                }
            else:
                new_comp_data = {
                    "status": "None"
                }
            try:
                comp_response = requests.put(url=comp_url, headers=headers, json=new_comp_data)
                comp_response.raise_for_status()
                self.table.removeRow(current_row)
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


class ComplaintsTable(QTableWidget):
    """
    Class representing the complaints table.
    """

    def __init__(self):
        super(ComplaintsTable, self).__init__()
        self.complaints_status = None
        self.header_list = ['ID', 'Complaint Text', 'Category', 'Status', 'Location', 'Submitted by', 'Submission Time']
        self.columns = len(self.header_list)
        self.setup_elements()

    def setup_elements(self):
        self.clearContents()
        self.clear()
        self.setRowCount(0)
        self.setColumnCount(len(self.header_list))
        self.setHorizontalHeaderLabels(self.header_list)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_header = self.horizontalHeader()
        table_header.setMinimumSectionSize(80)
        table_header.setDefaultSectionSize(150)
        table_header.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_header.setSectionResizeMode(QHeaderView.Interactive)
        table_header.setSortIndicatorShown(True)
        self.setSortingEnabled(True)
        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 300)

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
                    QTableWidgetItem(str(row_json['category_name'])),
                    QTableWidgetItem(str(row_json['status'])),
                    QTableWidgetItem(str(row_json['location'])),
                    QTableWidgetItem(str(row_json['citizen_name'])),
                    QTableWidgetItem(row_json['time_submitted'])
                ]
                for column in range(self.columns):
                    row_items[column].setFlags(row_items[column].flags() & ~Qt.ItemIsEditable)
                    self.setItem(row, column, row_items[column])
        except Error as err:
            show_error(str(err))
