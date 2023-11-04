import nltk
import spacy
import requests
from nltk.chat.util import Chat, reflections

class Chatbot:
    def __init__(self):
        # Initialize NLTK and spaCy
        nltk.download('punkt')
        self.nlp = spacy.load("en_core_web_sm")
        # Initialize the chatbot
        self.chatbot = Chat([
            # Greetings and introductions
            ('hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
            ('how are you', ['I am good, thank you.', 'I am doing well.']),
            ('what is your name', ['I am a chatbot.', 'I go by ChatGPT.']),
            ('(.*) your name', ['My name is ChatGPT.', 'I am ChatGPT, your virtual assistant.']),
            ('bye|goodbye', ['Goodbye!', 'See you later!', 'Farewell!']),

            # Jokes
            ('tell me a joke', ['Why did the computer keep freezing? Because it left its Windows open!']),

            # Weather information
            ('weather', ['I can check the weather for you. Please provide your location.']),
        ], reflections)
        self.context = {}

    def respond(self, user_input):
        response = self.chatbot.respond(user_input)
        if 'joke' in user_input:
            self.context['told_joke'] = True
        if 'weather' in user_input:
            if 'location' not in self.context:
                self.context['location'] = user_input
                response = f"Sure, I can check the weather for {user_input}. Please provide a date."
            elif 'date' not in self.context:
                self.context['date'] = user_input
                response = f"Great! I'll check the weather for {self.context['location']} on {user_input}."
            else:
                # Integrate with OpenWeatherMap API to get weather information
                weather_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
                location = self.context['location']
                date = self.context['date']
                url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}'
                try:
                    response_data = requests.get(url).json()
                    temperature = response_data['main']['temp']
                    description = response_data['weather'][0]['description']
                    response = f"The weather in {location} on {date} is {description} with a temperature of {temperature}°C."
                except Exception as e:
                    response = "I couldn't retrieve weather information. Please try again later."
        return response

# Example usage:
chatbot = Chatbot()
print("ChatGPT: Hello! How can I help you today? (Type 'exit' to end)")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("ChatGPT: Goodbye!")
        break
    response = chatbot.respond(user_input)
    print("ChatGPT:", response)
