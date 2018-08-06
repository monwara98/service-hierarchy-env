from flask import Blueprint, render_template, flash, request
from wtforms import Form, TextField, validators
import psycopg2 as p

class ReusableForm(Form):
    name = TextField('', validators=[validators.required()])
    
    
try:
    bp = Blueprint(__name__, __name__, template_folder='templates')
except Exception as e:
    print("error with bp")
else:

    @bp.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)
        yList = []
     
        if request.method == 'POST':
            name=request.form['name']
     
            if form.validate(): # save the comment here
                testingSomething()
                if len(searchingDictionary(name)) > 0:
                    yList = searchingDictionary(name)
                else:
                    flash("search not found")
            else:
                flash('All the form fields are required. ')
     
        return render_template('index.html', form=form, yList=yList)
    
    def cleaningLists(list):
        for l in list[:]:
            if l[1] == None:
                list.remove(l)
                
                
                
    def searchByValue(d,v):
        listOfKeys = [key  for (key, value) in d.items() if value == v]
        return listOfKeys
    
    
    
    def lookup(word,d):
        if word in d:
            k = d[word] 
            return searchByValue(d,k)
        else:
            return "search not found"
        
    def testingSomething():
        try:
            con = p.connect("dbname='odi' user='fmopex_test_ro' host='fmopex.cl19fspdhrve.eu-west-1.rds.amazonaws.com' password = 'admin'")
        except Exception as e:
            print("\ncould not connect to database\n")
        else:
            print("\nconnected to database\n")
            
        cursor = con.cursor()
        cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        row = cursor.fetchall()
        
        y = list(set(row))
        table_names = []
        for r in row:
            table_names.append(r[0])
        
        table_names = list(set(table_names))
        
        cursor.execute("select * from odi_test.problem")
        l = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        print(colnames)
        
        
        
        print(len(table_names))
        
        for t in table_names:
            try:
                cursor.execute("select * from odi_test." + t)
                l = cursor.fetchall()
            except Exception as e:
                table_names.remove(t)
            else:
                colnames = [desc[0] for desc in cursor.description]
                if (('business_service' in colnames) & ('number' in colnames)):
                    pass
                elif (('u_business_service' in colnames) & ('number' in colnames)):
                    pass
                elif (('masterserviceid' in colnames) & ('service' in colnames)):
                    pass
                elif (('masterserviceid' in colnames) & ('name' in colnames)):
                    pass
                else:
                    table_names.remove(t)
            
        print(len(table_names))
        
        for t in table_names:
            print(t)
        
       
            
        #tab = []
            
        #for r in row:
        #    try:
        #        cursor.execute("select * from odi_test." + r[0])
        #        colnames = [desc[0] for desc in cursor.description]
        #    except Exception as e:
        #        return "hello"
        #    else:
        #        if (('masterserviceid' in colnames) & ('service' in colnames)) or (('name' in colnames) & ('masterserviceid' in colnames)):
        #            if (('u_business_service' in colnames) & ('number' in colnames)) or (('business_service' in colnames) & ('number' in colnames)):
        #                tab.append(r[0])
                        
                
        #        print("hello")
        #        for t in tab:
        #            print(t)
        
    
    def searchingDictionary(word):
        try:
            con = p.connect("dbname='odi' user='fmopex_test_ro' host='fmopex.cl19fspdhrve.eu-west-1.rds.amazonaws.com' password = 'admin'")
        except Exception as e:
            print("\ncould not connect to database\n")
        else:
            print("\nconnected to database\n")
        
            cursor = con.cursor() 
            
            
            #for r in row:
                #print(r)
                #cursor.execute("select * from odi_test." + r[0])
                #li = cursor.fetchall()
                #print(li)
            
            x = {}
            
            # 1. loop through all of the tables in the odi_test database
            # 2. only add those databases that have 'number' or 'masterserviceid' as
            # their column names
            # 3. only accept those databases that have some actual data[rows] in them
            
            # perhaps consider automating this as well
            tables = ['isin','map_bcp','map_dataleaks','map_dotcom','map_gdpr',
                      'map_isrisk', 'map_pentest','map_remoteconnectivity',
                      'map_servicenow', 'problem', 'problem_old']
            for t in tables:
                cursor.execute("select * from odi_test." + t)
                colnames = [desc[0] for desc in cursor.description]
                
                if 'masterserviceid' in colnames:
                    if 'service' in colnames:
                        cursor.execute("select service,masterserviceid from odi_test." + t)
                        l = cursor.fetchall()
                    elif 'name' in colnames:
                        cursor.execute("select name,masterserviceid from odi_test." + t)
                        l = cursor.fetchall()
                elif 'u_business_service' in colnames:
                    if 'number' in colnames: 
                        cursor.execute("select u_business_service,number from odi_test." + t)
                        l = cursor.fetchall()
                elif 'business_service' in colnames:
                    if 'number' in colnames:
                        cursor.execute("select business_service,number from odi_test." + t)
                        l = cursor.fetchall()
                
             
                cleaningLists(l)
                d = dict(l)
                x[t] = d
                
            #my_dict = {}
            #my_list = []
            #my_dict = x.get('isin')
            #my_dict = x.get('map_pentest')
            #print(my_dict)
            
            #my_list.append(x.get('isin'))
            #my_list.append(x.get('map_pentest'))
            #print(my_list)
            
            #my_list = dict(my_list)
            #print(my_list)
                
            # find a way to loop through the 'tables' list and add them all to
            # the dictionary.
            
            # find a way to automate this 
            #d1 = x.get('isin')
            #d2 = x.get('map_bcp')
            #d3 = x.get('map_dataleaks')
            #d4 = x.get('map_dotcom')
            #d5 = x.get('map_gdpr')
            #d6 = x.get('map_isrisk')
            #d7 = x.get('map_pas')
            #d8 = x.get('map_pentest')
            #d9 = x.get('map_remoteconnectivity')
            #d10 = x.get('map_servicenow')
            #d11 = x.get('problem')
            #d12 = x.get('problem_old')
            
            z = {}
            for t in tables:
                try:
                    d = x.get(t)
                except Exception as e:
                    exit()
                else:
                    z = {**z,**d} # updayed the dictionary each time
            #print(z)
            
            #z = {**d1,**d2,**d3,**d4,**d5,**d6,**d7,**d8,**d9,**d10,**d11,**d12}
            #print(z)
            #z = {**d1}
            #z = {**z,**d2}
            #print(z)
        
            sorted_dict = {}
            for k, v in z.items():
                sorted_dict.setdefault(v, []).append(k)
                
            w = lookup(word,z)
        
            
            y = []
            for a in w: # a is the word
                for t in tables:
                    if a in x.get(t):
                        y.append([t,a])
                         
                        
            else:
                return y
   
        
