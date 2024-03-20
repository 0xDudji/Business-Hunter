# Business Hunter

**Overview**

Business Hunter leverages the Google Maps API to search for and report detailed information about businesses based on user-defined criteria. The output is an Excel file that includes the business name, place ID, rating, category, total ratings, address, whether it is permanently closed, phone number, Google Maps URL, last review timestamp, and the text of the last review. This tool is designed to assist in market research, competitor analysis, and general interest searches.

![image](https://github.com/skemil/Business-Hunter/assets/71653103/07e826f2-22df-43de-8e8b-c2323ff803a2)


![Business Hunter](https://github.com/skemil/Business-Hunter/assets/71653103/db4ffd23-cb25-4d4e-860b-4c08b08cddbc)


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

![image](https://github.com/skemil/Business-Hunter/assets/71653103/fa6de32e-e56b-4f41-aa80-053084b98784)


3. Navigate to the program's directory

![image](https://github.com/skemil/Business-Hunter/assets/71653103/88599a69-c67c-47f3-9b1c-5bf1f849b086)


4. Install dependencies
Before running Business Hunter, you need to install the necessary Python packages.

![image](https://github.com/skemil/Business-Hunter/assets/71653103/dcfe40ba-96d7-4a78-b971-273e509a5022)


This command will install all the required packages, including PyQt5, pandas, numpy, openpyxl, requests, and the Google Maps services Python library, ensuring that you have all the necessary components to run the application.

**Configuration**

Before using Business Hunter, you must obtain a Google Maps API key and configure the application to use this key. Insert your API key into the **API_KEY** variable within the script:

![image](https://github.com/skemil/Business-Hunter/assets/71653103/2a56317a-e219-4a0c-9370-ef6cb746145f)


Ensure that your Google Maps API key has access to the Places API, as this is crucial for the application to function correctly.

**Usage**

1. Launch the Application

Run the application with Python:

![image](https://github.com/skemil/Business-Hunter/assets/71653103/9e6a1b0b-973d-4209-b2dd-afa08c51421c)

2. Set Search Parameters

Use the graphical interface to input your search criteria, including location, distance, and any keywords relevant to the types of businesses you're interested in.

3. Start the Search

Click the "Search" button to initiate the search process. The application will then communicate with the Google Maps API and begin compiling the requested data.

4. View the Results

Once the search is complete, an Excel file named Leads.xlsx will be generated in the application's directory. This file contains all the gathered information, organized for easy analysis.
