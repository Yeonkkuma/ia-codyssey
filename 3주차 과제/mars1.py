import csv
import pickle

fcsv = 'Mars_Base_Inventory_List.csv'

# Mars_Base_Inventory_List.csv 의 내용을 읽어 들어서 출력
def read_csv(fcsv):
    # 기존 csv 파일 출력
    print('[기존 csv 파일]')

    try:
        with open(fcsv, 'r', encoding='utf-8') as file:
            for line in file:
                print(line.strip())

    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'오류가 발생했습니다.: {e}')
        return

    # Mars_Base_Inventory_List.csv 내용을 읽어서 Python의 리스트(List) 객체로 변환
    clist = []

    try:
        with open(fcsv, 'r', encoding='utf-8') as file:
            csv_r = csv.reader(file)
            for row in csv_r:
                clist.append(row)

    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'오류가 발생했습니다.: {e}')
        return

    # 배열 내용을 적제 화물 목록을 인화성이 높은 순으로 정렬
    try:
        # 첫 번째 행은 헤더이므로, 첫 번째 행을 제외하고 정렬
        sorted_clist = sorted(clist[1:], key=lambda x: x[-1], reverse=True)  # 첫 번째 행 제외하고 정렬

        print('\n[인화성 높은 순으로 정렬된 적제 화물 목록]')
        for row in sorted_clist:
            print(row)

        # 보너스 과제 1. 인화성 순서로 정렬된 배열의 내용을 이진 파일 형태로 저장
        with open('Mars_Base_Inventory_List.bin', 'wb') as bin_file:
            pickle.dump(sorted_clist, bin_file)

        # 보너스 과제 2. 저장된 파일의 내용을 다시 읽어 들여서 화면에 내용을 출력
        with open('Mars_Base_Inventory_List.bin', 'rb') as bin_file:
            bin_data = pickle.load(bin_file)

        print('\n[이진 파일 출력 데이터]')
        for row in bin_data:
            print(row)

        # 인화성 지수가 0.7 이상인 항목만 추출
        # float(row[-1])로 인화성 지수 추출 (첫 번째 행은 헤더로 제외)
        danger_list = [row for row in sorted_clist if float(row[-1]) >= 0.7]

        # 인화성 지수가 0.7 이상인 목록을 출력
        print('\n[인화성 지수가 0.7 이상인 화물 목록]')
        for row in danger_list:
            print(row)

        # 인화성 지수가 0.7 이상되는 목록을 CSV 포멧(Mars_Base_Inventory_danger.csv)으로 저장
        with open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8', newline='') as MBID_file:
            csv_w = csv.writer(MBID_file)
            # 헤더를 작성
            csv_w.writerow(['Substance', 'Weight (g/cm³)', 'Specific Gravity', 'Strength', 'Flammability'])
            # 인화성 지수가 0.7 이상인 항목들을 저장
            csv_w.writerows(danger_list)

        print("\n인화성 지수가 0.7 이상인 목록을 'Mars_Base_Inventory_danger.csv'로 저장했습니다.")

    except Exception as e:
        print(f'오류가 발생했습니다.: {e}')
        return

read_csv(fcsv)

# 이진 파일은 용량이 작고 처리 속도가 빠르지만 사람이 읽기 어려움
# 텍스트 파일은 사람이 읽고 수정하기 편하지만, 처리 속도가 느림