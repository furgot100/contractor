from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from functools import reduce
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/my_app_db')
client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()

players_collection = db.players
# HOMEPAGE
@app.route('/')
def index():
    return render_template('index.html', players=players_collection.find())

# CREATE
@app.route('/new')
def new_player():
    return render_template('new_player.html')

# CREATE 
@app.route('/new', methods=['POST'])
def create_player():
    player = {
        'name': request.form.get('name'),
        'position': request.form.get('position'),
        'img_url': request.form.get('img_url')
    }
    player_id = players_collection.insert_one(player).inserted_id
    return redirect(url_for('show_player', player_id=player_id))

# READ
@app.route('/player/<player_id>')
def show_player(player_id):
    player = players_collection.find_one({'_id': ObjectId(player_id)})
    return render_template('show_player.html', player=player)

# UPDATE
@app.route('/edit/<player_id>', methods=['POST'])
def update_player(player_id):
    
    new_player = {
        'name': request.form.get('name'),
        'position': request.form.get('position'),
        'img_url': request.form.get('img_url')
    }
    players_collection.update_one(
        {'_id': ObjectId(player_id)},
        {'$set': new_player}
    )
    return redirect(url_for('show_player', player_id=player_id))

# UPDATE
@app.route('/edit/<player_id>', methods=['GET'])
def edit_player(player_id):
    player = players_collection.find_one({'_id': ObjectId(player_id)})
    return render_template('edit_player.html', player=player)


# DELETE
@app.route('/delete/<player_id>', methods=['POST'])
def delete_player(player_id):
    players_collection.delete_one({'_id': ObjectId(player_id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))