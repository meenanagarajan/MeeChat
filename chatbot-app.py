from flask import Flask, render_template, request, jsonify
from nltk.chat.util import Chat, reflections

app = Flask(__name)

class Chatbot:
    def __init__(self):
        self.chatbot = Chat([
            # Greetings and introductions
            ('hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
            ('how are you', ['I am good, thank you.', 'I am doing well.']),
            ('what is your name', ['I am a chatbot.', 'I go by ChatGPT.']),
            ('(.*) your name', ['My name is ChatGPT.', 'I am ChatGPT, your virtual assistant.']),
            ('bye|goodbye', ['Goodbye!', 'See you later!', 'Farewell!']),

            # Jokes
            ('tell me a joke', ['Why did the computer keep freezing? Because it left its Windows open!'])
        ], reflections)
        self.context = {}

    def respond(self, user_input):
        response = self.chatbot.respond(user_input)
        return response

chatbot = Chatbot()

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    user_input = request.json.get('message')
    response = chatbot.respond(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
