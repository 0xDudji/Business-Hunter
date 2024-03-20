import googlemaps
import requests
import pandas as pd 
import time
import numpy as np
import datetime
import sys
import os
import openpyxl
from openpyxl.worksheet.table import TableStyleInfo
from openpyxl.styles import NamedStyle
from PyQt5 import QtWidgets
import threading
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5 import QtCore, QtGui, QtWidgets

API_KEY = "AIzaSyBBkt_RLHW-qx70M2ERdyyYtbq4I8cXaD4"

address = ""
distance = 0
search_string = []
reviewfilter = ""
norevs = False
n = 0

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = resource_path("Logo.png")

## Lat/Long Gathering
def getLatLng(address):
   latlongPayload = {'key': API_KEY, 'query': address, 'fields': "lat,lng"}
   longlat = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?", params=latlongPayload)
   try:
      lat = longlat.json()['results'][0]['geometry']['location']['lat']
      lng = longlat.json()['results'][0]['geometry']['location']['lng']
      return str(lat) + "," + str(lng)
   ## Catch errors
   except (IndexError, UnboundLocalError):
         pass

## PlaceID Gathering
def getPlaceIDs(address):
    nearbyPayload = {
        'key': API_KEY,
        'location': getLatLng(address),
        'radius': distance,
        'keyword': search_string
    }
    nearbyReq = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?", params=nearbyPayload)
    nearbysearches = nearbyReq.json()['results']
    placeIDList = []

    # Iterate through JSON and add place_ids to list
    for place in nearbysearches:
        placeIDList.append(place['place_id'])

    return placeIDList

## Generate a list of nearby phone numbers using the list of place IDs from getPlaceIDs()
def makePhoneNumberList():
    phoneNumsList = []
    for i in getPlaceIDs(address):
        placeIDpayload = {'key': API_KEY, 'place_id': i, 'fields': "formatted_phone_number"}
        phoneQuery = requests.get('https://maps.googleapis.com/maps/api/place/details/json?', params=placeIDpayload)
        phoneNumbs = phoneQuery.json()['result']
        phoneNumsList.append({"place_id": i, "phone_number": phoneNumbs.get("formatted_phone_number")})
    return phoneNumsList

