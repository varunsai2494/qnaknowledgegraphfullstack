import re
import json
import constants
import app
import neo4jNodeList as neo
from itertools import combinations


import generic_functions as genfunc
def determineTypeOfQuestion(question):
    questionWords=constants.questionWords.keys()
    typeOfQuestion=genfunc.doubleMatch(question,questionWords)
    if typeOfQuestion:
        return typeOfQuestion[0]
    else:
        return None

def determineidentifier(question,questionWord):
    questionWords=constants.questionWords
    conditionalChecks=questionWords[questionWord]
    identifier=None
    for key,value in conditionalChecks.iteritems():
        if genfunc.doubleMatch(question,value):
            identifier=key
            break
    return identifier

def determineRelationWithMovie(question):
    listOfRelations=app.doubleMatchTheRelationWithMovie(question)
    if listOfRelations:
        return app.doubleMatchTheRelationWithMovie(question)
    else:
        return []

def determineActorstalkedAbout(sentence):
    actors_movie=neo.getAllNodes()
    actors=[item for item in actors_movie if str(item[1])=="Person"]
    actorsFound=genfunc.doubleMatch(sentence,[item[0] for item in actors])
    ActorsFoundwithS=[i.replace("'s","") for i in (genfunc.doubleMatch(sentence,[str(str(item[0]).strip()+"'s") for item in actors]))]
    return list(set(actorsFound+ActorsFoundwithS))

def determineMovieTalkedAbout(sentence):
    actors_movie = neo.getAllNodes()
    movies = [item for item in actors_movie if str(item[1]) == "Movie"]

    if sentence:
        for item in movies:
            m= re.search("(^)the|The</b>",item[2])

            if m:
                movieNameWithoutThe=" ".join((str(item[2]).strip().split(" ")[1:]))
                if item[2] in sentence:
                    pass
                elif movieNameWithoutThe in sentence:
                    sentence= str(sentence).replace(str(movieNameWithoutThe),str(item[2]))

    print sentence
    moviesFound = genfunc.doubleMatch(sentence, [item[2] for item in movies])
    if moviesFound:
        moviesFoundTemporary=sorted(moviesFound, key=lambda time: len(time), reverse=True)
        print moviesFoundTemporary
        length=len(moviesFoundTemporary)
        temp=[]
        if length>1:
            for i in range(len(moviesFoundTemporary)):
                for j in moviesFoundTemporary[i+1:]:
                    if str(j) in str(moviesFoundTemporary[i]):
                        temp.append(j)

            moviesFound=list(set(moviesFoundTemporary)-set(temp))
        else:
            pass
        print moviesFound


    return moviesFound

def stringfilter(text):
    print text
    text = " ".join(filter(None, text.split(" ")))
    a = [[",", " , "], [".", " . "], ["?", " ? "], ["!", " ! "], ["-", ""]]
    for i in a:
        text = text.replace(i[0], i[1])
    text = " ".join(filter(None, text.split(" ")))
    return text

######### functions that determine the answer from graph db
def who(question):
    outputString=""
    relationsDict = constants.relationWithMovie
    identifier = determineidentifier(question, "who")
    if not identifier:
        identifier="plural"
    relationList = determineRelationWithMovie(question)


    movie=determineMovieTalkedAbout(question)
    if relationList and movie:
        for movieitem in movie:
            for item in list(set(relationList)):
                result = neo.queryGraphDbWho(str(item),str(movieitem))
                if len(result):
                    if identifier and identifier == "plural":
                        partialOutput = str((",").join([i["name"] for i in result]) + str(" " + relationsDict[item][0]) + " this movie.\n")
                    else:
                        partialOutput = str(result[0]["name"] + str(" " + relationsDict[item][0]) + " this movie.\n")
                else:
                    partialOutput = ""
                outputString = outputString + partialOutput
    if outputString:
        return outputString
    else:
        return "Sorry I couldn't find what you are looking for"

#algo
# 1.extract film names
# 2.extract person names
# 3.search person names in string (write a generic function for this)
# 4.search movie names
# 5.if you get 2 actors and 2 roles
# 6.validate the two relations if they seem fine give the concat answer

