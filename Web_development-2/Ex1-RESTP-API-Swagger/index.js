const express = require('express'); //Import the express dependency
const app = express();              //Instantiate an express app, the main work horse of this server
const port = 8000;                  // Save the port number where the server is listening

const bodyParser = require('body-parser'); //Makes parsin the request easier
app.use(bodyParser.json()); //Set application/json as the default
const fs = require('fs')

let buildings = require('./data/building.json');
let sensors = require('./data/sensors.json');


const AddEndpointRulesBuilding = {
    id: 'id',
    name: 'name',
    address: 'address',
    street_address: 'street_address',
    post_number: "post_number"
}

const AddEndpointRulesSensor = {
    id: 'id',
    building_id: 'building_id',
    name: 'name',
    value: 'value',
    state: 'state',
}

function matches(body, rules, type) {
    var keys = Object.keys(body);
    if (type == "building") {
        var innerKeys = Object.keys(body['address']);
    }
    let i = 0;
    let j = 0;
    // Loop through building JSON format rules
    for (let attribute in rules) {
        if (i > 2 && type == "building") {
            if (innerKeys[j] !== rules[attribute]) {
                return false
            }
            j += 1;
        }
        else if ((i <= 2 ||type == "sensor") && keys[i] !== rules[attribute]) {
            return false;
        }
        i += 1;
    }
    // All checked out, request body is OK
    return true;
}


function write_json(json, file) {
    fs.writeFile(`./data/${file}.json`, JSON.stringify(json), 'utf-8',  function(err) {
        if (err) throw err;
        console.log('complete');
        }
    );
}

// Building API methods
app.get('/buildings', (request, response) => {
    response.status(200).json(buildings)
});

app.get('/buildings/:id', (request, response) => {
    let id = request.params.id;
    let building = buildings.filter(building => building.id == id);
    if ( building.length !== 0) {
        response.status(200).json(building)
    } else {
        response.status(404).send()
    }
});

app.post('/buildings', (request, response) => {
    let newBuilding = request.body; // Assume that the body contains json object
    if (!matches(newBuilding, AddEndpointRulesBuilding, "building" )) {
        console.log("Request body is invalid")
        response.status(400).send()
    } else {
        console.log(newBuilding)
        newBuilding.id = buildings.length + 1;
        buildings.push(newBuilding)
        write_json(buildings, 'building')
        response.status(201).json(newBuilding)
    }
});

app.patch('/buildings/:id', (request, response) => {
    let id = request.params.id;
    if (buildings[id]) {
        let updatedBuilding = request.body;
        if (Object.keys(updatedBuilding).length === 0) {
            console.log('Json content missing')
            
        } else if (!matches(updatedBuilding, AddEndpointRulesBuilding, "building" )) {
            console.log("Request body is invalid")
            
        } else {
            buildings[id] = updatedBuilding;
            write_json(buildings, 'building')
            return response.status(204).send();
        }
        return response.status(400).send();
    } 
});


// API methods for sensor model
app.put('/sensor', (request, response) => {
    let newSensor = request.body;
    console.log("test",newSensor)
    if (Object.keys(newSensor).length === 0) {
        console.log('Json content missing')
    }
    else if ( !matches(newSensor, AddEndpointRulesSensor, 'sensor')) {
        console.log("Request body is invalid");
        
    } else {
        console.log(newSensor);
        newSensor.id = sensors.length + 1;
        sensors.push(newSensor);
        write_json(sensors, 'sensors');
        return response.status(201).json(newSensor);
    }
    return response.status(400).send();
});


// API methods to retrieve sensors 
app.get('/sensor/building/:id', (request, response) => {
    let building_id = request.params.id;
    let sensor = sensors.filter(sensor => sensor.building_id == building_id);
    if (Object.keys(sensor).length === 0) {
        sensor = "There are no sensors in the requested building.";
    }
    return response.status(200).json(sensor)
});




// Start server
const server = app.listen(port, () => {
    console.log(`Server is now listening on port ${port}`);
    
});