import io
import string
import base64
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, request, jsonify, render_template, send_file
from pymongo import MongoClient
from statistics import mean, median, mode
from bson import regex, ObjectId
from bson.json_util import dumps
from collections import defaultdict

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['Marvel-Vs-DC-Comic']
dbb = client['Marvel-Vs-DC-Movie']
comic_collection = db['comics']
movie_collection = dbb['Marvel-Vs-DC-Movie']

@app.route('/')
def home():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Marvel-Vs-DC-Comic']
        comic_collection = db['comics']
        print("Connected to MongoDB successfully")
    except Exception as e:
        print("Error connecting to MongoDB:", str(e))
    
    return render_template('index.html')

@app.route('/q1.html', methods=['GET'])
def q1_page():
    return render_template('q1.html')

@app.route('/distinct_characters', methods=['GET'])
def distinct_characters():
    try:
        # Retrieve the 'appearances' parameter from the query string
        appearances_param = request.args.get('appearances', type=int)

        # Define the aggregation pipeline based on the 'appearances' parameter
        pipeline = [
            {"$group": {"_id": "$Name", "Alignment": {"$first": "$Alignment"}, "Appearances": {"$first": "$Appearances"}}}
        ]

        if appearances_param is not None:
            # Filter characters based on appearances
            pipeline.append({"$match": {"Appearances": {"$gte": appearances_param}}})

        distinct_character_data = list(db.comics.aggregate(pipeline))

        # Convert ObjectId to string and handle Infinity
        for item in distinct_character_data:
            item['_id'] = str(item['_id']) if not isinstance(item['_id'], float) else str(item['_id'])

        # Prepare the response in a JSON format
        response_data = [{'name': item['_id'], 'alignment': item['Alignment'], 'appearances': item.get('Appearances', 0)} for item in distinct_character_data]

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/character_search', methods=['GET'])
def character_search_api():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Marvel-Vs-DC-Comic']
        comic_collection = db['comics']
        print("Connected to MongoDB successfully")
    except Exception as e:
        print("Error connecting to MongoDB:", str(e))

    character_name = request.args.get('character_name')

    # Adjust the character_name to be case-insensitive and within quotes
    # Example: If character_name is "Batman", transform it to case-insensitive regex "/Batman/i"
    character_name_query = regex.Regex(f".*{character_name}.*", "i")

    # Search for all instances of the character using a case-insensitive regex search
    character_data = list(db.comics.find({'Name': character_name_query}))

    if character_data:
        # Convert the ObjectId to a string for JSON serialization for each character
        for char in character_data:
            char['_id'] = str(char['_id'])
        return dumps(character_data), 200
    else:
        return jsonify({'error': 'Character not found'}), 404
  
@app.route('/q2.html', methods=['GET'])
def q2_page():
    return render_template('q2.html')

@app.route('/q3.html', methods=['GET'])
def q3_page():
    return render_template('q3.html')
  
@app.route('/search_movies', methods=['GET'])
def search_movies():
    try:
        # Retrieve the hero name from the query string
        hero_name = request.args.get('hero_name', '')

        # Perform a MongoDB query to find movie titles containing the hero name
        query = {"title": {"$regex": f".*{hero_name}.*", "$options": "i"}}  # Case-insensitive search
        movies = list(dbb.films.find(query, {"title": 1}))

        # Extract movie titles from the query result
        movie_titles = [movie['title'] for movie in movies]

        # Prepare the response in a JSON format
        response_data = {"movies_containing_hero": movie_titles}

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
  
# Endpoint to get MPA rating performance
@app.route('/q4.html', methods=['GET'])
def q4_page():
    generate_chart()  # Use the correct function name here
    return render_template('q4.html', chart_image='static/matplotlib_chart.png')
        
