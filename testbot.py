from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/bot', methods = ['POST'])
def bot():
    #data = request.json
    return jsonify(name="TestBot", folded=False, bet=4)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
