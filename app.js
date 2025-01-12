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


// Spawn promise
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
    } else if (msg.body === 'kirim ulang'){
        // Delete last message
        whatsapp.getChats().then((chats) => {
            chat = chats.find((chat) => chat.name === "Mista Roboto");
            chat.fetchMessages({
                limit: 1,
                fromMe: true
            }).then((lastMessages) => {
                lastMessage = lastMessages.find(e => true);
                lastMessage.delete(true);
            });
        });

        // Download dan kirim ulang agenda
        spawnPromise('.\\env\\Scripts\\python.exe .\\download_agenda.py').then(
            data => {
                spawnPromise('.\\env\\Scripts\\python.exe .\\send_whatsapp.py', ['--groupname "Dinas Sosial P3A Prov. Bali"', '--deletefile true', '--message "Ralat Agenda {date}"']).then(
                    data => console.log('data: ', data)
                ).catch((err) => console.log(err));;
            }
        ).catch((err) => console.log(err));
    } else {
        pesanMaaf = "Mohon maaf kak, saya hanya bot. Untuk download dan kirim ulang agenda ketik 'kirim ulang' huruf kecil semua";
        msg.getChat().then((chat) => {
            if (chat.isGroup) {
                // Ignore jika dari grup dinas
                if (chat.name === "Dinas Sosial P3A Prov. Bali") {
                    return;
                }
                mentionedMessage = msg.mentionedIds.find((ids) => ids === whatsapp.info.wid._serialized);
                if (mentionedMessage) {
                    msg.reply(pesanMaaf);
                } else if(msg.hasQuotedMsg) {
                    msg.getQuotedMessage().then((quotedMessage) => {
                        if (quotedMessage.fromMe){
                            msg.reply(pesanMaaf);
                        }
                    });
                }
            } else {
                msg.reply(pesanMaaf);
            }
        });
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
        if (!data.mime_type || !data.file_name) {
            res.status(200).json({
                result: false,
                message: "mime_type dan file_name perlu diisi"
            });
        }

        media = new MessageMedia(data.mime_type, data.file, data.file_name);

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

    whatsapp.getChats().then((chats) => {
        chat = chats.find((chat) => chat.name === data.group_name);
        
        if (!chat) {
            res.status(200).json({
                result: false,
                message: "Grup tidak ditemukan"
            });
            return;
        }

        if (data.file) {
            if (!data.mime_type || !data.file_name) {
                res.status(200).json({
                    result: false,
                    message: "mime_type dan file_name perlu diisi"
                });
                return;
            }

            media = new MessageMedia(data.mime_type, data.file, data.file_name);

            chat.sendMessage(media, {caption: data.message}).then((result) => {
                res.status(200).json({
                    result: true,
                    message: "Pesan terkirim"
                });
                return;
            }).catch((error) => {
                res.status(500).json({
                    result: false,
                    message: error.message
                });
                return;
            });
        } else {
            chat.sendMessage(data.message).then((result) => {
                res.status(200).json({
                    result: true,
                    message: "Pesan terkirim"
                });
                return;
            }).catch((error) => {
                res.status(500).json({
                    result: false,
                    message: error.message
                });
                return;
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