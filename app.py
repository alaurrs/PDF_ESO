from flask import Flask, render_template, request
from fileinput import filename
import plotly.graph_objects as go
import plotly
from test import extract_information
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        fig = extract_information(f.filename)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template("acknowledgement.html", graphJSON = graphJSON,name = f.filename)  




if __name__ == "__main__":
    app.run(host = '0.0.0.0',
            debug=True,
            port=8080)