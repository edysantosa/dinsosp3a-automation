const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();
app.use(express.json({limit: '25mb'}));
app.use(express.urlencoded({limit: '25mb', extended: true}));
const cors = require('cors');
app.use(cors());

// WhatsApp.js
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const whatsapp = new Client({
    authStrategy: new LocalAuth()
});


/*
    Inisialisasi WhatsappJS
 */
let currentQrCode='';

whatsapp.on('qr', (qr) => {
    console.log('Server belum login. Scan qrcode dibawah untuk login');
    qrcode.generate(qr, {small: true});
    currentQrCode = qr;
});

whatsapp.on('ready', () => {
    console.log('Server WhatsApp siap!');
});

whatsapp.on('disconnected', () => {
    whatsapp.initialize();
});

whatsapp.on('change_state', (reason) => {
  // console.log('Client was logged out.', reason)
});

whatsapp.on('message', async msg => {
    if (msg.body === 'test') {
        msg.reply('tost');
    }
});

whatsapp.initialize();


/*
    Fungsi-fungsi API
 */


// Testing get
app.get('/', (req, res) => {
    res.status(200).json({
        result: true,
        message: "Hallo world"
    });
});

// Dapatkan status koneksi whatsapp-js
app.get('/status', (req, res) => {
    whatsapp.getState().then((result) => {
        let returnStatus = true;
        if (result !== 'CONNECTED') {
            returnStatus = false;
        }
        res.status(200).json({
            result: returnStatus,
            message: result
        });
    }).catch((error) => {
        res.status(200).json({
            result: false,
            message: 'DISCONNECTED'
        });
    });
});

// Dapatkan qrcode untuk otentifikasi
app.get('/qr', (req, res) => {
    res.status(200).json({
        result: true,
        message: currentQrCode
    });
});

// Kirim pesan whatsapp
app.post('/send-message', (req, res) => {
    data = req.body;

    if (data.file) {
        if (!data.mimetype || !data.file_name) {
            res.status(200).json({
                result: false,
                message: "mimetype dan file_name perlu diisi"
            });
        }

        media = new MessageMedia(data.mimetype, data.file, data.file_name);

        whatsapp.sendMessage(sanitizePhoneNumber(data.phone_number), media, {caption: data.message}).then((result) => {
            res.status(200).json({
                result: true,
                message: "Pesan terkirim"
            });
        }).catch((error) => {
            res.status(500).json({
                result: false,
                message: error.message
            });
        });;
    } else {
        whatsapp.sendMessage(sanitizePhoneNumber(data.phone_number), data.message).then((result) => {
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
});

app.post('/send-group-message', (req, res) => {
    data = req.body;

    whatsapp.getChats().then((result) => {
        chat = result.find((chat) => chat.name === data.group_name);

        if (data.file) {
            if (!data.mimetype || !data.file_name) {
                res.status(200).json({
                    result: false,
                    message: "mimetype dan file_name perlu diisi"
                });
            }

            media = new MessageMedia(data.mimetype, data.file, data.file_name);

            chat.sendMessage(media, {caption: data.message}).then((result) => {
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

function sanitizePhoneNumber(phone_number) {
    //First remove all spaces:
    new_phone = phone_number.replace(/\s/g, '');

    if(new_phone.startsWith("+")){
        // Kalo awalan nomor ada + berarti hilangkan +nya aja
        new_phone = new_phone.substr(1);
    } else if(new_phone.startsWith("0")){
        // Kalo awalan 0 ganti dengan 62
        new_phone = `62${new_phone.substr(1)}`;
    }

    // Format ke nomor wa dan return
    return new_phone.includes('@c.us') ? new_phone : `${new_phone}@c.us`;
}

 
// Jalankan express di port 8000
// app.listen(8000, function() {
//     console.log('Server berjalan di port *:8000');
// });
app.listen(8000, () => {
    console.log('Server berjalan di port *:8000');
});