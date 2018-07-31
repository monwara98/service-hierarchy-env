from flask import Blueprint, render_template, flash, redirect, request, url_for
import psycopg2 as p

def cleaningLists(list):
    for l in list[:]:
        if l[1] == None:
            list.remove(l)        
            
# Things to consider:
# Automating the extraction of the data from the tables
# Attaching the tables names alongside the product services
        

bp = Blueprint(__name__, __name__, template_folder='templates')

try:
    con = p.connect("dbname='odi' user='fmopex_test_ro' host='fmopex.cl19fspdhrve.eu-west-1.rds.amazonaws.com' password = 'admin'")
except Exception as e:
    print("\ncould not connect to database\n")
else:
    print("\nconnected to database\n")
    
    cursor = con.cursor()
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    row = cursor.fetchall() # gets all the table names from the database
   
    # have only started off by doing this to a few services, will learn to 
    # automate this later and add more tables to the list
    c = con.cursor() 
    
    c.execute("select name,masterserviceid from odi_test.map_dotcom")
    map_dotcom = c.fetchall()
    cleaningLists(map_dotcom)
    d1 = dict(map_dotcom)
    
    c.execute("select service,masterserviceid from odi_test.map_dataleaks")
    map_dataleaks = c.fetchall()
    cleaningLists(map_dataleaks)
    d2 = dict(map_dataleaks)
    
    c.execute("select service,masterserviceid from odi_test.map_servicenow")
    map_servicenow = c.fetchall()
    cleaningLists(map_servicenow)
    d3 = dict(map_servicenow)
    
    c.execute("select service,masterserviceid from odi_test.map_isrisk")
    map_isrisk = c.fetchall()
    cleaningLists(map_isrisk)
    d4 = dict(map_isrisk)
    
    c.execute("select service,masterserviceid from odi_test.map_gdpr")
    map_gdpr = c.fetchall()
    cleaningLists(map_gdpr)
    d5 = dict(map_gdpr)
    
    c.execute("select service,masterserviceid from odi_test.map_pentest")
    map_pentest = c.fetchall()
    cleaningLists(map_pentest)
    d6 = dict(map_pentest)
    
    c.execute("select service,masterserviceid from odi_test.map_remoteconnectivity")
    map_remoteconnectivity = c.fetchall()
    cleaningLists(map_remoteconnectivity)
    d7 = dict(map_remoteconnectivity)
    
    c.execute("select service,masterserviceid from odi_test.map_bcp")
    map_bcp = c.fetchall()
    cleaningLists(map_bcp)
    d8 = dict(map_bcp)
    
    c.execute("select service,masterserviceid from odi_test.map_pas")
    map_pas = c.fetchall()
    cleaningLists(map_pas)
    d9 = dict(map_pas)
    
    c.execute("select * from odi_test.control")
    control = c.fetchall()
    cleaningLists(control)
    d10 = dict(control)
    
    c.execute("select service,batch from odi_test.evbbatchmetrics")
    evbbatchmetrics = c.fetchall()
    # they've compressed this all into 1 as they all have the same name
    # sort this out later
    cleaningLists(evbbatchmetrics)
    d11 = dict(evbbatchmetrics)
           
         
    z = {**d1,**d2,**d3,**d4,**d5,**d6,**d7,**d8,**d9,**d10,**d11}
    
    # groups together all the entries keys that have the same value
    # i.e. have the same masterserviceid, so are the same products but under
    # different names    
    sorted_dict = {}
    for k, v in z.items():
        sorted_dict.setdefault(v, []).append(k)
        
    #for key,val in sorted_dict.items():
        #print(key,'=>',val)
        
    #print(z['Transportation - Business Segment'])
    
    # they specify a certain key
    # find the value of that key
    # use the value to find all the other keys that have the same value
    
    def searchByValue(d,v):
        listOfKeys = [key  for (key, value) in d.items() if value == v]
        return listOfKeys
    
    # lets you search for the word in a dictionary
    def lookup(d):
        word = str(input("Search for: "))
        if word in d:
            k = d[word] 
            print(searchByValue(d,k))
            # return the value of that key
            # use searchByValue to get a list of all keys associated with that value
        else:
            print("search not found")
    #print(searchByValue(z,142))
    #lookup(z)  
    


@bp.route('/')
def show():
    return render_template('index.html') # maybe change this to layout.html and get rid of index

