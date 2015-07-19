from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/bot', methods = ['POST'])
def bot():
    #data = request.form['bullshit']
    #print "the data recieved : {}".format(data)
    return jsonify(name="TestBot", folded=False, bet=4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug = True)
