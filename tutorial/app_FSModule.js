const fs = require('fs')

const filesArray = fs.readdirSync('./')
console.log(filesArray)


fs.readdir('$',function(err,filesArray){
    if(err) console.log ('Error',err);
    else console.log('Result',filesArray)
})