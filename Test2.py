#RDF importer
import rdflib			
#create triples graph			
g=rdflib.Graph()
#load ontology into triples
g.parse("NRDCOntology.xml", format="xml")

for s,p,o in g:
	#show triples
    print (s,p,o)