# calculator.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Style Calculator')
        self.setFixedSize(320, 480)
        self.setStyleSheet('background-color: black;')
        self.init_ui()
        self.expression = ''

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 숫자창 설정
        self.display = QLineEdit('0')
        self.display.setReadOnly(True) # 직접 수정 X
        self.display.setAlignment(Qt.AlignRight) # 오른쪽 정렬
        self.display.setFixedHeight(80)
        self.display.setStyleSheet( # 아이폰 계산기처럼 스타일 적용
            'color: white; background-color: black; font-size: 36px; border: none; padding: 10px;'
        )
        self.layout.addWidget(self.display)

        # 버튼 배치
        self.button_layout = QGridLayout()
        self.layout.addLayout(self.button_layout)

        # 버튼 텍스트 목록
        self.buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 버튼 객체 저장소 / 버튼 생성 함수 호출
        self.button_refs = {}
        self.create_buttons()

    # 버튼 생성
    def create_buttons(self):
        for row_index, row in enumerate(self.buttons):
            for col_index, label in enumerate(row):
                button = QPushButton(label)
                button.setFont(QFont('Arial', 18))
                button.setFixedSize(70, 70)
                button.setStyleSheet(self.get_button_style(label))

                # 0 버튼 UI 변경
                if label == '0':
                    button.setFixedSize(150, 70)
                    self.button_layout.addWidget(button, row_index + 1, 0, 1, 2)
               # 나머지 버튼 UI 변경
                elif label == '.':
                    self.button_layout.addWidget(button, row_index + 1, 2)
                elif label == '=':
                    self.button_layout.addWidget(button, row_index + 1, 3)
                else:
                    self.button_layout.addWidget(button, row_index, col_index)

                button.clicked.connect(self.button_clicked)
                self.button_refs[label] = button  # 버튼 저장

    # 버튼 스타일 함수
    def get_button_style(self, label):
        if label in ['AC', 'C', '+/-', '%']:
            return 'background-color: lightgray; border-radius: 35px; color: black;'
        elif label in ['÷', '×', '-', '+', '=']:
            return 'background-color: orange; border-radius: 35px; color: white;'
        else:
            return 'background-color: #505050; border-radius: 35px; color: white;'

    # AC <-> C 버튼 전환
    def update_clear_button(self):
        clear_button = self.button_refs.get('AC') or self.button_refs.get('C')
        if self.expression == '':
            clear_button.setText('AC')
        else:
            clear_button.setText('C')

    # 버튼 클릭 처리 함수
    def button_clicked(self):
        clicked_button = self.sender()
        text = clicked_button.text()

        # AC(초기화) / C(지우기) 버튼 처리
        if text in ['AC', 'C']:
            if text == 'AC':
                self.expression = ''
            else:
                self.expression = self.expression[:-1]
            self.display.setText(self.expression if self.expression else '0')
            self.update_clear_button()

        # + / - 버튼 처리
        elif text == '+/-':
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.display.setText(self.expression)

        # % 버튼 처리
        elif text == '%':
            try:
                value = str(eval(self.expression) / 100)
                self.expression = value
                self.display.setText(value)
            except:
                self.display.setText('Error')

        # = 버튼 처리(계산 기능)
        elif text == '=':
            try:
                expression = self.expression.replace('×', '*').replace('÷', '/')
                result = str(eval(expression))
                self.display.setText(result)
                self.expression = result
            except:
                self.display.setText('Error')
                self.expression = ''
            self.update_clear_button()

        # 숫자 및 나머지 버튼 (일반 입력)
        else:
            if self.display.text() == '0' and text not in ['.', '+', '-', '×', '÷']:
                self.expression = text
            else:
                self.expression += text
            self.display.setText(self.expression)
            self.update_clear_button()

# 프로그램 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
