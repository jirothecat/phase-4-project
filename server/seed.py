#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from datetime import datetime
from app import app
from models import db, User, Recipe, Ingredient, RecipeIngredient, Comment, SavedRecipe

def create_users():
    users = [
        User(username="gordonramsay"),
        User(username="marcowhite"),
        User(username="guyfieri"),
        User(username="juliachilds")
    ]
    return users

def create_ingredients():
    ingredients = [
        # Vegetables
        Ingredient(name="tomato"),
        Ingredient(name="onion"),
        Ingredient(name="garlic"),
        Ingredient(name="carrot"),
        Ingredient(name="potato"),
        Ingredient(name="bell pepper"),
        # Proteins
        Ingredient(name="chicken breast"),
        Ingredient(name="ground beef"),
        Ingredient(name="salmon fillet"),
        Ingredient(name="eggs"),
        # Pantry Items
        Ingredient(name="olive oil"),
        Ingredient(name="salt"),
        Ingredient(name="black pepper"),
        Ingredient(name="flour"),
        Ingredient(name="sugar"),
        # Dairy
        Ingredient(name="butter"),
        Ingredient(name="milk"),
        Ingredient(name="heavy cream"),
        Ingredient(name="cheese"),
        # Herbs & Spices
        Ingredient(name="basil"),
        Ingredient(name="oregano"),
        Ingredient(name="thyme"),
        Ingredient(name="paprika"),
        Ingredient(name="cumin")
    ]
    return ingredients

def create_recipes(users):
    recipes = [
        Recipe(
            title="Classic Tomato Soup",
            description="A comforting homemade tomato soup that's perfect for any day.",
            instructions="""
1. Heat olive oil in a large pot over medium heat
2. Sauté onions and garlic until softened
3. Add chopped tomatoes and cook for 5 minutes
4. Add vegetable stock and bring to a boil
5. Simmer for 20 minutes
6. Blend until smooth
7. Stir in cream and season with salt and pepper
            """.strip(),
            cooking_time=30,
            user_id=users[0].id
        ),
        Recipe(
            title="Garlic Butter Chicken",
            description="Juicy chicken breast in a rich garlic butter sauce.",
            instructions="""
1. Season chicken breasts with salt and pepper
2. Heat butter in a skillet over medium-high heat
3. Cook chicken for 5-7 minutes per side
4. Remove chicken and set aside
5. In the same pan, add more butter and garlic
6. Create sauce with chicken broth and herbs
7. Return chicken to pan and coat with sauce
            """.strip(),
            cooking_time=25,
            user_id=users[1].id
        ),
        Recipe(
            title="Classic Beef Burger",
            description="The ultimate homemade beef burger with all the fixings.",
            instructions="""
1. Mix ground beef with seasonings
2. Form into patties
3. Heat grill or pan to medium-high
4. Cook burgers 4-5 minutes per side
5. Add cheese if desired
6. Toast buns
7. Assemble with lettuce, tomato, and condiments
            """.strip(),
            cooking_time=20,
            user_id=users[2].id
        ),
        Recipe(
            title="Creamy Mashed Potatoes",
            description="Smooth and creamy mashed potatoes that melt in your mouth.",
            instructions="""
1. Peel and cut potatoes into chunks
2. Boil in salted water until tender
3. Drain well
4. Add butter and warm milk
5. Mash until smooth
6. Season with salt and pepper
7. Stir in additional butter if desired
            """.strip(),
            cooking_time=35,
            user_id=users[3].id
        )
    ]
    return recipes

