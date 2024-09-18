import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import numpy as np
import requests

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Sample data for training the ML model
training_data = {
    "hello": "Hi there! How can I help?",
    "how are you": "I'm doing great! How about you?",
    "what is your name": "I am a chatbot created with Python.",
    "bye": "Goodbye! Have a nice day!",
    "weather": "I can check the weather for you. Please provide the city name."
}

# Vectorizer and model setup
vectorizer = TfidfVectorizer()

def train_model():
    questions = list(training_data.keys())
    responses = list(training_data.values())
    X_train = vectorizer.fit_transform(questions)
    y_train = np.array(responses)
    model = SVC(kernel='linear')
    model.fit(X_train, y_train)
    return model

# Predict function
def predict_response(model, user_input):
    X_input = vectorizer.transform([user_input])
    prediction = model.predict(X_input)[0]
    return prediction

# OpenWeatherMap API
API_KEY = 'your_openweather_api_key'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return f"The weather in {city} is {temperature}°C with {description}."
    else:
        return "Sorry, I couldn't fetch the weather data."

# Chatbot with NLP, ML, and Weather API
def chatbot():
    model = train_model()
    print("Chatbot: Hi! I can help with various tasks, including checking the weather.")
    
    while True:
        user_input = input("You: ").lower()
        if user_input == 'bye':
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        # Weather request
        if 'weather' in user_input:
            print("Chatbot: Please provide the city name.")
            city = input("You: ")
            weather_info = get_weather(city)
            print(f"Chatbot: {weather_info}")
        else:
            # Predict response using ML
            response = predict_response(model, user_input)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot()
