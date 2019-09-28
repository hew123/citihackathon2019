var express = require('express')
var router = express.Router()
var pool = require('../database.js')


router.get('/test',(req,res)=>{
    pool.getConnection((err,connection)=>{
        if(err)
        {
            console.log(err)
        }
        else 
        {
            console.log(connection)
        }
        res.send('success')
    })
})


module.exports = router