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
            flash("one")
            if form.validate(): # save the comment here
                #testingSomething()
                flash("two")
                flash("this is the name: " + name)
                if len(searchingDictionary(name)) > 0:
                    yList = searchingDictionary(name)
                    flash("three")  
                else:
                    flash("four")
                    flash("search not found")
            else:
                flash('All the form fields are required. ')
     
        # if button clicked once
        return render_template('index.html', form=form, yList=yList)
    
        # if button clicked twice
        # return redirect(url_for('service_hierarchy.views.index.hello'))
    
    def cleaningLists(list):
        for l in list[:]:
            if l[1] == None:
                list.remove(l)
                
    
    def lower_dict(d):
                new_dict = dict((k.lower(), v) for k, v in d.items())
                return new_dict
                
                
                
    def searchByValue(d,v):
        #print("\nsearch by value method")
        try:
         #   print("\nin the try block")
            listOfKeys = [key  for (key, value) in d.items() if value == v]
          #  for l in listOfKeys:
           #     print(l)
            #print(len(listOfKeys))
        except Exception as e:
            listOfKeys = []
            return listOfKeys
        else:
            return listOfKeys
    
    
    
    def lookup(word,d):
        if word in d:
            #print("\nare we inside here?")
            k = d[word]
            #print("\nk is: " + k)
            #for s in searchByValue(d,k):
            #    print(s)
            return searchByValue(d,k)
        #    try:
        #        k = d[word] 
        #    except Exception as e:
        #        k = 0
        #    return searchByValue(d,k)
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
            print("\n hello??????")
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
                      'map_isrisk', 'map_pas', 'map_pentest','map_remoteconnectivity',
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
                d1 = lower_dict(d)
                x[t] = d1
                
            print(d)
                
            print("\ndid we leave the loop?")
                
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
                d = x.get(t)
                d1 = lower_dict(d)
                z = {**z,**d1}
                
            print("\nsecond loop")
                
            
            #for t in tables:
            #    try:
            #        d = x.get(t)
            #    except Exception as e:
            #        exit()
            #    else:
            #        z = {**z,**d} # updated the dictionary each time
            #print(z)
            
            #z = {**d1,**d2,**d3,**d4,**d5,**d6,**d7,**d8,**d9,**d10,**d11,**d12}
            #print(z)
            #z = {**d1}
            #z = {**z,**d2}
            #print(z)
            
                
            w = lookup(word,z)
            
            print("")
            for a in w:
                print(a) 
            print("")
            
            y = []
            for a in w: # a is the word
                print("\nare we in here?")
                for t in tables:
                    #print(x.get(t))
                    if a in x.get(t):
                        print("any difference?")
                        y.append([t.lower(),a.lower()])
            print(len(y))
            for a in y:
                print(a)
                        
                         
                
            return y
   
        
