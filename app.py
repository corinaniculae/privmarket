# Main routing file for mapping the webapp requests.

from flask import Flask, render_template
app = Flask(__name__)


# Routing the webapp's main URL GET request.
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
