from flask import Flask, render_template, request, redirect, session
from flaskext.mysql import MySQL
app = Flask(__name__)

app.secret_key = "SFSU"
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Orange3953!'
app.config['MYSQL_DATABASE_DB'] = 'LinkedSF'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route('/', methods = ['GET', 'POST'] )
def Home():
    msg = ''
    if request.method == "POST":
        Company_Username = request.form['Company_Username']
        Password = request.form['Password']
        cursor.execute('SELECT * FROM Company WHERE Company_Username = %s AND Password = %s', (Company_Username, Password,))
        Company_account = cursor.fetchone()
        if Company_account:
            session['loggedin'] = True
            session['id'] = Company_account[0]
            return redirect('CompanyHomePage.html')
        else: 
            msg = 'Incorrect Username/Password'  
    if request.method == 'POST':
        JS_Username = request.form['Company_Username']
        Password = request.form['Password']
        cursor.execute('SELECT * FROM JobSeeker WHERE JS_Username = %s AND Password = %s', (JS_Username, Password,))
        JobSeeker_account = cursor.fetchone() 
        if JobSeeker_account:
            session['loggedin'] = True
            return redirect('StudentHomePage.html')
        else: 
            msg = 'Incorrect Username/Password'  

    return render_template("Homepage.html", msg=msg)

@app.route('/CompanyRegistration.html', methods = ['GET', 'POST'])
def CompanyRegister():
    if request.method == "POST":
        Company_Name = request.form['Company_Name']  
        Company_Email = request.form['Company_Email']
        Company_Username = request.form['Company_Username']
        Password = request.form['Password']
        cursor.execute("INSERT INTO Company (Company_Name, Company_Email, Company_Username, Password) Values (%s, %s, %s, %s)", (Company_Name, Company_Email, Company_Username, Password))
        conn.commit()
    return render_template("CompanyRegistration.html")

@app.route('/StudentRegistration.html', methods = ['GET', 'POST'])
def StudentRegistartion():
    if request.method == "POST":
        First_Name = request.form['First_Name'] 
        Last_Name = request.form['Last_Name'] 
        Email = request.form['Email']
        JS_Username = request.form['JS_Username']
        Resume = request.form['Resume']
        Password = request.form['Password']
        cursor.execute("INSERT INTO JobSeeker (JS_Username, First_Name, Last_Name, Email, Password, Resume) Values (%s, %s, %s, %s, %s, %s)", (JS_Username, First_Name, Last_Name, Email, Password, Resume))
        conn.commit()
    return render_template("StudentRegistration.html")
  
@app.route('/PostJob.html', methods = ['GET', 'POST'])
def PostJob():
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
        cursor.execute("INSERT INTO JobPost (Job_Title, Job_Description, Job_Skills, Job_Pay, Job_Street_Address, Job_City, Job_State, FK_Companyid, Job_Field) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (Job_Title, Job_Description, Job_Skills, Job_Pay, Job_Street_Address, Job_City, Job_State, User_Id, Job_Field))
        conn.commit()
    return render_template("PostJob.html")

@app.route('/CompanyHomePage.html')
def CompanyHome():
    return render_template("CompanyHomePage.html")

@app.route('/StudentHomePage.html')
def StudentHome():
    return render_template("StudentHomePage.html")

if __name__ == '__main__':
    app.debug = True
    app.run()