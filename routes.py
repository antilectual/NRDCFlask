from __future__ import print_function
import sys
import logging
logging.basicConfig(level=logging.DEBUG)
from flask import Flask
from flask import request
app = Flask(__name__) 				# Create app object as FLASK (variable app)
from flask import json, jsonify
#from flask_restplus import Namespace
#from functions import *
from functions import *
from flask_cors import CORS, cross_origin
CORS(app)


index()
# setting up the URIs for RESTful server. This is base URI
@app.route('/')
@app.route('/index')
def return_index():
    return index()

# This is a special URI to retrieve all triples of subject, predicate, object in the NRRC Ontology.
@app.route('/alltriples', methods=['GET'])
def return_triples():
    return get_triples()

# This is a special URI to retrieve all sites in the NRRC Ontology.
@app.route('/sites', methods=['GET'])
def return_json():
    return get_json()

# URI for finding namespaces in ontology
@app.route('/namespaces', methods=['GET'])
def return_namespaces():
    return get_namespaces()

# This is a URI for finding the navigational root
@app.route('/childrenOf', methods=['GET'])
def return_allChildOf():
    return get_allChildrenOf()

# This is a special URI for retrieving the hierarchy (todo)
@app.route('/hierarchyTree', methods=['GET'])
def return_hierarchy():
    return getHierarchy()

# This is a special URI for testing
@app.route('/allsubjects', methods=['GET'])
def return_allSubjects():
    return get_allsubjects()

# This is a special URI for secondary testing
@app.route('/test1', methods=['GET'])
def return_tests1():
    return get_tests1()

# URI for finding all predicates in the Ontology
@app.route('/predicates', methods=['GET'])
def return_predicates():
    return get_predicates()

# URI for finding all characteristics
@app.route('/allcharacteristics', methods=['GET'])
def return_allCharacteristics():
    return get_allcharacteristics()

# URI for parsing the ontology graph to structure the graph into a navigational hierarchy tree
@app.route('/Ragnarok/', methods=['GET'])
def return_ontology():
    return get_ontology()


# URI for parsing the ontology graph to structure the graph into a navigational hierarchy tree
@app.route('/saveJSON/', methods=['POST', 'OPTIONS'])
@cross_origin()
def save_json_here():
    return save_json_to_file()

# Declare port for use
if __name__ == '__main__':
    app.debug = False
    app.run(host="127.0.0.1", port=8300)
