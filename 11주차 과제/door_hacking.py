import zipfile
import string
import time
import os

def unlock_zip(zip_file_path='emergency_storage_key.zip'):
    if not os.path.isfile(zip_file_path):
        print('파일이 존재하지 않습니다.')
        return

    # 비밀번호 : 소문자 + 숫자
    charset = string.ascii_lowercase + string.digits  # 소문자 + 숫자
    total = len(charset) ** 6 # 6자리 숫자

    print('비밀번호 크래킹 시작...')
    start_time = time.time() # 시작 시간 기록

    attempt = 0
    found_password = ''
    with zipfile.ZipFile(zip_file_path) as zf:
        for c1 in charset:
            for c2 in charset:
                for c3 in charset:
                    for c4 in charset:
                        for c5 in charset:
                            for c6 in charset:
                                password = c1 + c2 + c3 + c4 + c5 + c6
                                attempt += 1
                                try:
                                    zf.extractall(pwd=bytes(password, 'utf-8'))
                                    found_password = password
                                    print('성공! 암호:', password)
                                    break # 성공 -> 중단
                                except:
                                    pass # 실패 -> 재시도

                                # 일정 횟수마다 진행 상황 출력
                                if attempt % 100000 == 0:
                                    elapsed = time.time() - start_time
                                    print('시도:', attempt, '/', total, '진행 시간:', round(elapsed, 2), '초')

                            if found_password:
                                break
                        if found_password:
                            break
                    if found_password:
                        break
                if found_password:
                    break
            if found_password:
                break
   # 성공 -> 비밀번호 저장
    if found_password:
        try:
            with open('password.txt', 'w') as f:
                f.write(found_password)
        except:
            print('비밀번호 저장에 실패했습니다.')
    else:
        print('암호를 찾지 못했습니다.')

    # 총 소요 시간 출력
    total_time = time.time() - start_time
    print('총 소요 시간:', round(total_time, 2), '초')

# 추가 과제
def faster_unlock_zip(zip_file_path='emergency_storage_key.zip'):
    if not os.path.isfile(zip_file_path):
        print('파일이 존재하지 않습니다.')
        return

    from itertools import product

    charset = string.ascii_lowercase + string.digits
    total = len(charset) ** 6

    print('[빠른 방식] 비밀번호 크래킹 시작...')
    start_time = time.time()

    attempt = 0
    found_password = ''
    with zipfile.ZipFile(zip_file_path) as zf:
        for combo in product(charset, repeat=6):
            password = ''.join(combo)
            attempt += 1
            try:
                zf.extractall(pwd=bytes(password, 'utf-8'))
                found_password = password
                print('성공! 암호:', password)
                break
            except:
                pass

            if attempt % 100000 == 0:
                elapsed = time.time() - start_time
                print('시도:', attempt, '/', total, '진행 시간:', round(elapsed, 2), '초')

    if found_password:
        try:
            with open('password.txt', 'w') as f:
                f.write(found_password)
        except:
            print('비밀번호 저장에 실패했습니다.')
    else:
        print('암호를 찾지 못했습니다.')

    total_time = time.time() - start_time
    print('총 소요 시간:', round(total_time, 2), '초')


# 메인 실행 예시
if __name__ == '__main__':
    # 기본 방식
    # unlock_zip()

    # 빠른 방식 (itertools.product 사용)
    faster_unlock_zip()
