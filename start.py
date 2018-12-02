from flask import Flask 
app = Flask(__name__) 				# Create app object as FLASK (variable app)
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
