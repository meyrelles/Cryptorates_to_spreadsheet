import requests
import time
from bs4 import BeautifulSoup

#google drive spreadsheet imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

i=0
j=4
cur_name = []
cur_short_name = []
cur_usd_val = []


theurl = "https://bitinfocharts.com/cryptocurrency-exchange-rates/"
thepage = requests.get(theurl)
soup = BeautifulSoup(thepage.text, 'html.parser')

table=soup.find('table', attrs={'class':'table table-bordered table-condensed ma-w2 abtb'})

for row in soup.select('tr.ptr td.hidden-phone.s6 span'):
    if (i==4):
        cur_short_name.append((soup.select('tr.ptr td.hidden-phone.s6 span')[i].text.strip()))
        j=4+7
    elif (i==j):
        cur_short_name.append((soup.select('tr.ptr td.hidden-phone.s6 span')[i].text.strip()))
        j=j+7
    i+=1

i=0
for row in soup.select('tr.ptr td span a'):
    try:
        cur_name.append(soup.select('tr.ptr td span a')[i].text.strip())
        cur_usd_val.append(soup.select('tr.ptr a.conv_cur')[i].text.strip())
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
for k in range(i):
    sheet.update_cell(k+2, 1, cur_name[k])
    sheet.update_cell(k+2, 2, cur_short_name[k])
    sheet.update_cell(k+2, 3, cur_usd_val[k])
