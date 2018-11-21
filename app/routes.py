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
w3 = Namespace("http://www.w3.org/2000/01/rdf-schema#label")


# generic get function 
def get_generic(subject, prediate, object, jsonify):
	tupleslist = []
	#ID key
	id = 0
	#for each triple in the graph
	for s,p,o in g.triples((subject, prediate, object)):
		newSPO = {'id': id, 'o': o, 'p': p, 's': s}
		id = id+1
		tupleslist.append(newSPO)
	if jsonify:
		#format and return triples
		return jsonify(tupleslist)	
	else:
		return tupleslist
	
	
# setting up the URIs for RESTful server. This is base URI
@nrdcApp.route('/')							
@nrdcApp.route('/index')
def index():
	return  "Hello, NRDC!"

# This is a special URI to retrieve all triples of subject, predicate, object in the NRRC Ontology.
@nrdcApp.route('/alltriples', methods=['GET']) 
def get_triples():
	jsonObject = get_generic(None, None, None, True)
	return jsonObject
	
# This is a special URI to retrieve all sites in the NRRC Ontology.	
@nrdcApp.route('/sites', methods=['GET']) 
def get_json():
	jsonObject = get_generic(Ontology.site, None, None, True)
	return jsonObject

# This is a special URI for testing
@nrdcApp.route('/test', methods=['GET']) 
def get_tests():
	jsonObject = []
	for objects in Ontology:
		jsonObject = jsonObject + get_generic(None, Ontology[objects], None, False)
	return jsonify(jsonObject)
	
	
# This is a special URI for secondary testing
@nrdcApp.route('/test1', methods=['GET']) 
def get_tests1():
	jsonObject = get_generic(None, None, Ontology.organizational_tier, True)
	return jsonObject
	
@nrdcApp.route('/predicates', methods=['GET']) 
def get_predicates():
	tupleslist = []
	#ID key
	id = 0
	#for each triple in the graph
	#for s,p,o in g:#.triples(None, 'greh', None):
	for s,p,o in g:
		newSPO = {'id': id, 'p': p}
		id = id+1
		tupleslist.append(newSPO)
	#format and return triples
	return jsonify(tupleslist)	
	

