import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QVBoxLayout, QLabel, QWidget
from PyQt5.uic import loadUi
from requests import exceptions

from src.categories_table import CategoriesWidget
from src.ccms_constants import *
from src.complaints_table import ComplaintsWidget
from src.db import *
from src.msg import show_error, show_success
from src.profile import ProfileInfo
from src.users_table import CitizensTable, EmployeesTable


class QDashboard(QMainWindow):
    """
    Class representing the dashboard of a logged in employee.
    """

    def __init__(self):
        super(QDashboard, self).__init__()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.forms_dir = os.path.join(self.base_dir, "forms")
        self.icons_root = os.path.join(self.base_dir, "icons")
        self.icons_theme_dir = os.path.join(self.icons_root, "white")
        loadUi(os.path.join(self.forms_dir, "ui_dashboard.ui"), self)
        self.s_w = QtWidgets.QStackedWidget()
        self.new_widget = None
        self.old_widget = None
        self.new_btn = None
        self.old_btn = None
        self.animation_side_bar = QPropertyAnimation(self.sideBarContainer, b"maximumWidth")
        self.move_to_center()
        self.check_logged_in()
        self.setup_elements()
        self.display_welcome()

    def move_to_center(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    def check_logged_in(self):
        pass

    def setup_elements(self):
        icon = QIcon(os.path.join(self.icons_theme_dir, "sb_collapse.svg"))
        self.toggleSideBar.setIcon(icon)
        self.toggleSideBar.clicked.connect(self.toggle_side_bar)
        self.btnProfile.clicked.connect(self.display_profile)
        self.btnCitizens.clicked.connect(self.display_citizens)
        self.btnEmployees.clicked.connect(self.display_employees)
        self.btnCategories.clicked.connect(self.display_categories)
        self.btnComplaintsNew.clicked.connect(self.display_complaints_new)
        self.btnComplaintsPending.clicked.connect(self.display_complaints_pending)
        self.btnComplaintsResolved.clicked.connect(self.display_complaints_resolved)
        self.logoutButton.clicked.connect(self.do_logout)
        self.displayHL.addWidget(self.s_w)
        self.s_w.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def display_welcome(self):
        """
        Method used to display welcome screen
        :return: None
        """
        d_w = QWidget()
        vbox = QVBoxLayout()
        d_w.setLayout(vbox)
        label1 = QLabel()
        label1.setAlignment(Qt.AlignCenter)
        pix_path = os.path.join(self.icons_root, "black", "smile.svg")
        pixmap = QPixmap(pix_path)
        pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
        label1.setPixmap(pixmap)
        label2 = QLabel('WELCOME')
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet("font-size:40px;")
        vbox.addWidget(label1, 0, Qt.AlignHCenter | Qt.AlignBottom)
        vbox.addWidget(label2, 0, Qt.AlignHCenter | Qt.AlignTop)
        vbox.setSpacing(60)
        self.new_widget = d_w
        self.add_new_remove_old()

    def toggle_side_bar(self):
        """
        When called, toggles the side bar.
        :return: None
        """
        side_bar_width_current = self.sideBarContainer.width()
        if side_bar_width_current == 0:
            side_bar_width_new = 250
            self.toggleSideBar.setIcon(QIcon(os.path.join(self.icons_theme_dir, "sb_collapse.svg")))
        else:
            side_bar_width_new = 0
            self.toggleSideBar.setIcon(QIcon(os.path.join(self.icons_theme_dir, "sb_expand.svg")))
        self.animation_side_bar.setDuration(500)
        self.animation_side_bar.setStartValue(side_bar_width_current)
        self.animation_side_bar.setEndValue(side_bar_width_new)
        self.animation_side_bar.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation_side_bar.start()

    def setup_side_buttons(self):
        self.sideBarMenuFrame.setStyleSheet(
            "QPushButton{ padding: 6 12 6 12; text-align:left; border:0; border-radius:2px; background-color:#01796f; } QPushButton::hover { padding: 6 12 6 12; text-align:left;  border:0; background-color:#004040; }"
        )

    def add_new_remove_old(self):
        """
        Displays a new widget in the 'main' area and removes the old one.
        :return: None
        """
        self.s_w.addWidget(self.new_widget)
        if self.old_widget is not None:
            self.s_w.removeWidget(self.old_widget)
        self.old_widget = self.new_widget
        if self.old_btn is not None:
            self.old_btn.setStyleSheet(
                "{padding: 6 12 6 12; text-align:left; border:0; border-radius:2px; background-color:#01796f;} :hover { padding: 6 12 6 12; text-align:left;  border:0; background-color:#004040; }"
            )
        self.setup_side_buttons()
        if self.new_btn is not None:
            self.new_btn.setStyleSheet(
                "border:0; border-radius:2px; background-color:#004040;"
            )
        self.old_btn = self.new_btn

    def display_profile(self):
        self.new_widget = ProfileInfo()
        self.new_btn = self.btnProfile
        self.add_new_remove_old()

    def display_citizens(self):
        self.new_widget = CitizensTable()
        self.new_btn = self.btnCitizens
        self.add_new_remove_old()

    def display_employees(self):
        self.new_widget = EmployeesTable()
        self.new_btn = self.btnEmployees
        self.add_new_remove_old()

    def display_categories(self):
        self.new_widget = CategoriesWidget()
        self.new_btn = self.btnCategories
        self.add_new_remove_old()

    def display_complaints_new(self):
        self.new_btn = self.btnComplaintsNew
        self.display_complaints("Submitted")

    def display_complaints_pending(self):
        self.new_btn = self.btnComplaintsPending
        self.display_complaints("Assigned")

    def display_complaints_resolved(self):
        self.new_btn = self.btnComplaintsResolved
        self.display_complaints("Resolved")

    def display_complaints(self, complaints_status):
        self.new_widget = ComplaintsWidget()
        self.new_widget.set_complaints_status(complaints_status)
        self.new_widget.fetch_n_show()
        self.add_new_remove_old()

    def do_logout(self):
        """
        Sends a POST request to the server to log out and deletes local data, then exits
        :return: None
        """
        self.logoutButton.setStyleSheet(
            "border:0;border-radius:2px;background-color:#004040;"
        )
        try:
            conn = db_create_connection()
            auth_token = db_select_auth_table(conn)
            db_delete_auth_table(conn)
            conn.close()
            logout_url = SERVER_URL + EP_LOGOUT
            headers = {"Authorization": "Token " + str(auth_token)}
            try:
                logout_response = requests.post(url=logout_url, headers=headers)
                if logout_response.status_code == 200:
                    show_success(logout_response.json()["detail"])
            except exceptions.ConnectTimeout:
                show_error('Connection Timeout')
            except exceptions.ConnectionError:
                show_error('Connection Error')
            except IOError as err:
                show_error(str(err))
        except Error as err:
            show_error(str(err))
        self.parentWidget().close()
