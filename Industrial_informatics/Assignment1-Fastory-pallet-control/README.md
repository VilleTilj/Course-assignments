# Fastory-line pallet control

This project is about controlling pallets in an assembly-line for small electronics. The assignment was to implement REST based event subscription and control the robot and conveyor workstations with the REST POST commands. To better see the program flow see the .drawio files.

## Logic
- Worksation moves pallets to different zones using conveyors
- Move pallet to robot that starts assembly if it has not been assembled yet. 
- Avoid collision between pallets.
 

## Used technologies
- Python (Flask backend)
- REST
- Wireshark (To monitor REST commands)
