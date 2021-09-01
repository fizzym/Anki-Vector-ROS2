import anki_vector as av
import time

robot1 = av.Robot(serial="006046ca")
robot2 = av.Robot(serial="00804458")
robot1.connect()
robot2.connect()
robot1.motors.set_wheel_motors(50,-50)
robot2.motors.set_wheel_motors(-50,50)
time.sleep(3)
robot1.motors.set_wheel_motors(0,0)
robot2.motors.set_wheel_motors(0,0)
time.sleep(3)
try:
    robot1.disconnect()
    robot2.disconnect()
except Exception as ex:
    print(str(ex))
    print("\n\nError disconnecting")