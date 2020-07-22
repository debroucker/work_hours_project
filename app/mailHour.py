import genLib as gl
from datetime import date 
import webbrowser
import time

def hoursDataBase(workerFile, hourFile, cssFile, show=True) :
    """
    write an html file with all work hours of all workers.
    :param workerFile: the path to the file with work hours.
    :param hourFile: the path to the html file, to write on it.
    :param cssFile: the path to the css, to write it in the html file. (when the html file is sended by email, we don't need to send the css file).
    :param show: default, true, to show the html file. (false when the html file is sended by email).
    """
    lines = gl.getLinesOfFile(workerFile)
    res = "<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>Heure des ouvriers du mois de" + gl.getMonth() + "</title>" 
    #read the css file to write it on the html file.
    f = open(cssFile, "r")
    css = f.read()
    f.close()
    res += "<style>" + css + "</style>"
    res += "</head><body>"
    for l in lines :
        line = l.split(";")
        name = line[0]
        firstName = line[1]
        res += "<p id='worker'>" + name + " " + firstName + "</p><table><tbody><tr><td id='date'>Date</td><td id='hour'>Nombre d'heure</td><td id='mg'>MG</td></tr>"
        sumHour = 0
        sumMG = 0
        lineLen = len(line)
        for i in range(2,lineLen) :
            try : 
                construction = line[i].split(":")
                d = construction[0]
                year = d[0:4]
                month = d[5:7]
                day = d[8:10]
                nbHour = construction[1]
                mg = construction[2]
                sumHour += float(nbHour)
                sumMG += float(mg)
                res += "<tr><td>" + day + "/" + month + "/" + year + "</td><td>" + nbHour + "</td><td>" + mg + "</td></tr>"
            except :
                None
        res += "<tr><td>Totaux</td><td>" + str(sumHour) + "</td><td>" + str(sumMG) + "</td></tr>"
        res += "</tbody></table>"
    res += "</body></html>"
    gl.writeInFile(hourFile, res)
    if show :
        webbrowser.open(hourFile)

def emptyHour(hourFile, fileNameWorker) :
    """
    to empty the file with work hours at the end of the month, and write the worker's name and firstname.
    :param hourFile: the path to the file with work hours.
    :param fileNameWorker: the path to the file with name and firstname workers.
    """
    lines = gl.getLinesOfFile(fileNameWorker)
    res = ""
    for l in lines :
        line = l.split(";")
        res += line[0] + ";" + line[1] + ";\n" 
    fileSendHour = open(hourFile, "w")
    fileSendHour.write(res)
    fileSendHour.close()
