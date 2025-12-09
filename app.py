from flask import Flask, request, jsonify
from models.meal import Meal
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:8SGijmpklM@localhost:3306/flask_daily_diet'
app.config['SECRET_KEY'] = "your_secret_key"
db.init_app(app)

#Cadastrar refeição
@app.route("/meals", methods=["POST"])
def create_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    in_diet = data.get("in_diet")

    if name and description and in_diet is not None:
        meal = Meal(name=name, description=description, in_diet=in_diet)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Meal created."})

    return jsonify({"message": "Invalid request"}), 400

#Listar todas as refeições
@app.route("/meals", methods=["GET"])
def get_meals():
    meals = Meal.query.all()
    meals_list = [{"id": meal.id, "name": meal.name, "description": meal.description, "in_diet": meal.in_diet} for meal in meals]
    return jsonify({"meals": meals_list})

#Listar refeição pelo ID
@app.route("/meals/<int:id_meal>", methods=["GET"])
def get_meal_by_id(id_meal):
    meal = Meal.query.get(id_meal)

    if meal:
        return jsonify({
            "name": meal.name,
            "description": meal.description,
            "in_diet": meal.in_diet
        })
    
    return jsonify({"message": f"Meal with ID {id_meal} not found"}), 404

#Atualizar uma refeição
@app.route("/meals/<int:id_meal>", methods=["PUT"])
def update_meal(id_meal):
    meal = Meal.query.get(id_meal)
    data = request.json

    if meal:
        name = data.get("name")
        description = data.get("description")
        in_diet = data.get("in_diet")
        if name:
            meal.name = name
        if description:
            meal.description = description
        if in_diet is not None:
            meal.in_diet = in_diet
        db.session.commit()

        return jsonify({"message": f"Meal with ID {id_meal} updated"})

    jsonify({"message": f"Meal with ID {id_meal} not found"}), 404

#Deletar uma refeição
@app.route("/meals/<int:id_meal>", methods=["DELETE"])
def delete_meal(id_meal):
    meal = Meal.query.get(id_meal)

    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Meal ID {id_meal} deleted."})
    
    return jsonify({"message": "Meal not found"}), 404
    


if __name__ == '__main__':
    app.run(debug=False)