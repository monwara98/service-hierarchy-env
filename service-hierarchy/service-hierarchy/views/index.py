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
            name=(request.form['name']).lower()
            if form.validate(): # save the comment here
                #testingSomething()
                if len(searchingDictionary(name)) > 0:
                    yList = searchingDictionary(name)
                else:
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
        
   
    
    def searchingDictionary(word):
        try:
            con = p.connect("dbname='odi' user='fmopex_test_ro' host='fmopex.cl19fspdhrve.eu-west-1.rds.amazonaws.com' password = 'admin'")
        except Exception as e:
            print("\ncould not connect to database\n")
        else:
            print("\nconnected to database\n")
        
            cursor = con.cursor() 
            
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
                
                
            
            
            
            
            z = {}
            for t in tables:
                d = x.get(t)
                d1 = lower_dict(d)
                z = {**z,**d1}
                
            
                
            w = lookup(word,z)
            
            
            y = []
            for a in w: # a is the word
                for t in tables:
                    if a in x.get(t):
                        y.append([t,a])
                        
                         
                
            return y
   
        
