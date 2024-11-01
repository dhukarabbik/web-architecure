from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

# List of stock companies
stocks = {
    'AAPL': 150.00,
    'GOOGL': 2800.00,
    'AMZN': 3400.00,
    'MSFT': 300.00,
    'TSLA': 700.00
}

def update_stock_prices():
    while True:
        time.sleep(2)  # Update every 2 seconds
        for stock in stocks:
            # Simulate random price change
            change = random.uniform(-5, 5)  # Random change between -5 and 5
            stocks[stock] = round(stocks[stock] + change, 2)
        # Emit the updated stock prices to all connected clients
        print(f"Emitting updated prices: {stocks}")  # Log the updated prices
        socketio.emit('update_prices', stocks)

@socketio.on('connect')
def handle_connect():
    print('Client connected')  # Log when a client connects

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start the background thread for updating stock prices
    thread = Thread(target=update_stock_prices)
    thread.start()
    socketio.run(app)
