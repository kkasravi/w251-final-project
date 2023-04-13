from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# In-memory database to store recipes
recipes = []


class RecipeList(Resource):
    def get(self):
        query = request.args.get('search', '')
        if query:
            search_results = [recipe for recipe in recipes if query.lower() in recipe['name'].lower()]
            return search_results, 200
        return recipes, 200

    def post(self):
        recipe = request.get_json()
        recipes.append(recipe)
        return recipe, 201


class Recipe(Resource):
    def get(self, recipe_id):
        for recipe in recipes:
            if recipe['id'] == recipe_id:
                return recipe, 200
        return {"error": "Recipe not found"}, 404


api.add_resource(RecipeList, '/recipes')
api.add_resource(Recipe, '/recipes/<int:recipe_id>')

if __name__ == '__main__':
    app.run(debug=True)

