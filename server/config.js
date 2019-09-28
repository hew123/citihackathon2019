const dotenv = require('dotenv');
dotenv.config();

module.exports = {
    port: process.env.PORT,
    dbHost:process.env.HOST,
    dbUser:process.env.DB_USER,
    dbPassword:process.env.PASSWORD,
    db:process.env.DATABASE,
    AWSAccessKeyId:process.env.AWSACCESSKEYID,
    AWSSecretKey:process.env.AWSSECRETKEY,
    Bucket:process.env.BUCKET,
    sgApiKey:process.env.SGAPIKEY,
    secretKey:process.env.SECRETKEY

}