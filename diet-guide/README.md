# 맞춤 건강 식단 가이드

신장, 당뇨, 고혈압, 간기능, 다이어트별 맞춤 식단과 음식 정보를 확인하는 앱입니다.
순수 HTML/CSS/JS로 만들어졌고, 웹(PWA) / 맥·윈도우 데스크톱(Electron) 두 가지 형태로 배포할 수 있습니다.

## 1. 그냥 웹으로 열기

별도 설치 없이 `index.html`을 더블클릭하거나, 로컬 서버로 띄워서 브라우저에서 바로 사용할 수 있습니다.

```bash
python3 -m http.server 8765
# 브라우저에서 http://localhost:8765 접속
```

## 2. 모바일 앱처럼 쓰기 (PWA)

앱스토어/플레이스토어 등록 없이, 위 방법으로 접속한 뒤 브라우저 메뉴에서 "홈 화면에 추가"만 하면 됩니다.

- **iPhone (Safari)**: 공유 버튼 → "홈 화면에 추가"
- **Android (Chrome)**: 메뉴(⋮) → "홈 화면에 추가" 또는 "앱 설치"

홈 화면 아이콘으로 실행하면 주소창 없이 전체 화면 앱처럼 열리고, 서비스 워커(`sw.js`)가 파일을 캐싱해 인터넷이 끊겨도 이미 방문한 화면은 계속 사용할 수 있습니다.

> PWA는 `http://` 또는 `https://`로 접속했을 때만 동작합니다(서비스 워커는 `file://`에서는 등록되지 않습니다). 실제 배포 시에는 Netlify, Vercel, GitHub Pages 등 아무 정적 호스팅에 폴더째 올리면 됩니다.

## 3. 맥/윈도우 데스크톱 앱 (Electron)

### 준비

```bash
cd diet-guide
npm install
```

### 실행해서 미리 보기

```bash
npm start
```

### 설치 파일 만들기

```bash
npm run dist:mac    # 맥용 .dmg → release/ 폴더에 생성
npm run dist:win    # 윈도우용 설치 프로그램(.exe) → release/ 폴더에 생성
npm run dist        # 둘 다 한 번에
```

- `dist:mac`은 맥에서 실행해야 합니다.
- `dist:win`은 맥에서도 빌드됩니다 (electron-builder가 필요한 Wine을 자체적으로 내려받아 사용하므로 별도 설치 불필요).
- 생성된 `release/*.dmg`, `release/*.exe` 파일을 그대로 배포하면, 사용자가 다운로드해서 설치할 수 있습니다.
- 앱 아이콘은 `build/icon.png`이며, 다른 이미지로 바꾸고 싶으면 이 파일만 1024x1024 PNG로 교체하면 됩니다.

### 배포 전 참고사항

- **맥 앱/실행 파일 이름은 영문(`DietGuide`)입니다.** 한글 앱 이름으로 빌드하면 Electron이 실행 직후 죽는 문제가 있어서(아래 "겪은 문제" 참고), 내부 실행 파일 이름은 영문으로 두고 Finder/Dock에 보이는 표시 이름(`CFBundleDisplayName`)만 "맞춤 건강 식단 가이드"로 보이게 설정했습니다. `.dmg`/설치 파일명은 한글 그대로입니다.
- **맥**: 코드 서명 없이(unsigned) 빌드됩니다. 처음 열 때 "확인할 수 없는 개발자" 경고가 뜨면, Finder에서 앱을 **우클릭 → 열기**로 실행하면 이후부터는 정상적으로 열립니다. 서명하려면 Apple Developer Program(유료) 인증서가 필요합니다.
- **윈도우**: 코드 서명 인증서가 없어 서명되지 않은 채로 빌드됩니다. 처음 실행 시 SmartScreen이 "알 수 없는 게시자" 경고를 띄울 수 있으며, "추가 정보 → 실행"으로 넘어갈 수 있습니다. 경고를 없애려면 별도의 코드 서명 인증서 구매가 필요합니다.

### 겪은 문제: 한글 앱 이름 → 실행 즉시 크래시

처음 빌드했을 때 `/Applications`에서 실행하면 앱이 바로 죽는(EXC_BREAKPOINT) 문제가 있었습니다. 원인을 추적해보니 **macOS용 Electron 앱의 실행 파일/헬퍼 앱 이름에 한글(비 ASCII) 문자가 들어가면 Electron이 부팅 중 자신의 Helper 앱을 찾지 못해 크래시**하는 것으로 확인됐습니다 (`electron_main_delegate_mac.mm: Unable to find helper app`). 코드 서명이나 권한(entitlements) 문제가 아니었습니다.

해결: `package.json`의 `productName`을 영문 `DietGuide`로 바꾸고, `mac.extendInfo.CFBundleDisplayName`으로 Finder/Dock 표시 이름만 한글로 지정했습니다. (`CFBundleName`까지 한글로 바꾸면 헬퍼 앱 경로 탐색이 또 깨지므로 `CFBundleDisplayName`만 바꿔야 합니다.)

### 구조

```
diet-guide/
  index.html, styles.css, app.js, data.js, recipes.js  # 웹 앱 본체
  manifest.json, sw.js, icons/                          # PWA 설정
  electron/main.js                                       # 데스크톱 앱 진입점
  build/icon.png                                         # 앱 아이콘 원본
  package.json                                           # Electron 빌드 설정
```

웹 앱 본체(`index.html` 등)를 수정하면 웹/PWA/데스크톱 앱에 모두 동일하게 반영됩니다.
