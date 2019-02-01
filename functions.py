from flask import json, jsonify
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
w3Namespace = Namespace("http://www.w3.org/2000/01/rdf-schema#")
namespace_manager = NamespaceManager(rdflib.Graph())
namespace_manager.bind('nrdcOntology', Ontology, override=False)
g.namespace_manager = namespace_manager
root = ""  # the root of the hierarchy

def get_ontology():
    organizationalTiers = []
    #ID key
    #for each triple in the graph
    #for s,p,o in g:#.triples(None, 'greh', None):
    for s,p,o in g.triples((None, None , Ontology.organizational_tier)):
        # Find the name of the OT
        name = rdflib.namespace.split_uri(s)[1]
        # Store the name in a dictionary
        tierInformation = { "Name": name }

        # Find the pluralization of the tier name
        for sP,pP,oP in g.triples((Ontology[name], Ontology.pluralization, None)):
            # Find the name of the OT
            tierInformation['Plural'] = oP

        # Find the referential characteristic
        for s,p,o in g.triples((Ontology[name], Ontology.referentialCharacteristic, None)):
            reference = o
        # Find the name of the OT
        tierInformation['referentialCharacteristic'] = o

        tierInfoParent = []
        # Find the parentOf of the tier name
        for sP,pP,oP in g.triples((Ontology[name], Ontology.childOf, None)):
            tierInfoParent.append(rdflib.namespace.split_uri(oP)[1])
            # Find the name of the OT

        tierInformation['ChildOf'] = tierInfoParent

        tierInfoChildren = []
        # Find the childOf of the tier name
        for sC,pC,oC in g.triples((Ontology[name], Ontology.parentOf, None)):
            tierInfoChildren.append(rdflib.namespace.split_uri(oC)[1])
            # Find the name of the OT

        tierInformation['ParentOf'] = tierInfoChildren
        tierCharacteristics = []
        # Find the characteristics of the tier
        for subject,predicate,object in g.triples((Ontology[name], Ontology.characteristic, None)):
            # Find the name of the characteristic
            for sub2,pred2,obj2 in g.triples((object, w3Namespace.label, None)):
                instanceOfACharacteristic = {}
                instanceOfACharacteristic['Label'] = obj2
            # Find the datatype of the characteristic
            for sub2,pred2,obj2 in g.triples((object, Ontology.datatype, None)):
                dataType = rdflib.namespace.split_uri(pred2)[1]
                instanceOfACharacteristic[dataType] = obj2
            # Add to list of characteristics for the OT
            tierCharacteristics.append(instanceOfACharacteristic)
        # Add list of characteristics to OT
        tierInformation['Characteristics'] = tierCharacteristics
        organizationalTiers.append(tierInformation)

    return jsonify(OrganizeTiers(organizationalTiers))

def OrganizeTiers(organizationalTiers):
    #Set root
    get_allChildrenOf()

    otList = []
    for ot in organizationalTiers:
        if(str(ot['Name']) == str(root)):
            otList.append( ot )
            otList.extend(getChildTier(organizationalTiers, ot))
    return otList

def getChildTier(organizationTiers, parentObject):
    otList = []
    for ot in organizationTiers:
        if(str(ot['Name']) == str(parentObject['ParentOf'][0])):
            parent = ot
            #print(parent['ParentOf'])
            otList.append( ot )
            if (parent['ParentOf'] == []):
                #print("no parent")
                return otList
            otList.extend(getChildTier(organizationTiers, parent))
            return otList

def get_allcharacteristics():
    tupleslist = []
    #ID key
    #for each triple in the graph
    #for s,p,o in g:#.triples(None, 'greh', None):
    for s,p,o in g.triples((None, None , Ontology.organizational_tier)):
        name = rdflib.namespace.split_uri(s)[1]
        for s1,p1,o1 in g.triples((Ontology[name], Ontology.characteristic, None)):
            #print(s1, p1, o1)
            for s2,p2,o2 in g.triples((o1, w3Namespace.label, None)):
                #print(o2)
                #characteristic1 = rdflib.namespace.split_uri(o1)[1]
                #newSPO = {'Organizational Tier': name, 'characteristic': o1}
                newSPO = {'Organizational Tier': name, 'Characteristic': o1, 'Name': o2}
                tupleslist.append(newSPO)
        #tupleslist[p] = 'p'

    #format and return triples
    return jsonify(tupleslist)

def get_predicates():
    tupleslist = []
    #ID key
    #for each triple in the graph
    #for s,p,o in g:#.triples(None, 'greh', None):
    for s,p,o in g:
        newSPO = {'p': p}
		#tupleslist[p] = 'p'
        tupleslist.append(newSPO)
    #format and return triples
    return jsonify(tupleslist)

def get_tests1():
    jsonObject = get_generic(None, None, None, True)
    return jsonObject

def get_allsubjects():
    allSubjects = get_subjects_list()
    return jsonify(allSubjects)

def getHierarchy():
    # excessive computing extra stuff,
    # but it defines the root
    get_allChildrenOf()
    thisThing = []
    # return everything having to do with the root
    root_items = json.loads(json.dumps((get_generic(Ontology[root], None, None, False))))
    id=0
    #iterate the items returned by get_generic()
    for item in root_items:
        # print(Ontology.characteristic)
        # print(item['p'])
        # if it's a characteristic, ignore it!
        # item['p'] finds the p item, short for predicate and compares it to
        # the Namespace (Ontology) + characteristic
        if(str(item['p']) != str(Ontology.characteristic)):
           thisThing.append({"id": id, "o": item['o'], "p": item['p'], "s": item['s']})
           id = id + 1
        # if (str(item['p']) != str(Ontology.parentOf)):
        #     thisThing = json.dumps(appendChildren(item))

    return jsonify(thisThing)

def get_allChildrenOf():
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
            # grabs the term after the namespace
            childOf = parents[0]["o"].split('#')[-1]
            allChildrenOf.append({'subject': subject, 'childOf': childOf})
            childrenWithParents.append(subject)
    # This for loop iterates though the subjects that were found to have parents,
    # grabs the parent, and checks to see if that parent is in the list of children with parents.
    # If it doesn't have a parent, it is the root node and defined as such.
    for subject in allChildrenOf:
        subject = subject["childOf"]
        if subject not in childrenWithParents:
            global root
            root = subject
    # component -> deployment -> system -> site -> site_network : site_network = root
    return jsonify(allChildrenOf)

def get_namespaces():
    all_ns = [n for n in g.namespace_manager.namespaces()]
    return jsonify(all_ns)

def get_json():
    jsonObject = get_generic(Ontology.site, None, None, True)
    #print(str(rdflib.namespace.split_uri(Ontology.site)[0])) # URI
    #print(str(rdflib.namespace.split_uri(Ontology.site)[1])) # name
    return jsonObject

def get_triples():
    jsonObject = get_generic(None, None, None, True)
    return jsonObject

def index():
    return  "Hello, NRDC!"

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

def appendChildren(item):
    # children = []
    # predicate = str(item['p']).split('#')[-1]
    # print(predicate)
    # if[str(predicate) == "parentOf"]:
    #     children.append(appendChildren(get_generic(Ontology[predicate], None, None, False)))
    # else:
    #     return ""
    # return children
    return None
