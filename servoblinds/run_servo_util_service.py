import os
import argparse
import time
import logging
import paho.mqtt.client as mqtt
from servoblinds.servo.ServoController import ServoController
from servoblinds.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')


def publish_config_numbers(sc):
    for channel, servo in sc.config.servo_channels.items():
        for k, v in servo.servo_details.items():
            client.publish(config.mqtt.util_base_topic + f'/config/{channel}/{k}', v, qos=1, retain=False)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Start MQTT client')

    arg_parser.add_argument('-c',
                            '--config_path',
                            help='Path to config',
                            required=False,
                            default=os.path.join(os.path.dirname(__file__), 'sample_config.yml'))

    arg_parser.add_argument('-it',
                            '--incremental_time',
                            help='Time in seconds for incremental movement of a servo',
                            required=False,
                            default=1)

    args = vars(arg_parser.parse_args())
    config = Config.read_current_config(args['config_path'])
    t = args['incremental_time']
    sc = ServoController(config)
    cover_avail_topic = config.mqtt.util_base_topic + '/availability'

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        logging.info("Connected with result code " + str(rc))

        # publish current values of the config
        publish_config_numbers(sc)

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        topic = config.mqtt.util_base_topic + '/#'
        logging.info(f'Subscribing to the following topic: {topic}')
        client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        logging.info(f'Received message from topic: {msg.topic}, message: {payload}')

        command_topic_list = msg.topic.split('/')
        if 'config' in command_topic_list:
            command_topic = command_topic_list[-1]
            channel = int(command_topic_list[-2])
            sc.config.servo_channels[channel].update_servo_details_value(command_topic, int(payload))
            sc.config.write_current_config()
        else:
            command_topic = command_topic_list[-1]
            if command_topic == 'pi_reboot':
                # note: ignores all inhibitors, including other users logged in
                os.system('sudo reboot')
            elif command_topic == 'incremental_close':
                # e.g. payload = "0"
                channel = int(payload)
                sc.get_servo_on_channel(channel=channel).move(sc.kit, movement="close", t=t)
            elif command_topic == 'incremental_open':
                # e.g. payload = "0"
                channel = int(payload)
                sc.get_servo_on_channel(channel=channel).move(sc.kit, movement="open", t=t)
            elif command_topic == 'override_state_blind_open':
                logging.info('State overridden to: open')
                sc.update_state(0.0)
                client.publish(config.mqtt.cover_base_topic + '/get', 'open', qos=1, retain=True)
            elif command_topic == 'override_state_blind_closed':
                logging.info('State overridden to: closed')
                sc.update_state(1.0)
                client.publish(config.mqtt.cover_base_topic + '/get', 'closed', qos=1, retain=True)
            else:
                logging.warning(f'Topic {command_topic} is not understood')


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
