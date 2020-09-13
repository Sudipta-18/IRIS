const express = require('express');
const {spawn} = require('child_process');
const fs = require('fs');
const cors = require('cors');
const app = express();

app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));

app.use(cors());


app.get('/', (req, res) => {
    fs.readFile('public/text_files/text.txt', function(err, data) {
        if(err) {
            console.log(err);
        } else {
            data = data.toString();
            // console.log(data);
            return res.json({data: data});
        }
    });
});

app.get('/script', (req, res) => {
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['script1.py']);
    // collect data from script
    python.stdout.on('data', function (data) {
    // console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    console.log(dataToSend);
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    // console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    return res.json({success: 1});
    });
    //return res.json({success: 1});
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log('Server Started!!!');
});


