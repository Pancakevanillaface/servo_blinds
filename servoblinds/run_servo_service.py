import os
import argparse
import time
import logging
import paho.mqtt.client as mqtt
from servoblinds.servo.ServoController import ServoController
from servoblinds.config import Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Start MQTT client')

    arg_parser.add_argument('-c',
                            '--config_path',
                            help='Path to config',
                            required=False,
                            default=os.path.join(os.path.dirname(__file__), 'sample_config.yml'))

    args = vars(arg_parser.parse_args())
    config = Config.read_current_config(args['config_path'])
    sc = ServoController(config)
    cover_avail_topic = config.mqtt.cover_base_topic + '/availability'

    # The callback for when the client receives a CONNECT response from the server.
    def on_connect(client, userdata, flags, rc):
        logging.info("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        topic = config.mqtt.cover_base_topic + '/#'
        logging.info(f'Subscribing to the following topic: {topic}')
        client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        logging.info(f'Received message from topic: {msg.topic}, message: {payload}')

        if msg.topic.split('/')[-1] == 'set':
            if payload == 'OPEN':
                client.publish(config.mqtt.cover_base_topic + '/get', 'opening', qos=0, retain=False)
                sc.open()
                client.publish(config.mqtt.cover_base_topic + '/get', 'open', qos=1, retain=True)
            elif payload == 'CLOSE':
                client.publish(config.mqtt.cover_base_topic + '/get', 'closing', qos=0, retain=False)
                sc.close()
                client.publish(config.mqtt.cover_base_topic + '/get', 'closed', qos=1, retain=True)
            elif payload == 'STOP':
                sc.stop()
                client.publish(config.mqtt.cover_base_topic + '/get', 'stopped', qos=1, retain=False)
            else:
                logging.warning(f'Message {payload} is not understood')

    client = mqtt.Client()
    client.username_pw_set(username=config.mqtt.username, password=config.mqtt.password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set(cover_avail_topic, "offline", qos=1)

    client.connect(config.mqtt.host)
    time.sleep(5)
    client.publish(cover_avail_topic, 'online', qos=1)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
