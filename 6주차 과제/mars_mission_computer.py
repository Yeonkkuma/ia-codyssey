import random
import time
import json
import threading
import platform
import os
import psutil

# [보너스 문제]
def create_default_setting_file():
    default_content = """[INFO]
운영체계
운영체계 버전
CPU의 타입
CPU의 코어 수
메모리의 크기

[LOAD]
CPU 실시간 사용량 (%)
메모리 실시간 사용량 (%)"""

    with open('setting.txt', 'w') as f:
        f.write(default_content)
    print("기본 설정 파일(setting.txt)을 생성했습니다.")


def load_settings():
    settings = {'INFO': [], 'LOAD': []}
    current_section = None

    if not os.path.exists('setting.txt'):
        create_default_setting_file()  # 👉 파일 없으면 자동 생성

    with open('setting.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line == '[INFO]':
                current_section = 'INFO'
            elif line == '[LOAD]':
                current_section = 'LOAD'
            elif line and current_section:
                settings[current_section].append(line)

    return settings

# 설정값 로드
settings = {
    'INFO': [],
    'LOAD': []
}


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

# 문제 4 + 문제 7
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
            if time.time() - start_time >= 10:  # 300초(5분)마다 실행
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

    # 문제 7 > MissionComputer 클래스에 추가함
    # 미션 컴퓨터의 정보를 알아내는 메소드명 > get_mission_computer_info()
    def get_mission_computer_info(self):
        try:
            system_info = {
                '운영체계': platform.system(),
                '운영체계 버전': platform.version(),
                'CPU의 타입': platform.processor(),
                'CPU의 코어 수': os.cpu_count(),
                '메모리의 크기': round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }

            filtered_info = {
                k: v for k, v in system_info.items()
                if not settings['INFO'] or k in settings['INFO']
            }

            print('\n===== Mission Computer Info =====')
            print(json.dumps(filtered_info, indent=4, ensure_ascii=False)) # JSON 형식으로 출력
            print('=================================\n')
        except Exception as e:
            print('Error occurred while retrieving system info:', str(e))

    # 미션 컴퓨터의 부하를 가져오는 메소드명 > get_mission_computer_load()
    def get_mission_computer_load(self):
        try: # CPU 실시간 사용량 / 메모리 실시간 사용량
            load_info = {
                'CPU 실시간 사용량 (%)': psutil.cpu_percent(interval=1),
                '메모리 실시간 사용량 (%)': psutil.virtual_memory().percent
            }

            filtered_load = {
                k: v for k, v in load_info.items()
                if not settings['LOAD'] or k in settings['LOAD']
            }

            print('\n===== Mission Computer Load =====')
            print(json.dumps(filtered_load, indent=4, ensure_ascii=False)) # JSON 형식으로 출력
            print('=================================\n')
        except Exception as e:
            print('Error occurred while retrieving system load:', str(e))

    # [보너스 과제] 특정 키 입력 시 실행 종료
    def stop(self):
        self.running = False
        print("System stopped....")

# [문제 4] MissionComputer 인스턴스 생성 및 실행
# [문제 7]
def main():
    runComputer = MissionComputer()

    # [문제 7] 시스템 정보에 대한 값을 출력
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

    # 센서 데이터 수집을 별도 스레드에서 실행
    thread = threading.Thread(target=runComputer.get_sensor_data)
    thread.start()

    while True:
        user_input = input("종료하려면 '0'를 입력하세요: ").strip().lower()
        if user_input == '0':
            runComputer.stop()
            break

    thread.join()


if __name__ == "__main__":
    main()
