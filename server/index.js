const express = require('express');
const bodyparser = require('body-parser');

const { port } = require('./config');

var cors = require('cors');
var app = express();


console.log(`Your port is ${port}`); 
app.use(bodyparser.json({limit: '150mb'}))
app.use(cors())
var customer = require('./routes/customer.js')
app.use('/customer',customer)


app.listen(port,()=>{
    console.log('Express server is running at port 3000');
})

app.get('/test',(req,res)=>{
    console.log('test')
})







