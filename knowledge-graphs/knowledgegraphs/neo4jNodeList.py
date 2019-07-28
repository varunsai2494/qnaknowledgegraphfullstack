from neo4j.v1 import GraphDatabase, basic_auth
import json
#function to return the list of all the nodes
driver = GraphDatabase.driver("bolt://localhost")
session = driver.session()

def getAllNodes():
    read_query = "MATCH (n) RETURN n.name as name,n.title as title,labels(n) as label"
    result=session.run(read_query)
    # nodeList = []
    # for i in result:
    #     if i['label'][0] in ["Movie","Person"] :
    #         try:
    #             nodeList.append([str(i["name"].encode('utf8')),i["label"][0],i["title"]])
    #         except:
    #             nodeList.append([str(i["name"]),i["label"][0],i["title"]])
    nodeList=[[str(record["name"]),record["label"][0],record["title"]] for record in result if record["label"][0] in ["Movie","Person"]]
    print nodeList
    # print "There are currently "+str(len(nodeList)) +" nodes"
    # print nodeList
    return nodeList



def queryGraphDbWho(relation,movie):
    print relation ,movie
    a="MATCH (n:Movie{title:'"+movie+"'})-[p:" + relation +" ]->(m) RETURN m.name as name,(p.performance_good+p.performance_bad+p.performance_neutral) AS cnt order by cnt desc"
    print a
    result = session.run(a)
    nodeList = [record for record in result]
    # b=sorted(nodeList.items(), key=lambda time: time[1]['time'], reverse=True)
    return nodeList

def queryGraphDbHow(relation,person,movie):
    print relation,person,movie,"varun"
    if movie:
        if person and relation:
            a = "match (n:Movie{title: " + str("'" + movie + "'") + "})-[p:" + relation + "]->(m:Person{name: " + str( "'" + person + "'") + "}) return distinct p.performance_good as good,p.performance_bad as bad,p.performance_neutral as neutral,n.title as moviename"
            print a

        elif (person and not relation):
            a = "match (n:Movie{title: " + str(
                "'" + movie + "'") + "})-[p]->(m:Person{name: " + str(
                "'" + person + "'") + "}) return distinct p.performance_good as good,p.performance_bad as bad,p.performance_neutral as neutral,n.title as moviename"
        elif not person and relation:
            a = "match (n:Movie{title: " + str(
                "'" + movie + "'") + "})-[p:" + relation + "]->(m:Person) return distinct p.performance_good as good,p.performance_bad as bad,p.performance_neutral as neutral,n.title as moviename"
        elif not (person or relation):
            a = "match (n:Movie{title: " + str("'" + movie + "'") + "})-[p]->(m) return distinct n.performance_good as good,n.performance_bad as bad,n.performance_neutral as neutral,n.title as moviename"
    else:
        if relation and not person:
            a="match (n)-[p:"+relation+"]->(m:Person) return distinct p.performance_good as good,p.performance_bad as bad,p.performance_neutral as neutral,n.title as moviename"

        elif  relation and not person:
            a="match (n)-[p:"+relation+"]->(m:Person) return distinct p.performance_good as good,p.performance_bad as bad,p.performance_neutral as neutral,n.title as moviename,type(p)"
        elif relation and  person:
            a = "match (n)-[p:" + relation + "]->(m:Person{name: " + str(
                "'" + person + "'") + "}) return distinct p.performance_good as good,p.performance_bad as bad,p.performance_neutral as neutral,n.title as moviename,type(p)"

    result = session.run(a)
    nodeList = [record for record in result]
    return nodeList


