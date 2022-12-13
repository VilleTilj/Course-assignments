# SCADA-system

This project consists of creating a SCADA (Supervisory Control And Data Acquisition) system for FASTORY assembly line in Tampere University. With it will get robot state changes in the CAMX 2541 standard. The changes are gotten via middleware that send mqtt-messages over broker and the application subscribes to that. The application follows MVC (Model-View-Control) pattern to save, control and showing the data to the user. 

## Used technologies
- Python (Flask backend)
- MQTT
- SQLITE
- JavaScript
- CSS
- HTML
