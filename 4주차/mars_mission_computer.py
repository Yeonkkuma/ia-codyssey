import random
import time

# 더미 센서에 해당하는 클래스를 생성함 > 클래스의 이름은 DummySensor로 정의한다.
class DummySensor:
    def __init__(self):
        # 딕셔너리를 초기화한다.
        self.env_values = {
            "mars_base_internal_temperature": 0,
            "mars_base_external_temperature": 0,
            "mars_base_internal_humidity": 0,
            "mars_base_external_illuminance": 0,
            "mars_base_internal_co2": 0,
            "mars_base_internal_oxygen": 0
        }

    # set_env() 메소드를 추가함
    # random으로 주어진 범위 안의 값을 생성해서 env_values 항목에 채워주는 역할
    def set_env(self):
        # 각 항목의 범위 지정
        # get_env() 메소드는 env_values를 return
        self.env_values["mars_base_internal_temperature"] = random.randint(18, 30)
        self.env_values["mars_base_external_temperature"] = random.randint(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.randint(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.randint(500, 715)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 3)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} | " + " | ".join(f"{k}: {v}" for k, v in self.env_values.items())

        with open("log.txt", "a") as log_file:
            log_file.write(log_entry + "\n")

        return self.env_values


# DummySensor 클래스를 ds라는 이름으로 인스턴스(Instance)로 생성
ds = DummySensor()

# 환경 값 설정 및 확인
ds.set_env()
env_data = ds.get_env()

# 출력 확인
print(env_data)
