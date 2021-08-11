from PyQt5.QtWidgets import QMessageBox


def show_my_msg(icon, title, text):
    """
    Creates and displays a QMessageBox dialog.
    :param icon: icon to be used for the dialog
    :param title: title of the dialog
    :param text: text of the dialog
    :return: None
    """
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()


def show_error(text):
    """
    Used to show error message by calling show_my_msg function with necessary parameters.
    :param text: text to be displayed
    :return: None
    """
    show_my_msg(QMessageBox.Critical, "Error", text)


def show_success(text):
    """
    Used to show success message by calling show_my_msg function with necessary parameters.
    :param text: text to be displayed
    :return: None
    """
    show_my_msg(QMessageBox.Information, "Success", text)
