from flask import Flask, request, make_response 
  
app = Flask(__name__) 
  
# Only allow access to index route '/' if the cookie is set with the correct value
@app.route('/')
def index():
    unique_id = request.cookies.get('unique_id')
    if unique_id == 'unique_cookie_value':
        return 'You are allowed to access the index page'
    else:
        return 'You are not allowed to access the index page'

# Using set_cookie() method from make_response to set the key-value pairs
@app.route('/set_cookie') 
def setcookie(): 
    resp = make_response('Setting the cookie')  
    resp.set_cookie('unique_id','unique_cookie_value')
    return resp 

# Using get() method from request to read the cookie value
@app.route('/get_cookie')
def getcookie():
    if request.cookies.get('unique_id') == 'unique_cookie_value':
        unique_id = request.cookies.get('unique_id')
        return unique_id
    else:
        return make_response('No cookie found')

# Using set_cookie() method from make_response to set the key-value pairs with expiration time
@app.route('/delete_cookie')
def deletecookie():
    resp = make_response('Deleting the cookie')  
    resp.set_cookie('unique_id','unique_cookie_value', expires=0)
    return resp

if __name__ == '__main__':
    app.run()