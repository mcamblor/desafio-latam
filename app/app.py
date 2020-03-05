from flask import Flask,render_template,jsonify,request,Response
from flask_restful import Resource, Api, reqparse, abort
from models.person import PersonModel
from db.database import create_database
import HelpersDate as hd
import os

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
base_dir = os.path.dirname(os.path.realpath(__file__))

@app.route("/")
def index():
    return render_template("index.html")
# Service for Birthday Latam
# shows poem when is birthday or show missing days
class ServiceBirthday(Resource):
    def post(self):
        if request.method == 'POST':
            #json_input = request.get_json(force=True)
            parser.add_argument('name',type=str,location='form')
            parser.add_argument('born',type=str,location='form')
            #request.get_json(force=True)
            args = parser.parse_args()
            #_name = json_input['name']
            #_born = json_input['born']
            _name = str(args['name'])
            _born = str(args['born'])
            try:
                if isinstance(hd.validateDate(_born),str) == False:
                    if PersonModel.find_by_name(hd.getName(_name)['firstname'],hd.getName(_name)['lastname']):
                        resp = jsonify(message='Persona ya existe!')
                        resp.status_code = 400
                    else:
                        PersonModel.insert_into_table(hd.getName(_name)['firstname'],hd.getName(_name)['lastname'],hd.changeFormatDate(_born),hd.calculate_age(_born),hd.daysMissing(_born))
                        resp = jsonify(
                            firstname=hd.getName(_name)['firstname'],
                            lastname=hd.getName(_name)['lastname'],
                            date=hd.changeFormatDate(_born),
                            age=hd.calculate_age(_born),
                            text=hd.daysMissing(_born),
                            message='Persona agregada a la base de datos!')
                        resp.status_code = 200
                else:
                    resp = jsonify(message='Error fecha incorrecta, la fecha deberia ser DD-MM-YYYY o una valida.')
                    resp.status_code = 500
            except Exception as e:
                resp = jsonify(error='Error al consumir servicio de cumpleaños, {}'.format(str(e)))
                resp.status_code = 400
            return resp

class AllPeople(Resource):
    def get(self):
        if request.method == 'GET':
            try:
                users = PersonModel.find_all()
                if users:
                    resp = jsonify(people=[user.json() for user in users])
                    resp.status_code = 200
                else:
                    resp = jsonify(message='No se han registrado personas!')
                    resp.status_code = 404
            except ValueError as e:
                resp = jsonify(message='Error, {}'.format(e))
                resp.status_code = 500
            
            return resp 

class GetPeople(Resource):
    def get(self,id):
        if request.method == 'GET':
            try:
                user = PersonModel.find_by_id(id)
                if user:
                    resp = jsonify(person=user.json())
                    resp.status_code = 200
                else:
                    resp = jsonify(message='No se encontró persona con ese id!')
                    resp.status_code = 404
            except ValueError as e:
                resp = jsonify(message='Error, {}'.format(e))
                resp.status_code = 500

            return resp

##
## Actually setup the Api resource routing here
##
api.add_resource(ServiceBirthday, '/birthday')
api.add_resource(AllPeople,'/get-people')
api.add_resource(GetPeople,'/get-people-id/<string:id>')

if __name__ == "__main__":
    create_database('{}/db/database_file.db'.format(base_dir))
    app.run(debug=True,host='127.0.0.1')