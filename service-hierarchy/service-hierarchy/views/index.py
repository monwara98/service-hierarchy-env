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
                if searchingDictionary(name) == "no matches found":
                    flash("no matches found")
                elif len(searchingDictionary(name)) > 0:
                    try:
                        yList = searchingDictionary(name)
                    except Exception as e:
                        yList = []
                else:
                    flash("search not found")
            else:
                flash('All the form fields are required. ')
                
        #if request.method == 'GET':
        #    colours = ['Red', 'Blue', 'Black', 'Orange']
        tables = ['', 'map_dotcom', 'map_dataleaks', 'map_servicenow', 'map_gdpr', 
                      'map_pentest', 'map_remoteconnectivity', 'map_bcp', 'map_pas',
                      'masterservicemapping']
        
        return render_template('index.html', form=form, yList=yList, tables=tables)
    
    
        
    
    
    def cleaningLists(list):
        for l in list[:]:
            if l[1] == None:
                list.remove(l)
                
    
    def lower_dict(d):
        try:
            new_dict = dict((k.lower(), v) for k, v in d.items())
        except Exception as e:
            new_dict = {}
        else:
            return new_dict
                
                
                
    def searchByValue(d,v):
        try:
            listOfKeys = [key  for (key, value) in d.items() if value == v]
        except Exception as e:
            listOfKeys = []
            return listOfKeys
        else:
            return listOfKeys
    
    
    
    def lookup(word,d):
        if word in d:
            try:
                k = d[word]
            except Exception as e:
                k = 0
            else:
                return searchByValue(d,k)
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
            
            tables = ['map_dotcom', 'map_dataleaks', 'map_servicenow', 'map_gdpr', 
                      'map_pentest', 'map_remoteconnectivity', 'map_bcp', 'map_pas',
                      'masterservicemapping']
            
            for t in tables:
                cursor.execute("select * from odi_test." + t)
                colnames = [desc[0] for desc in cursor.description]
                
                if 'masterserviceid' in colnames:
                    
                    if 'service' in colnames:
                        try:
                            cursor.execute("select service,masterserviceid from odi_test." + t)
                            l = cursor.fetchall()
                        except Exception as e:
                            l = []
                            
                    elif 'name' in colnames:
                        try:
                            cursor.execute("select name,masterserviceid from odi_test." + t)
                            l = cursor.fetchall()
                        except Exception as e:
                            l = []
                            
                elif ('service' in colnames) & ('pkey' in colnames):
                    try:
                        cursor.execute("select service,pkey from odi_test." + t)
                        l = cursor.fetchall()
                    except Exception as e:
                        l = []
                        
                else:
                    l = []
                
             
                cleaningLists(l)
                
                try:
                    d = dict(l)
                except Exception as e:
                    d = {}
                
                try:
                    d1 = lower_dict(d)
                except Exception as e:
                    d1 = {}
                
                try:
                    x[t] = d1
                except Exception as e:
                    x[t] = {}
                
                
            z = {}
            for t in tables:
                
                try:
                    d = x.get(t)
                except Exception as e:
                    d = {}
                    
                try:    
                    d1 = lower_dict(d)
                except Exception as e:
                    d1 = {}
                    
                try:
                    z = {**z,**d1}
                except Exception as e:
                    z = {}
                
            try:
                w = lookup(word,z)
            except Exception as e:
                w = []
            
            y = []
            for a in w: # a is the word
                for t in tables:
                    if a in x.get(t):
                        try:
                            y.append([t,a])
                        except Exception as e:
                            y = []
            
            if len(y) > 0:
                return y
            else:
                return "no matches found"
   
        
