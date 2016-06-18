# Main routing file for mapping the webapp requests.

import flask
import sys
#import pysftp

sys.path.append('data/')
from tfl_manager import TFLManager
from mysql_manager import MySQLManager
from cryptdb_manager import CryptDBManager


app = flask.Flask(__name__)
tfl_manager = TFLManager()

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
    #sftp = pysftp.Connection('146.169.46.236', username='cn1612', password='Lala.2116')
    #test = sftp.pwd
    #sftp.close()
    #cryptdb_manager = CryptDBManager()
    #size = cryptdb_manager.count_size()
    return flask.render_template('test.html',
                                 stop_points=tfl_manager._stops_set,
                                 size="")


@app.route('/new_test')
def get_new_test():
    return flask.render_template('new_test.html')


@app.route('/templates/<file_name>')
def get_template_with_name(file_name):
    return flask.render_template(file_name + '.html')


@app.route('/possible_forms')
def get_possible_forms():
    return flask.render_template('possible_forms.html',
                                 stop_points=tfl_manager._stops_set)


@app.route('/issue_query1?lat=<lat>&lon=<lon>&timestamp=<timestamp>')
def issue_query_1():
    return


@app.route('/issue_query2?lat=<lat>&lon=<lon>&timestamp=<timestamp>')
def issue_query_2():
    return



if __name__ == "__main__":
    app.debug = True
    app.run()
