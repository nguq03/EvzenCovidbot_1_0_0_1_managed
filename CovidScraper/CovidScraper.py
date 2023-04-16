from bs4 import BeautifulSoup as b
import requests as r
import pandas as p
import sys
import pyodbc as odbc


def get_covid():
    myURL = ["https://onemocneni-aktualne.mzcr.cz/covid-19/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/PHA/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/ULK/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/STC/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/JHC/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/PLK/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/KVK/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/LBK/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/HKK/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/PAK/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/VYS/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/JHM/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/OLK/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/ZLK/widget",
    "https://onemocneni-aktualne.mzcr.cz/covid-19/kraje/MSK/widget"]
    #konečný outputlist
    dataList = []
    idZaznam = int()
    #loop pro počet stránek
    for pg in myURL:
        page = r.get(pg, headers= {"User-Agent":"test"})
        soup = b(page.text, "html.parser")

        #kod místa
        kodMisto = pg.replace("https://onemocneni-aktualne.mzcr.cz/covid-19", "")
        kodMisto = kodMisto.replace("/widget", "")
        kodMisto = kodMisto.replace("/kraje/", "")
        #misto
        strMisto = location = soup.find("h1").text.replace("COVID‑19: ", "").replace("COVID-19 v ČR", "Česká republika")
        #id
        idZaznam += 1
        #počet případů
        countSick = soup.find("span", {"id": "count-sick"})
        countSick = countSick["data-value"]
        #počet mrtvých
        countDead = soup.find("p", {"id": "count-dead"}).text.replace(" ","").replace("\n","")
        #počet vyléčených
        countRecover = soup.find("p", {"id": "count-recover"}).text.replace(" ","").replace("\n","")
        #počet očkovaných
        yelDiv = soup.find("div", class_="background--yellow pa-10 border--radius-rounded")
        child = yelDiv.findChild("span")
        countVac = child["data-value"]
        #datum
        lastModified = soup.find("p", class_="text--sm text--center").text.replace("k datu:  ", "")

        #vytvoření listu
        data = []
        data.append(idZaznam)
        data.append(kodMisto)
        data.append(strMisto)
        data.append(countSick)
        data.append(countDead)
        data.append(countRecover)
        data.append(countVac)
        data.append(lastModified)
        #pro CZE
        if data[1] == "":
            data[1] = "CZE"
        
        dataList.append(data)

    #kontrola vytažených dat
    print(dataList)

    #Propojení s databází
    DRIVER = "SQL Server"
    SERVER_NAME = "DESKTOP-NSPSS0D\COVIDBCZ"
    DATABASE_NAME = "COVIDSTATS"

    conn_string = f"""
        Driver={{{DRIVER}}};
        Server={SERVER_NAME};
        Database={DATABASE_NAME};
        UID = sa;
        PWD = dbpassword;
    """

    try:
        conn = odbc.connect(conn_string)
    except Exception as e:
        print(e)
        print("Task ukončen")
        sys.exit()
    else:
        cursor = conn.cursor()

    query = """
        INSERT INTO CovidTable
        VALUES (?,?,?,?,?,?,?,?)
    """
    queryClear = """
        DELETE FROM CovidTable
    """
    cursor.execute(queryClear)

    try: 
        for dataL in dataList:
            print(set)
            cursor.execute(query, dataL)
    except Exception as e:
        cursor.rollback()
        print(e.value)
        print("Trasakce zrušena")
    else:
        print("Data úspěšně uložena")
        cursor.commit()
        cursor.close()
    finally:
        if conn.connected == 1:
            print("Spojení ukončeno")
            conn.close()



get_covid()





