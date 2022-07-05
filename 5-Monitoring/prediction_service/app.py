import os 
import pickle
import requests

from pymongo import MongoClient

from flask import Flask, request, jsonify

MODEL_FILE = os.getenv('MODEL_FILE', 'lin_reg.bin')

EVIDENTLY_SERVICE_ADDRESS = os.getenv('EVIDENTLY_SERVICE', 'http://127.0.0.1:5000')
MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://127.0.0.1:27017")