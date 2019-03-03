#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import ctypes
import threading
import time

def setInterval(func, time):
  e = threading.Event()
  while not e.wait(time):
    func()

def yes24_check_rest_seat():
  play_dates = ['2017-03-31', '2017-04-01', '2017-04-02']

  get_play_time_url = 'http://movie.yes24.com/AsyncRequest/getPlayTime.aspx'
  get_play_time_data = {'M_ID': 'M000023633', 'T_ID': 'T0740', 'modechk': 2}

  check_rest_seat_url = 'http://movie.yes24.com/DataService/DataService.aspx'
  check_rest_seat_data = {'PERSON': '1|0|0|0|0', 'FLAG': 'RESTSEAT'}

  for date in play_dates:
    get_play_time_data['PLAY_DT'] = date

    get_play_time_response = requests.get(get_play_time_url, data=get_play_time_data).json()
    pt_id = get_play_time_response[0][0]

    check_rest_seat_data['PT_ID'] = pt_id

    check_rest_seat_response = requests.get(check_rest_seat_url, data=check_rest_seat_data).text
    seat_info = check_rest_seat_response.split('INFO>')[1].replace('</', '')

    if seat_info == 'E0000':
      MessageBox = ctypes.windll.user32.MessageBoxW
      MessageBox(None, date, 'NOW!!!!!!!!!!!!!!!!', 0)
    else:
      print('{} {}'.format(date, seat_info))


if __name__ =='__main__':
  setInterval(yes24_check_rest_seat, 30)
