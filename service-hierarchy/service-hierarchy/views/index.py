from flask import Blueprint, render_template, flash, request
from wtforms import Form, TextField, validators
import psycopg2 as p
from tabulate import tabulate
from prettytable import PrettyTable
from flask_table import Table, Col

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
     
        if request.method == 'POST':
            name=request.form['name']
     
            if form.validate(): # save the comment here
                yList = searchingDictionary(name)
                #flash(displayData(searchingDictionary(name)))
                #flash(searchingDictionary(name))
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
        
    
    def populateTable(list):
        if len(list) > 0:
            t = PrettyTable(['Table', 'Service'])
            for x in list:
                t.add_row(x)
        return t
        
    
    def searchingDictionary(word):
        try:
            con = p.connect("dbname='odi' user='fmopex_test_ro' host='fmopex.cl19fspdhrve.eu-west-1.rds.amazonaws.com' password = 'admin'")
        except Exception as e:
            print("\ncould not connect to database\n")
        else:
            print("\nconnected to database\n")
        
            cursor = con.cursor() 
            
            x = {}
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
                x[t] = d
                
            tables = ['isin','map_bcp','map_dataleaks','map_dotcom','map_gdpr',
                      'map_isrisk', 'map_pas', 'map_pentest','map_remoteconnectivity',
                      'map_servicenow', 'problem', 'problem_old']
                
            d1 = x.get('isin')
            d2 = x.get('map_bcp')
            d3 = x.get('map_dataleaks')
            d4 = x.get('map_dotcom')
            d5 = x.get('map_gdpr')
            d6 = x.get('map_isrisk')
            d7 = x.get('map_pas')
            d8 = x.get('map_pentest')
            d9 = x.get('map_remoteconnectivity')
            d10 = x.get('map_servicenow')
            d11 = x.get('problem')
            d12 = x.get('problem_old')
            
            z = {**d1,**d2,**d3,**d4,**d5,**d6,**d7,**d8,**d9,**d10,**d11,**d12}
            
            #if 'Janes_Search_Report' in x.get('map_dotcom'): 
            #    print('map_pentest -> DSMatch')
        
            sorted_dict = {}
            for k, v in z.items():
                sorted_dict.setdefault(v, []).append(k)
                
            w = lookup(word,z)
            
            for a in w:
                for key,value in x.items():
                    if value == a:
                        print(key)
        
            
            y = []
            for a in w: # a is the word
                for t in tables:
                    if a in x.get(t):
                        y.append([t,a])
                        #y.append(t + ' -> ' + a)
                         
            t = PrettyTable(['Table', 'Service'])
            for x in y:
                t.add_row(x)
                        
            if len(y) == 0:
                return 'no matches found'
            else:
                return y
                #print(t)
                #return populateTable(y)
                #return tabulate(y, headers=['Table', 'Service'], tablefmt='orgtbl')
           
    def displayData(y):
        
        return "<table border='1'><tr><th>Table</th><th>Product</th></tr>"
        
        print("<table border='1'>")
        print("<tr>")
        print("<th>Table</th>")
        print("<th>Product</th>")
        print("</tr>")
        for x in y:
            print("<tr>")
            print("<td>{0}</td>".format(x[0]))
            print("<td>{0}</td>".format(x[1]))
            print("</tr>")
        print("</table>")
        
