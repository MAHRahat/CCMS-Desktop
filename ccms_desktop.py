import sys
from sqlite3 import Error

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from src.ccms_main import CCMSMain
from src.dashboard import QDashboard
from src.db import db_create_connection, db_create_auth_table, db_select_auth_table

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    is_signed_in = False
    try:
        conn = db_create_connection()
        db_create_auth_table(conn)
        if db_select_auth_table(conn) is None:
            is_signed_in = False
        else:
            is_signed_in = True
        conn.close()
    except Error as err:
        print(str(err))
    if is_signed_in:
        widget.addWidget(QDashboard())
        widget.setMinimumSize(800, 600)
        widget.setMaximumSize(16777215, 16777215)
    else:
        widget.addWidget(CCMSMain())
        widget.setFixedSize(500, 550)
    fg = widget.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    fg.moveCenter(cp)
    widget.move(fg.topLeft())
    widget.show()
    sys.exit(app.exec())
