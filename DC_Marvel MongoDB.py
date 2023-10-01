#!/usr/bin/env python
# coding: utf-8

# 
# mongoimport --type csv -d Marvel-Vs-DC-Comic -c comics --headerline  dc_bad_df.csv
# 
# mongoimport --type csv -d Marvel-Vs-DC-Comic -c comics --headerline  dc_good_df.csv
# 
# mongoimport --type csv -d Marvel-Vs-DC-Comic -c comics --headerline   dc_neutral_df.csv
# 
# 
# mongoimport --type csv -d Marvel-Vs-DC-Comic -c comics --headerline   marvel_bad_df.csv
# 
# mongoimport --type csv -d Marvel-Vs-DC-Comic -c comics --headerline   marvel_good_df.csv
# 
# mongoimport --type csv -d Marvel-Vs-DC-Comic -c comics --headerline  marvel_neutral_df.csv
# 
# mongoimport --type csv -d Marvel-Vs-DC-Movie -c films --headerline  dc_movies.csv
# 
# mongoimport --type csv -d Marvel-Vs-DC-Movie -c films --headerline  marvel_movies.csv
# 

# In[1]:


# Import dependencies
from pymongo import MongoClient
from pprint import pprint


# In[2]:


# Create an instance of MongoClient
mongo = MongoClient(port=27017)


# In[3]:


# confirm that our new databases was created
print(mongo.list_database_names())


# In[4]:


# assign the databases to a variable name

db= mongo['Marvel-Vs-DC-Comic']
db2 = mongo['Marvel-Vs-DC-Movie']


# In[5]:


# review the collections in the databases
print(db.list_collection_names())
print(db2.list_collection_names())


# In[6]:


#review a document in the comics collection
pprint(db.comics.find_one())


# In[7]:


#review a document in the films collection
pprint(db2.films.find_one())


# In[8]:


#assign collection to a variable
character = db['comics']

films=db2['films']


# # Exploring character collection by analyzing  Question 1: 
# How does a characters' identity influence their alignment(good, bad, neutral)?

# In[9]:


# find out how many characters have a "secret" identity in the DC universe
query = {'Alignment': 'Good', 
         'Identity': 'Secret', 
         'Universe': 'DC'
        }
query2 = {'Alignment': 'Bad', 
         'Identity': 'Secret', 
         'Universe': 'DC'
        }

query3 = {'Alignment': 'Neutral', 
         'Identity': 'Secret', 
         'Universe': 'DC'
        }
good_alignment = character.count_documents(query)
bad_alignment= character.count_documents(query2)
neutral_alignment =character.count_documents(query3)
print(f'There are {good_alignment} good characters, {bad_alignment} bad characters , and {neutral_alignment} neutral characters that have a secret identity within the DC Universe.')


# In[10]:


# find out how many characters have a "secret" identity in the Marvel Universe
query = {'Alignment': 'Good', 
         'Identity': 'Secret', 
         'Universe': 'Marvel'
        }
query2 = {'Alignment': 'Bad', 
         'Identity': 'Secret', 
         'Universe': 'Marvel'
        }

query3 = {'Alignment': 'Neutral', 
         'Identity': 'Secret', 
         'Universe': 'Marvel'
        }
good_alignment = character.count_documents(query)
bad_alignment= character.count_documents(query2)
neutral_alignment =character.count_documents(query3)
print(f'There are {good_alignment} good characters, {bad_alignment} bad characters , and {neutral_alignment} neutral characters that have a secret identity within the Marvel Universe.')


# In[11]:


#find out how many documents have a "public" identity within the DC Universe
query = {'Alignment': 'Good', 
         'Identity': 'Public', 
         'Universe': 'DC'
        }
query2 = {'Alignment': 'Bad', 
         'Identity': 'Public', 
         'Universe': 'DC'
        }

query3 = {'Alignment': 'Neutral', 
         'Identity': 'Public', 
         'Universe': 'DC'
        }
good_alignment = character.count_documents(query)
bad_alignment= character.count_documents(query2)
neutral_alignment =character.count_documents(query3)
print(f'There are {good_alignment} good characters, {bad_alignment} bad characters , and {neutral_alignment} neutral characters that have a public identity within the DC Universe.')


# In[12]:


#find out how many documents have a "public" identity within the Marvel Universe
query = {'Alignment': 'Good', 
         'Identity': 'Public', 
         'Universe': 'Marvel'
        }
query2 = {'Alignment': 'Bad', 
         'Identity': 'Public', 
         'Universe': 'Marvel'
        }

query3 = {'Alignment': 'Neutral', 
         'Identity': 'Public', 
         'Universe': 'Marvel'
        }
good_alignment = character.count_documents(query)
bad_alignment= character.count_documents(query2)
neutral_alignment =character.count_documents(query3)
print(f'There are {good_alignment} good characters, {bad_alignment} bad characters , and {neutral_alignment} neutral characters that have a public identity within the Marvel Universe.')


# In[13]:


#find out how many documents have a "non-dual" identity within the DC Universe
query = {'Alignment': 'Good', 
         'Identity': 'Non-dual', 
         'Universe': 'DC'
        }
query2 = {'Alignment': 'Bad', 
         'Identity': 'Non-dual', 
         'Universe': 'DC'
        }

query3 = {'Alignment': 'Neutral', 
         'Identity': 'Non-dual', 
         'Universe': 'DC'
        }
good_alignment = character.count_documents(query)
bad_alignment= character.count_documents(query2)
neutral_alignment =character.count_documents(query3)
print(f'There are {good_alignment} good characters, {bad_alignment} bad characters , and {neutral_alignment} neutral characters that have a non-dual identity within the DC Universe.')


# In[14]:


#find out how many documents have a "non-dual" identity within the Marvel Universe
query = {'Alignment': 'Good', 
         'Identity': 'Non-dual', 
         'Universe': 'Marvel'
        }
query2 = {'Alignment': 'Bad', 
         'Identity': 'Non-dual', 
         'Universe': 'Marvel'
        }

query3 = {'Alignment': 'Neutral', 
         'Identity': 'Non-dual', 
         'Universe': 'Marvel'
        }
good_alignment = character.count_documents(query)
bad_alignment= character.count_documents(query2)
neutral_alignment =character.count_documents(query3)
print(f'There are {good_alignment} good characters, {bad_alignment} bad characters , and {neutral_alignment} neutral characters that have a non-dual identity within the Marvel Universe.')


# # Exploring film collection

# In[15]:


#review a document in the films collection
pprint(db2.films.find_one())


# In[16]:


query = {'entity': 'DC'}
results = films.count_documents(query)
print(results)


# In[17]:


query = {'entity': 'MARVEL'}
results = films.count_documents(query)
print(results)


# In[ ]:




