# Main routing file for mapping the webapp requests.

import flask
import gmplot
import shutil


app = flask.Flask(__name__)


# Routing the webapp's main URL GET request.
@app.route('/')
def index():
    return flask.render_template('index.html')


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


if __name__ == "__main__":
    app.debug = True
    app.run()
