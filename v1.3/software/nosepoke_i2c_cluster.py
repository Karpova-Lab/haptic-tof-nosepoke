from devices.vl53L4 import VL53L4CD
from devices.vl6180 import VL6180
from machine import I2C


class VL53L4CD_cluster:
    def __init__(self, left_port, center_port, right_port, sampling_rate=75, i2c_freq=100_000):
        assert right_port.I2C is not None, "! Analog nosepoke needs a port with I2C."

        i2c = I2C(right_port.I2C, freq=i2c_freq)

        self.left = VL53L4CD(
            port=left_port,
            i2c_instance=i2c,
            sampling_rate=sampling_rate,
            nose_event="l_nose",
            threshold=0,
        )
        self.center = VL53L4CD(
            port=center_port,
            i2c_instance=i2c,
            sampling_rate=sampling_rate,
            nose_event="c_nose",
            threshold=0,
        )
        self.right = VL53L4CD(
            port=right_port,
            i2c_instance=i2c,
            sampling_rate=sampling_rate,
            nose_event="r_nose",
            threshold=0,
        )
        try:
            self.left.i2c_setup(0x20)
        except Exception:
            raise Exception("\nTrouble connecting to left TOF sensor")

        try:
            self.center.i2c_setup(0x30)
        except Exception:
            raise Exception("\nTrouble connecting to center TOF sensor")
        try:
            self.right.i2c_setup(0x40)
        except Exception:
            raise Exception("\nTrouble connecting to right TOF sensor")

        self.left.begin()
        self.center.begin()
        self.right.begin()

    def set_all_thresholds(self, thresholds, offsets):
        for i, nosepoke in enumerate((self.left, self.center, self.right)):
            nosepoke.threshold.threshold = thresholds[i]
            nosepoke.entrance = offsets[i]

    @property
    def readings(self):
        return (self.left.proximity, self.center.proximity, self.right.proximity)

    @property
    def connection_errors(self):
        return (self.left.connection_error, self.center.connection_error, self.right.connection_error)


class VL6180_cluster:
    def __init__(self, i2c_port, aux_a_port, aux_b_port, sampling_rate=40):
        assert i2c_port.I2C is not None, "! Analog nosepoke needs a port with I2C."
        try:
            self.left = VL6180(
                port=i2c_port,
                tof_enable_pin=aux_a_port.DIO_B,
                motor_pin=aux_a_port.POW_B,
                overhead_LED_pin=aux_b_port.POW_A,
                sampling_rate=sampling_rate,
                threshold=40,
                nose_event="l_nose",
                mux_channel=b"\x04",
            )
        except Exception:
            raise Exception("\nTrouble connecting to left TOF sensor")
        try:
            self.center = VL6180(
                port=i2c_port,
                tof_enable_pin=aux_a_port.DIO_A,
                motor_pin=aux_a_port.POW_A,
                overhead_LED_pin=i2c_port.POW_B,
                sampling_rate=sampling_rate,
                threshold=40,
                nose_event="c_nose",
                mux_channel=b"\x02",
            )
        except Exception:
            raise Exception("\nTrouble connecting to center TOF sensor")
        try:
            self.right = VL6180(
                port=i2c_port,
                tof_enable_pin=aux_b_port.DIO_B,
                motor_pin=aux_b_port.POW_B,
                overhead_LED_pin=i2c_port.POW_A,
                sampling_rate=sampling_rate,
                threshold=40,
                nose_event="r_nose",
                mux_channel=b"\x01",
            )
        except Exception:
            raise Exception("\nTrouble connecting to right TOF sensor")

    def set_all_thresholds(self, thresholds, offsets):
        for i, nosepoke in enumerate((self.left, self.center, self.right)):
            nosepoke.threshold.threshold = thresholds[i]
            nosepoke.entrance = offsets[i]

    @property
    def readings(self):
        return (self.left.proximity, self.center.proximity, self.right.proximity)

    @property
    def connection_errors(self):
        return (self.left.connection_error, self.center.connection_error, self.right.connection_error)
