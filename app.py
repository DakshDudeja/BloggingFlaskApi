from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_cors import CORS


app = Flask(__name__)
CORS(app,origins="*")

app.config["MONGO_URI"] = "mongodb://localhost:27017/blogs"
mongo = PyMongo(app)


# Create User
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    id = data.get("_id")
    if 'username' in data or 'password' in data:
        if not id:
            user_id = mongo.db.users.insert_one(data).inserted_id
            return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201
        else:
            update_user(data)
    else:
        return jsonify({'error': 'Incomplete data provided'}), 400

# login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Incomplete data provided'}), 400

    user = mongo.db.users.find_one({'username': username, 'password': password})

    if user:
        user_id = str(user['_id'])
        return jsonify({'message': 'User Exists', 'user_id': user_id}), 201
    else:
        return jsonify({'message': 'User not found'}), 404

# Update User
# @app.route('/user/<string:user_id>', methods=['PUT'])
def update_user(data):
    data = request.json
    id = data.get("_id")
    if 'username' in data or 'password' in data:
        update_data = {}
        if 'username' in data:
            update_data['username'] = data['username']
        if 'password' in data:
            update_data['password'] = data['password']

        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': update_data})
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'No data provided for update'}), 400

# Delete User
@app.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Get Users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(mongo.db.users.find())
    serialized_users = [serialize_user(user) for user in users]
    return jsonify(serialized_users), 200

def serialize_user(user):
    user['_id'] = str(user['_id'])
    return user


@app.route('/blogpost', methods=['POST'])
def create_blog_post():
    data = request.json
    id = data.get("_id")
    if 'title' in data and 'desc' in data and 'posted_by' in data:
        try:
            posted_by_object_id = ObjectId(id)
        except Exception as e:
            return jsonify({'error': 'Invalid ObjectId for posted_by'}), 400

        # Update 'posted_by' with the provided user's _id
        data['posted_by'] = str(posted_by_object_id)

        blog_post_id = mongo.db.blogPosts.insert_one(data).inserted_id
        return jsonify({'message': 'Blog post created successfully', 'blog_post_id': str(blog_post_id)}), 201
    else:
        return jsonify({'error': 'Incomplete or invalid data provided'}), 400


# Update Blog Post
@app.route('/blogpost/<string:blog_post_id>', methods=['PUT'])
def update_blog_post(blog_post_id):
    data = request.json
    update_data = {}
    if 'title' in data:
        update_data['title'] = data['title']
    if 'desc' in data:
        update_data['desc'] = data['desc']
    if 'likes' in data:
        update_data['likes'] = data['likes']

    mongo.db.blogPosts.update_one({'_id': ObjectId(blog_post_id)}, {'$set': update_data})
    return jsonify({'message': 'Blog post updated successfully'}), 200

# Delete Blog Post
@app.route('/blogpost/<string:blog_post_id>', methods=['DELETE'])
def delete_blog_post(blog_post_id):
    result = mongo.db.blogPosts.delete_one({'_id': ObjectId(blog_post_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Blog post deleted successfully'}), 200
    else:
        return jsonify({'error': 'Blog post not found'}), 404

# Get Blog Posts
@app.route('/blogposts', methods=['GET'])
def get_blog_posts():
    blog_posts = list(mongo.db.blogPosts.find())
    return jsonify({'blog_posts': blog_posts}), 200


# Fetch Blog Posts by User ID
@app.route('/blogposts/user/<string:user_id>', methods=['GET'])
def get_blog_posts_by_user(user_id):
    try:
        # Ensure 'user_id' contains a valid ObjectId
        user_object_id = (user_id)
    except Exception as e:
        return jsonify({'error': 'Invalid ObjectId for user_id'}), 400

    blog_posts = list(mongo.db.blogPosts.find({'posted_by': str(user_object_id)}))
    serialized_blog_posts = [serialize_blog_post(post) for post in blog_posts]

    return jsonify({'blog_posts': serialized_blog_posts}), 200

def serialize_blog_post(post):
    # Convert ObjectId to string
    post['_id'] = str(post['_id'])
    return post



if __name__ == '__main__':
    app.run(debug=True)
