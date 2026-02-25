from flask import Blueprint, request, jsonify
import json
import os

cars_bp = Blueprint("cars_bp", __name__)
FILE_NAME = "cars.json"

def load_cars():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_cars(cars):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(cars, file, indent=2)

@cars_bp.route("/cars", methods=["GET"])
def get_cars():
    return jsonify(load_cars()), 200

@cars_bp.route("/cars/<regnr>", methods=["GET"])
def get_car(regnr):
    cars = load_cars()
    for car in cars:
        if car.get("regnr", "").lower() == regnr.lower():
            return jsonify(car), 200
    return jsonify({"error": "Car not found"}), 404

@cars_bp.route("/cars", methods=["POST"])
def add_car():
    new_car = request.get_json()
    if not new_car or "regnr" not in new_car:
        return jsonify({"error": "Missing regnr"}), 400

    cars = load_cars()
    for car in cars:
        if car["regnr"].lower() == new_car["regnr"].lower():
            return jsonify({"error": "Car already exists"}), 409

    cars.append(new_car)
    save_cars(cars)
    return jsonify(new_car), 201

@cars_bp.route("/cars/<regnr>", methods=["PUT"])
def update_car(regnr):
    cars = load_cars()
    data = request.get_json()

    for car in cars:
        if car["regnr"].lower() == regnr.lower():
            car.update(data)
            save_cars(cars)
            return jsonify(car), 200

    return jsonify({"error": "Car not found"}), 404

@cars_bp.route("/cars/<regnr>", methods=["DELETE"])
def delete_car(regnr):
    cars = load_cars()

    for car in cars:
        if car["regnr"].lower() == regnr.lower():
            cars.remove(car)
            save_cars(cars)
            return jsonify({"message": "Car deleted"}), 200

    return jsonify({"error": "Car not found"}), 404