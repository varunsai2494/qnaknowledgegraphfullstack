from neo4j.v1 import GraphDatabase, basic_auth
import json
driver = GraphDatabase.driver("bolt://localhost")
session = driver.session()
# the_dark_knight.json
#batman_begins
#dark_knight_rises
#inception
#interstellar
import re
def _lowercase(obj):
    """ Make dictionary lowercase """
    if isinstance(obj, dict):
        return {k.lower(): _lowercase(v) for k, v in obj.iteritems()}
    elif isinstance(obj, list):
        return [_lowercase(k) for k in obj]
    elif isinstance(obj, basestring):
        return obj.encode('ascii','ignore').lower()
    else:
        return obj
# aa = re.sub(r'[?|$|.|%|^|&|*|(|)|!|@|#|$|%|_|}|{|!]', '', "Richard M. Daley")
for item in ["the_dark_knight.json","inception.json","interstellar.json","batman_begins.json","dark_knight_rises.json"]:
    with open(item,"rb") as f:
        interstellardata = json.load(f)

    interstellardata = _lowercase(interstellardata)
    FM = {1:"Female",2:"Male",0:"Unknown"}
    for i in interstellardata["credits"]["crew"]:
        i["gender"]=FM[i["gender"]]
        i["job"] = i["job"].replace(' ','_')+"_at"
    for i in interstellardata["credits"]["cast"]:
        i["gender"]=FM[i["gender"]]
    insert_query = "UNWIND {pairs} as pair MERGE (TheMatrix:Movie {title:pair.original_title, released:pair.release_date, tagline:pair.tagline})"
    session.run(insert_query,parameters={"data":interstellardata["original_title"],"pairs":[interstellardata],"genres":interstellardata["genres"],"keywords":interstellardata["keywords"]["keywords"],"production_companies":interstellardata["production_companies"],"crew":interstellardata["credits"]["crew"],"cast":interstellardata["credits"]["cast"]})

    insert_query1 = "UNWIND {genres} as genre MATCH (TheMatrix:Movie {title:{data}}) MERGE (Genres:Genre {name:genre.name}) MERGE (TheMatrix)-[:has_a]->(Genres);"
    session.run(insert_query1,parameters={"data":interstellardata["original_title"],"pairs":[interstellardata],"genres":interstellardata["genres"],"keywords":interstellardata["keywords"]["keywords"],"production_companies":interstellardata["production_companies"],"crew":interstellardata["credits"]["crew"],"cast":interstellardata["credits"]["cast"]})

    insert_query2 = "UNWIND {keywords} as keyword MATCH (TheMatrix:Movie {title:{data}}) MERGE (Keywordd:Keyword {name:keyword.name}) MERGE (TheMatrix)-[:has_a]->(Keywordd);"
    session.run(insert_query2,parameters={"data":interstellardata["original_title"],"pairs":[interstellardata],"genres":interstellardata["genres"],"keywords":interstellardata["keywords"]["keywords"],"production_companies":interstellardata["production_companies"],"crew":interstellardata["credits"]["crew"],"cast":interstellardata["credits"]["cast"]})

    insert_query3 = "UNWIND {production_companies} as prodcomp MATCH (TheMatrix:Movie {title:{data}}) MERGE (Prodcompany:Company {name:prodcomp.name}) MERGE (TheMatrix)-[:produced]->(Prodcompany);"
    session.run(insert_query3,parameters={"data":interstellardata["original_title"],"pairs":[interstellardata],"genres":interstellardata["genres"],"keywords":interstellardata["keywords"]["keywords"],"production_companies":interstellardata["production_companies"],"crew":interstellardata["credits"]["crew"],"cast":interstellardata["credits"]["cast"]})

    insert_query5 = "UNWIND {cast} as genres MATCH (TheMatrix:Movie {title:{data}}) MERGE (Genres:Person {name:genres.name,gender:genres.gender}) MERGE (TheMatrix)-[:acted_in {character:genres.character,generic_type:'job'}]->(Genres);"
    session.run(insert_query5,parameters={"data":interstellardata["original_title"],"pairs":[interstellardata],"genres":interstellardata["genres"],"keywords":interstellardata["keywords"]["keywords"],"production_companies":interstellardata["production_companies"],"crew":interstellardata["credits"]["crew"],"cast":interstellardata["credits"]["cast"]})

    # insert_query = ' WITH 1 as dummy '.join([insert_query,insert_query1,insert_query2,insert_query3,insert_query5])
    # session.run(insert_query,parameters={"pairs":[interstellardata],"genres":interstellardata["genres"],"keywords":interstellardata["keywords"]["keywords"],"production_companies":interstellardata["production_companies"],"crew":interstellardata["credits"]["crew"],"cast":interstellardata["credits"]["cast"]})

    insert_query4 = ''
    for n in interstellardata["credits"]["crew"]:
        job = re.sub(r'''[?|$|.|%|^|&|*|(|)|!|@|#|$|%|~|}|{|!|'|"|+|=|/|\|;|:|>|<|]''', '', n["job"]).lower().replace("-", "")
        insert_query4 = '''MATCH (TheMatrix:Movie {title:{data}}) MERGE (Genres:Person {name:"'''+n["name"].lower()+'''",gender: "'''+n["gender"].lower()+'''"})''' + ''' MERGE (TheMatrix)-[:'''+job +''' {department:"'''+n["department"].lower()+'''",generic_type:"job"}]->(Genres);'''
        # print insert_query4
        session.run(insert_query4,parameters={"data":interstellardata["original_title"],"pairs":[interstellardata],"genres":interstellardata["genres"],"keywords":interstellardata["keywords"]["keywords"],"production_companies":interstellardata["production_companies"],"crew":interstellardata["credits"]["crew"],"cast":interstellardata["credits"]["cast"]})
        createNodeperformance="match(n:Movie)-[p]->(m:Person) set n.performance_good=0,n.performance_bad=0,n.performance_neutral=0,p.performance_good=0,p.performance_bad=0,p.performance_neutral=0"
        session.run(createNodeperformance)
