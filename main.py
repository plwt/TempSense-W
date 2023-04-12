import network
import socket
from time import sleep
from picozero import pico_temp_sensor
import machine
import time

ssid = 'ADDIDHERE'
password = 'ADDPASSWORDHERE'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, uptime_hours):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <body style="background-color:#000000">
            <p> </p>
            <p style="color:#00ff41; font-size:40px">Temperature is {temperature}</p>
            <p> </p>
            <p style="color:#00ff41; font-size:40px">Uptime is {uptime_hours} hours</p> 
            </body>
            </html>
            """
    return str(html)
 
def serve(connection):
    #Start a webserver
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        temperature = pico_temp_sensor.temp
	uptime_seconds = time.ticks_us()
	uptime_hours = uptime_seconds / 3600000000
	html = webpage(temperature, uptime_hours)
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