def main():
    

    total_progress = 100  # Total progress steps
    current_progress = 0  # Current progress
    # Function to update the progress bar
    def update_progress_bar():
        nonlocal current_progress


    # Start a separate thread for updating the progress bar
    progress_thread = threading.Thread(target=update_progress_bar)
    progress_thread.start()
    
    # Increment the progress by a certain amount
    def increment_progress(amount):
        nonlocal current_progress
        current_progress += amount
        update_progress(current_progress)

    increment_progress(100000000)
    if address is not None:
        tempPhoneList = makePhoneNumberList()
    increment_progress(100000000)
    map_client = googlemaps.Client(API_KEY)
    location = getLatLng(address)
    business_list = []
   
    for keyword in search_string:
        response = map_client.places_nearby(
            location=location,
            keyword=keyword,
            name=keyword,
            radius=distance
        )
        
        business_list.extend(response.get('results', []))
        next_page_token = response.get('next_page_token')
        
        while next_page_token:
            time.sleep(2)
            response = map_client.places_nearby(
                location=location,
                keyword=keyword,
                name=keyword,
                radius=distance,
                page_token=next_page_token
            )
            business_list.extend(response.get('results', []))
            next_page_token = response.get('next_page_token')
    increment_progress(100000000)
    df = pd.DataFrame(business_list)
    phone_numbers = [np.nan] * len(df)

    for i, phone_info in enumerate(tempPhoneList):
        place_id = phone_info["place_id"]
        phone_number = phone_info["phone_number"]
        if place_id in df['place_id'].values:
            idx = df.index[df['place_id'] == place_id][0]
            phone_numbers[idx] = phone_number
    df['Phone number'] = phone_numbers
    df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']
    df.drop(['icon', 'scope', 'icon_background_color', 'icon_mask_base_uri', 'geometry', 'photos', 'plus_code', 'reference', 'business_status', "opening_hours"], axis=1, inplace=True)



    increment_progress(100000000)
    # Create empty lists to store review information
    last_review_times = []
    last_review_timestamps = []
    last_review_texts = []

    # Retrieve the last review from the API response
    for i in range(len(df)):
        place_id = df.loc[i, 'place_id']
        details_payload = {'key': API_KEY, 'place_id': place_id, 'fields': 'reviews'}
        details_response = requests.get('https://maps.googleapis.com/maps/api/place/details/json?', params=details_payload)
        resp_details = details_response.json()

        # Check if reviews exist for the place
        if 'reviews' in resp_details['result']:
            reviews = resp_details['result']['reviews']

            # Check if there is at least one review
            if len(reviews) > 0:
                last_review = reviews[-1]  # Get the last review

                # Extract the information of the last review
                last_review_time = last_review['relative_time_description']
                last_review_timestamp = last_review['time']
                last_review_text = last_review['text']

                # Append the last review information to the respective lists
                last_review_times.append(last_review_time)
                last_review_timestamps.append(last_review_timestamp)
                last_review_texts.append(last_review_text)
            else:
                # If no reviews, append None values
                last_review_times.append(None)
                last_review_timestamps.append(None)
                last_review_texts.append(None)
        else:
            # If no reviews, append None values
            last_review_times.append(None)
            last_review_timestamps.append(None)
            last_review_texts.append(None)
    increment_progress(100000000)
    # Add the last review information as new columns in the DataFrame
    df['Last Review Time'] = last_review_times
    df['Last Review Timestamp'] = last_review_timestamps
    df['Last Review Text'] = last_review_texts
    df['Last Review Timestamp'].fillna(0, inplace=True)
    df['Last Review Text'].fillna("None", inplace=True)
    df['Last Review Timestamp'] = df['Last Review Timestamp'].apply(lambda ts: datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y"))
    df['Last Review Timestamp'].replace("01-01-1970", "No reviews", inplace=True)
    df.rename(columns={"Last Review Text":"Last Review","place_id":"Place ID", "name":"Name","rating":"Rating","types":"Category","user_ratings_total":"Total Ratings","vicinity":"Address"}, inplace=True)
    df['Last Review'].replace("", "None", inplace=True)
    # Save the DataFrame to Excel with adjusted column widths
    df.fillna("None", inplace=True)
    writer = pd.ExcelWriter("Leads.xlsx", engine="openpyxl")
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    increment_progress(100000000)
    # Adjust column widths
    workbook = writer.book
    worksheet = workbook["Sheet1"]
    increment_progress(100000000)
    for column in worksheet.columns:
        max_length = 0
        column_name = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except TypeError:
                pass
        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column_name].width = adjusted_width
    increment_progress(100000000)
    # Create a NamedStyle for the table
    table_style = NamedStyle(name="PurpleMediumTableStyle19")
    table_style.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium19", showFirstColumn=False, showLastColumn=False,
        showRowStripes=True, showColumnStripes=False
    )

    # Add a table to the worksheet
    table = openpyxl.worksheet.table.Table(
        displayName="Table1", ref=worksheet.dimensions, tableStyleInfo=table_style.tableStyleInfo
    )
    worksheet.add_table(table)
    
    # Rename the sheet to "Leads"
    worksheet.title = "Leads"

    increment_progress(100000000) 
    if norevs == False:
        df = df.dropna(subset=['Last Review Time'])

    # df['Last Review Timestamp'] = pd.to_datetime(df['Last Review Timestamp'], format='%d-%m-%Y')
    # df = df[df['Last Review Timestamp'] >= reviewfilter]
    



    increment_progress(99999999)
    # Save the workbook
    workbook.save(filename="Leads.xlsx")
    workbook.close()
    progress_thread.join()

