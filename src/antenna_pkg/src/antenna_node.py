from rclpy.node import Node, Publisher, Subscription
from serial import Serial
from sensor_msgs.msg import Imu, NavSatFix, NavSatStatus, MagneticField
from glob import glob
from os import getenv
from time import sleep
from threading import Thread
import sys
import signal
import atexit
import rclpy

anchor_node: "None | AnchorNode" = None
thread: None | Thread = None


class AnchorNode(Node):
    imu_pub: Publisher
    sat_pub: Publisher
    rover_sat_sub: Subscription
    serial: Serial

    def __init__(self):
        super().__init__("tracking_antenna")

        # Create publishers
        self.imu_pub = self.create_publisher(Imu, "/antenna/feedback/imu", 10)
        self.sat_pub = self.create_publisher(NavSatFix, "/antenna/feedback/sat", 10)

        self.rover_sat_sub = self.create_subscription(
            NavSatFix, "/core/gps", self.send_angle, 10
        )

        self.port = getenv("PORT_OVERRIDE")

        # try 4 times
        for _ in range(4):
            # if we have a port already we can skip
            if self.port is not None:
                break
            # test all possible ports
            for port in glob("/dev/ttyUSB*") + glob("/dev/ttyACM*"):
                try:
                    ser = Serial(port, 115200, timeout=1)
                    ser.write(b"ping\n")
                    res = ser.read_until(bytes("\n", "utf8"))

                    # if we didn't get a pong back, we aren't talking to the right thing
                    if b"pong" not in res:
                        continue

                    self.port = port
                    self.get_logger().info(f"Found MCU at {self.port}")
                except:
                    pass

        if self.port is None:
            self.get_logger().info("Unable to find MCU...")
            sleep(1)
            exit(1)

        self.serial = Serial(self.port, 115200)

        atexit.register(self.cleanup)

    def run(self):
        global thread
        thread = Thread(target=rclpy.spin, args={self}, daemon=True)
        thread.start()

        try:
            while rclpy.ok():
                self.read_mcu()
        except KeyboardInterrupt:
            exit(0)

    def read_mcu(self):
        pass

    def send_angle(self, msg: NavSatFix):
        pass

    def cleanup(self):
        pass


def my_except_hook(type, value, traceback):
    print("Uncaught exception:", type, value)
    if anchor_node:
        anchor_node.cleanup()


def main(args=None):
    rclpy.init(args=args)
    sys.excepthook = my_except_hook

    global anchor_node

    anchor_node = AnchorNode()
    anchor_node.run()


if __name__ == "__name__":
    signal.signal(signal.SIGTERM, lambda signum, frame: exit(0))
    main()

