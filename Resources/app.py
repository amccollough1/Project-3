from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Create an instance of MongoClient
client = MongoClient(port=27017)

# Assign the databases to a variable name
db_comic = client['Marvel-Vs-DC-Comic']
db_movie = client['Marvel-Vs-DC-Movie']

# Assign collections to variables
comics_collection = db_comic['comics']
films_collection = db_movie['films']

@app.route('/static/index.html')
def character_count_over_time():
    data = request.get_json()
    start_year = int(data.get('start_year'))
    end_year = int(data.get('end_year'))
    universe = data.get('universe')
    alignment = data.get('alignment')

    # Perform MongoDB queries to get character counts over the specified time period
    # Implement the appropriate queries based on the provided parameters
    # For demonstration purposes, returning a static response
    years = list(range(start_year, end_year + 1))
    good_character_counts = [100, 120, 90]  # Sample counts for good characters
    bad_character_counts = [50, 60, 70]     # Sample counts for bad characters

    return jsonify({
        'years': years,
        'goodCharacterCounts': good_character_counts,
        'badCharacterCounts': bad_character_counts
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

@app.route('/api/dc_comics', methods=['GET'])
def get_dc_comics():
    dc_comics = list(comics_collection.find({"Universe": "DC"}))
    return jsonify(dc_comics)

@app.route('/api/marvel_comics', methods=['GET'])
def get_marvel_comics():
    marvel_comics = list(comics_collection.find({"Universe": "Marvel"}))
    return jsonify(marvel_comics)

@app.route('/api/dc_movies', methods=['GET'])
def get_dc_movies():
    dc_movies = list(films_collection.find({"entity": "DC"}))
    return jsonify(dc_movies)

@app.route('/api/marvel_movies', methods=['GET'])
def get_marvel_movies():
    marvel_movies = list(films_collection.find({"entity": "MARVEL"}))
    return jsonify(marvel_movies)

if __name__ == '__main__':
    app.run(debug=True, port=5000)