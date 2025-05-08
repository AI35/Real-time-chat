# Real-Time Chat Application
A real-time chat application built with Django and Channels, allowing users to communicate instantly in chat rooms.

## Features
- Real-time messaging using WebSockets
- User authentication and authorization
- Multiple chat rooms
- Message history
- Responsive design

## Technologies Used
- Django 5.2.1
- Django Channels 4.0.0
- Daphne 4.0.0
- Channels Redis 4.1.0
- WhiteNoise 6.5.0
- Django CORS Headers 4.3.0

## Prerequisites
- Python 3.9+
- pip

## Installation
1. Clone the repository
```bash
git clone github.com/Ai35/Real-time-chat.git
```
2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate
```
3. Install the dependencies
```bash
pip install -r requirements.txt
```
4. Set up the database
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```
6. Collect static
```bash
python manage.py collectstatic
```
7. Run the server
```bash
python run_daphne.py
```
## Usage
1. Open the application in your web browser
2. Log in with your superuser credentials
3. Create a new chat room or join an existing one
4. Start chatting with other users in real-time

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments
- Django Channels documentation
- Channels Redis documentation
- Django documentation
- Python documentation
