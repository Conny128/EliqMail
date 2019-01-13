import requests
import smtplib, ssl
from datetime import datetime

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "mymail@gmail.com"  # Enter your address
receiver_email = "mymail@gmail.com"  # Enter receiver address
password = "password" # Enter password
accesstoken = "Accesstoken" #Enter Accesstoken
energy_data=[]

acumaltive_used_energy_per_day= 0.0
Eliq_start_date= datetime.now().strftime('%Y-%m-%d')
true = 1

Eliq_start_date= datetime.now().strftime('%Y-%m-%d')
 
Eliq_request_string = ('https://my.eliq.io/api/data?accesstoken={}&startdate={}&intervaltype=hour&channelid=32217'.format(accesstoken, Eliq_start_date))
response = requests.get (Eliq_request_string)
Eliq_HISTORY = (response.json())
energy_list = Eliq_HISTORY['data']

present_hour = len(energy_list)

for data_dictionary in energy_list:
    energy_data.append(data_dictionary['energy'])

for energy_used_per_hour in energy_data:
    acumaltive_used_energy_per_day = acumaltive_used_energy_per_day + energy_used_per_hour
    
print ('Total power is  {} Watts so far today'.format(acumaltive_used_energy_per_day))
acumaltive_used_energy_per_day_int = int(acumaltive_used_energy_per_day)
acumaltive_used_energy_per_day_str = str (acumaltive_used_energy_per_day_int)

if present_hour-1 > 7 and present_hour-1 < 23: # Only mail between 7 AM to 23 PM
    message = """\
    Energy used so far {} Watts : Hour {} """.format(acumaltive_used_energy_per_day_str, present_hour-1 )    
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

acumaltive_used_energy_per_day_int= 0
acumaltive_used_energy_per_day= 0
energy_used_per_hour = 0
energy_data=[]
