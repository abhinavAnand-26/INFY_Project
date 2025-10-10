🧠 SmartQuizzer – AI-Based Adaptive Quiz Platform

A Django-powered quiz app with AI-driven question generation, adaptive learning, and gamified progression.

🌟 Key Highlights
🤖 AI Intelligence

MCQ Generation: Extracts from PDFs or uses AI to create 50 questions per topic.

Adaptive Difficulty: Automatically increases quiz level based on your performance.

AI Learning Assistant: Chatbot explains topics in simple terms.

Smart Suggestions: Personalized quiz recommendations using Google Gemini AI.

Performance Insights: AI analyzes your results to guide improvement.

Topic Requests: Users can ask for new topics—AI generates them automatically.

🎮 Gamification

Earn XP, levels, and badges for accuracy and streaks.

Track daily streaks, leaderboards, and progress charts.

📊 Analytics

Real-time Dashboard with interactive charts.

Track performance by week, month, or topic.

Admins get full user growth and usage analytics.

🎯 Adaptive Learning

Prevents skipping levels without mastering the basics.

Gives personalized topic recommendations.

Includes structured learning paths and topic tracking.

🧩 Quiz Features

Combines PDF + AI questions seamlessly.

Filters by topic, subtopic, and difficulty.

Shows correct answers and explanations after quizzes.

Timer, confidence rating, and keyboard shortcuts for quick input.

👥 User & Admin Management

Role-based dashboards for users and admins.

Admin Tools: Manage users, block/unblock, view growth stats.

User Profiles: Custom settings, progress tracking, password security.

💻 UI/UX

Modern design: Responsive, animated, and accessible.

Interactive forms and charts with live data updates.

⚙️ Installation

Clone Repo:

git clone https://github.com/dharani043/Smart_Quizzer.git
cd Smart_Quizzer


Setup Environment:

python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac


Install Dependencies:

pip install -r requirements.txt


Configure .env File:
Copy .env.example → .env and add your Google AI API key.

Migrate & Run:

python manage.py migrate
python manage.py runserver

🔐 Security & Deployment

Store your API keys securely in .env.

Example environment variables:

export SECRET_KEY="your-key"
export DEBUG="False"
export ALLOWED_HOSTS="yourdomain.com"
export GOOGLE_AI_API_KEY="your-api-key"

🏗️ Project Structure
smartquizzer/
├── base/ (core logic)
├── media/ (user uploads)
├── static/ (CSS, JS, images)
├── sample/ (settings, URLs)
└── requirements.txt

🎮 Rules & Configurations

Quiz Progression:

Easy → Medium: 5 attempts, 80% avg

Medium → Hard: 5 attempts, 75% avg

Hard → Next Topic: 3 attempts, 80% avg

XP System:

10 XP per quiz, +5 bonus for 80%+ score

1.5× multiplier for daily streaks

🧠 AI Integration

Google Gemini AI powers question generation and insights.

Caching improves performance and reduces API calls.

🤝 Contributing

Fork & create a branch

Commit your changes

Open a Pull Request

📝 License

Licensed under the MIT License.
Made with ❤️ to make learning smarter and more engaging.

Would you like me to simplify it even further for use as a presentation script or one-page summary?

You said:
add a line between each sub topics for git hub
ChatGPT said:

Sure! Here’s your simplified SmartQuizzer README formatted with clear line breaks between each subtopic — perfect for GitHub readability 👇

🧠 SmartQuizzer – AI-Based Adaptive Quiz Platform

A Django-powered quiz app with AI-driven question generation, adaptive learning, and gamified progression.

🌟 Key Highlights
🤖 AI Intelligence

MCQ Generation: Extracts from PDFs or uses AI to create 50 questions per topic.

Adaptive Difficulty: Automatically increases quiz level based on your performance.

AI Learning Assistant: Chatbot explains topics in simple terms.

Smart Suggestions: Personalized quiz recommendations using Google Gemini AI.

Performance Insights: AI analyzes your results to guide improvement.

Topic Requests: Users can ask for new topics—AI generates them automatically.

🎮 Gamification

Earn XP, levels, and badges for accuracy and streaks.

Track daily streaks, leaderboards, and progress charts.

📊 Analytics

Real-time Dashboard with interactive charts.

Track performance by week, month, or topic.

Admins get full user growth and usage analytics.

🎯 Adaptive Learning

Prevents skipping levels without mastering the basics.

Gives personalized topic recommendations.

Includes structured learning paths and topic tracking.

🧩 Quiz Features

Combines PDF + AI questions seamlessly.

Filters by topic, subtopic, and difficulty.

Shows correct answers and explanations after quizzes.

Timer, confidence rating, and keyboard shortcuts for quick input.

👥 User & Admin Management

Role-based dashboards for users and admins.

Admin Tools: Manage users, block/unblock, view growth stats.

User Profiles: Custom settings, progress tracking, password security.

💻 UI/UX

Modern design: Responsive, animated, and accessible.

Interactive forms and charts with live data updates.

⚙️ Installation

Clone Repo:

git clone https://github.com/dharani043/Smart_Quizzer.git
cd Smart_Quizzer


Setup Environment:

python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac


Install Dependencies:

pip install -r requirements.txt


Configure .env File:
Copy .env.example → .env and add your Google AI API key.

Migrate & Run:

python manage.py migrate
python manage.py runserver

🔐 Security & Deployment

Store your API keys securely in .env.

Example environment variables:

export SECRET_KEY="your-key"
export DEBUG="False"
export ALLOWED_HOSTS="yourdomain.com"
export GOOGLE_AI_API_KEY="your-api-key"

🏗️ Project Structure
smartquizzer/
├── base/ (core logic)
├── media/ (user uploads)
├── static/ (CSS, JS, images)
├── sample/ (settings, URLs)
└── requirements.txt

🎮 Rules & Configurations

Quiz Progression:

Easy → Medium: 5 attempts, 80% avg

Medium → Hard: 5 attempts, 75% avg

Hard → Next Topic: 3 attempts, 80% avg

XP System:

10 XP per quiz, +5 bonus for 80%+ score

1.5× multiplier for daily streaks

🧠 AI Integration

Google Gemini AI powers question generation and insights.

Caching improves performance and reduces API calls.

🤝 Contributing

Fork & create a branch

Commit your changes

Open a Pull Request

📝 License

Licensed under the MIT License.

Made with ❤️ to make learning smarter and more engaging.
