from datetime import date

def getLinesOfFile(f) :
    """
    get the lines of a file.
    :param f: the file to get lines.
    :rtype: list
    :return: lines of the file.
    """
    readFile = open(f, "r")
    lines = readFile.readlines()
    readFile.close()
    return lines

def getMonth() :
    """
    return the actualy month.
    :rtype: str
    :return: acutaly month in French.
    """
    month = int(str(date.today()).split("-")[1])
    months = ["Janvier" , "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    return months[month-1]

def notDoubleInListAndSort(l) :
    """
    return list wihtout double, and sorted. (used in combobox).
    :param l: the list to sorted and remove double.
    :rtype: list
    :return: sorted list without double.
    """
    ll = list(set(l))
    ll.sort()
    return ll

def writeInFile(f, res) :
    """
    write in file.
    :param f: file to write. 
    :param res: what write on the file.
    """
    fileToWrite = open(f, "w")
    fileToWrite.write(res)
    fileToWrite.close()