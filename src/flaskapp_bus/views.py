from flask import render_template, abort, request, redirect

from flaskapp_bus import app
from flaskapp_bus.bus_request import get_bus_list


@app.route('/bus/<num>')
def route_bus(num: str):
    bus_list = get_bus_list()
    for bus in bus_list:
        if bus['bus_num'] == num:
            return render_template('bus.html', Bus_stop_list=bus['bus_stop'])


@app.route('/')
@app.route('/bus_search')
def bus_search():
    return render_template('bus_search.html')


@app.route('/bus/detail', methods=['POST'])
def bus_detail():
    form_dict = request.form.to_dict()
    if 'bus_num' not in form_dict:
        return abort(400)

    bus_num: str = form_dict['bus_num']
    bus_list = get_bus_list()
    for bus in bus_list:
        if bus_num == bus['bus_num']:
            return redirect(f'/bus/{bus_num}')
    return abort(404)


