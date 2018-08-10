from flask import Blueprint, render_template, flash, request 
from wtforms import Form, TextField, validators
import psycopg2 as p


class ReusableForm(Form):
    try:
        name = TextField('', validators=[validators.required()])
    except Exception as e:
        print("error with the name")
    
try:
    bp = Blueprint(__name__, __name__, template_folder='templates')
except Exception as e:
    print("error with bp")
else:

    @bp.route("/", methods=['GET', 'POST'])
    def hello():
        try:
            form = ReusableForm(request.form)
        except Exception as e:
            print("error with the form")
        else:
            yList = []
            new_list = []
            
            # This table consists of all the services that have 'masterserviceid' as a column
            # name. It also contains 'masterservicemapping'. These were the only service tables
            # that Martin wanted
            tables = ['', 'map_dotcom', 'map_dataleaks', 'map_servicenow', 'map_gdpr', 
                          'map_pentest', 'map_remoteconnectivity', 'map_bcp', 'map_pas',
                          'masterservicemapping']
         
            if request.method == 'POST':
                try:
                    name=(request.form['name']).lower() # lower case for case insensitivity
                except Exception as e:
                    print("error with the name")
                
                if form.validate(): # save the comment here
                    
                    # if no matches were found then the table would be empty and the user
                    # is alerted of this
                    if searchingDictionary(name) == "no matches found":
                        flash("no matches found")
                        
                    # if some matches were found...    
                    elif len(searchingDictionary(name)) > 0:
                        
                        try:
                            
                            # then these matches are displayed in a table format
                            yList = searchingDictionary(name)
                            
                            # selection is whatever is selected from the drop down menu
                            selection = request.form.get('drop_down')
                            
                            for t in tables:
                                if selection == t:
                                    for y in yList:
                                        if t in y[0]:
                                            new_list.append(y)
                           
                        except Exception as e:
                            print("error")
                            new_list = []
                    else:
                        flash("search not found")
                else:
                    flash('All the form fields are required. ')
        
        
        return render_template('index.html', form=form, new_list=new_list, tables=tables)
    
    
    
    # this just cleans the lists as some of them have 'None' as their masterserviceid,
    # and we don't want that
    def cleaningLists(list):
        for l in list[:]:
            if l[1] == None:
                list.remove(l)
                
    
    # used for case insensitivity
    def lower_dict(d): 
        try:
            new_dict = dict((k.lower(), v) for k, v in d.items())
        except Exception as e:
            new_dict = {}
        else:
            return new_dict
                
                
         
    # returns list of keys that have the same masterserviceid        
    def searchByValue(d,v): 
        try:
            listOfKeys = [key  for (key, value) in d.items() if value == v]
        except Exception as e:
            listOfKeys = []
            return listOfKeys
        else:
            return listOfKeys
    
    
    
    # looks for the value of the key in the dictionary
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
        
        # connecting to the odi database, if it can't connect the first time then it will try 3 times
        attempts = 3
        attemptCount = 1
        try: 
            con = p.connect("dbname='odi' user='fmopex_test_ro' host='fmopex.cl19fspdhrve.eu-west-1.rds.amazonaws.com' password = 'admin'")
        except Exception as e:
            print("\ncould not connect to database, attempt: %s" % attemptCount)
            attempts = attempts - 1
            
            while attempts >= 1:
                attemptCount = attemptCount + 1
                try:
                    con = p.connect("dbname='odi' user='fmopex_test_ro' host='fmopex.cl19fspdhrve.eu-west-1.rds.amazonaws.com' password = 'admin'")
                except Exception as e:
                    print("\ncould not connect to database, attempt: %s" % attemptCount)
                    attempts = attempts - 1
        else:
            print("\nconnected to database\n")
        
            try:         
                cursor = con.cursor() 
            except Exception as e:
                print("error with the cursor")
            
            x = {}
            
            # same tables list as before
            tables = ['map_dotcom', 'map_dataleaks', 'map_servicenow', 'map_gdpr', 
                      'map_pentest', 'map_remoteconnectivity', 'map_bcp', 'map_pas',
                      'masterservicemapping']
            
            # select statement for all the services in the tables list
            for t in tables:
                try:
                    cursor.execute("select * from odi_test." + t)
                except Exception as e:
                    print("could not execute cursor")
                else:
                    # returns a list of all the column names for particalur service
                    colnames = [desc[0] for desc in cursor.description]
                
                # we want to only include those services that have 'masterserviceid' as a column name
                # has a select statement for this
                if 'masterserviceid' in colnames:
                    
                    if 'service' in colnames:
                        try:
                            cursor.execute("select service,masterserviceid from odi_test." + t)
                        except Exception as e:
                            l = []
                        else:
                            l = cursor.fetchall()
                            
                    elif 'name' in colnames:
                        try:
                            cursor.execute("select name,masterserviceid from odi_test." + t)
                        except Exception as e:
                            l = []
                        else:
                            l = cursor.fetchall()
                 
                # this select statement is specifically for masterservicemapping    
                elif ('service' in colnames) & ('pkey' in colnames):
                    try:
                        cursor.execute("select service,pkey from odi_test." + t)
                    except Exception as e:
                        l = []
                    else:
                        l = cursor.fetchall()
                        
                else:
                    l = []
                
                # cleaning the list to get rid if any services that have 'None' as their 
                # masterservicemapping
                cleaningLists(l)
                
                # converting the lists into a dictionary
                try:
                    d = dict(l)
                except Exception as e:
                    d = {}
                
                # making the dictionary case insensitive
                try:
                    d1 = lower_dict(d)
                except Exception as e:
                    d1 = {}
                
                # putting that dictionary into another dictionary
                # e.g. { key: {key : value} }
                # this is because i wanted to associate the table names with the products
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
                    
                # joinging the two dictionaries together    
                try:
                    z = {**z,**d1}
                except Exception as e:
                    z = {}
                
            # looks for the value of the word/key in the specified dictionary    
            try:
                w = lookup(word,z)
            except Exception as e:
                w = []
            
            y = []
            try:
                for a in w: # a is the word
                    for t in tables:
                        if a in x.get(t):
                            try:
                                # creates a final list of tuples/pairs (table name, product)
                                y.append([t,a])
                            except Exception as e:
                                y = []
            except Exception as e:
                y = []
            
            # returning the list as long as it contains something
            try:
                if len(y) > 0:
                    return y
                else:
                    return "no matches found"
            except Exception as e:
                print("error with returning the list")
   
        
