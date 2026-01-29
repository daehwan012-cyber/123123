# 로또 번호 랜덤 추천 웹사이트 (6/45)

1~45 중 6개를 **중복 없이** 뽑아 **오름차순**으로 추천해주는 단일 페이지 웹사이트입니다.

## 미니 게임: 어둠 속 복도 (호러)

리소스 없이 도형/손전등 시야로 만든 짧은 2D 미니 호러 게임입니다.

- 실행 파일: `horror.html`
- 조작: WASD/화살표 이동, 마우스 방향, R 재시작, M 음소거
- 목표: **열쇠를 줍고 문으로 탈출**

## 기능

- 1게임/3게임/5게임 한번에 생성
- 제외 번호 입력 지원 (예: `7, 13, 25`)
- 복사 기능
  - 이번 추천 복사
  - 각 줄(게임) 복사
  - 히스토리 전체 복사
- 히스토리(최대 20개) + 클릭 복사

## 실행 방법

### 방법 1) 파일 더블클릭

`index.html`을 더블클릭해서 브라우저로 열면 됩니다.

### 방법 2) 간단 서버로 실행 (권장)

PowerShell에서 아래 명령으로 실행 후 브라우저에서 `http://localhost:5173` 접속:

```bash
cd "c:\Users\도망쳐\Desktop\11"
python -m http.server 5173
```

> PC에 Python이 없다면, Windows Store에서 Python 설치 후 다시 시도하세요.

## (추가) 터미널용 로또 추천 프로그램 (Python)

웹페이지가 아니라 **터미널에서 바로** 로또 번호를 뽑고 싶다면 `lotto.py`를 실행하세요.

```bash
cd "c:\Users\도망쳐\Desktop\11"
python lotto.py
```

옵션 예시:

```bash
python lotto.py -n 5
python lotto.py -n 3 --exclude 7,13,25 --fixed 1,2
```

## 파일 구성

- `index.html`: 화면 구조
- `styles.css`: 스타일(UI)
- `app.js`: 로또 생성/복사/히스토리 로직
- `lotto.html`: 단일 파일(HTML+CSS+JS) 버전 로또 추천기
- `horror.html`: 미니 호러 게임 화면
- `horror.css`: 미니 호러 게임 스타일
- `horror.js`: 미니 호러 게임 로직(캔버스)
- `portfolio.html`: 목표 연 8% 포트폴리오 매니저(채권/한국주식/미국주식)
- `portfolio.css`: 포트폴리오 매니저 스타일
- `portfolio.js`: 비중 계산/시뮬레이션/저장/복사 로직

