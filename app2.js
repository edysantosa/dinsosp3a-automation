const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();
app.use(express.json({limit: '25mb'}));
app.use(express.urlencoded({limit: '25mb', extended: true}));
const cors = require('cors');
app.use(cors());

const spawn = require('node:child_process').spawn;

const spawnPromise = (cmd, args) => {
    return new Promise((resolve, reject) => {
        try {
            // const runCommand = spawn(cmd, args, {shell: true});
            // runCommand.stdout.on('data', data => resolve(data.toString()));
            // runCommand.on('error', err => {
            //     throw new Error(err.message);
            // });
            const pyprog = spawn(cmd, args, {shell: true});
            pyprog.stdout.on('data', (data) => {
                resolve(data.toString());
            });
            pyprog.stderr.on('data', (data) => {
                reject(data.toString());
            });
        } catch (e) {
            reject(e);
        }
    });
};


// Dapatkan qrcode untuk otentifikasi
app.get('/test', (req, res) => {
    res.write('welcome\n');

    // runPy.then((fromRunpy) => {
    //     console.log(fromRunpy.toString());
    //     res.end(fromRunpy);
    // }).catch(err => {
    //   console.log(err)
    // });

    spawnPromise('.\\env\\Scripts\\python.exe .\\download_agenda.py').then(
        data => {
            spawnPromise('.\\env\\Scripts\\python.exe .\\test.py').then(
                data => console.log('data: ', data)
            ).catch((err) => console.log(err));;
        }
    ).catch((err) => console.log(err));;

    // spawnPromise('python ./downl.py', ['-h']).then(
    //     data => console.log('data: ', data)
    // );

    res.end("fromRunpy");

    // const spawn = require('node:child_process').spawn;
    // const spawnPromise = (cmd, args) => {
    //     return new Promise((resolve, reject) => {
    //     try {
    //         const runCommand = spawn(cmd, args);
    //             runCommand.stdout.on('data', data => resolve(data.toString()));
    //             runCommand.on('error', err => {
    //             throw new Error(err.message);
    //         });
    //     } catch (e) {
    //         reject(e);
    //     }
    //     });
    // };


});
 
// Jalankan express di port 8000
// app.listen(8000, function() {
//     console.log('Server berjalan di port *:8000');
// });
app.listen(8000, () => {
    console.log('Server berjalan di port *:8000');
});