# Simple rule-based chatbot
def chatbot():
    print("Chatbot: Hi! I'm your chatbot. How can I assist you?")
    
    while True:
        # Get user input
        user_input = input("You: ").lower()
        
        # Exit condition
        if user_input == 'bye':
            print("Chatbot: Goodbye! Have a nice day!")
            break
        
        # Responses based on user input
        if 'hello' in user_input:
            print("Chatbot: Hello! How are you today?")
        elif 'how are you' in user_input:
            print("Chatbot: I'm just a bot, but I'm functioning well! How about you?")
        elif 'weather' in user_input:
            print("Chatbot: I can't check the weather at the moment, but it's always a good day to code!")
        elif 'help' in user_input:
            print("Chatbot: I'm here to assist you with general questions. Try asking me about the weather or saying hello!")
        else:
            print("Chatbot: Sorry, I didn't understand that. Can you please rephrase?")
