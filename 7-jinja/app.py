from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Data som vi bruger i Flask applikationen
title = "Velkommen til Jinja Template Engine Demo"

menu = ['Forside', 'Billeder', 'Forms og Input', 'Lister og Tabeller']

data = [
    ['Mikkel', 'Softwarekonstruktion 2', 'Økonomi og IT'],
    ['Helle', 'Systemudvikling 2', 'Økonomi og IT']
]

images = [
    'https://www.w3schools.com/w3css/img_lights.jpg',
    'https://www.w3schools.com/w3css/img_nature.jpg',
    'https://www.w3schools.com/w3css/img_mountains.jpg',
]

regionData = ""

# Vi bruger to typer HTTP metoder: GET og POST

# En HTTP GET anmodning håndterer at sende data til en klient
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", title=title, menu=menu, data=data, images=images, regionData=regionData)

# Vi bruger variabel routing til at håndtere de forskellige sider i en menu
@app.route("/<string:page_name>", methods=['GET'])
def page(page_name):
    if page_name.lower() == "forside":
        redirect(url_for('index'))
    else:
        for item in menu:
            if item.lower() == page_name.lower():
                return render_template("page.html", title=item, menu=menu, data=data, images=images)
    return redirect(url_for('index'))

# En HTTP POST anmodning anvendes til at tage imod data fra en klient
@app.route("/forms-og-input", methods=['POST'])
def forms_og_input():
    if request.method == 'POST':
        data.append([request.form['name'], request.form['favclass'], request.form['education']])
    return redirect(url_for('index'))

@app.route("/billeder", methods=['POST'])
def billeder():
    if request.method == 'POST':
        images.append(request.form['link'])
    return redirect(url_for('index'))

@app.route("/region", methods=['POST'])
def region():
    if request.method == 'POST':
        data = request.form['region']
        # global regionData
        # add data to global variable regionData
        global regionData
        regionData = data

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)