# insert_query4 = "MATCH (TheMatrix:Movie) UNWIND {crew} as genres MERGE (Genres:Person {name:genres.name,gender:genres.gender}) MERGE (TheMatrix)-[:{genres.job} {department:genres.department,generic_type:job}]->(Genres);"


# insert_query = ' WITH 1 as dummy '.join([insert_query,insert_query1,insert_query2,insert_query3,insert_query4,insert_query5])
# print insert_query
# insert_query = "UNWIND {pairs} as pair MERGE (TheMatrix:Movie {title:pair.original_title, released:pair.release_date, tagline:pair.tagline})"
# insert_query = "MATCH (TheMatrix:Movie) UNWIND {genres} as genre MERGE (Genres:Genre {name:genre.name}) MERGE (TheMatrix)-[:has_a]->(Genres);"
# insert_query = "MATCH (TheMatrix:Movie) UNWIND {keywords} as keyword MERGE (Keywordd:Keyword {name:keyword.name}) MERGE (TheMatrix)-[:has_a]->(Keywordd);"
# insert_query = "MATCH (TheMatrix:Movie) UNWIND {production_companies} as prodcomp MERGE (Prodcompany:Company {name:prodcomp.name}) MERGE (TheMatrix)-[:has_a]->(Prodcompany);"
# insert_query = "MATCH (TheMatrix:Movie) UNWIND {crew} as genres MERGE (Genres:Person {name:genres.name,gender:genres.gender}) MERGE (TheMatrix)-[:genres.job {department:genres.department,generic_type:job}]->(Genres);"
# insert_query = "MATCH (TheMatrix:Movie) UNWIND {cast} as genres MERGE (Genres:Person {name:genres.name,gender:genres.gender}) MERGE (TheMatrix)-[:acted_in {character:genres.character,generic_type:job}]->(Genres);"

# insert_query = "UNWIND {pairs} as pair CREATE (TheMatrix:Movie {title:pair.original_title, released:pair.release_date, tagline:pair.tagline}) WITH UNWIND {genre} as genres MERGE (Genres:Genre {name:genres.name}) CREATE (TheMatrix)-[:Genres]-(Genres);"
# insert_query = "UNWIND {pairs} as pair UNWIND {pair.production_companies} as prodcomp CREATE (TheMatrix:`Production companies` {name:prodcomp.name})"

# data = [["Jim",10,"Mike",12],["Jim",10,"Billy",13],["Anna",14,"Jim",10],
#           ["Anna",14,"Mike",12],["Sally",10,"Anna",14],["Joe",11,"Sally",10],
#           ["Joe",11,"Bob",11],["Bob",11,"Sally",10]]


# session.run(insert_query,parameters={"pairs":[interstellardata],"genres":interstellardata["genres"],"keywords":interstellardata["keywords"]["keywords"],"production_companies":interstellardata["production_companies"],"crew":interstellardata["credits"]["crew"],"cast":interstellardata["credits"]["cast"]})

