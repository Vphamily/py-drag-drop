from flask import Flask, redirect, render_template, request, session, url_for
import pandas as pd

app = Flask(__name__)

allowed_extensions = {'.csv'}
app.secret_key = 'loveithere'

@app.route('/')
def index():
    return render_template("index.html")

# upload route
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f:
            # use pandas to read put the csv to the dataframe
            df = pd.read_csv(f)
             # Convert to HTML and return as response
            data =  df.to_html(classes = 'data', header="true")
            session['data'] = data 
    return render_template('detail.html', data = session['data'])
    
# redirect route
@app.route('/back')
def back():
    return redirect(url_for('index'))

# redirect route sending the data from df to mysql database 
# modify if need to use other db
@app.route('/imports', methods=['POST', 'GET'])
def imports():

    return "import scucessfully"

if __name__ == '__main__':
    app.run()
