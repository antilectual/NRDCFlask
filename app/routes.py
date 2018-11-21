from app import nrdcApp
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
	for s,p,o in g.triples((None, RDF.type, Ontology.organizational_tier)):
		newSPO = {'id': id, 'o': o, 'p': p, 's': s}
		id = id+1
		tupleslist.append(newSPO)
	#format and return triples
	return jsonify(tupleslist)

@nrdcApp.route('/alltriples', methods=['GET']) 
def get_triples():
	tupleslist = []
	#ID key
	id = 0
	#for each triple in the graph
	#for s,p,o in g:#.triples(None, 'greh', None):
	for s,p,o in g:
		newSPO = {'id': id, 'o': o, 'p': p, 's': s}
		id = id+1
		tupleslist.append(newSPO)
	#format and return triples
	return jsonify(tupleslist)

@nrdcApp.route('/sites', methods=['GET']) 
def get_json():
	tupleslist = []
	#ID key
	id = 0
	# Check for edge cases of (parent without parent, child without child)
	for s,p,o in g.triples((Ontology.component, None, None)):
		newSPO = {'id': id, 'o': o, 'p': p, 's': s}
		id = id+1
		tupleslist.append(newSPO)
	#format and return triples
	return jsonify(tupleslist)

# if checking for child of and is not the subject of a query, then it is the topmost parent