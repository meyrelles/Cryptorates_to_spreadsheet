import requests
import time
from bs4 import BeautifulSoup

#google drive spreadsheet imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

#Time functions
import schedule
import time

i=0
j=k=4
cur_name = []
cur_short_name = []
cur_usd_val = []
cur_fiat_name = []
cur_fiat_val = []

def Fiatrate():
    theurl = "http://x-rates.com/table/?from=USD&amount=1"
    thepage = requests.get(theurl)
    soup = BeautifulSoup(thepage.text, 'html.parser')
    k=0
    i=0

    cur_fiat_name.append('USD')
    cur_fiat_val.append('1')
    for row in soup.select('table.ratesTable tbody tr'):
        #Update names
        if (i==0):
            cur_fiat_name.append((soup.select('table.ratesTable tbody tr td')[i].text.strip()))
            j=3
        elif (i==j):
            cur_fiat_name.append((soup.select('table.ratesTable tbody tr td')[i].text.strip()))
            j=j+3
            
        #update values
        if (i==0):
            cur_fiat_val.append((soup.select('table.ratesTable tbody tr a')[i].text.strip()))
            k=2
        elif (i==k):
            cur_fiat_val.append((soup.select('table.ratesTable tbody tr a')[i].text.strip()))
            k=k+2
        i+=1

    #exchenge '.' with ','
    for i, val in enumerate(cur_fiat_val):
        cur_fiat_val[i]=cur_fiat_val[i].replace(".",",")

    #send data to google spreadsheet
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("cryptorates").worksheet('FiatRates')

    start_row = 2
    start_list = 'A'
    end_list = 'A'

    #Update currency name
    end_row=start_row + len(cur_fiat_name) - 1

    cell_list = sheet.range("%s%d:%s%d" % ('A', start_row, 'A', end_row))

    for i, val in enumerate(cur_fiat_name):
        cell_list[i].value = val

    sheet.update_cells(cell_list)

    #Update currency short name
    end_row=start_row + len(cur_fiat_val) - 1

    cell_list = sheet.range("%s%d:%s%d" % ('C', start_row, 'C', end_row))

    for i, val in enumerate(cur_fiat_val):
        cell_list[i].value = val

    sheet.update_cells(cell_list)

    cur_fiat_name.clear()
    cur_fiat_val.clear()



def Cryptorate():
    theurl = "https://bitinfocharts.com/cryptocurrency-exchange-rates/"
    thepage = requests.get(theurl)
    soup = BeautifulSoup(thepage.text, 'html.parser')

    table=soup.find('table', attrs={'class':'table table-bordered table-condensed ma-w2 abtb'})
    i=0
    j=0
    for row in soup.select('tr.ptr td.hidden-phone.s6 span'):
        if (i==4):
            cur_short_name.append((soup.select('tr.ptr td.hidden-phone.s6 span')[i].text.strip()))
            j=4+7
        elif (i==j):
            cur_short_name.append((soup.select('tr.ptr td.hidden-phone.s6 span')[i].text.strip()))
            j=j+7
        i+=1

    i=0

    try:
        cur_short_name.remove('1')
    except ValueError:
        print("No number 1")
        
    for row in soup.select('tr.ptr td span a'):
        try:
            cur_name.append(soup.select('tr.ptr td span a')[i].text.strip())
            cur_usd_val.append(soup.select('tr.ptr a.conv_cur')[i].text.strip())
            cur_usd_val[i]=cur_usd_val[i].replace('$ ','')
            cur_usd_val[i]=cur_usd_val[i].replace(',','')
            cur_usd_val[i]=cur_usd_val[i].replace('.',',')
            #print(soup.select('tr.ptr td span a')[i].text.strip() + ': ' + soup.select('tr.ptr a.conv_cur')[i].text.strip())
            i+=1
        except ValueError:
            print("END OF LIST")

    #send data to google spreadsheet

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)


    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("cryptorates").sheet1



    # Extract and print all of the values
    #list_of_hashes = sheet.get_all_records()
    #print(list_of_hashes)

    #write to spreadsheet
    start_row = 2
    start_list = 'A'
    end_list = 'A'

    #Update currency name
    end_row=start_row + len(cur_name) - 1

    cell_list = sheet.range("%s%d:%s%d" % ('A', start_row, 'A', end_row))

    for i, val in enumerate(cur_name):
        cell_list[i].value = val

    sheet.update_cells(cell_list)

    #Update currency short name
    end_row=start_row + len(cur_short_name) - 1

    cell_list = sheet.range("%s%d:%s%d" % ('B', start_row, 'B', end_row))

    for i, val in enumerate(cur_short_name):
        cell_list[i].value = val

    sheet.update_cells(cell_list)

    #Update currency rate
    end_row=start_row + len(cur_usd_val) - 1

    cell_list = sheet.range("%s%d:%s%d" % ('C', start_row, 'C', end_row))

    for i, val in enumerate(cur_usd_val):
        cell_list[i].value = val

    sheet.update_cells(cell_list)


    cur_name.clear()
    cur_short_name.clear()
    cur_usd_val.clear()

    print("AGAIN")


schedule.every(1).minutes.do(Cryptorate)
schedule.every(1).minutes.do(Fiatrate)


while 1:
    schedule.run_pending()
    time.sleep(1)
"""
Cryptorate()
Fiatrate()
"""
