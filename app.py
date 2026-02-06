import os
import psycopg2 # ← これに戻します
from flask import Flask, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# --- データベース接続関数（本番用に戻しました！） ---
def get_db_connection():
    url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(url)
    return conn

# --- データベースの初期設定 ---
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # PostgreSQL用の方言：SERIAL PRIMARY KEY に戻します
    c.execute('CREATE TABLE IF NOT EXISTS stamps (id SERIAL PRIMARY KEY, stamp_date DATE UNIQUE)')
    conn.commit()
    conn.close()

# --- スタンプを押した日付を全部取得する ---
def get_stamped_dates():
    init_db()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT stamp_date FROM stamps')
    # PostgreSQLから日付を文字列のリストにして取得
    dates = [row[0].strftime('%Y-%m-%d') for row in c.fetchall()]
    conn.close()
    return dates

# --- 今日のスタンプを押す ---
def add_today_stamp():
    conn = get_db_connection()
    c = conn.cursor()
    today = datetime.now().date()
    # PostgreSQL用の「重複無視」の書き方に戻します
    c.execute('INSERT INTO stamps (stamp_date) VALUES (%s) ON CONFLICT DO NOTHING', (today,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    stamped_dates = get_stamped_dates()
    return render_template('index.html', stamped_dates=stamped_dates)

@app.route('/add')
def add():
    add_today_stamp()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)