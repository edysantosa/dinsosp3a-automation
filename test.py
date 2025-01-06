from babel.dates import format_date
from datetime import date, datetime, timedelta

tommorow = date.today() + timedelta(days=1) 
print(tommorow.strftime("%A"))

# print(format_date(tommorow, locale='de'))
print(format_date(tommorow, "yyyy-MM-dd", locale='id'))
print(format_date(tommorow, "EEEE, d MMMM yyyy", locale='id'))

print("https://kanal.baliprov.go.id/agenda/download_agenda?agenda_date={date}&agenda_type=OPD".format(date=format_date(tommorow, "yyyy-MM-dd", locale='id')))
