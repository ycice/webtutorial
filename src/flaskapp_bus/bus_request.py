import requests
from bs4 import BeautifulSoup


def get_bus_list():
    bus_list = [
        {
            'bus_num': '101',
            'bus_id': '228000179',
            'bus_stop': []
        },
        {
            'bus_num': '343',
            'bus_id': '107000002',
            'bus_stop': []
        },
        {
            'bus_num': '15-1',
            'bus_id': '204000073',
            'bus_stop': []
        },
        {
            'bus_num': '1009',
            'bus_id': '234000310',
            'bus_stop': []
        },
        {
            'bus_num': '9007',
            'bus_id': '204000070',
            'bus_stop': []
        }
    ]

    for bus in bus_list:
        url = f'http://m.gbis.go.kr/search/getBusRouteDetail.do?routeId={bus["bus_id"]}&osInfoType=M'
        response = requests.post(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        stops_soup = soup.find_all('a')
        stops_soup = stops_soup[8:]
        for i in range(len(stops_soup)):
            stop_info = stops_soup[i].text.split()
            bus['bus_stop'].append(stop_info)
        print(1)
    return bus_list


if __name__ == '__main__':
    get_bus_list()