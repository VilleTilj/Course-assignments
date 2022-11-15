from flask import Flask, request, jsonify
from .orchestrator import Orchestrator

app = Flask(__name__)
orchestrator = Orchestrator()


@app.route('/')
def move_pallet():
    data = request.json
    orchestrator.workstation.trans_zone12()
    print(data)
    return jsonify(data)


def check_zone_change(data):
    if data["id"] == "Z1_Changed":
        orchestrator.change_ws_state("Z1")
        if orchestrator.workstation.zone_states["Z1"]:
            orchestrator.move_pallet("Z1", data["payload"]["PalletID"])
    elif data["id"] == "Z2_Changed":
        orchestrator.change_ws_state("Z2")
        if orchestrator.workstation.zone_states["Z2"]:
            orchestrator.move_pallet("Z2", data["payload"]["PalletID"])
    elif data["id"] == "Z3_Changed":
        orchestrator.change_ws_state("Z3")
        if orchestrator.workstation.zone_states["Z3"]:
            orchestrator.robot_draw(data["payload"]["PalletID"])
    elif data["id"] == "DrawEndExecution":
            orchestrator.move_pallet("Z3", data["payload"]["PalletID"])
    elif data["id"] == "Z4_Changed":
        orchestrator.change_ws_state("Z4")
        if orchestrator.workstation.zone_states["Z4"]:
            orchestrator.move_pallet("Z4", data["payload"]["PalletID"])
    elif data["id"] == "Z5_Changed":
        orchestrator.change_ws_state("Z5")
        if orchestrator.workstation.zone_states["Z5"]:
            orchestrator.move_pallet("Z5", data["payload"]["PalletID"])
    

def move_pallet():
    pass


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=8080)