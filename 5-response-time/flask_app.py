from flask import Flask, request
import time

app = Flask(__name__)

# The function decorated with app.before_request will run for every incoming HTTP request, 
# regardless of which route or URL is being accessed
@app.before_request
def before_request():
    request._start_time = time.time()

# Define a function to add a custom response header with response time
@app.after_request
def add_response_time_header(response):
    # Calculate the response time in seconds
    response_time = time.time() - request._start_time

    # Convert response time to milliseconds and format it
    response_time_ms = "{:.2f}".format(response_time * 1000)  # Convert to milliseconds

    # Add the custom header to the response
    response.headers['X-Response-Time'] = response_time_ms + ' ms'

    return response

# Define a index route
@app.route('/')
def index():
    return "Hello World!"

# Define a route that simulates a delay for demonstration
@app.route('/delayed')
def delayed_response():
    time.sleep(3)  # Simulate a 3-second delay
    return "Delayed Response"

# Run the app
if __name__ == '__main__':
    app.run()