class Worker(QObject):
    finished = pyqtSignal()

    def run_main(self):
        global address, distance, search_string, reviewfilter, norevs

        address = ui.locationfield.toPlainText()
        distance = int(ui.distancefield.toPlainText()) * 1000
        search_string = ui.keywordsfield.toPlainText().split(',')
        search_string = [s.strip() for s in search_string]
        reviewfilter = ui.dateEdit.date().toString("dd-MM-yyyy")

        # Check the state of the checkbox
        if ui.checkBox.isChecked():
            norevs = True
        else:
            norevs = False

        main()
        self.finished.emit()

def update_progress(progress):
        ui.progressBar.setValue(progress)
        QtWidgets.QApplication.processEvents()


def start_main():
    worker = Worker()
    worker.finished.connect(stop_progress)
    thread = threading.Thread(target=worker.run_main)
    thread.start()
    
def stop_progress():
    ui.progressBar.setEnabled(False)
    # Show a message box to indicate that the search is done
    QtWidgets.QMessageBox.information(MainWindow, "Skemil Business Hunter", "Search is complete!")  # Disable the progress bar

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global n
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(344, 489)
        MainWindow.setFixedSize(344, 489)
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Logo), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(10, 390, 321, 41))
        self.button1.clicked.connect(self.start_search)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.button1.setFont(font)
        self.button1.setObjectName("button1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 68, 19))
        self.label.setObjectName("label")
        self.keywordsfield = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.keywordsfield.setGeometry(QtCore.QRect(10, 90, 321, 31))
        self.keywordsfield.setObjectName("keywordsfield")
        self.keywordsfield.setTabChangesFocus(True)
        self.locationfield = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.locationfield.setGeometry(QtCore.QRect(10, 160, 321, 31))
        self.locationfield.setObjectName("locationfield")
        self.locationfield.setTabChangesFocus(True)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 111, 19))
        self.label_2.setObjectName("label_2")
        self.distancefield = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.distancefield.setGeometry(QtCore.QRect(10, 230, 321, 31))
        self.distancefield.setObjectName("distancefield")
        self.distancefield.setTabChangesFocus(True)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 200, 141, 19))
        self.label_3.setObjectName("label_3")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(False)
        self.progressBar.setGeometry(QtCore.QRect(10, 440, 321, 21))
        self.progressBar.setAcceptDrops(False)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setMaximum(1000000000)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(10, 350, 291, 20))
        self.checkBox.setObjectName("checkBox")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(10, 310, 321, 22))
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2023, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setMaximumDate(QtCore.QDate(9999, 12, 31))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 280, 141, 19))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(0, 0, 351, 51))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(""))
        self.label_5.setObjectName("label_5")

        


        MainWindow.setCentralWidget(self.centralwidget)
    
       # Set tab order
        self.keywordsfield.setFocus()
        QtWidgets.QWidget.setTabOrder(self.keywordsfield, self.locationfield)
        QtWidgets.QWidget.setTabOrder(self.locationfield, self.distancefield)
        QtWidgets.QWidget.setTabOrder(self.distancefield, self.dateEdit)
        QtWidgets.QWidget.setTabOrder(self.dateEdit, self.checkBox)
        QtWidgets.QWidget.setTabOrder(self.checkBox, self.button1)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 344, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

    def start_search(self):
        self.progressBar.setEnabled(True)  # Enable the progress bar
        self.progressBar.setValue(0)  # Reset the progress bar value to 0

        # Start the main code execution in a separate thread
        start_main() 

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Skemil Business Hunter"))
        self.button1.setText(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "Keywords"))
        self.label_2.setText(_translate("MainWindow", "Location"))
        self.label_3.setText(_translate("MainWindow", "Distance (in km)"))
        self.checkBox.setText(_translate("MainWindow", "Include businesses without reviews"))
        self.label_4.setText(_translate("MainWindow", "Date of last review"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


