//Empieza con mayúscula porque es una clase.
//const EventEmitter = require('events');
//const emitter = new EventEmitter();

const Logger = require('./logger.js');
const logger = new Logger(); //Instancia de la clase Logger de logger.js

//Crear un Listener del evento
//El primer argumento "messageLogged" debe llamarse igual al argumento del emit.
logger.on('messageLogged',/*function*/(arg) =>{// e, eventArg
    console.log('Listener called', arg)
})

logger.log('message')


// Raise: logging (data:message)