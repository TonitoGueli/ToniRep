const Joi = require ('joi');
const express = require ('express');
const app = express();


app.use(express.json());

//npm init --yes
//npm i express
//npm i -g nodemon
//nodemon sirve para actualizar automáticamente los cambios en el sitio.
// -g es para instalarlo global

const courses = [
    {id: 1, name: 'course1'},
    {id: 2, name: 'course2'},
    {id: 3, name: 'course3'},
]

app.get('/',(req,res) =>{
    res.send('Hello World!!!')
})

app.get('/api/courses',(req,res)=>{
    res.send(courses)
})

app.get('/api/courses/:id',(req,res)=>{
    const course = courses.find(c => c.id === parseInt(req.params.id))
    if(!course) {
        res.status(404).send('No se encontró el curso con ese ID')
    }
        res.send(course)
})

app.post('/api/courses', (req,res) =>{

    const {error} = validateCourse(req.body); //{error} = result.error
    if(error){
        //400 Bad Request
        res.status(400).send(error.details[0].message);
        return;
    }
    const course = {
        id: courses.length+1,
        name: req.body.name
    };
    courses.push(course);
    res.send(course);
});

app.put('/api/courses/:id',(req,res) =>{
    //Buscar el curso
    //Si no existe, retornar 404

    const course = courses.find(c => c.id === parseInt(req.params.id))
    if(!course) {
        res.status(404).send('No se encontró el curso con ese ID')
        return;
    }
    //Validar el input
    //Si no es válido, retornar 400 - Bad Request
    
    const result = validateCourse(req.body);
    const {error} = validateCourse(req.body); //{error} = result.error
    if(error){
        //400 Bad Request
        res.status(400).send(error.details[0].message);
        return;
    }

    //Actualizar un curso
    course.name = req.body.name;

    //Retorna el curso actualizado
    res.send(course);
});

function validateCourse(course){
    const schema = Joi.object(
        {
            name:Joi.string().min(3).required()
        });

    return schema.validate(course);
}

app.delete ('/api/courses/:id',(req, res)=>{
    // Buscar el curso con el id que corresponde.
    //Si no existe, retornar 404.
    
    const course = courses.find(c => c.id === parseInt(req.params.id))
    if(!course) {
        res.status(404).send('No se encontró el curso con ese ID')
        return;
    }
    //Si existe, eliminar el registro.

    const index = courses.indexOf(course);
    courses.splice(index, 1);
    //Devolver el mismo curso

    res.send(course);
})

//---------------Inicio Misma ruta---------------
app.get('/api/post/:year/:month',(req,res)=>{
    res.send(req.params)
})

app.get('/api/post/:year/:month',(req,res)=>{
    res.send(req.query)
})
//---------------Cierre Misma ruta---------------


const PORT = process.env.PORT || 3000;
app.listen(PORT, ()=>console.log(`Listening on port ${PORT}...`))

