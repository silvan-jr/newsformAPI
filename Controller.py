from flask import Flask,jsonify
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoflask import MongoJSONEncoder, ObjectIdConverter

client = MongoClient('localhost:27017')
app = Flask(__name__)
app.json_encoder = MongoJSONEncoder
app.url_map.converters['objectid'] = ObjectIdConverter

db = client.APINEWS

#I CONSIDER THAT BEFORE THIS API, THERE WILL BE A LOGIN API AND THAT THIS LOGIN API WILL PROVIDE THE LOGED AUTHOR ID
'''
#Creat users for testing
@app.route("/create_autor", methods = ['POST'])
def create_autor():
    autorCollection = db.autor
    name_autor = str(request.json['name_autor'])
    autor_insert = autorCollection.insert({'name_autor': name_autor})
    autor_inserted = autorCollection.find_one({"_id": ObjectId(autor_insert)})
    output = {'name_autor': autor_inserted['name_autor']}
    return jsonify({'Autor inserido': output})'''

# Creat a new news
@app.route("/create_news", methods = ['POST'])
def create_news():
    autorCollection= db.autor
    newsCollection= db.news
    autor_id=str(request.json['autor_id'])
    autor = autorCollection.find_one({"_id": ObjectId(autor_id)})
    name_autor = autor['name_autor']
    description = str(request.json['description'])
    title = str(request.json['title'])
    news_id = newsCollection.insert({'description':description,'title':title,'autor_id':autor_id,'name_autor': name_autor})
    news= newsCollection.find_one({"_id": ObjectId(news_id)})
    output = {'_id':news['_id'],'title':news['title']}
    return jsonify({'inserted':output})

#Shows all news created by the author
@app.route("/news_list", methods = ['GET'])
def news_list():
     newsCollection=db.news
     autor_id = str(request.json['autor_id'])
     news_list=newsCollection.find({'autor_id':autor_id})
     list_news = []
     for q in news_list:
         list_news.append({'_id' : q['_id'],'title' : q['title'],'name_autor':q['name_autor']})
     return jsonify({'result': list_news})

#Edit the news selected
@app.route("/edit_news", methods = ['POST'])
def edit_news():
    newsCollection = db.news
    news_id = str(request.json['news_id'])
    description = str(request.json['description'])
    title = str(request.json['title'])
    news_update = newsCollection.find_one_and_update({'_id':ObjectId(news_id)},{'$set' : {'title': title,'description' : description}},upsert=False)
    news_updated = newsCollection.find_one({'_id':ObjectId(news_id)})
    return jsonify({'result': news_updated})

#Delete the news selected
@app.route("/delete", methods = ['POST'])
def delete():
    newsCollection = db.news
    news_id = str(request.json['news_id'])
    newsCollection.delete_one({'_id': ObjectId(news_id)})
    return jsonify({'deletado':news_id})

if __name__ == '__main__':
     app.run(debug=True)
