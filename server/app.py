# app.py
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, Recipe, Ingredient, RecipeIngredient, SavedRecipe, Comment
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Recipe API'}), 200


@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        new_user = User(username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except IntegrityError:
        return {'error': 'Username already exists'}, 400
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@app.route('/api/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify(recipe.to_dict())

@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    try:
        data = request.json
        new_recipe = Recipe(
            title=data['title'],
            description=data.get('description'),
            instructions=data['instructions'],
            cooking_time=data['cooking_time'],
            user_id=data['user_id']
        )
        db.session.add(new_recipe)
        db.session.commit()

        # Handle ingredients
        for ingredient_data in data.get('ingredients', []):
            ingredient = Ingredient.query.filter_by(name=ingredient_data['name'].lower()).first()
            if not ingredient:
                ingredient = Ingredient(name=ingredient_data['name'])
                db.session.add(ingredient)
                db.session.commit()

            recipe_ingredient = RecipeIngredient(
                recipe_id=new_recipe.id,
                ingredient_id=ingredient.id,
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )
            db.session.add(recipe_ingredient)
        
        db.session.commit()
        return jsonify(new_recipe.to_dict()), 201
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    try:
        data = request.json
        for key, value in data.items():
            if key != 'ingredients':
                setattr(recipe, key, value)

        if 'ingredients' in data:
            RecipeIngredient.query.filter_by(recipe_id=recipe.id).delete()

            for ingredient_data in data['ingredients']:
                ingredient = Ingredient.query.filter_by(name=ingredient_data['name'].lower()).first()
                if not ingredient:
                    ingredient = Ingredient(name=ingredient_data['name'])
                    db.session.add(ingredient)
                    db.session.commit()

                recipe_ingredient = RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=ingredient_data['quantity'],
                    unit=ingredient_data['unit']
                )
                db.session.add(recipe_ingredient)

        db.session.commit()
        return jsonify(recipe.to_dict())
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return '', 204

@app.route('/api/recipes/<int:recipe_id>/comments', methods=['GET'])
def get_recipe_comments(recipe_id):
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    return jsonify([comment.to_dict() for comment in comments])

@app.route('/api/recipes/<int:recipe_id>/comments', methods=['POST'])
def create_comment():
    try:
        data = request.json
        new_comment = Comment(
            content=data['content'],
            user_id=data['user_id'],
            recipe_id=data['recipe_id']
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.to_dict()), 201
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/saved-recipes', methods=['POST'])
def save_recipe():
    try:
        data = request.json
        saved_recipe = SavedRecipe(
            user_id=data['user_id'],
            recipe_id=data['recipe_id'],
            notes=data.get('notes')
        )
        db.session.add(saved_recipe)
        db.session.commit()
        return jsonify(saved_recipe.to_dict()), 201
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/users/<int:user_id>/saved-recipes', methods=['GET'])
def get_saved_recipes(user_id):
    saved_recipes = SavedRecipe.query.filter_by(user_id=user_id).all()
    return jsonify([sr.to_dict() for sr in saved_recipes])

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.to_dict() for ingredient in ingredients])

if __name__ == '__main__':
    app.run(port=5555, debug=True)