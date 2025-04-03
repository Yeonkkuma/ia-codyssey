import time
import json
import threading
from Week4_DS import ds  # Week4_DS.py에서 DummySensor 불러오기

# 미션 컴퓨터에 해당하는 클래스를 생성함 > 클래스의 이름은 MissionComputer로 정의
class MissionComputer:
    def __init__(self):
        # 초기화
        # 화성 기지의 환경에 대한 값을 저장할 수 있는 객체 > env_values라는 속성으로 포함
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.sensor = ds  # Week4_DS.py의 DummySensor 사용
        self.running = True # 실행 상태
        self.data_log = [] # [보너스 과제] 5분 평균값을 계산하기 위한 데이터 저장 공간

    # MissionComputer에 get_sensor_data() 메소드를 추가함
    def get_sensor_data(self):
        start_time = time.time() # 시작 시간 기록
        while self.running: # 실행 상태가 True인 동안 반복

            # 환경 값을 가져와서 env_values에 담음
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()

            # [보너스 과제] 5분 평균 계산을 위해 데이터 저장
            self.data_log.append(self.env_values.copy())
            if len(self.data_log) > 60: # 5초 간격으로 60개 데이터 저장
                self.data_log.pop(0) # 가장 오래된 데이터 삭제

            # env_values를 JSON 형태로 출력
            json_output = json.dumps(self.env_values, indent=4)
            print(json_output)

            # [보너스 과제] 5분이 경과했는지 확인 -> print_avg_values 메서드 호출
            if time.time() - start_time >= 300:
                self.print_avg_values()
                start_time = time.time() # 다음 5분 주기 준비

            time.sleep(5) # 5초마다 반복

    # [보너스 과제] 5분에 한번씩 각 환경값에 대한 5분 평균 값을 별도로 출력
    def print_avg_values(self):
        # 데이터 로그가 비어있는지 확인함
        if not self.data_log:
            print('No data available for averaging.')
            return # 계산할 데이터가 없으면 메서드 종료

        # 평균 값을 저장할 딕셔너리 초기화
        avg_values = {key: 0 for key in self.env_values}
        # 데이터 로그에 저장된 항목의 개수 계산
        data_count = len(self.data_log)

        # 데이터 로그의 각 항목에 대해 반복
        for entry in self.data_log:
            for key in avg_values:
                avg_values[key] += entry[key]

        # 누적된 합을 항목 수로 나누어 평균 계산
        for key in avg_values:
            avg_values[key] = round(avg_values[key] / data_count, 3)

        print('\n===== 5분 평균 환경 값 =====')
        print(json.dumps(avg_values, indent=4))
        print('===========================\n')

    # [보너스 과제] 특정 키 입력 시 실행 종료
    def stop(self):
        self.running = False
        print('System stopped....')

# MissionComputer 인스턴스 생성 및 실행 > RunComputer 라는 이름으로 인스턴스화
def main():
    RunComputer = MissionComputer()

    # 데이터 수집을 별도 스레드에서 실행
    thread = threading.Thread(target=RunComputer.get_sensor_data)
    thread.start()

    # 특정 키
    while True:
        user_input = input('종료하려면 0을 입력하세요: ').strip().lower()
        if user_input == '0':
            RunComputer.stop()
            break

    thread.join()

if __name__ == '__main__':
    main()
