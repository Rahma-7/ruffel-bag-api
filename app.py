from flask import Flask, jsonify
from routes.cars import cars_bp

app = Flask(__name__)
app.register_blueprint(cars_bp)

@app.route("/")
def home():
    return jsonify({"message": "Ruffel & Båg Cars API fungerar!"})

if __name__ == "__main__":
    app.run(debug=True)