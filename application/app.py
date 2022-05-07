#from crypt import method
from crypt import methods
import os
import base64
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory
from flaskext.mysql import MySQL

app = Flask(__name__)


#the code below establishes 
#the login credentials to connect to database
app.secret_key = "SFSU"
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root66730'
app.config['MYSQL_DATABASE_DB'] = 'LinkedSF'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'    


#Connects flaskapp to Mysql database 
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

def company_required(func):
    def secure_function():
        if 'employer' not in session['type']:
            return redirect('/CompanyRegistration.html')
        return func()
    return secure_function

# def student_required(func):
#     def secure_function():
#         if 'student' not in session['type']:
#             return redirect('/StudentRegistration.html')
#         return func()
#     return secure_function


# This app route is for the home page 
@app.route('/', methods = ['GET', 'POST'] )
def Home():
# uses the POST method to request information entered into fields
# this info is then stored into variables  
    if request.method == "POST":
        Company_Username = request.form['Company_Username']
        Password = request.form['Password']

# uses execute statement and sql statement 
# to retrieve an account based on matching login info
        cursor.execute('SELECT * FROM Company WHERE Company_Username = %s AND Password = %s', (Company_Username, Password,))
        Company_account = cursor.fetchone()

#checks to see if the selected account is a company account
# if it is a company, then we direct the user to a company home page
        if Company_account:
            session['loggedin'] = True 
            session['id'] = Company_account[0]
            session['type'] = 'employer'
            return redirect('CompanyHomePage.html')
 # uses execute statement and sql statement 
# to retrieve an account based on matching login info          
    if request.method == 'POST':
        JS_Username = request.form['Company_Username']
        Password = request.form['Password']
        cursor.execute('SELECT * FROM JobSeeker WHERE JS_Username = %s AND Password = %s', (JS_Username, Password,))
        JobSeeker_account = cursor.fetchone() 

#checks to see if the selected account is a student account
# if it is a company, then we direct the user to a student home page
        if JobSeeker_account:
            session['loggedin'] = True
            session['id'] = JobSeeker_account[0]
            session['type'] = 'student'
            return redirect('StudentHomePage.html')
#if the user has entered incorrect login info then 
# we will display an error message
        else: 
            flash("Incorrect Username/Password")

    return render_template("Homepage.html")

#route to the company registration 
@app.route('/CompanyRegistration.html', methods = ['GET', 'POST'])
def CompanyRegister():
#uses POST method to request information entered by user
#then stores the info into variables 
    if request.method == "POST":
        Company_Name = request.form['Company_Name']  
        Company_Email = request.form['Company_Email']
        Company_Username = request.form['Company_Username']
        Password = request.form['Password']
#execute statement inserts the stored vairable into the DB
        cursor.execute("INSERT INTO Company (Company_Name, Company_Email, Company_Username, Password) Values (%s, %s, %s, %s)", (Company_Name, Company_Email, Company_Username, Password))
        conn.commit()
#sends message when account is successfully created
        flash("Account Created")
        ### To do: validate input

        return redirect("/")
    return render_template("CompanyRegistration.html")

@app.route('/StudentRegistration.html', methods = ['GET', 'POST'])
def StudentRegistration():
    if request.method == "POST":
        First_Name = request.form['First_Name'] 
        Last_Name = request.form['Last_Name'] 
        Email = request.form['Email']
        JS_Username = request.form['JS_Username']
        Resume = request.files['Resume']
        Resume_data = Resume.read()
        Password = request.form['Password']

        ### To do: validate input

        cursor.execute("INSERT INTO JobSeeker (JS_Username, First_Name, Last_Name, Email, Password, Resume) Values (%s, %s, %s, %s, %s, %s)", (JS_Username, First_Name, Last_Name, Email, Password, Resume_data))
        cursor.execute("INSERT IGNORE INTO JobSeeker (JS_Username, First_Name, Last_Name, Email, Password, Resume) Values (%s, %s, %s, %s, %s, %s)", (JS_Username, First_Name, Last_Name, Email, Password, Resume_data))
        conn.commit()
        flash("Account Created")
        return redirect("/")
    return render_template("StudentRegistration.html")

#route for creating a job post
@app.route('/PostJob.html', methods = ['GET', 'POST'])
def PostJob():

#uses POST method to request information entered by the user
#info is then stored into variables
    if request.method == "POST":
        Job_Title = request.form['Job_Title']  
        Job_Description= request.form['Job_Description']
        Job_Skills = request.form['Job_Skills']
        Job_Pay = request.form['Job_Pay']
        Job_Street_Address = request.form['Job_Street_Address']
        Job_City = request.form['Job_City']
        Job_State = request.form['Job_State']
        User_Id = session['id']
        Job_Field = request.form['Job_Field']
    
