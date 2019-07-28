import recipe
import json
#getting the verbs,noun grams,adjectives and pronouns
def tagwords(recipeoutput):
    tagwordsdictionary={}
    if "pos" in recipeoutput:
        # print "123"
        for item in recipeoutput["pos"]:
            print item
            if item["pos_tag"] in ["NOUN","VERB","ADJECTIVE","PRONOUN"]:
                if item["pos_tag"] in tagwordsdictionary:
                    tagwordsdictionary[item["pos_tag"]].append(str(item["word"]))
                else:
                    tagwordsdictionary[item["pos_tag"]]=[str(item["word"])]
        l=int(len(recipeoutput["pos"]))
        for i in range(int(l)):
            if i == l-1:
                break
            elif recipeoutput["pos"][i]["pos_tag"] == "NOUN":
                for j in range(i,l):
                    # print "123"
                    if recipeoutput["pos"][j]["pos_tag"] == "NOUN":
                        g=[k["word"] for k in recipeoutput["pos"][i:j+1]]
                        # print g
                        tagwordsdictionary["NOUN"].append(str(" ".join(g)))
                    else:
                        break

    return tagwordsdictionary

#recipe pos call
def getngrams(text):
    recipeoutput =recipe.callrecipe("pos","google",text)
    if recipeoutput:
        return tagwords(recipeoutput)
    else:
        return None


# print getngrams("fantastic movie to start off an era of christian bale")