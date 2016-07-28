from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/bot', methods = ['POST'])
def bot():
    data = request.get_json()
    bet = data["past_moves"][-1]["bet"]
    print(bet)
    return jsonify(name="TestBot", folded=False, bet=4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
