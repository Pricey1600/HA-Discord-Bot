import pytesseract
import re
import requests
import time
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


result = pytesseract.image_to_string('week_rota.jpg', lang='eng', config='--psm 6', output_type='string')
result_split = re.split('\s+', result)
print(result_split)
ha_webhook = 'https://homeassistant.priceyserver.net/api/webhook/rota'

#print(result)

months = {'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'aug':'08', 'sept':'09', 'oct':'10', 'nov':'11', 'dec':'12'}
todays_date = datetime.now()

shift = {}
day = ''
month = ''
year = ''
date = ''
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
    #print(payload.text)

for x in result_split:
    
    if re.search("[0-9][0-9][:][0-9][0-9]", x):
        print("Found a time")
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
        print("Found a day")
        reset_variables()
        day = x

    elif re.search("[a-zA-Z][a-zA-Z][a-zA-Z]", x):
        month_found = False
        for m in months:
            if m in x.lower():
                print("Found a month")
                month_found = True
                month = months[m]
                #print(todays_date.month + int('08'))
                if (todays_date.month + int(month)) < (int(month)*2)-1:
                    print("Rota found for next year")
                    year = todays_date.year + 1
                else:
                    year = todays_date.year 
        if month_found == False:
            print('didnt find a month')
    else:
        print('didnt find either')


    # if its the date we're looking at:
    # if re.findall("[0-3][0-9][ ][a-zA-Z][a-zA-Z][a-zA-Z]", x):
    #     #dates.append(x)
    #     shift = {}
    #     start_time = ''

    #     split_date = x.split(" ")

    #     for m in months:
    #         if m in split_date[1].lower():
    #             month_number = months[split_date[1].lower()]

    #     todays_date = datetime.now()
    #     shift_date = '2024'+'-'+month_number+'-'+split_date[0]
    #     shift_datetime = shift_date+' 00:00:00'

    #     if abs(todays_date.month - datetime.strptime(shift_datetime, '%Y-%m-%d %H:%M:%S').month) > 1: # make sure its not just a rota that covers the end of one month and the start of another
    #         #print('THATS NEXT YEAR')
    #         year = str(todays_date.year+1)
    #         shift_date = year+'-'+'-'+month_number+'-'+split_date[0]


    # # if its the time we're looking at:
    # elif re.findall("[0-3][0-9]", x):
    #     #times.append(x)
    #     if start_time == '':
    #         start_time = x
    #         if "." in start_time:
    #             start_time = start_time.replace(".", ":")
    #     else:
    #         end_time = x
    #         if "." in end_time:
    #             end_time = end_time.replace(".", ":")
            
    #         start_datetime = shift_date+' '+start_time
    #         end_datetime = shift_date+' '+end_time

    #         shift['start'] = str(datetime.strptime(start_datetime, '%Y-%m-%d %H:%M'))
    #         shift['end'] = str(datetime.strptime(end_datetime, '%Y-%m-%d %H:%M'))

    #         send_to_HA(shift)
    #         time.sleep(3)



