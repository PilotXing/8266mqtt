import time
import lib.mqttinfo as info
from lib.simple import MQTTClient
from lib.ssd1306 import SSD1306, SSD1306_I2C
from machine import I2C, Pin, Timer, reset

last_message = 0
message_interval = 5
counter = 0

# init_ssd1306
i2c = I2C(scl=Pin(14), sda=Pin(2), freq=100000)
s = SSD1306_I2C(128, 64, i2c)
t = Timer(1)


def sub_cb(topic, msg):
    """
    call back
    """
    print(topic, msg)
    s.fill(0)
    s.text(msg+topic, 0, 0)
    s.show()


def connect():
    """
    docstring
    """
    c = MQTTClient(info.CLIENT_ID, info.SERVER, info.PORT,
                   user=info.USER_NAME, password=info.PASSWORD, keepalive=60)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(info.TOPIC)
    c.publish(info.TOPIC, "!!!!!!!!!!!!!!")
    return c


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    reset()


try:
    client = connect()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            msg = b'Hello #%d' % counter
            client.publish(info.TOPIC, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()
