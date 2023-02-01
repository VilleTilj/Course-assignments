const express = require('express'); //Import the express dependency
const app = express();              //Instantiate an express app, the main work horse of this server
const port = 3000;                  // Save the port number where the server is listening

const bodyParser = require('body-parser'); //Makes parsin the request easier
app.use(bodyParser.json()); //Set application/json as the default


let building = require('./data/building.json');
let sensors = require('./data/sensors.json');


// Start server
const server = app.listen(port, () => {
    console.log(`Server is now listening on port ${port}`);
    
});