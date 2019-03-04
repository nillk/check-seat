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


class InterparkPlayInfo(object):
  def __init__(self, data):
    self.play_date = data['Playdate']
    self.play_seq = data['PlaySeq']
    self.play_time = data['PlayTime'].strip()
    self.play_time_value = data['PlayTimeValue']
    self.seat = True if data['SeatYN'] == 'Y' else False
    self.balance_seat = True if data['BalanceSeatYN'] == 'Y' else False
    self.online_date = data['OnlineDate']
    self.no_of_time = data['NoOfTime']
    self.cancelable_date = data['CancelableDate']

  def __str__(self):
    return f"play_date={self.play_date}, play_seq={self.play_seq}, play_time={self.play_time}, seat={self.seat}"


def interpark_check_seat():

  def get_play_info(session, play_date):
    def parse_response(response_json):
      return [InterparkPlayInfo(s) for s in response_json['JSON']]

    url = f"http://ticket.interpark.com/Ticket/Goods/GoodsInfoJSON.asp?Flag=PlaySeq&GoodsCode={goods_code}&PlaceCode=17000398&PlayDate={play_date}&Callback=parse_response"

    result = session.get(url)
    return eval(result.text[:-1])

  goods_code = '18011457'
  play_dates = ['20190305', '20190306', '20190307', '20190309',
                '20190310', '20190312', '20190313', '20190314', '20190316',
                '20190317', '20190319', '20190320', '20190321', '20190322', '20190323',
                '20190324', '20190326', '20190327', '20190328']

  session = requests.Session()
  session.headers.update({'referer': f"http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode={goods_code}"})

  play_infos = [get_play_info(session, date) for date in play_dates]
  seat_info = [info for list_info in play_infos for info in list_info if info.seat]
  print(seat_info)

if __name__ =='__main__':
  setInterval(interpark_check_seat, 30)
