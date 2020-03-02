from flask import Flask,render_template,jsonify,request,Response
from flask_restful import Resource, Api, reqparse, abort
import HelpersDate as hd

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


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
                if hd.validateDate(_born):
                    resp = jsonify(
                        nombre=_name.split(' ')[0],
                        apellido=_name.split(' ')[1],
                        fecha= hd.changeFormatDate(_born),
                        edad=hd.calculate_age(_born),
                        poem=hd.daysMissing(_born)
                    )
                    resp.status_code=200
                else:
                    resp = jsonify(error='Error fecha incorrecta, la fecha deberia ser DD-MM-YYYY o una valida.')
                    resp.status_code = 500
            except Exception as e:
                resp = jsonify(error='Error al consumir servicio de cumpleaños, {}'.format(str(e)))
                resp.status_code = 400
            return resp


##
## Actually setup the Api resource routing here
##
api.add_resource(ServiceBirthday, '/birthday')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')