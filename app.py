# Import Package
import os
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
import re
from bson import ObjectId

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

def createSlug(title):
    slug = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    slug = slug.lower().strip().replace(" ", "-")
    return slug

@app.route('/')
def home(): 
  return render_template('index.html')

@app.route('/blog')
def blog() : 

  posts = list(db.posts.find({}, {'_id' : False}))
  return render_template('blog.html', posts=posts)

@app.route('/blog/create')
def createBlog() :
  return render_template('create.html')

@app.route('/blog', methods=["post"])
def store() : 
  title = request.form.get('title')
  body = request.form.get('body')
  author = request.form.get('author')

  original_slug = createSlug(title)
  slug = original_slug
  counter = 1
  while db.posts.find_one({"slug": slug}):
      slug = f"{original_slug}-{counter}"
      counter += 1

  doc = {
      "title": title,
      "slug": slug,
      "body": body,
      "author": author,
      "date": datetime.now().strftime("%d-%m-%Y"),
  }

  db.posts.insert_one(doc)

  data = {
      "result": "success",
      "message": "Post created successfully!",
      "slug": slug
  }

  return jsonify(data), 201

@app.route('/blog/edit/<slug>')
def editBlog(slug) :
  post = db.posts.find_one({"slug" : slug})

  if post:
        post['_id'] = str(post['_id'])
  else : 
    return jsonify({"message" : "Post Not Found"}), 404
   
  return render_template('edit.html', post=post)

@app.route('/blog/<post_id>', methods=["put"])
def update(post_id) : 
  title = request.form.get('title')
  body = request.form.get('body')
  author = request.form.get('author')

  post = db.posts.find_one({"_id": ObjectId(post_id)})
  if not post:
      return jsonify({"result": "error", "message": "Post not found"}), 404
  
  update_data = {}

  if title and title != post['title']:
      original_slug = createSlug(title)
      slug = original_slug
      counter = 1
      while db.posts.find_one({"slug": slug, "_id": {"$ne": ObjectId(post_id)}}):
          slug = f"{original_slug}-{counter}"
          counter += 1
      update_data["title"] = title
      update_data["slug"] = slug

  if body:
      update_data["body"] = body

  if author:
      update_data["author"] = author

  update_data["last_updated"] = datetime.now().strftime("%d-%m-%Y")

  db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": update_data})
  
  data = {
      "result": "success",
      "message": "Post updated successfully!",
  }
  
  return jsonify(data), 200

@app.route('/blog/<slug>', methods=["delete"])
def destroy(slug) :
  db.posts.delete_one({"slug" : slug})
  data = {
    "result" : "success",
    "message" : "Post deleted successfully!",
  }

  return jsonify(data)

@app.route('/about')
def about() : 
  return render_template('about.html')

port=5000
debug=True
if __name__ == "__main__" : 
  app.run('0.0.0.0', port=port, debug=debug)