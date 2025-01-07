from flask import Flask, request, redirect
import sqlite3
import random
import string
import sys

app = Flask(__name__)

def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

@app.route("/make")
def shorturl():
    try:
        url = request.args.get("url")
        cd = randomname(10)
        filepath = "shorturl.sqlite"
        conn = sqlite3.connect(filepath) 
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS shorturl(id, code, url)""")
        cur.execute(f"INSERT OR REPLACE INTO shorturl(code, url) VALUES('{cd}', '{url}');")
        conn.commit()
        cur.close()
        conn.close()
        return f"{cd}"
    except:
        return "None"

@app.route("/<code>")
def index(code):
    try:
        filepath = "shorturl.sqlite"
        conn = sqlite3.connect(filepath) 
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM shorturl WHERE code = "{code}"')
        return redirect(f"{cur.fetchall()[0][2]}")
    except:
        return f"Error<br>{sys.exc_info()}"
