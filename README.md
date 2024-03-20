# Business Hunter

**Overview**

Business Hunter leverages the Google Maps API to search for and report detailed information about businesses based on user-defined criteria. The output is an Excel file that includes the business name, place ID, rating, category, total ratings, address, whether it is permanently closed, phone number, Google Maps URL, last review timestamp, and the text of the last review. This tool is designed to assist in market research, competitor analysis, and general interest searches.

**Features**

* Customizable search parameters including location, keywords, and search radius
* Detailed business information extracted and compiled into a user-friendly Excel format
* Utilizes Google Maps API for up-to-date and accurate business information
* Simple GUI for easy operation by users of all technical levels

**Prerequisites**

* Python 3.x
* Google Maps API key

**Installation**

1. Clone or download the repository
/git clone <repository-url>

2. Navigate to the program's directory
/cd Business Hunter

3. Install dependencies
Before running Business Hunter, you need to install the necessary Python packages.

/pip install -r requirements.txt

This command will install all the required packages, including PyQt5, pandas, numpy, openpyxl, requests, and the Google Maps services Python library, ensuring that you have all the necessary components to run the application.

**Configuration**

Before using Business Hunter, you must obtain a Google Maps API key and configure the application to use this key. Insert your API key into the **API_KEY** variable within the script:
/API_KEY = "Your_Google_Maps_API_Key_Here"

Ensure that your Google Maps API key has access to the Places API, as this is crucial for the application to function correctly.
