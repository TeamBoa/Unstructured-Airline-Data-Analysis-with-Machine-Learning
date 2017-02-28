# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:58:26 2017

@author: Aditya Gogoi
"""

import sys
sys.path.append('c:\python27\lib\site-packages')
import py2neo
from py2neo import Graph, Node, Relationship

py2neo.authenticate("localhost:7474","neo4j","neo4j1")
graph=Graph("http://localhost:7474/db/data/")

### Queries to create graph model of the analysed data

## Trial Query
results = graph.run(""" match (n:Author)-[:REVIEWED]->(o:Airline) where n.name="A Acosta" return n.o""")
for result in results:
    print(result)
    
## Competing Airlines

results = graph.run("""MATCH (o.Airline)<-[r:REVIEWED]-(n:Author)-[r1:REVIEWED]->(o1.Airline)
                    where o<>o1 return n.name, o.airlinename, o1.airlinename, r.ratingoverall, r.recommended, r.lsentiment,
                    r1.ratingoverall, r1.recommended, r1.lsentiment""")

for result in results:
    print(result)
    
## Raters with Common Interests
results=graph.run("""MATCH (n1:Author)-[r1:REVIEWED]->(a:Airline)
                    WITH a
                    MATCH (a)<-[REVIEWED]-(n2:Author)
                    RETURN DISTINCT (n2.name) as CommonTraveller, a.airlinename as CommonAirline""")

for result in results:
    print(result)
    
## Finding Raters who rated Similarly
results=graph.run("""MATCH (n1:Author)-[r1:REVIEWED]->(a:Airline)
                WITH a, r1, n1
                MATCH (a)<-[r2:REVIEWED]-(n2:Author)
                WHERE r2.lsentiment=r1.lsentiment AND
                0.9*r2.ratingoverall<=r1.ratingoverall<=1.1*r2.ratingoverall AND n1<>n2 AND r1<>r2
                RETURN DISTINCT n2.name as AuthorName, r2.lsentiment as CommonSentiment,
                r2.ratingoverall as CommonRating, a.airlinename as CommonAirline""")

for result in results:
    print(result)
