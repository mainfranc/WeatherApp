import requests
import time


class Wheather:
    def __init__(self,
                 app_id=None,
                 city_id=None,
                 city_name=None,
                 lat_coordinates=None,
                 lon_coordinates=None):
        self.app_id = app_id
        if city_id:
            self.city_id = city_id
        else:
            if city_name:
                self.city_id = self.get_city_id(city_name=city_name)
            else:
                self.city_id = self.get_city_id(lat_coordinates=lat_coordinates, lon_coordinates=lon_coordinates)
        self.data = None


    def get_city_id(self, city_name=None, lat_coordinates=None, lon_coordinates=None):
        if city_name:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city_name,
                                   'type': 'like',
                                   'units': 'metric',
                                   'lang': 'ru',
                                   'APPID': self.app_id},)
        else:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'lat': lat_coordinates,
                                       'lon': lon_coordinates,
                                       'type': 'like',
                                       'units': 'metric',
                                       'lang': 'ru',
                                       'APPID': self.app_id},)

        data = res.json()
        city_id = data['list'][0]['id']
        if isinstance(city_id, int):
            return city_id
        print(f"city {city_name} not found")
        return None

    def request_forecast(self):
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': self.city_id,
                                   # 'cnt': '5',
                                   'units': 'metric',
                                   'lang': 'ru',
                                   'APPID': self.app_id,
                                   },)
        self.data = res.json()

    def max_pressure(self):
        lst_pressures = {i['main']['pressure']: i['dt']  for i in self.data['list']}
        max_pres = max(lst_pressures.keys())
        return f'max pressure ({max_pres}) will be: {time.ctime(lst_pressures[max_pres])}'

    def min_difference(self):
        lst_days_temps = []
        for i in self.data['list']:
            curr_time = time.strptime(time.ctime(i['dt']))
            key_for_day = f'{curr_time.tm_mday}.{curr_time.tm_mon}'
            if not key_for_day in lst_days_temps:
                lst_days_temps.append(key_for_day)
        result_dict = {i: [0,0] for i in lst_days_temps[:4]}

        for i in self.data['list']:
            curr_time = time.strptime(time.ctime(i['dt']))
            key_for_day = f'{curr_time.tm_mday}.{curr_time.tm_mon}'
            if key_for_day in result_dict.keys():
                if int(curr_time.tm_hour) == 0:
                    result_dict[key_for_day][0] = i['main']['temp']
                if int(curr_time.tm_hour) == 12:
                    result_dict[key_for_day][1] = i['main']['temp']
                    result_dict[key_for_day] = round(abs(result_dict[key_for_day][1] - result_dict[key_for_day][0]), 2)
        lst_temp_diff = sorted(result_dict.items(), key=lambda x: x[1])
        return f'min temperature diff will be on {lst_temp_diff[0][0]} - {lst_temp_diff[0][1]}'


if __name__ == '__main__':
    W_id = '' # id gained after the registration on api.openweathermap.org
    forecast = Wheather(app_id=W_id, city_name='Moscow')
    forecast.request_forecast()
    print(forecast.max_pressure())
    print(forecast.min_difference())
