from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def move_pallet():
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=8080)