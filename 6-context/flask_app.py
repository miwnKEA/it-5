from flask import Flask, render_template, redirect

app = Flask(__name__)

pageMenu = [
    ['/', 'Forside'],
    ['om-os', 'Om os'],
    ['kontakt', 'Kontakt']
]

# inject context processer to all pages
# injects variables into the context of a page
@app.context_processor
def inject_page_menu():
    return dict(pageMenu=pageMenu)

@app.route('/')
def index():
    pageTitle = 'Hjemmesiden'
    pageDescription = '''Velkommen til vores hjemmeside. Her kan du læse om os og kontakte os.'''
    return render_template('index.html', pageTitle=pageTitle, pageDescription=pageDescription, pageMenu=pageMenu)

# eksempel på variable routing
# menuen vil ikke virke for kontakt, hvis ikke der er oprettet en kontakt.html
@app.route('/<page>')
def sitePage(page):
    for p in pageMenu:
        return render_template(page + '.html', p=p)

if __name__ == '__main__':
    app.run(debug=True)