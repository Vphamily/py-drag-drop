from flask import Flask, redirect, render_template, request, session, url_for
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

app = Flask(__name__)

allowed_extensions = {'.csv'}
app.secret_key = 'loveithere'


def generate_visualizations(df):
    """Generate various visualizations based on dataframe content"""
    visualizations = {}

    # Get numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    # 1. Basic statistics
    visualizations['stats'] = df.describe().to_html(classes='table table-striped')

    # 2. Bar chart for categorical columns (if any)
    if len(categorical_cols) > 0:
        sample_cat_col = categorical_cols[0]
        fig = px.bar(df[sample_cat_col].value_counts())
        visualizations['bar_chart'] = json.loads(fig.to_json())

    # 3. Histogram for numeric columns (if any)
    if len(numeric_cols) > 0:
        sample_num_col = numeric_cols[0]
        fig = px.histogram(df, x=sample_num_col)
        visualizations['histogram'] = json.loads(fig.to_json())

    # 4. Scatter plot if we have at least 2 numeric columns
    if len(numeric_cols) >= 2:
        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])
        visualizations['scatter'] = json.loads(fig.to_json())

    # 5. Box plots for numeric columns
    if len(numeric_cols) > 0:
        fig = go.Figure()
        for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
            fig.add_trace(go.Box(y=df[col], name=col))
        visualizations['boxplot'] = json.loads(fig.to_json())

    return visualizations


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f:
            try:
                # Read the CSV file
                df = pd.read_csv(f)

                # Store DataFrame in session as HTML
                session['data'] = df.to_html(classes='table table-striped', header="true")

                # Store raw data in session for visualization
                session['raw_data'] = df.to_dict('records')

                return render_template('detail.html', data=session['data'])
            except Exception as e:
                return f"Error processing file: {str(e)}", 400

    return render_template('detail.html')


@app.route('/viz')
def visualize():
    if 'raw_data' not in session:
        return redirect(url_for('index'))

    # Reconstruct DataFrame from session data
    df = pd.DataFrame(session['raw_data'])

    # Generate visualizations
    visualizations = generate_visualizations(df)

    return render_template('visualize.html',
                           visualizations=visualizations,
                           data=session['data'])


@app.route('/back')
def back():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)