from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

pet1 = {'id':1, 'name':'Dixie'}
pet2 = {'id':2, 'name':'Charlie'}
pets = [pet1, pet2]
# Define a route for the root URL
@app.route('/')
def pets_list():
    return pets



# Run the app only if this script is executed (not imported)
if __name__ == '__main__':
    app.run(debug=True)
