from app import nrdcApp
from flask import json, jsonify
#from flask_restplus import Namespace
#RDF importer
import rdflib	
from rdflib import Namespace, RDF
from rdflib.namespace import NamespaceManager
JSON_SORT_KEYS = False

#create triples graph
g=rdflib.Graph()
#load ontology into triples
g.parse("NRDCOntology.xml", format="xml")
#Header namespace declaration
Ontology = Namespace("http://www.sensor.nevada.edu/ontologies/research_site_hierarchy#")
namespace_manager = NamespaceManager(rdflib.Graph())
namespace_manager.bind('nrdcOntology', Ontology, override=False)
g.namespace_manager = namespace_manager
root = ""  # the root of the hierarchy


# generic get function 
def get_generic(subject, prediate, object, jsonificate):
    tupleslist = []
    #ID key
    id = 0
    #for each triple in the graph
    for s,p,o in g.triples((subject, prediate, object)):
        newSPO = {'id': id, 'o': o, 'p': p, 's': s}
        id = id+1
        tupleslist.append(newSPO)
    if jsonificate:
        #format and return triples
        return jsonify(tupleslist)
    else:
        return tupleslist

def get_subjects_list():
    # create a dictionary
    allSubjects = {}
    # find all subjects without the namespace and add it as a key to the dictionary
    # this keeps the subjects unique
    for s in g.subjects():
        s = s.split('#')[-1]
        # "" is just to give the key a value with it. It is irrelevant
        allSubjects[s] = ""
    # create a list since jsonify() can't work on dictionaries
    newAllSubjects = []
    # sort the dictionary and
    # add all dictionary and set the dictionary key as the value now.
    for key in sorted(allSubjects):
        newAllSubjects.append({key})
    # return a json response object (Note: can't edit a jsonify object once it is created)
    return newAllSubjects

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
@nrdcApp.route('/namespaces', methods=['GET'])
def get_namespaces():
    all_ns = [n for n in g.namespace_manager.namespaces()]
    return jsonify(all_ns)

# This is a special URI for testing
@nrdcApp.route('/childrenOf', methods=['GET'])
def get_childrenOf():
    allChildrenOf = []                            # All objects that are a childOf something
    childrenWithParents = []                      # The list of objects that are a childOf a parent
    allSubjects = get_subjects_list()             # Get all subjects from subject/predicate/object triples
    # This for loop finds all the subjects that are a childOf an object
    # and adds them to two lists, one that is converted to a json showing subject-childOf relationship
    # and one that contains all subjects that are a childOf themselves.
    # The second list will be used to find the root
    for subject in allSubjects:
        subject = (list(subject))[0]
        parents = get_generic(Ontology[subject], Ontology.childOf, None, False)
        if parents != []:
            childOf = parents[0]["o"].split('#')[-1]
            allChildrenOf.append({'subject': subject, 'childOf': childOf})
            childrenWithParents.append(subject)
    # This for loop iterates though the subjects that were found to have parents,
    # grabs the parent, and checks to see if that parent is in the list of children with parents.
    # If it doesn't have a parent, it is the root node and defined as such.
    for subject in allChildrenOf:
        subject = subject["childOf"]
        if subject not in childrenWithParents:
            root = subject
    # component -> deployment -> system -> site -> site_network : site_network = root
    return jsonify(allChildrenOf)

# This is a special URI for testing
@nrdcApp.route('/test', methods=['GET'])
def get_test():
    allSubjects = get_subjects_list()
    return jsonify(allSubjects)

# This is a special URI for secondary testing
@nrdcApp.route('/test1', methods=['GET']) 
def get_tests1():
    jsonObject = get_generic(None, Ontology.childOf, None, True)
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

