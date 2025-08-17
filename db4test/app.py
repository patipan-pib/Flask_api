from flask import Flask, request, jsonify
from models import SessionLocal, User

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Welcome to the User Management API TEST"


@app.route("/users", methods=["GET"])
def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return jsonify([{"id": u.id, "name": u.name, "age": u.age} for u in users])

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    session = SessionLocal()
    user = User(name=data["name"], age=data["age"])
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return jsonify({"id": user.id, "name": user.name, "age": user.age})

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    session = SessionLocal()
    user = session.query(User).get(user_id)
    if not user:
        session.close()
        return jsonify({"error": "User not found"}), 404
    user.name = data.get("name", user.name)
    user.age = data.get("age", user.age)
    session.commit()
    session.close()
    return jsonify({"message": "User updated"})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    session = SessionLocal()
    user = session.query(User).get(user_id)
    if not user:
        session.close()
        return jsonify({"error": "User not found"}), 404
    session.delete(user)
    session.commit()
    session.close()
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)
