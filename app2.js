const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();
app.use(express.json({limit: '25mb'}));
app.use(express.urlencoded({limit: '25mb', extended: true}));
const cors = require('cors');
app.use(cors());


app.post('/send-group-message', (req, res) => {
    data = req.body;

    whatsapp.getChats().then((result) => {
        chat = result.find((chat) => chat.name === data.group_name);

        if (data.file) {
            if (!data.mimetype) {
                res.status(200).json({
                    result: false,
                    message: "mimetype perlu diisi"
                });
            }

            media = new MessageMedia(data.mimetype, data.file, data.filename);

            chat.sendMessage(media, {caption: data.caption}).then((result) => {
                res.status(200).json({
                    result: true,
                    message: "Pesan terkirim"
                });
            }).catch((error) => {
                res.status(500).json({
                    result: false,
                    message: error.message
                });
            });
        } else {
            chat.sendMessage(data.message).then((result) => {
                res.status(200).json({
                    result: true,
                    message: "Pesan terkirim"
                });
            }).catch((error) => {
                res.status(500).json({
                    result: false,
                    message: error.message
                });
            });
        }

    }).catch((error) => {
        res.status(200).json({
            result: false,
            message: 'DISCONNECTED'
        });
    });
});


 
// Jalankan express di port 8000
// app.listen(8000, function() {
//     console.log('Server berjalan di port *:8000');
// });
app.listen(8000, () => {
    console.log('Server berjalan di port *:8000');
});