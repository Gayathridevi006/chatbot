import datetime
import json
import os

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# File to store user history
history_file = 'data/period_history.json'

def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return {}

def save_history(history):
    with open(history_file, 'w') as file:
        json.dump(history, file, indent=4)

def get_user_details(existing_user=None):
    if existing_user:
        print(f"\nChatbot: Welcome back, {existing_user.get('name', 'User')}!")
        print("Chatbot: Here is your stored period history:")
        print(f"Last Period: {existing_user.get('last_period', 'N/A')}")
        print(f"Cycle Length: {existing_user.get('cycle_length', 'N/A')} days")
        print(f"Period Length: {existing_user.get('period_length', 'N/A')} days")
        print(f"Next Period: {existing_user.get('next_period', 'N/A')}")
        print(f"Ovulation Window: {existing_user.get('ovulation_start', 'N/A')} to {existing_user.get('ovulation_end', 'N/A')}")
        print(f"Symptoms Logged: {', '.join(existing_user.get('symptom_log', [])) if existing_user.get('symptom_log') else 'None'}")
        
        return existing_user.get('name', 'User'), datetime.datetime.strptime(existing_user.get('last_period', '1970-01-01'), '%Y-%m-%d').date(), existing_user.get('cycle_length', 28), existing_user.get('period_length', 5), existing_user.get('symptom_log', [])
    
    print("Chatbot: Hello! I can help you track your periods.")
    
    while True:
        user_name = input("Chatbot: What's your name? ").strip()
        if user_name:
            break
        else:
            print("Chatbot: Please enter a valid name.")
    
    while True:
        last_period_input = input("Chatbot: When did your last period start? (YYYY-MM-DD): ")
        try:
            last_period = datetime.datetime.strptime(last_period_input, '%Y-%m-%d').date()
            break
        except ValueError:
            print("Chatbot: Please enter the date in the correct format (YYYY-MM-DD).")
    
    while True:
        cycle_length_input = input("Chatbot: What is your average cycle length in days? (typically 28): ")
        try:
            cycle_length = int(cycle_length_input)
            if 20 <= cycle_length <= 45:
                break
            else:
                print("Chatbot: Please enter a realistic cycle length between 20 and 45 days.")
        except ValueError:
            print("Chatbot: Please enter a valid number for cycle length.")

    while True:
        period_length_input = input("Chatbot: How many days does your period usually last? (typically 4-7): ")
        try:
            period_length = int(period_length_input)
            if 1 <= period_length <= 10:
                break
            else:
                print("Chatbot: Please enter a realistic period length (between 1 and 10 days).")
        except ValueError:
            print("Chatbot: Please enter a valid number for period length.")
    
    # Symptom tracking
    symptoms = input("Chatbot: Would you like to track any symptoms? (Yes/No): ").strip().lower()
    symptom_log = []
    if symptoms == 'yes':
        while True:
            symptom = input("Chatbot: Please describe your symptom or type 'done' to finish: ")
            if symptom.lower() == 'done':
                break
            symptom_log.append(symptom)
    
    return user_name, last_period, cycle_length, period_length, symptom_log

def estimate_next_period(last_period, cycle_length):
    next_period = last_period + datetime.timedelta(days=cycle_length)
    ovulation_start = last_period + datetime.timedelta(days=(cycle_length // 2) - 3)
    ovulation_end = last_period + datetime.timedelta(days=(cycle_length // 2) + 3)
    return next_period, ovulation_start, ovulation_end

def provide_advice(symptoms):
    if symptoms:
        print("\nChatbot: Based on the symptoms you provided, here are some general tips:")
        for symptom in symptoms:
            if 'cramps' in symptom.lower():
                print("- Drink plenty of water and try a warm compress.")
            elif 'mood' in symptom.lower():
                print("- Practice relaxation techniques and ensure you get enough sleep.")
            elif 'headache' in symptom.lower():
                print("- Consider over-the-counter pain relief and rest.")
            else:
                print(f"- For '{symptom}', monitor the symptom and consult a healthcare provider if needed.")
    else:
        print("\nChatbot: No symptoms were logged today. Remember to track any symptoms for more personalized advice.")

def period_tracker():
    history = load_history()
    
    # Debug: Print the history file contents
    print("Debug: Loaded history data")
    json.dumps(history, indent=4)
    
    # Check if user is in history
    user_name_input = input("Chatbot: Please enter your name to check your history: ").strip()
    user_id = None
    existing_user = None
    for key, value in history.items():
        if value.get('name', '').lower() == user_name_input.lower():
            user_id = key
            existing_user = value
            break
    
    if existing_user:
        user_name, last_period, cycle_length, period_length, symptom_log = get_user_details(existing_user)
        
        # Ask if the user wants to update their data
        while True:
            update_choice = input("Chatbot: Would you like to update your period history with new data? (Yes/No): ").strip().lower()
            if update_choice in ['yes', 'no']:
                break
            else:
                print("Chatbot: Please enter 'Yes' or 'No'.")
        
        if update_choice == 'yes':
            next_period, ovulation_start, ovulation_end = estimate_next_period(last_period, cycle_length)
            
            # Update history
            user_id = f"{user_name}_{last_period}"
            history[user_id] = {
                "name": user_name,
                "last_period": last_period.strftime('%Y-%m-%d'),
                "cycle_length": cycle_length,
                "period_length": period_length,
                "symptom_log": symptom_log,
                "next_period": next_period.strftime('%Y-%m-%d'),
                "ovulation_start": ovulation_start.strftime('%Y-%m-%d'),
                "ovulation_end": ovulation_end.strftime('%Y-%m-%d')
            }
            save_history(history)
            
            print(f"\nChatbot: {user_name}, based on the information you provided:")
            print(f"Your next period is expected to start on: {next_period.strftime('%Y-%m-%d')}")
            print(f"Your ovulation window is likely between: {ovulation_start.strftime('%Y-%m-%d')} and {ovulation_end.strftime('%Y-%m-%d')}")
            print(f"Period length: {period_length} days")
            
            provide_advice(symptom_log)
            
            print("\nChatbot: I've updated your period history.")
        else:
            print("\nChatbot: No updates made to your period history.")
    
    else:
        user_name, last_period, cycle_length, period_length, symptom_log = get_user_details()
        
        next_period, ovulation_start, ovulation_end = estimate_next_period(last_period, cycle_length)
        
        # Store history
        user_id = f"{user_name}_{last_period}"
        history[user_id] = {
            "name": user_name,
            "last_period": last_period.strftime('%Y-%m-%d'),
            "cycle_length": cycle_length,
            "period_length": period_length,
            "symptom_log": symptom_log,
            "next_period": next_period.strftime('%Y-%m-%d'),
            "ovulation_start": ovulation_start.strftime('%Y-%m-%d'),
            "ovulation_end": ovulation_end.strftime('%Y-%m-%d')
        }
        save_history(history)
        
        print(f"\nChatbot: {user_name}, based on the information you provided:")
        print(f"Your next period is expected to start on: {next_period.strftime('%Y-%m-%d')}")
        print(f"Your ovulation window is likely between: {ovulation_start.strftime('%Y-%m-%d')} and {ovulation_end.strftime('%Y-%m-%d')}")
        print(f"Period length: {period_length} days")
        
        provide_advice(symptom_log)
        
        print("\nChatbot: I've saved your period history. If you need to check past records or have any other questions, just let me know!")

if __name__ == "__main__":
    period_tracker()
