import genLib as gl

def takeValuesCombobox(i, f) :
    """
    take the line of the file to put it in the combobox.
    :param i: the index to take the name (0) or the firstname (1).
    :param f: the file to read the name and firstname's workers.
    :rtype: list
    :return: the list of all names or all firstnames.
    """
    res = []
    lines = gl.getLinesOfFile(f)
    for l in lines :
        worker = l.split(";")
        workerValue = worker[i]
        res.append(workerValue)
    return res

def addWorkerNameDataBase(name, firstName, fileWorkerName, fileWorkerHour) :
    """
    add the worker at the databse.
    :param name: the worker's name.
    :param firstName: the worker's firstname.
    :param fileWOrkerName: the path to the file to get name and firstname's worker.
    :param fileWorkerHour: the path to the fileto get work hours, to add the name on this file.
    :rtype: str
    :return: message to check the adding.
    """
    if name == "" :
        return "name"
    elif firstName == "" :
        return "firstname"
    else :
        res = ""
        add = False
        lines = gl.getLinesOfFile(fileWorkerName)
        if lines == [] : #if the file is empty, add name and firstname directly.
            #for name
            gl.writeInFile(fileWorkerName, name + ";" + firstName + ";\n")
            #for hour
            gl.writeInFile(fileWorkerHour, name + ";" + firstName + ";\n")
            return "okAddWorker"
        for l in lines : #else, add them in alphabetical order.
            line = l.split(";")
            if not add and line[0] == name and line[1] == firstName : #same name and firstname.
                return "double" 
            if not add and line[0] > name : #
                res += name + ";" + firstName + ";\n" + l
                add = True
            elif not add and line[0] == name :
                if line[1] > firstName :
                    res += name + ";" + firstName + ";\n" + l
                    add = True
                else :
                    res += l
            else :
                res += l
        if not add :
            res += name + ";" + firstName + ";\n"
        #for name
        gl.writeInFile(fileWorkerName, res)
        #for hour
        fileWorker = open(fileWorkerHour, "a")
        fileWorker.write(name + ";" + firstName + ";\n")
        fileWorker.close()
        return "okAddWorker"

def removeWorkerNameDataBase(name, firstName, fileWorkerName) :
    """
    remove worker off the database.
    :param name: the worker's name.
    :param firstName: the worker's firstname.
    :param fileWOrkerName: the path to the file to get name and firstname's worker.
    :rtype: str
    :return: message to check the removing.
    """
    if name == "" :
        return "name"
    elif firstName == "" :
        return "firstname"
    else :
        res = ""
        remove = False
        lines = gl.getLinesOfFile(fileWorkerName)
        for l in lines :
            line = l.split(";")
            nameFile = line[0]
            firstNameFile = line[1]
            if not(name == nameFile and firstName == firstNameFile) : #if not the worker ti remove, write the line.
                res += l
            else : #else, do nothing to not write the line.
                remove = True 
        gl.writeInFile(fileWorkerName, res)
        if remove :
            return "okRemoveWorker"
        else :
            return "remove"