import genLib as gl

def addCityDataBase(city, mg, f) :
    """
    add city and this MG in databse.
    :param city: the name of the city.
    :pram mg: the MG.
    :param f: the work hours file.
    :rtype: str
    :return: message to check the adding.
    """
    if city == "" : #empty city.
        return "city" 
    elif mg == "" : #empty MG.
        return "mg" 
    elif "," in mg : #MG with comma.
        return "mg,"
    else : 
        try :
            res = ""
            add = False
            mg = float(mg)
            print(mg)
            lines = gl.getLinesOfFile(f)
            for l in lines :
                line = l.split(";")
                if not add and line[0] > city : #not add, and alphabetical order
                    res += city + ";" + str(mg) + "\n" + l
                    add = True
                else :
                    res += l
            if not add :
                res += city + ";" + str(mg) + "\n"
            gl.writeInFile(f,res)
            return "okAddCity" #city added.
        except :
            print("error")
            return "errorMG" #invalid MG.
