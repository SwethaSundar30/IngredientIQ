import streamlit as st
from main import read_image
from bert import data_summary
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Load the question_response_pairs from the pickle file
with open("question_response_pairs.pkl", "rb") as f:
    question_response_pairs = pickle.load(f)

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

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
    best_similarity = similarities[best_question]

    if best_similarity > 0:
        return question_response_pairs[best_question]
    else:
        return "Bot: Ingredient not found."

st.sidebar.image('https://th.bing.com/th/id/OIP.B4mhnzvK_a7ltCfTxx5iKQHaE8?rs=1&pid=ImgDetMain',
                 use_column_width=False)
st.sidebar.markdown("""
                    > Made by [*Beta*]( )
                    """)

user_color      = '#000000'
title_webapp    = "IngredientIQ"
image_link      = "https://th.bing.com/th/id/OIP.w9gXyd2xzaca3OyruTqhrgHaEJ?rs=1&pid=ImgDetMain"

html_temp = f"""
            <div style="background-color:{user_color};padding:12px">
            <h1 style="color:white;text-align:center;">{title_webapp}
            <img src = "{image_link}" align="right" width=300px ></h1>
            </div>
            """
st.markdown(html_temp, unsafe_allow_html=True)
st.sidebar.header("About")
st.sidebar.info("Our application combines the power of artificial intelligence and nutrition science to provide users with comprehensive information about the ingredients in their food products.By generating detailed reports on each ingredient, including their benefits, side effects, and overall impact, our application empowers users to make informed decisions about the foods they consume. Whether it's understanding the nutritional value of a snack or uncovering potential allergens, our platform equips users with the knowledge they need to prioritize their health and well-being.")
st.sidebar.info("By bridging the gap between complex ingredient labels and consumer understanding, our application revolutionizes the way people engage with packaged foods, promoting transparency, health-consciousness, and informed decision-making. With our platform, users can navigate the modern food landscape with confidence, knowing they have access to accurate, personalized information about the products they consume.")

def main():
    st.title("Info Genie")

    execute_program = st.sidebar.checkbox("Execute program")

    if execute_program:
        st.write("Bot: Hello! I'm your chatbot. Ask me anything or say 'exit' to end the conversation.")

        user_input = st.text_input("You: ")

        if user_input.lower() == 'exit':
            st.write("Bot: Goodbye! Have a great day.")
        else:
            if user_input:  
                response = get_best_response(user_input, question_response_pairs)
                st.write("Bot:", response)
    else:
        st.write("Program execution is currently disabled. Check the box to enable.")
        st.markdown("<h2 style='text-align: center; color: blue;'> Ocr Extraction</h2>", unsafe_allow_html=True)
    inp = st.file_uploader("UPLOAD THE FILE:")
    if inp is not None:
        a = read_image(inp.name)
        predicted_attributes_list = data_summary(a)
        menu=[item['Ingredient'] for item in predicted_attributes_list]
        selected_ingredient = st.sidebar.selectbox("Select Ingredient",menu )
        selected_ingredient_dict = next((item for item in predicted_attributes_list if item['Ingredient'] == selected_ingredient), None)
        if selected_ingredient_dict is not None:
            st.write("".format(selected_ingredient_dict['Ingredient']))
            st.write("".format(selected_ingredient_dict['Predicted Description']))
            st.write("".format(selected_ingredient_dict['Predicted Dietary Needs']))
            st.write("".format(selected_ingredient_dict['Predicted Allergies']))
            st.write("".format(selected_ingredient_dict['Predicted Preferences']))
            st.write("".format(selected_ingredient_dict['Predicted Advantages']))
            st.write("".format(selected_ingredient_dict['Predicted Disadvantages']))
            st.write("".format(selected_ingredient_dict['Predicted Benefits']))
            st.write("".format(selected_ingredient_dict['Predicted Impact']))
            st.write("".format(selected_ingredient_dict['Predicted Side Effects']))

            # Add a line break before the HTML table
            st.markdown("<br>", unsafe_allow_html=True)

            # Display the details in a table-like structure using HTML
            st.markdown("<span style='font-weight: bold;'>Details for:</span> {}".format(selected_ingredient_dict['Ingredient']), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<table>", unsafe_allow_html=True)
            for key, value in selected_ingredient_dict.items():
                st.markdown("<tr><td><span style='font-weight: bold;'>{}:</span></td><td>{}</td></tr>".format(key, value), unsafe_allow_html=True)
            st.markdown("</table>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
