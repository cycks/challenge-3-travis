from flask import Flask, request, Blueprint, jsonify

sikolia = Blueprint('sikolia', __name__)

@sikolia.route('api/auth/v2', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to my home page"})
