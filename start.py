from flask import Flask 
nrdcApp = Flask(__name__) 				# Create app object as FLASK (variable app)
from flask import jsonify
#from flask_restplus import Namespace
#RDF importer
import rdflib	
from rdflib import Namespace, RDF

#create triples graph			
g=rdflib.Graph()
#load ontology into triples
g.parse("NRDCOntology.xml", format="xml")

#Header namespace declaration
Ontology = Namespace("http://www.sensor.nevada.edu/ontologies/research_site_hierarchy#")
	
# setting up the URIs for RESTful server. This is base URI
@nrdcApp.route('/')							
@nrdcApp.route('/index')
def index():
	return  "Hello, NRDC!"
	
# This is a special URI to retrieve the JSON tasks	
@nrdcApp.route('/test', methods=['GET']) 
def get_tasks():
	tupleslist = []
	#ID key
	id = 0
	#for each triple in the graph
	#for s,p,o in g:#.triples(None, 'greh', None):
	for s,p,o in g.triples((None, RDF.tyype, Ontology.organizational_tier, None)):
		newSPO = {'id': id, 'o': o, 'p': p, 's': s}
		id = id+1
		tupleslist.append(newSPO)
	#format and return triples
	return jsonify(tupleslist)