def create_recipe_ingredients(recipes, ingredients):
    recipe_ingredients = []
    
    # Tomato Soup ingredients
    soup = recipes[0]
    recipe_ingredients.extend([
        RecipeIngredient(recipe_id=soup.id, ingredient_id=ingredients[0].id, quantity="4", unit="large"),  # tomatoes
        RecipeIngredient(recipe_id=soup.id, ingredient_id=ingredients[1].id, quantity="1", unit="medium"),  # onion
        RecipeIngredient(recipe_id=soup.id, ingredient_id=ingredients[2].id, quantity="3", unit="cloves"),  # garlic
        RecipeIngredient(recipe_id=soup.id, ingredient_id=ingredients[17].id, quantity="1/2", unit="cup"),  # heavy cream
    ])

    # Garlic Butter Chicken ingredients
    chicken = recipes[1]
    recipe_ingredients.extend([
        RecipeIngredient(recipe_id=chicken.id, ingredient_id=ingredients[6].id, quantity="4", unit="pieces"),  # chicken breast
        RecipeIngredient(recipe_id=chicken.id, ingredient_id=ingredients[15].id, quantity="4", unit="tbsp"),  # butter
        RecipeIngredient(recipe_id=chicken.id, ingredient_id=ingredients[2].id, quantity="6", unit="cloves"),  # garlic
    ])

    # Beef Burger ingredients
    burger = recipes[2]
    recipe_ingredients.extend([
        RecipeIngredient(recipe_id=burger.id, ingredient_id=ingredients[7].id, quantity="1", unit="pound"),  # ground beef
        RecipeIngredient(recipe_id=burger.id, ingredient_id=ingredients[12].id, quantity="1", unit="tsp"),  # black pepper
        RecipeIngredient(recipe_id=burger.id, ingredient_id=ingredients[11].id, quantity="1", unit="tsp"),  # salt
    ])

    # Mashed Potatoes ingredients
    potatoes = recipes[3]
    recipe_ingredients.extend([
        RecipeIngredient(recipe_id=potatoes.id, ingredient_id=ingredients[4].id, quantity="4", unit="large"),  # potatoes
        RecipeIngredient(recipe_id=potatoes.id, ingredient_id=ingredients[15].id, quantity="1/2", unit="cup"),  # butter
        RecipeIngredient(recipe_id=potatoes.id, ingredient_id=ingredients[16].id, quantity="1/2", unit="cup"),  # milk
    ])

    return recipe_ingredients

def create_comments(users, recipes):
    comments = [
        Comment(
            content="Absolutely delicious! I added a bit more garlic and it was perfect.",
            user_id=users[1].id,
            recipe_id=recipes[0].id
        ),
        Comment(
            content="My family loves this recipe. It's become a weekly staple!",
            user_id=users[2].id,
            recipe_id=recipes[1].id
        ),
        Comment(
            content="Great recipe but I needed to cook it a bit longer than stated.",
            user_id=users[3].id,
            recipe_id=recipes[2].id
        ),
        Comment(
            content="Simple and perfect. Just like my grandmother used to make!",
            user_id=users[0].id,
            recipe_id=recipes[3].id
        )
    ]
    return comments

def create_saved_recipes(users, recipes):
    saved_recipes = [
        SavedRecipe(
            user_id=users[1].id,
            recipe_id=recipes[0].id,
            notes="Add extra cream next time"
        ),
        SavedRecipe(
            user_id=users[2].id,
            recipe_id=recipes[1].id,
            notes="Family favorite - double the recipe"
        ),
        SavedRecipe(
            user_id=users[3].id,
            recipe_id=recipes[2].id,
            notes="Try with turkey next time"
        ),
        SavedRecipe(
            user_id=users[0].id,
            recipe_id=recipes[3].id,
            notes="Perfect for Sunday roast"
        )
    ]
    return saved_recipes

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        
        # Clear existing data
        Comment.query.delete()
        SavedRecipe.query.delete()
        RecipeIngredient.query.delete()
        Recipe.query.delete()
        Ingredient.query.delete()
        User.query.delete()
        
        # Create new data
        print("Creating users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Creating ingredients...")
        ingredients = create_ingredients()
        db.session.add_all(ingredients)
        db.session.commit()

        print("Creating recipes...")
        recipes = create_recipes(users)
        db.session.add_all(recipes)
        db.session.commit()

        print("Creating recipe ingredients...")
        recipe_ingredients = create_recipe_ingredients(recipes, ingredients)
        db.session.add_all(recipe_ingredients)
        db.session.commit()

        print("Creating comments...")
        comments = create_comments(users, recipes)
        db.session.add_all(comments)
        db.session.commit()

        print("Creating saved recipes...")
        saved_recipes = create_saved_recipes(users, recipes)
        db.session.add_all(saved_recipes)
        db.session.commit()

        print("Seeding completed!")