from datetime import date
import genLib

def getHourInInt(h) :
    """
    get the hour of the hour given.
    :param h: the hour, to recup wihtout minutes.
    :rtype: float or str if was an error.
    :return: the hour and the minute in float, or an error message.
    """
    try :
        theHour = h.upper().split("H")
        hour = int(theHour[0])
        minute = getMinuteInInt(theHour[1])
        if minute == "errorMinute" :
            return "errorMinute"
        return hour + minute
    except :
        return "errorHour"
    
def getMinuteInInt(m) :
    """
    get the minutes of the hour given.
    :param m: the hour, to recup wihtout hours. It must be equal to 0, 15, 30 0r 45.
    :rtype: float or str if was an error.
    :return: the minute in float, or an error message.
    """
    if m not in ["", "0","00", "15", "30", "45"] :
        return "errorMinute"
    minute = 0
    if m == "15" :
        minute = 0.25
    elif m == "30" : 
        minute = 0.5
    elif m == "45" :
        minute = 0.75
    return minute

def takeMG(c, f) :
    """
    take the MG to the associeted city.
    :param c: the name of the city.
    :param f: the file includes the city and this MG.
    :rtype: float
    :return: the MG associted at the city.
    """
    lines = genLib.getLinesOfFile(f)
    mg = -1 #if not found city, mg = -1 to show error
    for l in lines :
        res = l.split(";")
        if res[0] == c :
            mg = res[1]
    return float(mg)

def checkParams(workerName, workerFirstName, workerArrivingTime, workerDepartureTime, workerMeal, fileWorkerHourPath) :
    """
    check params, to correct them.
    :param workerName: the worker's name.
    :param workerFirstName: the worker's firstname.
    :parzm workerArrivingTime: the arriving time.
    :param workerDepartureTime: the departure time.
    :param workerMeal: the meal time.
    :param fileWorkerHourPath: the path to the file includes the work hours of workers.
    :rtype: tuple (float, list), or str if was an error.
    :return: tuple of work hours of the day and the lines of the file given, or message error.
    """
    if workerName == "" :
        return "name"
    elif workerFirstName == "" :
        return "firstname"
    elif workerArrivingTime == "" :
        return "arriving"
    elif workerDepartureTime == "" :
        return "departure"
    elif  workerMeal == "" :
        return "meal"
    else :
        hourBegin = getHourInInt(workerArrivingTime)
        if hourBegin == "errorHour" or hourBegin == "errorMinute":
            return "errorHourBegin"
        hourEnd = getHourInInt(workerDepartureTime)
        if hourEnd == "errorHour" or hourEnd == "errorMinute" :
            return "errorHourEnd"
        minuteMeal = getMinuteInInt(workerMeal)
        if minuteMeal == "errorMinute" :
            return "errorMinute"
        workerHour = hourEnd - hourBegin - minuteMeal
        lines = genLib.getLinesOfFile(fileWorkerHourPath)
        return workerHour, lines

def addWorkerDataBase(workerName, workerFirstName, workerArrivingTime, workerDepartureTime, workerMeal, workerCity, fileWorkerHourPath, fileCityPath) :
    """
    add work hours on the database.
    :param workerName: the worker's name.
    :param workerFirstName: the worker's firstname.
    :parzm workerArrivingTime: the arriving time.
    :param workerDepartureTime: the departure time.
    :param workerMeal: the meal time.
    :param workerCity: the city where the worker work.
    :param fileWorkerHourPath: the path to the file includes the work hours of workers.
    :param fileCityPath: the path to the file includes the coty and this MG.
    :rtype: str
    :return: message to check the adding.
    """
    if workerCity == "" : 
        return "city"
    try :
        workerHour, lines = checkParams(workerName, workerFirstName, workerArrivingTime, workerDepartureTime, workerMeal, fileWorkerHourPath)
        res = ""
        mg = takeMG(workerCity, fileCityPath)
        add = False
        for l in lines :
            line = l.split(";")
            if line[0] == workerName and line[1] == workerFirstName :
                try : #if this first work date, there isn't last date.
                    lastDate = line[-1].split(":")[0]
                except :
                    lastDate = ""
                if str(date.today()) != lastDate :
                    add = True
                    res += l[0:-2] + ";" + str(date.today()) + ":" +str(workerHour) + ":" + str(mg) + "\n"
                else :
                    return "errorSameDate" #already work hours added for this day.
            else : 
                res += l
        genLib.writeInFile(fileWorkerHourPath, res)
        if add :
            return "okAddHour"
        else :
            return "add"
    except :
        return checkParams(workerName, workerFirstName, workerArrivingTime, workerDepartureTime, workerMeal, fileWorkerHourPath)


def editWorkerDataBase(workerName, workerFirstName, workerArrivingTime, workerDepartureTime, workerMeal, editDate, fileWorkerHourPath) :
    """
    edit work hours on the database.
    :param workerName: the worker's name.
    :param workerFirstName: the worker's firstname.
    :parzm workerArrivingTime: the arriving time.
    :param workerDepartureTime: the departure time.
    :param workerMeal: the meal time.
    :param editDate: date to edit work hours.
    :param fileWorkerHourPath: the path to the file includes the work hours of workers.
    :rtype: str
    :return: :return: message to check the editing.
    """
    try :
        workerHour, lines = checkParams(workerName, workerFirstName, workerArrivingTime, workerDepartureTime, workerMeal, fileWorkerHourPath)
        res = ""
        edit=False
        for l in lines :
            line = l.split(";")
            if line[0] == workerName and line[1] == workerFirstName : #good worker
                lineLen = len(line)
                for i in range(2,lineLen) : #range 2 -> 2 first element are name and firstname
                    construction = line[i].split(":")
                    if construction[0] == editDate : #good date
                        edit = True
                        index = l.index(editDate)
                        res +=  l[0:index - 1] + ";" + editDate + ":" + str(workerHour) + ":" + construction[2] + l[ (index + len(editDate) + len(str(workerHour)) + 2 + len(construction[2]) ): -1]
                    #if not found the date, we copy the whole line anyway
                    if not(edit) and i == lineLen - 1 :
                        res += l
            else : 
                res += l
        genLib.writeInFile(fileWorkerHourPath, res)
        if edit :
            return "okEditWorker"
        else :
            return "edit"
    except :
        return checkParams(workerName, workerFirstName, workerArrivingTime, workerDepartureTime, workerMeal, fileWorkerHourPath)
