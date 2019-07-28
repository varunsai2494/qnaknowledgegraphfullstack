    var express = require('express');

    var app = express(); 
    var morgan = require('morgan');             // log requests to the console (express4)
    var bodyParser = require('body-parser');    // pull information from HTML POST (express4)
    var methodOverride = require('method-override'); // simulate DELETE and PUT (express4)


// ================= configuration ================= //

    app.use(express.static(__dirname + '/public'));                 // set the static files location /public/img will be /img for users
    app.use(morgan('dev'));                                         // log every request to the console
    app.use(bodyParser.urlencoded({'extended':'true'}));            // parse application/x-www-form-urlencoded
    app.use(bodyParser.json());                                     // parse application/json
    app.use(bodyParser.json({ type: 'application/vnd.api+json' })); // parse application/vnd.api+json as json
    app.use(methodOverride());
    // Add headers
    app.use(function (req, res, next) {
        // Website you wish to allow to connect
        res.setHeader('Access-Control-Allow-Origin', 'http://35.164.231.42:8000/qna', 'http://35.164.231.42:8000/updategraph');

        // Request methods you wish to allow
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT');

        // Request headers you wish to allow
        res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

        // Set to true if you need the website to include cookies in the requests sent
        // to the API (e.g. in case you use sessions)
        res.setHeader('Access-Control-Allow-Credentials', true);

        // Pass to next layer of middleware
        next();
    });

// ================= listen (start app with node server.js) ======================================
    app.listen(8000);
    console.log("App listening on port 8000");