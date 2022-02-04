from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def Home():
    return render_template("Homepage.html")

@app.route('/Christian.html')
def Christian():
    return render_template("Christian.html")
  

@app.route('/Jeff.html')
def Jeff():
    return render_template("Jeff.html")

@app.route('/Bridget.html')
def Bridget():
    return render_template("Bridget.html")

@app.route('/Dominique.html')
def Dominique():
    return render_template("Dominique.html")

@app.route('/Justin.html')
def Justin():
    return render_template("Justin.html")

@app.route('/Richard.html')
def Richard():
    return render_template("Richard.html")

if __name__ == '__main__':
    app.run(debug= True, port= 5000)