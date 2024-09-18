# chatbot
 <!-- chat bot using python -->
python -m spacy download en_core_web_sm
python3 period-tracker-chatbot/period-tracker.py

docker build -t chatbot-image .
docker run -it chatbot-image