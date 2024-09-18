# # Simple rule-based chatbot
# def chatbot():
#     print("Chatbot: Hi! I'm your chatbot. How can I assist you?")
    
#     while True:
#         # Get user input
#         user_input = input("You: ").lower()
        
#         # Exit condition
#         if user_input == 'bye':
#             print("Chatbot: Goodbye! Have a nice day!")
#             break
        
#         # Responses based on user input
#         if 'hello' in user_input:
#             print("Chatbot: Hello! How are you today?")
#         elif 'how are you' in user_input:
#             print("Chatbot: I'm just a bot, but I'm functioning well! How about you?")
#         elif 'weather' in user_input:
#             print("Chatbot: I can't check the weather at the moment, but it's always a good day to code!")
#         elif 'help' in user_input:
#             print("Chatbot: I'm here to assist you with general questions. Try asking me about the weather or saying hello!")
#         else:
#             print("Chatbot: Sorry, I didn't understand that. Can you please rephrase?")
        
#         # return None


# chatbot()



import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import numpy as np

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Sample data for training the ML model
training_data = {
    "hello": "Hi there! How can I help?",
    "how are you": "I'm doing great! How about you?",
    "what is your name": "I am a chatbot created with Python.",
    "bye": "Goodbye! Have a nice day!"
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

# Chatbot without weather feature
def chatbot():
    model = train_model()
    print("Chatbot: Hi! I can help with various tasks. How can I assist you today?")
    
    while True:
        user_input = input("You: ").lower()
        if user_input == 'bye':
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        # Predict response using ML
        response = predict_response(model, user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot()
