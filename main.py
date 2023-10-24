from gevent import monkey
monkey.patch_all()
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from flask import Flask
from replit import db
from gevent.pywsgi import WSGIServer
from flask_compress import Compress

app = Flask(__name__, static_folder='static')

def to_sats(i):
  return i * 100_000_000
  
def fetch_data():
    response = requests.get('https://blockchain.info/tobtc?currency=USD&value=1')
    if response.status_code == 200:
        db['usd'] = to_sats(float(response.json()))
    else:
        return 'Error: Unable to fetch data'


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_data, 'interval', hours=1)
scheduler.start()

@app.route('/')
def index():
    return f"""
      <link rel="stylesheet" type="text/css" href="/static/style.css">
      <body>
      <div><h1>Relative SATS benchmarks (updated every hour)</h1>
      <p>For people interested in spending their BTC</p>
      <span class="large-number">$1 = {format(int(db['usd']), ',')}</span> SATS
      <ul class="list-unstyled">
        <li><span class="large-number">{format(int(db['usd']) * 15, ',')}</span> 
        SATS = 🍔 ($15 meal)</li>
        <li><span class="large-number">{format(int(db['usd']) * 70, ',')}</span> 
        SATS = 📶 ($70 service)</li>
        <li><span class="large-number">{format(int(db['usd']) * 200, ',')}</span> 
        SATS = 🧥 ($200 nice jacket)</li>
        <li><span class="large-number">{format(int(db['usd']) * 500, ',')}</span> 
        SATS = 🎸 ($500 instrument)</li>
        <li><span class="large-number">{format(int(db['usd']) * 900, ',')}</span> 
        SATS = 📱 ($900 phone)</li>
        <li><span class="large-number">{format(int(db['usd']) * 3500, ',')}</span> 
        SATS = 💍 ($3,500 wedding ring)</li>
      </ul>
      </div></body>
      """

fetch_data()

compress = Compress()
compress.init_app(app)

http_server = WSGIServer(('0.0.0.0', 8080), app)
http_server.serve_forever()

