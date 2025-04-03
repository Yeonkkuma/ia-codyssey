import random
import time

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = random.randint(18, 30)
        self.env_values["mars_base_external_temperature"] = random.randint(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.randint(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.randint(500, 715)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 3)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} | " + " | ".join(f"{k}: {v}" for k, v in self.env_values.items())

        with open("log2.txt", "a") as log_file:
            log_file.write(log_entry + "\n")

        return self.env_values

# 인스턴스를 생성하여 다른 파일에서 import할 수 있도록 함
ds = DummySensor()
