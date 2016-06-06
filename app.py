# Main routing file for mapping the webapp requests.

import flask
# import gmplot
import shutil
import sys

sys.path.append('data/')
from tfl_manager import TFLManager

app = flask.Flask(__name__)


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
"""

@app.route('/test')
def get_tube_map():
    _generate_html_map()
    return flask.render_template('mymap.html')


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
    user = {'nickname': 'Miguel'}  # fake user
    tfl_manager = TFLManager()
    return flask.render_template('test.html',
                                 stop_points=tfl_manager._stops_set)


if __name__ == "__main__":
    app.debug = True
    app.run()
