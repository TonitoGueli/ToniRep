const os = require('os');

var totalMemory = os.totalmem();

var freeMemory = os.freemem();

//console.log('total memory '+totalMemory);

// Template String
//ES6 / ECMAScript 6 
// Sintanxis `` para string puro || ${} Para parámetros

console.log(`Total Memory: ${totalMemory}`);
console.log(`Free Memory: ${freeMemory}`);