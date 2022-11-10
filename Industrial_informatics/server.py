from flask import Flask, request, jsonify
from orchestrator import Orchestrator

app = Flask(__name__)
orchestrator = Orchestrator()

@app.route('/')
def move_pallet():
    data = request.json
    print(data)
    return jsonify(data)

def check_zone_change(data):
    if data["id"] == "Z1_Changed":
        orchestrator.change_ws_state("Z1")
    elif data["id"] == "Z2_Changed":
        orchestrator.change_ws_state("Z2")
    elif data["id"] == "Z3_Changed":
        orchestrator.change_ws_state("Z3")
    elif data["id"] == "Z4_Changed":
        orchestrator.change_ws_state("Z4")
    elif data["id"] == "Z5_Changed":
        orchestrator.change_ws_state("Z5")
    

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=8080)