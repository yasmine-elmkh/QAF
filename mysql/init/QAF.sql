-- Sélection de la base
USE chatbot;

-- Création de la table FAQ
CREATE TABLE IF NOT EXISTS faqs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  question TEXT NOT NULL,
  answer TEXT NOT NULL
);

-- Création de la table chat_logs
CREATE TABLE IF NOT EXISTS chat_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_message TEXT,
  bot_reply TEXT,
  similarity_score FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO faqs (question, answer) VALUES
-- Salutations
('Hi', 'Hello! How can I help you today?'),
('Hey', 'Hey there! What can I do for you?'),
('Good morning', 'Good morning! How are you today?'),
('Good evening', 'Good evening! Hope you had a good day.'),

-- Informations générales sur le bot
('Who created you?', 'I was created by Yasmine El Mkhantar.'),
('What can you do?', 'I can answer simple questions and chat with you.'),
('How old are you?', 'I do not have an age. I am a bot!'),
('Are you intelligent?', 'I try my best to help you using AI!'),

-- Conversations courantes
('How is the weather?', 'I cannot see the weather, but I hope it is nice!'),
('What time is it?', 'I cannot tell the exact time, please check your device.'),
('Tell me a joke', 'Why did the computer show up at work late? It had a hard drive!'),
('Thank you', 'You are welcome!'),
('Thanks', 'No problem!'),

-- FAQ spécifiques
('What is your name?', 'I am Alpha Bot.'),
('How are you?', 'I am always fine, thanks for asking!'),
('Hello', 'Hi there!'),
('Can you help me?', 'Yes! Ask me any question you want.'),
('Do you like humans?', 'Of course! My purpose is to help humans.'),
('What is AI?', 'AI stands for Artificial Intelligence.'),
('What is machine learning?', 'Machine Learning is a field of AI that allows computers to learn from data.'),
('What is deep learning?', 'Deep Learning is a type of machine learning using neural networks.'),
('Goodbye', 'Goodbye! Have a nice day.'),
('Bye', 'See you later! Take care.');
