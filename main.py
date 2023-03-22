from flask import Flask, redirect, render_template, request, session, url_for
import pandas as pd

app = Flask(__name__)

allowed_extensions = {'.csv'}
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f:
            df = pd.read_csv(f)
            # Do something with the dataframe here
             # Convert to HTML and return as response
            data =  df.to_html(classes = 'data', header="true")
    return render_template('detail.html', data = data)
    

# redirect route
@app.route('/back')
def back():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
