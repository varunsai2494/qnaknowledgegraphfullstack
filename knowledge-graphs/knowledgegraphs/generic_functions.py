

def doubleMatch(string, substringarray):
    string =string.replace(","," , ").replace("."," . ")
    match=[item for item in substringarray if  str(" "+str(item).lower().strip()+" ") in str(" "+str(string).lower().strip()+" ")]
    return match

def doubleMatchWithNoDuplicates(string, substringarray):
    string =string.replace(","," , ").replace("."," . ")
    temp = sorted(substringarray, key=lambda t: t.count(" "), reverse=True)
    match=[]
    for item in temp:
        if str(" " + str(item).lower().strip() + " ") in str(" " + str(string).lower().strip() + " "):
            match.append(item)
            string=string .replace(item," ")
    return match



