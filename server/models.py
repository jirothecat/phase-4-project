from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-recipes.user', '-saved_recipes.user', '-comments.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    recipes = db.relationship('Recipe', back_populates='user', cascade='all, delete-orphan')
    saved_recipes = db.relationship('SavedRecipe', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    @validates('username')
    def validate_username(self, key, username):
        if not len(username) >= 3:
            raise ValueError("Username must be at least 3 characters long")
        return username

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    serialize_rules = ('-user.recipes', '-comments.recipe', '-recipe_ingredients.recipe', '-saved_recipes.recipe')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='recipes')
    comments = db.relationship('Comment', back_populates='recipe', cascade='all, delete-orphan')
    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade='all, delete-orphan')
    saved_recipes = db.relationship('SavedRecipe', back_populates='recipe', cascade='all, delete-orphan')
    
    ingredients = association_proxy('recipe_ingredients', 'ingredient')

    @validates('title')
    def validate_title(self, key, title):
        if not len(title) >= 3:
            raise ValueError("Title must be at least 3 characters long")
        return title

class Ingredient(db.Model, SerializerMixin):
    __tablename__ = 'ingredients'

    serialize_rules = ('-recipe_ingredients.ingredient',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='ingredient', cascade='all, delete-orphan')
    recipes = association_proxy('recipe_ingredients', 'recipe')

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Ingredient name cannot be empty")
        return name.lower()

class RecipeIngredient(db.Model, SerializerMixin):
    __tablename__ = 'recipe_ingredients'

    serialize_rules = ('-recipe.recipe_ingredients', '-ingredient.recipe_ingredients')

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity = db.Column(db.String, nullable=False)
    unit = db.Column(db.String, nullable=False)

    recipe = db.relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if not quantity:
            raise ValueError("Quantity cannot be empty")
        return quantity

class SavedRecipe(db.Model, SerializerMixin):
    __tablename__ = 'saved_recipes'

    serialize_rules = ('-user.saved_recipes', '-recipe.saved_recipes')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    notes = db.Column(db.Text)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='saved_recipes')
    recipe = db.relationship('Recipe', back_populates='saved_recipes')

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    serialize_rules = ('-user.comments', '-recipe.comments')

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    recipe = db.relationship('Recipe', back_populates='comments')

    @validates('content')
    def validate_content(self, key, content):
        if not len(content) >= 1:
            raise ValueError("Comment cannot be empty")
        return content