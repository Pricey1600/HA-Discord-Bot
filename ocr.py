import pytesseract
import re
import requests
from datetime import datetime

# Used to define tesseract location if not already in path
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

result = pytesseract.image_to_string('week_rota.jpg', lang='eng', config='--psm 6', output_type='string')
result_split = re.split('\s+', result)
print(result_split)

# get the home assistant webhook URL from secrets.txt (local, non-tracked file) 
with open('secrets.txt', 'r') as file:
    lines = file.readlines()
ha_webhook = lines[0].strip()

#print(result)

months = {'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'aug':'08', 'sept':'09', 'oct':'10', 'nov':'11', 'dec':'12'} #find the month number
todays_date = datetime.now()

#global formatting variables
shift = {}
day = ''
month = ''
year = ''
start_time = ''
end_time = ''

def reset_variables():
    global day, month, year, start_time, end_time, shift
    day = ''
    month = ''
    year = ''
    start_time = ''
    end_time = ''
    shift = {}

def format_shift():
    print("Formatting a shift")

    start_datetime = str(year)+'-'+month+'-'+day+' '+start_time
    end_datetime = str(year)+'-'+month+'-'+day+' '+end_time
    print(start_datetime)
    print(end_datetime)


    shift['start'] = str(datetime.strptime(start_datetime, '%Y-%m-%d %H:%M'))
    shift['end'] = str(datetime.strptime(end_datetime, '%Y-%m-%d %H:%M'))

def send_to_HA(shift):
    print("preparing to send to HA")
    payload = requests.post(ha_webhook, json = shift)

for x in result_split:
    
    if re.search("[0-9][0-9][:][0-9][0-9]", x):
        #print("Found a time")
        if start_time == '':
            start_time = x
        elif end_time == '':
            end_time = x
            #send shift set to be formatted
            format_shift()
            #send shift to HA
            send_to_HA(shift)
        else:
            print("ERROR: Both time variables are already populated")
    elif re.search("[0-3][0-9]", x):
        #print("Found a day")
        reset_variables()
        day = x

    elif re.search("[a-zA-Z][a-zA-Z][a-zA-Z]", x):
        month_found = False
        for m in months:
            if m in x.lower():
                #print("Found a month")
                month_found = True
                month = months[m]
                if (todays_date.month + int(month)) < (int(month)*2)-1:
                    print("Rota found for next year")
                    year = todays_date.year + 1
                else:
                    year = todays_date.year 
        if month_found == False:
            #print('didnt find a month')
            continue
    else:
        #print('didnt find either')
        continue