#uses execute statement to insert variables into the DB
        cursor.execute("INSERT INTO JobPost (Job_Title, Job_Description, Job_Skills, Job_Pay, Job_Street_Address, Job_City, Job_State, FK_Companyid, Job_Field) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (Job_Title, Job_Description, Job_Skills, Job_Pay, Job_Street_Address, Job_City, Job_State, User_Id, Job_Field))
        conn.commit()
#sends success message when a post is created
        flash("Created Successfully")

   
    return render_template("PostJob.html")

@app.route('/StudentHomePage.html', methods=['GET', 'POST'])
def SearchJob():
    if request.method == "POST":
        if request.form['submit'] == "submit_search":
            Job_Field = request.form['Job_Field']
            Search_Value = request.form['Search']

        #if the search is null but user selects a field of work, it will on show posts in the field selected
            if (Search_Value == '' and Job_Field == '5G' or Job_Field == 'Iot' or Job_Field == 'AI/Machine Learning' or Job_Field == 'RPA'
                or Job_Field == 'Cyber Security' or Job_Field == 'Quantum Computing' or Job_Field == 'Edge Computing'
                or Job_Field == 'Blockchain' or Job_Field == 'VR/Augmented'):
                cursor.execute('SELECT * FROM JobPost WHERE Job_Field = %s', (Job_Field))
                conn.commit()
                data = cursor.fetchall()


            elif Search_Value == '': 
                cursor.execute("SELECT * FROM JobPost")
                conn.commit()
                data = cursor.fetchall()
            
            else: 
                cursor.execute('SELECT * FROM JobPost WHERE Job_Title LIKE %s AND Job_Field = %s', ('%' + Search_Value + '%', Job_Field,))
                conn.commit()
                data = cursor.fetchall()
            # all in the search box will return all the tuples
            return render_template('StudentHomePage.html', data = data)
        if request.form['submit'] == "submit_apply":
                buttonID = request.form['buttonID']
                cursor.execute('INSERT IGNORE INTO applied (FK_Postid, FK_JobSeekerid) Values (%s, %s)', (int(buttonID), int(session['id'])))
                conn.commit()
                flash("You Have Successfully Applied")
    return render_template("StudentHomePage.html")

@app.route('/CompanyHomePage.html' , methods=['GET', 'POST'])
@company_required
def CompanyHome():
    cursor.execute('SELECT * FROM JobPost WHERE FK_Companyid = %s', (session['id']))
    if request.method == "POST":
        buttonID = request.form['buttonID'].split("_")[-1]
        if request.form['buttonID'].split("_")[0] == "view":
            session['JobPostid'] = buttonID
            return redirect(url_for("ShowApplicants"))
        else:
            cursor.execute('DELETE FROM applied WHERE FK_Postid = %s', (buttonID))
            cursor.execute('DELETE FROM JobPost WHERE idJobPost = %s', (buttonID))
            conn.commit()
            cursor.execute('SELECT * FROM JobPost WHERE FK_Companyid = %s', (session['id']))
            data = cursor.fetchall()
            return render_template("CompanyHomePage.html", data = data)
    else:
        cursor.execute('SELECT * FROM JobPost WHERE FK_Companyid = %s', (session['id']))
        data = cursor.fetchall()
        return render_template("CompanyHomePage.html", data = data)

@app.route('/ShowApplicants.html', methods=['GET', 'POST'])
def ShowApplicants():
    if request.method == "POST":
        buttonID = request.form['buttonID']
        session['JobSeekerid'] = buttonID
        return redirect(url_for("ShowResume"))

    cursor.execute('SELECT * FROM JobSeeker, Applied WHERE Fk_JobSeekerid = idjobseeker AND FK_Postid = %s', session['JobPostid'])
    data = cursor.fetchall()
    return render_template("ShowApplicants.html", data = data)

@app.route('/ShowResume.html', methods=['GET', 'POST'])
def ShowResume():
    cursor.execute('SELECT Resume FROM JobSeeker WHERE idJobSeeker = %s', (session['JobSeekerid']))
    data = cursor.fetchall()
    with open('Temp.pdf', 'wb') as fp:
        fp.write(data[0][0])
    return send_from_directory(os.path.abspath(os.getcwd()), 'Temp.pdf')

#logout route
@app.route('/logout')
def logout():
#ends the users session 
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('type', None)
#sends the a message when user is logged out 
# and returns them to home page
    flash("You Have Successfully Logged Out")
    return redirect('/')




if __name__ == '__main__':
    app.debug = True
    app.run()
