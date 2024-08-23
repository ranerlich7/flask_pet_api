from flask import Flask, request

# Create an instance of the Flask class
app = Flask(__name__)

pet1 = {'id':1, 'name':'Dixie', 'age':5,'image':'https://t4.ftcdn.net/jpg/01/99/00/79/360_F_199007925_NolyRdRrdYqUAGdVZV38P4WX8pYfBaRP.jpg'}
pet2 = {'id':2, 'name':'Charlie','age':2,'image':'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg'}
pets = [pet1, pet2]

# pet list
@app.route('/pets')
def pets_list():
    return pets

@app.route('/pets', methods=["POST"])
def add_pet():
    new_pet = request.get_json()
    pets.append(new_pet)
    return {'result':'added succesfuly'}

     


@app.route('/pets/<id>/')
def single_pet(id):
    try:
        for pet in pets:
                if pet['id'] == int(id):
                    return pet
    except:
        print('error in id')
    return {'result':'Pet not found'}


# Run the app only if this script is executed (not imported)
if __name__ == '__main__':
    app.run(debug=True)
