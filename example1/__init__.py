from flask import Flask, jsonify, request, abort, current_app
from models import *
from flask_cors import CORS, cross_origin

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aashishraj:123@localhost:5432/plantsdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION")
        return response

    with app.app_context():
        db.create_all()

    @app.route("/plants", methods=["GET", "POST"])
    def get_plants():
        with app.app_context():
            page = request.args.get("page", 1, type=int)
            start = (page - 1) * 10
            end = start + 10

            plants = Plant.query.all()
            formatted_plants = [plant.format() for plant in plants]
            return jsonify({
                "success": True,
                "plants": formatted_plants[start:end],
                "total_plants": len(formatted_plants)
            })

    @app.route("/plants/<int:plant_id>")
    def get_specific_plant(plant_id):
        with app.app_context():
            plant = Plant.query.filter(Plant.id == plant_id).one_or_none()
            if plant is None:
                abort(404)
            else:
                return jsonify({"success": True, "plant": plant.format()})



    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="localhost", port=8000, debug=True)