import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1171, 729)
        Dialog.setMaximumSize(QtCore.QSize(1171, 729))
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(110, 470, 171, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 560, 171, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(870, 560, 171, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(870, 470, 171, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(15, 11, 1141, 411))
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.tableWidget.horizontalHeader().setDefaultSectionSize(284)
        self.tableWidget.verticalHeader().setVisible(False)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(390, 642, 121, 61))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 640, 121, 61))
        self.pushButton_2.setObjectName("pushButton_2")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 450, 101, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 540, 101, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(870, 450, 101, 16))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(870, 540, 101, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.insert_data)
        self.pushButton_2.clicked.connect(self.delete_data)

        self.create_connection()
        self.load_data()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Student Number"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Student Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Level/Section"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Account Balance"))

        self.pushButton.setText(_translate("Dialog", "Insert"))
        self.pushButton_2.setText(_translate("Dialog", "Delete"))

        self.label.setText(_translate("Dialog", "Student Number:"))
        self.label_2.setText(_translate("Dialog", "Student Name:"))
        self.label_3.setText(_translate("Dialog", "Level/Section:"))
        self.label_4.setText(_translate("Dialog", "Account Balance:"))

    def create_connection(self):
        self.conn = sqlite3.connect("students.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, student_number TEXT, student_name TEXT, level_section TEXT, account_balance TEXT)"
        )
        self.conn.commit()

    def load_data(self):
        self.cur.execute("SELECT * FROM students")
        data = self.cur.fetchall()
        self.tableWidget.setRowCount(0)  # Clear existing rows
        for row_index, row_data in enumerate(data):
            self.tableWidget.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(col_data)))

    def insert_data(self):
        student_number = self.lineEdit.text()
        student_name = self.lineEdit_2.text()
        level_section = self.lineEdit_3.text()
        account_balance = self.lineEdit_4.text()

        self.cur.execute("INSERT INTO students (student_number, student_name, level_section, account_balance) VALUES (?, ?, ?, ?)",
                         (student_number, student_name, level_section, account_balance))
        self.conn.commit()

        self.load_data()  # Refresh the table after insertion

    def delete_data(self):
        selected_rows = set(index.row() for index in self.tableWidget.selectedIndexes())
        if selected_rows:
            for row in sorted(selected_rows, reverse=True):
                student_id = self.tableWidget.item(row, 0).text()
                self.cur.execute("DELETE FROM students WHERE id=?", (student_id,))
                self.conn.commit()
                self.tableWidget.removeRow(row)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
