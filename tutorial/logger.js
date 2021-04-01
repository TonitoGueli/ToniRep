const EventEmitter = require('events');
const emitter = new EventEmitter();

var url = 'http://mylogger.io/log';

class Logger extends EventEmitter{//La clase Logger tendrá todas las funcionalidades del EventEmitter

    /*function*/ log(message){
        //Send http request
        console.log(message)
    //Este es el evento que el listener va a escuchar
    //Emit = making a noise, produce something.
    this.emit('messageLogged',{id: 1, url: 'http://'})
    }
}
module.exports = Logger;