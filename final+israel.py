
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
        tags={}
        for action,elem in ET.iterparse(filename):
            if elem.tag in tags:
                tags[elem.tag]=tags[elem.tag]+1
            else:
                tags[elem.tag]=1
            elem.clear()
        return tags

pprint.pprint(count_tags('jerusalem_israel.osm'))


# In[2]:

import xml.etree.ElementTree as ET
import pprint
import re


#defining regular expressions for quality check
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#going through tag and check against RegEx
def key_type(element, keys):
    if element.tag == "tag":
        value = element.attrib['k']
        if re.search(problemchars,value):
            keys['problemchars']=keys['problemchars']+1
        elif re.search(lower_colon,value):
            keys['lower_colon']=keys['lower_colon']+1
        elif re.search(lower,value):
            keys['lower']=keys['lower']+1
        else:
            keys['other']=keys['other']+1
        pass
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

print process_map('jerusalem_israel.osm')


# In[3]:

import xml.etree.ElementTree as ET
import pprint
import re


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        for e in element:
            if 'uid' in e.attrib:
                users.add(e.attrib['uid'])

    return users
users = process_map('jerusalem_israel.osm')
print len(users), "users in osm file in total"


# In[4]:

def find_elem_kval(kvals_to_inspect):    
    context = ET.iterparse('jerusalem_israel.osm', events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in ('node', 'way', 'relation'):
            for tag in elem.findall("tag"):
                if (tag.get("k") in kvals_to_inspect):
                    print elem.tag+" id:"+elem.attrib["id"]
                    for tag in elem.findall("tag"):
                        print "\t"+tag.tag+": k="+tag.get("k"), "v="+tag.get("v")
                    print "***********************************************"
            root.clear()

find_elem_kval(["FIXME"])
print ""
find_elem_kval(["addr:street2","addr2:street"])
print ""
find_elem_kval(["name:be-tarask"])


# In[5]:


import xml.etree.cElementTree as ET
import codecs
from collections import defaultdict
import re
import pprint

OSMFILE = 'jerusalem_israel.osm'
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Lane"]
# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            'Rd.': 'Road',
            'Ave': 'Avenue',
            'Pkwy': 'Parkway',
            'Dr': 'Drive',
            'Dr.': 'Drive',
            'Exressway': 'Expressway',
            'Expessway': 'Expressway',
            'Trl': 'Trail',
            'Blvd': 'Boulevard',
            'Blvd.': 'Boulevard',
            }
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# returns true if an element contains a street value
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# function that reads osm file line by line and finds street names to audit
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

# function to change incorrect street types to correct street types
def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = name.replace(street_type, mapping[street_type])

    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types)) #print out dictonary of potentially incorrect street types

    for st_type, ways in st_types.iteritems():
        for name in ways:
            if street_type_re.search(name).group() in mapping:
                better_name = update_name(name, mapping)
                print name, "=>", better_name #print out street names that were changed

if __name__ == '__main__':
    test()


# In[6]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
from pymongo import MongoClient


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def is_address(elem):
    if elem.attrib['k'][:5] == "addr:":
        return True



def shape_element(element):
    node = {}

    if element.tag == "node" or element.tag == "way" :

      node['type'] = element.tag

      # Parse attributes
      for a in element.attrib:
        if a in CREATED:
          if 'created' not in node:
            node['created'] = {}
          node['created'][a] = element.attrib[a]

        elif a in ['lat', 'lon']:
          if 'pos' not in node:
            node['pos'] = [None, None]

          if a == 'lat':
            node['pos'][0] = float(element.attrib[a])
          else:
            node['pos'][1] = float(element.attrib[a])

        else:
          node[a] = element.attrib[a]

      # Iterate tag children
      for tag in element.iter("tag"):
        if not problemchars.search(tag.attrib['k']):
          # Tags with single colon
          if lower_colon.search(tag.attrib['k']):

            # Single colon beginning with addr
            if tag.attrib['k'].find('addr') == 0:
              if 'address' not in node:
                node['address'] = {}

              sub_attr = tag.attrib['k'].split(':', 1)
              node['address'][sub_attr[1]] = tag.attrib['v']

            # All other single colons processed normally
            else:
              node[tag.attrib['k']] = tag.attrib['v']

          # Tags with no colon
          elif tag.attrib['k'].find(':') == -1:
            node[tag.attrib['k']] = tag.attrib['v']

      # Iterate nd children
      for nd in element.iter("nd"):
        if 'node_refs' not in node:
          node['node_refs'] = []
        node['node_refs'].append(nd.attrib['ref'])

      return node
    else:
      return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('jerusalem_israel.osm', False)
    print len(data)
    pprint.pprint(data[10])
    pprint.pprint(data[-10])
    

if __name__ == "__main__":
    test()


# In[17]:

#!/usr/bin/env python

import json
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client.openstreetmap

def insert_json(infile, db):
    jsonfile=open(infile)
    for dic in jsonfile:
        data=json.loads(dic)
        db.maps.insert_one(data)
insert_json('jerusalem_israel.osm.json',db)


# In[22]:

client = MongoClient('localhost:27017')
db = client.peru
collection = db.map_data

with open('jerusalem_israel.osm.json', 'r') as f:
    for row in f:
        data = json.loads(row)
        db.map_data.insert(data)


# In[62]:

database_stats = db.command("dbstats")
userids = collection.distinct("created.uid")

# find number of elements associated with each user and outputs the latest timestamp associated with each user
user_contribution = collection.aggregate([{"$group": {"_id": "$created.user","entries": {"$sum":1}, "max":{"$max":"$created.timestamp"}}},
                      {"$sort": {"entries":-1}}])

# data for users that have contributed less than 10 elements to the data set
userslt10_contribution = collection.aggregate([{"$group": 
                                                    {"_id": "$created.user","entries": {"$sum":1}, 
                                                     "max":{"$max":"$created.timestamp"}}},
                      {"$match": {"entries":{"$lt":10}}},
                      {"$sort":{"max":-1}}])

# WAY AND NODE ELEMENT ANALYSIS
# outputs distinct element types in data set: only should output way and node
element_types = collection.distinct("type")

# total documents in the database
element_count = collection.count()

# counts number of elements created by year
timestamps = collection.aggregate([{"$group": {"_id": {"$substr": ["$created.timestamp", 0, 4]}, "count":{"$sum":1}}},
                                   {"$sort": {"_id":1}}])


# AMENITY ANALYSIS: SCHOOLS, CHURCHES, RESTAURANTS, ETC.
# list of all amenities included in the data base
distinct_amenity = collection.distinct("amenity")

# counts of entries for each amenity type
amenity_count = collection.aggregate([{"$match": {"amenity":{"$exists":1}}},
                      {"$group": {"_id": "$amenity", "count":{"$sum":1}}},
                      {"$sort": {"count":-1}}])


# In[52]:

print database_stats


# In[53]:

print(list(user_contribution))


# In[37]:

print element_types


# In[38]:

print element_count


# In[41]:

print (list(timestamps))


# In[44]:

print distinct_amenity 


# In[48]:

print (list(amenity_count))

