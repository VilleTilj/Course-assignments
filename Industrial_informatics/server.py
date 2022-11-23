from flask import Flask, request
from orchestrator import Orchestrator
from time import sleep

WORKSTATION: int = 9

app = Flask(__name__)
orchestrator = Orchestrator(WORKSTATION)


# Method to move pallet through workstation using RTU events
def check_zone_change(data):
    if data["id"] == "Z1_Changed" and data["payload"]["PalletID"] != '-1':
        orchestrator.change_ws_state("Z1", pallet_id=data["payload"]["PalletID"], new_pallet=True)
        orchestrator.move_pallet("Z1", data["payload"]["PalletID"])
    elif data["id"] == "Z2_Changed" and data["payload"]["PalletID"] != '-1':
        orchestrator.move_pallet("Z2")
    elif data["id"] == "Z3_Changed" and  data["payload"]["PalletID"] != '-1':
        sleep(2)
        orchestrator.robot_draw(data["payload"]["PalletID"])
            
    elif data["id"] == "DrawEndExecution":
        orchestrator.move_pallet("Z3")

    elif data["id"] == "Z4_Changed" and  data["payload"]["PalletID"] != '-1':
        orchestrator.move_pallet("Z4")
    elif data["id"] == "Z5_Changed" and  data["payload"]["PalletID"] == '-1':
        orchestrator.move_pallet("Z5")
    elif data["id"] == "Z5_Changed" and  data["payload"]["PalletID"] != '-1':
        if orchestrator.workstation.zone3status() == '-1' and orchestrator.workstation.zone2status() != '-1':
            orchestrator.workstation.trans_zone23()
    


@app.route('/events',methods=['POST'])
def receive_events():
    print("endpoint hit")
    data = request.json
    print(data)
    check_zone_change(data)
    return "ok"


if __name__ == '__main__':
     app.run(host='192.168.0.'+str(WORKSTATION)+'0', port=8080, debug=True)