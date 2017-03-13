## OpenStreetMap Data Wrangling with SQL

## Map Area: Jerusalem, Israel

The reason why I pick Israel is because in this 8,019 mi² country. It contains geographically diverse features within its relatively small area and also the most arguable religions history. From Judaism, Islam, Christianity and Druzism. 

# 1. Problems

from the tag analysis:
{'problemchars': 1, 
'lower': 120538, 
'other': 13502, 
'lower_colon': 43343}

Then I found lots of affiliation with group of number begins with U followed behind it. 
u'Aljoz': set([u'\u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0635\u0646\u0627\u0639\u064a\u0629  ending of the Industrial zone Wadi Aljoz']),
u'school': set([u'\u0634\u0627\u0631\u0639 \u0641\u0631\u0639\u064a / \u0637\u0631\u064a\u0642 \u0645\u062e\u062a\u0635\u0631 \u0644\u0644\u0645\u062f\u0631\u0633\u0629 A side street / shortcut to the school']),


However, the end with the explanations at the end such as the industrial zone or shortcut to the school, shouldn’t be worry about it. 

Other than that, I found the data is pretty reliable. 
They are transform into this json format. 
710686 {'created': {'changeset': '22153763',
              'timestamp': '2014-05-05T19:51:57Z',
              'uid': '385027',
              'user': 'Ori952',
              'version': '5'},
  'id': '29942465',
  'pos': [31.7766745, 35.22721],
  'type': 'node'}
 {'building': 'yes',
  'created': {'changeset': '41795805',
              'timestamp': '2016-08-30T09:52:18Z',
              'uid': '189946',
              'user': 'BMM994',
              'version': '1'},
  'id': '439863338',
  'node_refs': ['4375400348',
                '4375400293',
                '4375400279',
                '4375400264',
                '4375400300',
                '4375400262',
                '4375400294',
                '4375400254',
                '4375400249',
                '4375400263',
                '4375400325',
                '4375400353',
                '4375400351',
                '4375400329',
                '4375400350',
                '4375400276',
                '4375400352',
                '4375400290',
                '4375400304',
                '4375400336',
                '4375400334',
                '4375400330',
                '4375400332',
                '4375400348'],  'type': 'way'}


There are also 513 users contribute from this osm file.

# 2. Data Overview
'''
File sizes:
Jerusalem_israel.osm 				132.3 MB
Jerusalem_israel.osm.json	  			154.8 MB


Summary count of jerusalem_israel.osm from xml file
{'bounds': 1,  
'member': 3881,  
'nd': 716073,  
'node': 645370,  
'osm': 1,  
'relation': 535,  
'tag': 177384,  
'way': 65316}
'''


Data source:
open street: 'http://www.openstreetmap.org/relation/1473946'
wiki 'http://wiki.openstreetmap.org/wiki/WikiProject_Israel'

