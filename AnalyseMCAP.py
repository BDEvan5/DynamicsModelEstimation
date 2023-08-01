import numpy as np

from mcap.reader import make_reader
# from mcap_protobuf.decoder import DecoderFactory
from mcap_ros1.decoder import DecoderFactory

def view_scans():

    with open("demo.mcap", "rb") as f:
        reader = make_reader(f)
        for schema, channel, message in reader.iter_messages(topics=["/scan"]):
            print(f"{channel.topic} ({schema.name}): {message.data}")



def make_data_set():
    action_topic = "/vesc/high_level/ackermann_cmd_mux/input/nav_1"
    odom_topic = "/car_state/odom"
    file_name = "RawData/demo.mcap"
    # with open(file_name, "rb") as f:
    #     reader = make_reader(f)
    #     for schema, channel, message in reader.iter_messages(topics=[action_topic, odom_topic]):
    #         print(f"{channel.topic} ({schema.name})")
            # print(f"{channel.topic} ({schema.name}): {message.data}")

    actions = []
    states = []
    with open(file_name, "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        for schema, channel, message, proto_msg in reader.iter_decoded_messages():
            # print(f"{channel.topic} {schema.name} [{message.log_time}]: {proto_msg}")
            if channel.topic == action_topic:
                speed = proto_msg.drive.speed
                steering = proto_msg.drive.steering_angle
                action = np.array([steering, speed])
                actions.append(action)

            if channel.topic == odom_topic:
                x = proto_msg.pose.pose.position.x
                y = proto_msg.pose.pose.position.y

                # ox = proto_msg.pose.pose.orientation.x
                # oy = proto_msg.pose.pose.orientation.y
                oz = proto_msg.pose.pose.orientation.z
                ow = proto_msg.pose.pose.orientation.w

                v = proto_msg.twist.twist.linear.x

                odom = np.array([x, y, oz, ow, v])
                states.append(odom)

    actions = np.stack(actions)
    np.save("Data/DemoActions.npy", actions)
    states = np.stack(states)
    np.save("Data/DemoStates.npy", states)

    print(actions.shape)
    print(states.shape)



make_data_set()