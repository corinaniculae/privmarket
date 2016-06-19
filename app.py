# Main routing file for mapping the webapp requests.

import flask
import sys
#import pysftp

sys.path.append('data/')
import query_agent
import tfl_manager


app = flask.Flask(__name__)
tfl_man = tfl_manager.TFLManager()
#agent = query_agent.QueryAgent(tfl_man.get_all_tube_stops())


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
    print 'does this get requested?'
    a1 = flask.request.form.get('a1')
    a2 = flask.request.form.get('a2')
    b1 = flask.request.form.get('b1')
    b2 = flask.request.form.get('b2')
    from_time = flask.request.form.get('from_time')
    to_time = flask.request.form.get('to_time')
    return ('a1: ' + str(a1) +
            '\na2: ' + str(a2) +
            '\nb1: ' + str(b1) +
            '\nb2: ' + str(b2) +
            '\nfrom time: ' + str(from_time) +
            '\nto time: ' + str(to_time))


@app.route('/issue_query1?lat=<lat>&lon=<lon>&timestamp=<timestamp>')
def issue_query_1():
    return


@app.route('/issue_query2?lat=<lat>&lon=<lon>&timestamp=<timestamp>')
def issue_query_2():
    return


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
