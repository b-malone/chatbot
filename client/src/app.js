/**
 * Module dependencies
 */
// var express = require('express');
var routes = require('./routes');
var api = require('./routes/api');
// var http = require('http');
var path = require('path');

// development only
if (app.get('env') === 'development') {
    // app.use(express.errorHandler());
}

// production only
if (app.get('env') === 'production') {
    // TODO
};
  

/**
 * Routes
 */
// serve index and view partials
app.get('/', routes.index);

// Socket.io Communication
io.sockets.on('connection', require('./routes/socket'));

/**
 * Start Server
 */
// server.listen(app.get('port'), function () {
//     console.log('Express server listening on port ' + app.get('port'));
// });
