# URL Shortener Service 🔗

A simple and efficient **URL Shortener Web Application** built with **Flask** and **SQLite**.  
This project allows users to shorten long URLs into short, shareable links, track click counts, and view recent activity.

---

## 🚀 Features
- Shorten long URLs into unique short codes.
- Persistent storage using **SQLite**.
- Click tracking (counts how many times a short link is used).
- Recent 10 shortened URLs displayed on the homepage.
- User-friendly **Bootstrap-based UI**.
- 404 Error page for invalid/expired short codes.
- Session-based flash messages for better interaction.

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask, SQLite
- **Frontend:** HTML, Bootstrap, Jinja2
- **Other:** Git, VS Code

---

## 📂 Project Structure
url_shortener/
│── app.py # Main Flask application
│── urls.db # SQLite database (auto-created)
│── templates/ # HTML templates
│ ├── layout.html
│ ├── index.html
│ └── 404.html
│── static/ # CSS/JS (Bootstrap via CDN)
│── requirements.txt # Dependencies


---

## ⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ayushxx17/url-shortener-flask-service.git
   cd url-shortener-flask-service
2. Create a virtual environment and activate it:
   python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On Mac/Linux
3. Install dependencies:
   pip install -r requirements.txt
4. Run the application:
   python app.py
5. Open your browser and go to:
   http://127.0.0.1:5000


📸 Screenshots


### Recently Shortened URLs
![Recent URLs](screenshots/recent_urls.png)


🔮 Future Improvements

--> User authentication (login to manage personal URLs).

--> Expiration dates for short links.

--> Analytics dashboard with charts.

--> Deployment on Render/Heroku for live access.


🤝 Contributing

Contributions are welcome! Feel free to open issues and pull requests.

📜 License

This project is licensed under the MIT License.


👨‍💻 Developed by Ayush Kumar Singh
