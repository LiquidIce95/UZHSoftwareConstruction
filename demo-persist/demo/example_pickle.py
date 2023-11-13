import pickle

# Define a dictionary to represent our recipe book
recipe_book = {
    'Pancakes': {
        'ingredients': ['flour', 'milk', 'egg', 'sugar', 'baking powder'],
        'steps': [
            'Mix all ingredients together.',
            'Heat a pan with a little oil.',
            'Pour batter into the pan.',
            'Cook until bubbles form, then flip and cook the other side.'
        ]
    },
    'Spaghetti': {
        'ingredients': ['spaghetti', 'tomato sauce', 'garlic', 'olive oil'],
        'steps': [
            'Boil water and cook spaghetti.',
            'Heat oil and sauté garlic.',
            'Add tomato sauce and simmer.',
            'Mix spaghetti with the sauce and serve.'
        ]
    }
}

with open('recipes.pkl','wb') as file:
    pickle.dump(recipe_book, file)

with open('recipes.pkl','rb') as file:
    loaded_recipe_book = pickle.load(file)

print(loaded_recipe_book)

