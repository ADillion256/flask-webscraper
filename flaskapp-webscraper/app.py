"""Flask Web App for Web Scraping Data Project"""
import os
import json
from flask import Flask, render_template, jsonify
from scraper import scrape



# Defining the Flask app
app = Flask('__name__')

# Route for the root directory / main page
@app.route('/')
def home():
    """Renders basic homepage"""
    return render_template('index.html')


@app.route('/about')
def about():
    """Creates the about page"""
    return render_template('about.html')

@app.route('/api/data')
def api_data():
    """Returns webscraper data as JSON"""
    file_path = os.path.join(os.getcwd(), 'data.json')

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
            return jsonify({'data': data})
        except FileNotFoundError:
            return jsonify({'error': 'File not found. Visit /scraper first.'}), 404


    url = 'https://en.wikipedia.org/wiki/List_of_Spotify_streaming_records'
    scrape_result = scrape(url)

    if 'error' in scrape_result:
        return jsonify({'error': scrape_result['error']}), 500

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify({"data": data})
    except FileNotFoundError:
        return jsonify({"ERROR: File not found. Please run scraper."}), 404


@app.route('/scrape')
def scrape_data():
    """Runs the scraper and returns and displays the results via /api/data"""
    url = 'https://en.wikipedia.org/wiki/List_of_Spotify_streaming_records'
    scrape_result = scrape(url)
    if 'error' in scrape_result:
        return jsonify({'error': scrape_result['error']}), 500
    return jsonify({'message': 'Scraping finished, pleasevisit /api/data for results.'})



if __name__ == '__main__':
    app.run(debug=True)