@app.route('/generate_chart', methods=['GET'])
def generate_chart():
    try:
        mpa_rating1 = request.args.get('mpa_rating1')
        mpa_rating2 = request.args.get('mpa_rating2')

        # Retrieve data from MongoDB for the selected MPA ratings
        cursor1 = dbb.films.find({'mpa_rating': mpa_rating1})
        cursor2 = dbb.films.find({'mpa_rating': mpa_rating2})

        # Aggregate incomes for each MPA rating
        mpa1_incomes = [float(document['imdb_gross'].replace('$', '').replace(',', '')) for document in cursor1]
        mpa2_incomes = [float(document['imdb_gross'].replace('$', '').replace(',', '')) for document in cursor2]

        # Calculate sum total for IMDb gross
        sum_total_mpa1 = round(sum(mpa1_incomes), 2)
        sum_total_mpa2 = round(sum(mpa2_incomes), 2)
        
        # Prepare chart data
        labels = ['Sum Total Gross Income']
        values1 = [sum_total_mpa1]
        values2 = [sum_total_mpa2]

        chart_data = {
            'labels': labels,
            'values1': values1,
            'values2': values2
        }

        # Calculate mean, median, and mode for IMDb rating
        cursor1_imdb = dbb.films.find({'mpa_rating': mpa_rating1, 'imdb_rating': {'$ne': ''}})
        cursor2_imdb = dbb.films.find({'mpa_rating': mpa_rating2, 'imdb_rating': {'$ne': ''}})
        imdb_ratings_mpa1 = [float(document['imdb_rating']) for document in cursor1_imdb]
        imdb_ratings_mpa2 = [float(document['imdb_rating']) for document in cursor2_imdb]

        mean_imdb_mpa1 = mean(imdb_ratings_mpa1)
        mean_imdb_mpa2 = mean(imdb_ratings_mpa2)
        median_imdb_mpa1 = median(imdb_ratings_mpa1)
        median_imdb_mpa2 = median(imdb_ratings_mpa2)
        mode_imdb_mpa1 = mode(imdb_ratings_mpa1)
        mode_imdb_mpa2 = mode(imdb_ratings_mpa2)

        # Return the calculated statistics for both analyses
        return jsonify({
            'chartData': chart_data,
            'sum_total_mpa1': sum_total_mpa1,
            'sum_total_mpa2': sum_total_mpa2,
            'mean_mpa1': round(mean(mpa1_incomes),2),
            'mean_mpa2': round(mean(mpa2_incomes),2),
            'median_mpa1': round(median(mpa1_incomes),2),
            'median_mpa2': round(median(mpa2_incomes),2),
            'mode_mpa1': round(mode(mpa1_incomes),2),
            'mode_mpa2': round(mode(mpa2_incomes),2),
            'mean_imdb_mpa1': round(mean_imdb_mpa1,2),
            'mean_imdb_mpa2': round(mean_imdb_mpa2,2),
            'median_imdb_mpa1': round(median_imdb_mpa1,2),
            'median_imdb_mpa2': round(median_imdb_mpa2,2),
            'mode_imdb_mpa1': round(mode_imdb_mpa1,2),
            'mode_imdb_mpa2': round(mode_imdb_mpa2,2)
        }), 200

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': 'An error occurred during chart generation'}), 500


def createOrUpdateBarChart(labels, values1, values2):
    # Ensure the lengths match
    min_length = min(len(labels), len(values1), len(values2))
    labels = labels[:min_length]
    values1 = values1[:min_length]
    values2 = values2[:min_length]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    plt.figure(figsize=(12, 6))  # Adjust the figure size

    rects1 = plt.bar(x, values1, width, label='MPA 1')
    rects2 = plt.bar(x + width, values2, width, label='MPA 2')  # Adjust the x position

    # Add the sums above the bars
    for rect in rects1:
        height = rect.get_height()
        plt.annotate(f'{height:.0f}',
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom')

    for rect in rects2:
        height = rect.get_height()
        plt.annotate(f'{height:.0f}',
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom')

    # Add some text for labels, title, and custom x-axis tick labels, etc.
    plt.xlabel('MPA Ratings')  # Update x-axis label to MPA ratings
    plt.ylabel('Total Gross Income')
    plt.title('Total Gross Income by MPA Rating')
    plt.xticks(x + width / 2, labels)  # Adjust x-axis tick positions and labels
    plt.legend()

    # Autoformat ensures that labels fit in the figure area
    plt.autofmt_xdate()

    # Save the plot to a file
    chart_filename = 'static/matplotlib_chart.png'
    plt.savefig(chart_filename)
    plt.close()

    return chart_filename
    
@app.route('/api/compare_imdb_ratings', methods=['GET'])
def compare_imdb_ratings():
    mpa_rating1 = request.args.get('mpa_rating1')
    mpa_rating2 = request.args.get('mpa_rating2')

    # Query MongoDB to get IMDb rating statistics for the selected MPA ratings
    result = movie_collection.aggregate([
        {
            '$match': {
                'mpa_rating': {'$in': [mpa_rating1, mpa_rating2]},
                'imdb_rating': {'$ne': ''}
            }
        },
        {
            '$group': {
                '_id': '$mpa_rating',
                'mean_imdb_rating': {'$avg': '$imdb_rating'},
                'median_imdb_rating': {'$avg': '$imdb_rating'},  # Adjust this based on your calculation for median
                'mode_imdb_rating': {'$first': '$imdb_rating'}  # Adjust this based on your calculation for mode
            }
        }
    ])

    rating_statistics = {rating['_id']: {
        'mean_imdb_rating': rating['mean_imdb_rating'],
        'median_imdb_rating': rating['median_imdb_rating'],
        'mode_imdb_rating': rating['mode_imdb_rating']
    } for rating in result}

    return jsonify(rating_statistics)


# ... (rest of the previous code)

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
    
@app.route('/api/compare_gross_income', methods=['GET'])
def compare_gross_income():
    mpa_rating1 = request.args.get('mpa_rating1')
    mpa_rating2 = request.args.get('mpa_rating2')

    # Query MongoDB to get the summed gross income for the selected MPA ratings
    result = movie_collection.aggregate([
        {
            '$match': {
                'mpa_rating': {'$in': [mpa_rating1, mpa_rating2]}
            }
        },
        {
            '$group': {
                '_id': '$mpa_rating',
                'sum_gross_income': {'$sum': {'$toDouble': {'$substrCP': ['$imdb_gross', 1, -1]}}}
            }
        }
    ])

    comparison_data = {rating['_id']: rating['sum_gross_income'] for rating in result}
    return jsonify(comparison_data)


if __name__ == '__main__':
    app.run(debug=True, threaded=False)