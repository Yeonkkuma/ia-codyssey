fname = 'mission_computer_main.log'

# 파일 오픈 및 읽기
try:
    with open(fname, 'r', encoding='utf-8') as file:
        content = file.read()
    print(content)

except FileNotFoundError:
    print('해당 파일을 찾을 수 없습니다.')
except Exception as e:
    print(f'오류가 발생했습니다. : {e}')
    # print('오류가 발생했습니다.' , e)
finally:
    print('처리 완료')

# 파일을 열고 전체 내용을 화면에 출력 (open 기본 문법)
# file = open('mission_computer_main.log', 'r', encoding='utf-8')
# content = file.read()
# file.close()

# 파일을 처리할 때에 발생할 수 있는 예외를 처리한다.
# 1. 파일을 찾을 수 없는 경우(존재X) - FileNotFoundError
# 2. 그 외 알 수 없는 오류 ㄱ- .. - Exception

# mission_computer_main.log의 내용을 통해서 사고의 원인을 분석하고 정리
# 2023-08-27 11:35:00,INFO,Oxygen tank unstable. 산소 탱크 불안정
# 2023-08-27 11:40:00,INFO,Oxygen tank explosion. 산소 탱크 폭발
# 센터 및 임무 제어 시스템 전원 종료
# 2023-08-27 12:00:00,INFO,Center and mission control systems powered down.
