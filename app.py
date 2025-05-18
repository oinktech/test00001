from flask import Flask, render_template_string, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# SSH 伺服器資訊
SSH_INFO = {
    "host": "192.168.1.100",
    "port": 22,
    "username": "your_user",
    "password": "your_password"
}

# 建立登入紀錄的資料表
def init_db():
    conn = sqlite3.connect('logins.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 🔐 模擬 SSH 登入（實際可接入 paramiko）
def simulate_ssh_login(username):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('logins.db')
    c = conn.cursor()
    c.execute('INSERT INTO logins (username, timestamp) VALUES (?, ?)', (username, timestamp))
    conn.commit()
    conn.close()

# 📄 網站頁面
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        simulate_ssh_login(username)
        return redirect("/")

    conn = sqlite3.connect('logins.db')
    c = conn.cursor()
    c.execute("SELECT username, timestamp FROM logins ORDER BY id DESC")
    logins = c.fetchall()
    conn.close()

    return render_template_string('''
        <h2>🔐 SSH 登入資訊</h2>
        <p>主機：{{ host }}<br>帳號：{{ user }}<br>密碼：{{ password }}</p>
        <hr>
        <form method="post">
            <label>模擬 SSH 登入：</label>
            <input name="username" placeholder="輸入使用者名稱" required />
            <button type="submit">登入</button>
        </form>
        <hr>
        <h3>📜 登入紀錄：</h3>
        <ul>
        {% for user, time in logins %}
            <li>{{ time }} - {{ user }}</li>
        {% endfor %}
        </ul>
    ''', host=SSH_INFO["host"], user=SSH_INFO["username"], password=SSH_INFO["password"], logins=logins)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
