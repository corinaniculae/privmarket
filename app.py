# Main routing file for mapping the webapp requests.

import flask
import sys

sys.path.append('data/')
import query_agent
import tfl_manager


app = flask.Flask(__name__)
tfl_man = tfl_manager.TFLManager()
agent = query_agent.QueryAgent(tfl_man.get_all_tube_stops())


# Routing the webapp's main URL GET request.
@app.route('/')
def index():
    return flask.render_template('index.html')

"""
def _generate_html_map():
    gmap = gmplot.GoogleMapPlotter(51.4700, 0.4543, 10)
    gmap.plot([51.4988], [0.1749], 'cornflowerblue', edge_width=10)
    gmap.draw("mymap.html")
    shutil.move("./mymap.html",
                "./templates/mymap.html")


@app.route('/test')
def get_tube_map():
    _generate_html_map()
    return flask.render_template('mymap.html')
"""

@app.route('/ubicomp')
def get_ubicomp_map():
    return flask.render_template('ubicomp.html')


@app.route('/tfl')
def get_tfl_map():
    return 'ok, lets do this!'


@app.route('/query')
def get_query_page():
    return flask.render_template('query.html')


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


@app.route('/gettest')
def get_test():
    return flask.render_template('test.html',
                                 stop_points=tfl_man.get_all_tube_stops())


@app.route('/new_test')
def get_new_test():
    return flask.render_template('new_test.html')


@app.route('/templates/<file_name>')
def get_template_with_name(file_name):
    return flask.render_template(file_name + '.html')


@app.route('/possible_forms')
def get_possible_forms():
    return flask.render_template('possible_forms.html',
                                 stop_points=tfl_man.get_all_tube_stops())


@app.route('/get_syntactic_query_1', methods=['POST'])
def get_query_1():
    a1 = flask.request.form.get('a1')
    a2 = flask.request.form.get('a2')
    b1 = flask.request.form.get('b1')
    b2 = flask.request.form.get('b2')
    from_time = flask.request.form.get('from_time')
    to_time = flask.request.form.get('to_time')
    res = agent.get_syntactic_count_one_area(a1, a2, b1, b2, from_time, to_time)
    return ('a1: ' + str(a1) +
            '<br>a2: ' + str(a2) +
            '<br>b1: ' + str(b1) +
            '<br>b2: ' + str(b2) +
            '<br>from time: ' + from_time +
            '<br>to time: ' + str(to_time) +
            '<br><br> query: ' + res)


@app.route('/get_syntactic_query_2', methods=['POST'])
def get_query_2():
    a1 = flask.request.form.get('a1')
    a2 = flask.request.form.get('a2')
    b1 = flask.request.form.get('b1')
    b2 = flask.request.form.get('b2')
    c1 = flask.request.form.get('c1')
    c2 = flask.request.form.get('c2')
    d1 = flask.request.form.get('d1')
    d2 = flask.request.form.get('d2')
    coords = [a1, a2, b1, b2, c1, c2, d1, d2]
    from_time = flask.request.form.get('from_time')
    to_time = flask.request.form.get('to_time')
    res = agent.get_syntactic_count_two_areas(coords, from_time, to_time)
    return ('a1: ' + str(a1) +
            '<br>a2: ' + str(a2) +
            '<br>b1: ' + str(b1) +
            '<br>b2: ' + str(b2) +
            '<br>c1: ' + str(c1) +
            '<br>c2: ' + str(c2) +
            '<br>d1: ' + str(d1) +
            '<br>d2: ' + str(d2) +
            '<br>from time: ' + str(from_time) +
            '<br>to time: ' + str(to_time) +
            '<br><br> query: ' + res)


@app.route('/get_semantic_query_form_1')
def get_form_3():
    return flask.render_template('semantic_query_1.html',
                                 stop_points=tfl_man.get_all_tube_stops())


@app.route('/get_semantic_query_1', methods=['POST'])
def get_query_3():
    tube_stop = flask.request.form.get('select_one')
    from_time = flask.request.form.get('from_time')
    to_time = flask.request.form.get('to_time')
    res = agent.get_semantic_count_one_stop(tube_stop, from_time, to_time)
    return ('tube stop: ' + tube_stop +
            '<br>from time: ' + str(from_time) +
            '<br>to time: ' + str(to_time) +
            '<br><br>query: ' + res)


@app.route('/get_semantic_query_form_2')
def get_form_4():
    return flask.render_template('semantic_query_2.html',
                                 stop_points=tfl_man.get_all_tube_stops())


@app.route('/get_syntactic_query_form_1')
def get_form_1():
    return flask.render_template('syntactic_query_1.html')


@app.route('/get_syntactic_query_form_2')
def get_form_2():
    return flask.render_template('syntactic_query_2.html')


@app.route('/get_semantic_query_2', methods=['POST'])
def get_query_4():
    from_tube_stop = flask.request.form.get('select_from')
    to_tube_stop = flask.request.form.get('select_to')
    from_time = flask.request.form.get('from_time')
    to_time = flask.request.form.get('to_time')
    res = agent.get_semantic_count_two_stops(from_tube_stop, to_tube_stop, from_time, to_time)
    return ('from tube stop: ' + from_tube_stop +
            '<br>to tube stop: ' + to_tube_stop +
            '<br>from time: ' + str(from_time) +
            '<br>to time: ' + str(to_time) +
            '<br><br>query: ' + res)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