def how(question):
    outputString=""
    partialstring=""
    relationList = determineRelationWithMovie(question)
    peopleFound=determineActorstalkedAbout(question)
    movieFound=determineMovieTalkedAbout(question)
    dynamicloopBasedOnLEngthOfArrays = sorted({"relation": relationList, "person": peopleFound, "movie": movieFound}.items(), key=lambda temp: len(temp[1]), reverse=True)
    position={}
    print "varun"
    print dynamicloopBasedOnLEngthOfArrays
    for i in range(0,int(len(dynamicloopBasedOnLEngthOfArrays))):
        position[dynamicloopBasedOnLEngthOfArrays[i][0]]=i
    print position
    print dynamicloopBasedOnLEngthOfArrays
    if dynamicloopBasedOnLEngthOfArrays[0][1]:
        for i in list(set(dynamicloopBasedOnLEngthOfArrays[0][1])):
            if dynamicloopBasedOnLEngthOfArrays[1][1]:
                for j in list(set(dynamicloopBasedOnLEngthOfArrays[1][1])):
                    if dynamicloopBasedOnLEngthOfArrays[2][1]:
                        for k in list(set(dynamicloopBasedOnLEngthOfArrays[2][1])):
                            m=[i,j,k]
                            movie=m[int(position["movie"])]
                            person=m[int(position["person"])]
                            relation=m[int(position["relation"])]
                            output=neo.queryGraphDbHow(relation,person,movie)
                            if output:
                                for item in output:
                                    partialstring = person + "'s " + str(
                                        constants.relationWithMovie[relation][1]) + " got " + str(
                                        item["good"]) + " likes , " + str(item["bad"]) + " dislikes and " + str(
                                        item["neutral"]) + " neutral responses.\n"
                                    print i,j,k
                                    print "v1"
                                    outputString = outputString + partialstring
                    else:
                        k=None
                        m = [i, j, k]
                        movie = m[int(position["movie"])]
                        person = m[int(position["person"])]
                        relation = m[int(position["relation"])]
                        output=neo.queryGraphDbHow(relation, person, movie)
                        if output:
                            if int(position["person"])==2:
                                goodscore=badscore=neutralscore=0
                                goodscore=[item["good"] for item in output if item["good"]]
                                badscore = [item["bad"] for item in output if item["bad"]]
                                neutralscore = [item["neutral"] for item in output if item["neutral"]]
                                a=sum(goodscore)
                                b=sum(badscore)
                                c=sum(neutralscore)
                                partialstring=str(constants.relationWithMovie[relation][1])+" in  "+str(movie)+" got "+ str(a) +" likes ,"+str(b) +" dislikes "+str(c) +" responses\n"
                                outputString=outputString+partialstring
                                print "v2"
                                print i,j,k
                            else:
                                for item in output:
                                    print item
                                    partialstring = person  + " got " + str(
                                        item["good"]) + " likes , " + str(item["bad"]) + " dislikes and " + str(
                                        item["neutral"]) + " neutral responses for his role in "+str(item["moviename"])+"\n"
                                    print "v3"
                                    print i, j, k
                                    outputString = outputString + partialstring

            else:
                j=k=None
                m = [i, j, k]
                print i,j,k
                movie = m[int(position["movie"])]
                person = m[int(position["person"])]
                relation = m[int(position["relation"])]
                output=neo.queryGraphDbHow(relation, person, movie)
                print output
                if output:
                    for item in output:
                        partialstring= movie+" got "+str(item["good"])+" likes , "+str(item["bad"])+" dislikes and "+str(item["neutral"])+" neutral responses.\n"
                        print "v4"
                        print i, j, k
                        outputString=outputString+partialstring


    # for relation in relationList:
    #     for person in peopleFound:
    #         print relation,person,movieFound,"varun"
    #         output=neo.queryGraphDbHow(relation,person,movieFound)
    #     if output:
                # if movieFound:
                #     if not relation and not person:
                #         for item in output:
                #             partialstring=movie +" got "+str(item["good"])+" likes , "+str(item["bad"])+" dislikes and "+str(item["neutral"])+" neutral responses.\n"
                #             outputString = outputString + partialstring
                # else:

    if outputString and (outputString).strip():
        return outputString
    else:
        return "Sorry I couldn't find what you are looking for"


def what():
    print "what"


def when():
    print "when"

#############################################################

switchDictionary = {"who": who,"what" :what,"when" :when,"how":how}

def finalOutput(question):
    output = ""
    questiontype = determineTypeOfQuestion(question)
    if questiontype:
        output = switchDictionary[questiontype](question)
    return output


# print "OUTPUT"
# print "asking one  name"
# print finalOutput("who is the art director  dark knight ")
# print finalOutput("who are the actor in Batman Begins")
# print "Asking without is/are/was/were"
# print finalOutput("who directed Batman Begins")
# print "asking multiple questions"
# print finalOutput("who directed  batman begins and  list of all the actors")

##########how
# print finalOutput("how is the dark knight")
# print finalOutput("how is direction in the dark knight")
# print finalOutput("how did christian bale perform in the dark knight")
# print finalOutput("how did christian bale perform ")
# print finalOutput("how was the performance of christian bale , heath ledger and hans zimmer in the dark knight")
# print finalOutput("How was art direction in the dark knight")
