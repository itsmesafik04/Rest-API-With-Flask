from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for users
users = {
    1: {"name": "John", "email": "john@example.com"},
    2: {"name": "Alice", "email": "alice@example.com"}
}


# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


# GET single user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        return jsonify(users[user_id])

    return jsonify({"message": "User not found"}), 404


# POST new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"message": "Name and email are required"}), 400

    new_id = max(users.keys(), default=0) + 1

    users[new_id] = {
        "name": data['name'],
        "email": data['email']
    }

    return jsonify({
        "message": "User added successfully",
        "user": users[new_id]
    }), 201


# PUT update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    users[user_id] = {
        "name": data.get("name", users[user_id]["name"]),
        "email": data.get("email", users[user_id]["email"])
    }

    return jsonify({
        "message": "User updated successfully",
        "user": users[user_id]
    })


# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404

    deleted_user = users.pop(user_id)

    return jsonify({
        "message": "User deleted successfully",
        "user": deleted_user
    })


if __name__ == '__main__':
    app.run(debug=True)