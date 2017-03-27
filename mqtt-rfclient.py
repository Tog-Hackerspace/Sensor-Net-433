import json
import paho.mqtt.client as mqtt
from datetime import datetime
import rfpi


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/tog/sensors/rf/common_room")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    try:
        data = json.loads(msg.payload)
    except ValueError:
        print "Ignoring junk payload"
        return None
    else:
        state = "on" if data.get("state") == True else "off"
        rfpi.transmit_code("%s_%s" % (data.get("socket"),state))
        data.update({"when": datetime.now().isoformat()})
        client.publish("/tog/sensors/rf/common_room/acks", payload=json.dumps(da
ta))


if __name__ == "__main__":

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.tog.ie", 1883, 60)
    client.loop_forever()
