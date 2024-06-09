import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import random


def check_ingredients(user_input):
    ingredients = [
        "Potatoes", "Vegetable oil", "Salt", "Barbecue seasoning",
        "Sour cream and onion seasoning", "Salt and vinegar seasoning",
        "Cheddar and sour cream seasoning", "Wheat flour", "Sugar",
        "Soybean oil", "Corn starch", "Cocoa powder", "Milk powder",
        "Onion powder", "Garlic powder", "Monosodium glutamate (MSG)",
        "High-fructose corn syrup", "Palm oil", "Artificial flavors",
        "Artificial colors", "Preservatives", "Emulsifiers",
        "Hydrogenated oils", "Natural flavors", "Corn syrup solids",
        "Modified food starch", "Yeast extract", "Calcium carbonate",
        "Xanthan gum", "Guar gum", "Coconut oil", "Vanilla extract",
        "Almond extract", "Ground cinnamon", "Dried cranberries",
        "Whole grain oats", "Coconut milk", "Chia seeds", "Quinoa",
        "Flaxseeds", "Hemp seeds", "Cashews", "Pine nuts", "Sesame seeds",
        "Sunflower seeds", "Pumpkin seeds", "Molasses", "Agave nectar",
        "Pecans", "Walnuts", "Hazelnuts", "Rice vinegar",
        "Blackstrap molasses", "White vinegar", "Miso", "Mirin",
        "Rice wine vinegar", "Hoisin sauce", "Oyster sauce", "Fish sauce",
        "Tamarind paste", "Gochujang", "Tahini", "Harissa",
        "Anchovy paste", "Sambal oelek", "Worcestershire sauce"
    ]
    user_tokens = preprocess_text(user_input)
    for ingredient in ingredients:
        if ingredient.lower() in user_tokens:
            return True
    return False

# Save the check_ingredients function to a pickle file
with open("check_ingredients.pkl", "wb") as f:
    pickle.dump(check_ingredients, f)

with open("question_response_pairs.pkl", "rb") as f:
    question_response_pairs = pickle.load(f)

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def get_best_response(user_input, question_response_pairs):
    user_tokens = preprocess_text(user_input)

    similarities = {}
    for question, response in question_response_pairs.items():
        question_tokens = preprocess_text(question)
        intersection = set(user_tokens) & set(question_tokens)
        union = set(user_tokens) | set(question_tokens)
        jaccard_similarity = len(intersection) / len(union)
        similarities[question] = jaccard_similarity

    best_question = max(similarities, key=similarities.get)

    return question_response_pairs[best_question]

print("Bot: Hello! I'm your chatbot. Ask me anything or say 'exit' to end the conversation.")

while True:
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        print("Bot: Goodbye! Have a great day.")
        break

    response = get_best_response(user_input, question_response_pairs)
    print("Bot:", response)