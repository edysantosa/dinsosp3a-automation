import requests
from babel.dates import format_date
from datetime import date, datetime, timedelta
import mimetypes
import base64
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mengirim pesan ke grup whatsapp"
    )
    parser.add_argument("--groupname", required=True, help="Nama grup whatsapp")
    parser.add_argument("--message", required=True, help="Pesan yang dikirim")
    parser.add_argument("--deletefile", action='store_true', help="Path dari file yang akan dikirim")
    args = parser.parse_args()

    groupName = args.groupname
    message = args.message
    deleteFile = args.deletefile

    if (datetime.now().hour > 12):
        tommorow = date.today() + timedelta(days=1) 
    else:
        tommorow = date.today()
    
    tommorowFormat = format_date(tommorow, "yyyy-MM-dd", locale='id')
    tommorowName = format_date(tommorow, "EEEE, d MMMM yyyy", locale='id')
    file_name = "agenda-{fileName}.pdf".format(fileName=tommorowFormat)

    try:
        with open(file_name, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())

        headers = {"Content-Type": "application/json;charset=utf-8"}
        json_payload = {
            "group_name":groupName,
            "message":message.format(date=tommorowName),
            "file_name": "Agenda {date}".format(date=tommorowFormat),
            "mime_type": mimetypes.guess_file_type("export.pdf")[0],
            "file": encoded_string.decode("utf-8")
        }

        url = 'http://localhost:8000/send-group-message'
        r = requests.post(url, headers=headers, json=json_payload)
        print (r)

        # Hapus file agenda
        if deleteFile:
            if os.path.exists(file_name):
                os.remove(file_name)
            else:
                print("The file does not exist")
    # except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
    # except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
    except OSError as e:
        print("File agenda tidak ditemukan")
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)
