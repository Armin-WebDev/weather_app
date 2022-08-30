import requests
import time
import mysql.connector

def database_connect():
    mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="weather.db"
)
    cursor = mydb.cursor()

    return mydb,cursor

def create_table(mydb,cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS weather(weather TEXT, country TEXT ,  city TEXT, time TEXT)")
    mydb.commit()
    
def get_data_weather(city='Tehran',API_KEY='ff95c106f999bdd33317d19a8ac3543d'):

    res = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city,API_KEY))
    info = res.json()
    return info

def forcast(info):
    current_main_weather = info['weather'][0]['main']
    country = info['sys']['country']
    forcast_city = info['name']
    forcast_time = info['dt']
    yield current_main_weather
    yield country
    yield forcast_city
    yield time.ctime(float(forcast_time))

def insert_data(mydb,cursor,data):
    values=tuple(x for x in data)
    cursor.execute("INSERT INTO weather VALUES(%s , %s ,%s , %s)",values)
    mydb.commit()

mydb , cursor = database_connect()
create_table(mydb,cursor)

while True:
    data_weather = forcast(get_data_weather('london'))
    insert_data(mydb,cursor,data_weather)
    time.sleep(15)

