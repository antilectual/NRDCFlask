from app import nrdcApp
from flask import jsonify
#RDF importer
import rdflib	

#create triples graph			
g=rdflib.Graph()
#load ontology into triples
g.parse("NRDCOntology.xml", format="xml")
	
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
	for s,p,o in g:
		newSPO = {'id': id, 'o': o, 'p': p, 's': s}
		id = id+1
		tupleslist.append(newSPO)
	#format and return triples
	return jsonify(tupleslist)

	
	
# This is a special URI to retrieve the JSON tasks	
#	@nrdcApp.route('/organizationTier', methods=['GET']) 
#	def getOTs():
#		tupleslist = []
#		#ID key
#		id = 0
#		#for each triple in the graph
#		for s,p,o in g.triples(None, None, None):
#			newSPO = {'id': id, 'o': o, 'p': p, 's': s}
#			id = id+1
#			tupleslist.append(newSPO)
#		#format and return triples
#		return jsonify(tupleslist)
