import random
import time
import json
import threading

# 문제 3
# 더미 센서에 해당하는 클래스를 생성함 > 클래스의 이름은 DummySensor로 정의한다.
class DummySensor:
    def __init__(self):
        # 딕셔너리 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    # set_env() 메소드를 추가함
    # random으로 주어진 범위 안의 값을 생성해서 env_values 항목에 채워주는 역할
    def set_env(self):
        # 각 항목의 범위를 지정하고 그 범위 안에서 환경 값 랜덤 지정
        # get_env() 메소드는 env_values를 return
        self.env_values["mars_base_internal_temperature"] = random.randint(18, 30)
        self.env_values["mars_base_external_temperature"] = random.randint(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.randint(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.randint(500, 715)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 3)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    # 환경 값을 로그 파일에 저장하고 반환
    def get_env(self):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} | " + " | ".join(f"{k}: {v}" for k, v in self.env_values.items())

        with open("log.txt", "a") as log_file:
            log_file.write(log_entry + "\n")

        return self.env_values

# DummySensor 클래스를 ds라는 이름으로 인스턴스(Instance)로 생성
ds = DummySensor()

"""---------------------------------------------------------------------------------------------"""

# 문제 4
# 미션 컴퓨터에 해당하는 클래스를 생성
class MissionComputer:
    def __init__(self):
        # 화성 기지의 환경에 대한 값을 저장할 수 있는 사전(Dict) 객체가 env_values라는 속성으로 포함되어야 함

        # 미션 컴퓨터 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0, #화성 기지 내부 온도
            'mars_base_external_temperature': 0, #화성 기지 외부 온도
            'mars_base_internal_humidity': 0, # 화성 기지 내부 습도
            'mars_base_external_illuminance': 0, #화성 기지 외부 광량
            'mars_base_internal_co2': 0, # 화성 기지 내부 이산화탄소 농도
            'mars_base_internal_oxygen': 0 # 화성 기지 내부 산소 농도
        }
        self.sensor = ds # DummySensor 인스턴스 사용
        self.running = True  # 실행 상태
        self.data_log = []  # 보너스 과제 |  5분 평균값을 계산하기 위한 데이터 저장 공간

    # MissionComputer에 get_sensor_data() 메소드를 추가함
    def get_sensor_data(self):
        start_time = time.time()  # 시작 시간 기록
        while self.running: # 실행 상태가 True인 동안 반복

            # [문제 4] 센서의 값을 가져와서 env_values에 담는다.
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()

            # [보너스 과제] 5분 평균 계산을 위해 데이터 저장
            self.data_log.append(self.env_values.copy())
            if len(self.data_log) > 60:  # 5초 간격으로 60개 데이터 저장 (5분치)
                self.data_log.pop(0)  # 가장 오래된 데이터 삭제

            # [문제 4] env_values를 JSON 형태로 출력
            json_output = json.dumps(self.env_values, indent=4)
            print(json_output)

            # [보너스 과제] 5분마다 평균값 출력
            if time.time() - start_time >= 300:  # 300초(5분)마다 실행
                self.print_avg_values()
                start_time = time.time()  # 타이머 초기화

            time.sleep(5)  # [문제 4] 5초마다 반복

    def print_avg_values(self):
        # 5분간 데이터 평균을 계산하여 출력
        if not self.data_log:
            print("No data available for averaging.")
            return

        avg_values = {key: 0 for key in self.env_values}
        data_count = len(self.data_log)

        for entry in self.data_log:
            for key in avg_values:
                avg_values[key] += entry[key]

        for key in avg_values:
            avg_values[key] = round(avg_values[key] / data_count, 3)

        print("\n===== 5분 평균 환경 값 =====")
        print(json.dumps(avg_values, indent=4))
        print("===========================\n")

    # [보너스 과제] 특정 키 입력 시 실행 종료
    def stop(self):
        self.running = False
        print("System stopped....")

# [문제 4] MissionComputer 인스턴스 생성 및 실행
def main():
    RunComputer = MissionComputer()

    # 센서 데이터 수집을 별도 스레드에서 실행
    thread = threading.Thread(target=RunComputer.get_sensor_data)
    thread.start()

    while True:
        user_input = input("종료하려면 '0'를 입력하세요: ").strip().lower()
        if user_input == '0':
            RunComputer.stop()
            break

    thread.join()


if __name__ == "__main__":
    main()
