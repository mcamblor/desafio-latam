from datetime import date
from datetime import datetime
import requests
import datetime
import os
import random

##
## Function helper to service
##
def validateDate(date_text):
    day,month,year = date_text.split('-')
    isValidDate = True
    try:
        datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        isValidDate = False

    return isValidDate

def daysMissing(date_text):
    day,month,year = date_text.split('-')
    t_day,t_month,t_year = date.today().strftime("%d-%m-%Y").split('-')
    t_date = date(int(t_year),int(t_month),int(t_day))
    b_date = date(int(t_year),int(month),int(day))
    birthday = date(t_date.year, int(month), int(day))
    if b_date > t_date:
        day_missing = 'Faltan {} días para tu cumpleaños'.format((birthday - t_date).days + 1)
    elif (birthday == t_date):
        #llamo al servicio de poemas
        try:
            url = 'https://www.poemist.com/api/v1/randompoems'
            response = requests.get(url)
            json_data = response.json()
            #print('consume api poemas')
            rand_poem = random.randrange(0,len(json_data))
            #print('Title: {}, Poem: {}'.format(json_data[rand_poem]['title'],json_data[rand_poem]['content']))
            day_missing = json_data[rand_poem]['content']
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            day_missing='Error Poem Api Timeout.'
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            day_missing='Error Poem Api TooManyRedirects.'
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            day_missing = 'Error Poem Api request. '+str(e)
    else:
        birthday = date(t_date.year+1, int(month), int(day))
        day_missing = 'Faltan {} días para tu cumpleaños'.format((birthday - t_date).days + 1)
        #day_missing = 'Tu cumpleaños ya paso'
    
    return day_missing

def changeFormatDate(date_text):
    oldformatdate = datetime.datetime.strptime(date_text,'%d-%m-%Y')
    newformatdate = oldformatdate.strftime('%d/%m/%y')
    return newformatdate

def calculate_age(born):
    today = date.today()
    born_day,born_month,born_year = born.split('-')
    return today.year - int(born_year) - ((today.month, today.day) < (int(born_month), int(born_day)))
