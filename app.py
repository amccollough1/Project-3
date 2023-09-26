#!/usr/bin/env python
# coding: utf-8

# In[229]:


from flask import Flask, jsonify, request
from pymongo import MongoClient
from pprint import pprint
import sys
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello!'


# In[230]:


client = MongoClient('mongodb://localhost:27017/')
db = client['Marvel-Vs-DC-Comic']
db2 = client['Marvel-Vs-DC-Movie']
comics_collection = db['Marvel-Vs-DC-Comic'] 
film_collection = db2['Marvel-Vs-DC-Movie']


# In[231]:


try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Marvel-Vs-DC-Movie']
    film_collection = db['Marvel-Vs-DC-Movie']
    print("Connected to MongoDB successfully")
except Exception as e:
    print("Error connecting to MongoDB:", str(e))


# In[227]:


@app.route('/api/dc_comics', methods=['GET'])
def get_dc_comics():
    dc_comics = list(comics_collection.find({"universe": "DC"}))

    return jsonify(dc_comics)


# In[120]:


query = {'Universe':'Marvel'}
results = list(comics_collection.find(query))
print(len(results))


# In[121]:


query = {'Universe':'DC'}
results = list(comics_collection.find(query))
print(len(results))


# In[122]:


# How does a characters' identity influence their alignment(good, bad, neutral)?
@app.route('/api/character_identity_influence', methods=['GET'])
def character_identity_influence():
    identity_alignment_mapping = {
        "Secret": {"alignment": {"Good": 0, "Bad": 0, "Neutral": 0}},
        "Public": {"alignment": {"Good": 0, "Bad": 0, "Neutral": 0}},
        "Non-dual": {"alignment": {"Good": 0, "Bad": 0, "Neutral": 0}}
    }

    for identity, alignment_data in identity_alignment_mapping.items():
        alignment_count = alignment_data["alignment"]
        
        query = {"Identity": identity}
        characters = list(comics_collection.find(query))

        for character in characters:
            alignment = character["Alignment"]
            alignment_count[alignment] += 1

    return jsonify(identity_alignment_mapping)
if __name__ == '__main__':
    app.run(port=5000)
#http://127.0.0.1:5000/api/character_identity_influence


# In[127]:


# How does the number of good vs bad characters changes over x period of years in both DC and Marvel?
@app.route('/api/good_bad_character_changes', methods=['GET'])
def get_good_bad_character_changes():
    start_year = request.args.get('First_appeared', type=int)
    current_year = 2023

    dc_query = {
        "Universe": "DC",
        "First_appeared": {"$lte": current_year},
        "Alignment": {"$in": ["Good", "Bad"]},
        "Alive": "Yes" 
    }

    marvel_query = {
        "Universe": "Marvel",
        "First_appeared": {"$lte": current_year},
        "Alignment": {"$in": ["Good", "Bad"]},
        "Alive": "Yes"
    }

    dc_pipeline = [
        {"$match": dc_query},
        {"$group": {"_id": {"Year": "$First_appeared", "Alignment": "$Alignment"}, "count": {"$sum": 1}}}
    ]

    dc_results = list(comics_collection.aggregate(dc_pipeline))

    marvel_pipeline = [
        {"$match": marvel_query},
        {"$group": {"_id": {"Year": "$First_appeared", "Alignment": "$Alignment"}, "count": {"$sum": 1}}}
    ]

    marvel_results = list(comics_collection.aggregate(marvel_pipeline))

    response = {
        "DC_Characters": dc_results,
        "Marvel_Characters": marvel_results
    }

    return jsonify(response)
if __name__ == '__main__':
    app.run(port=5000)
# http://127.0.0.1:5000/api/good_bad_character_changes?First_appeared=2000


# In[143]:


# How does the number of appearances in DC/Marvel comics compare to the films released?

@app.route('/api/characters_in_both_datasets', methods=['GET'])
def get_characters_in_both_datasets():
    comic_characters = set(doc['Character_Name'] for doc in comics_collection.find({}, {"Character_Name": 1}))
    
    film_titles = [doc['title'] for doc in film_collection.find({}, {"title": 1})]
    
    film_characters = set()
    for title in film_titles:
        character_names = re.findall(r'\b[A-Z][a-zA-Z ]+[A-Z]\b', title)
        film_characters.update(character_names)
    
    common_characters = list(comic_characters.intersection(film_characters))
    
    response = {
        "common_characters": common_characters
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)


# In[ ]:


# Film Release : Is there a particular MPA rating that peforms better over another?

@app.route('/api/mpa_rating_performance', methods=['GET'])
def get_mpa_rating_performance():
    # Define the MPA ratings you want to analyze
    mpa_ratings = ["PG", "G", "PG-13", "R"]
    
    rating_performance = {}
    
    for rating in mpa_ratings:
        query = {"mpa_rating": rating}
        films = list(film_collection.find(query))
        
        if not films:
            continue
        
        films_data = []
        
        for film in films:
            title = film.get("title")
            imdb_gross = film.get("imdb_gross")
            films_data.append({"title": title, "imdb_gross": imdb_gross})
        
        rating_performance[rating] = films_data
    
    if not rating_performance:
        return jsonify({"message": "No films found for these ratings."})
    
    response = {
        "rating_performance": rating_performance
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)


# In[ ]:




