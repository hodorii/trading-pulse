# AGENTS.md - Trading Pulse 개발 가이드

> 이 프로젝트는 AI 에이전트가 운영하는 정밀 트레이딩 리포트 서비스입니다.

## 프로젝트 개요

- **유형**: 정적 사이트 (Jekyll + GitHub Pages)
- **주소**: https://hodorii.github.io/trading-pulse
- **검색**: Fuse.js 기반 클라이언트 사이드 검색
- **JS 의존성**: Fuse.js (CDN)

---

## 1. 빌드/개발 명령어

### 로컬 서버 실행

```bash
# Jekyll 서버 실행 (기본 포트 4000)
bundle exec jekyll serve

# 포트 지정
bundle exec jekyll serve --port 4001

# 변경사항 자동 재빌드 (개발용)
bundle exec jekyll serve --watch
```

### 빌드

```bash
# 정적 파일 생성 (_site/)
bundle exec jekyll build

# 프로덕션 빌드
JEKYLL_ENV=production bundle exec jekyll build
```

### 테스트

> 이 프로젝트는 정적 사이트로 단위 테스트가 없습니다.
> 브라우저에서 수동으로 검색 기능을 확인하세요.

---

## 2. 코드 스타일 가이드

### JavaScript (js/search.js)

#### 포맷팅
- **들여쓰기**: 2 spaces
- **줄 끝**: LF (Unix)
- **세미콜론**: 필수
- ** quotes**: 작은따옴표 (`'`)优先

```javascript
// Good
const example = 'hello';
function myFunction() {
  return true;
}

// Bad
const example = "hello";
function myFunction(){
return true;
}
```

#### 변수 선언
- `const`를 기본으로 사용
- 값이 재할당되는 경우만 `let` 사용
- `var`는 금지

```javascript
// Good
const config = { threshold: 0.3 };
let counter = 0;

// Bad
var config = { threshold: 0.3 };
```

#### 함수
- 함수 표현식보다 화살표 함수 선호 (단일 행 또는 단순 로직)
- 명명: camelCase, 동사前缀

```javascript
// Good
function loadIndex() { ... }
const handleSearch = () => { ... };

// Bad
function LoadIndex() { ... }
```

#### 비교
- `===` / `!==` 사용 (암묵적 형변환 금지)
- `==` / `!=` 금지

```javascript
// Good
if (value !== null) { ... }

// Bad
if (value != null) { ... }
```

#### 오류 처리
- `try-catch` 필수, 오류 로깅 필수
- 빈 catch 블록 금지

```javascript
// Good
try {
  const data = await fetch(url);
} catch (error) {
  console.error('Failed to load:', error);
}

// Bad
try { ... } catch (e) { }
```

#### DOM 접근
- null 체크 후 접근 (可选链 `?.` 사용)

```javascript
// Good
const input = document.getElementById('search-input');
if (input) { ... }

// 또는
document.getElementById('search-input')?.addEventListener(...);
```

---

## 3. 네이밍 컨벤션

| 구분 | 규칙 | 예시 |
|------|------|------|
| 변수/함수 | camelCase | `searchIndex`, `handleSearch` |
| 상수 | UPPER_SNAKE_CASE | `TYPES`, `STOCKS` |
| CSS 클래스 | kebab-case | `session-group`, `report-item` |
| 파일 | kebab-case | `search.js` |

---

## 4. 새로운 포스트 추가

### 구조
```
_posts/
├── 2024-01-15-1430_IDR_분석.md
├── 2024-01-15-1500_MAD_결정.md
└── ...
```

### Front Matter 필수 항목

```yaml
---
layout: post
title: "IDR_2024-01-15_1430_SK하이닉스_매크로분석"
date: 2024-01-15 14:30:00 +0900
categories: [IDR, Analysis]
session_id: "2024-01-15-1430"
session_order: 1
---
```

### 필드 설명
- `title`: `{유형}_{날짜}_{시간}_{종목}_{제목}` 형식
- `session_id`: 세션 그룹 식별자 (같은 세션의 여러 포스트를 묶음)
- `session_order`: 세션 내 포스트 순서

---

## 5. 검색 인덱스 업데이트

`search.json`은 Jekyll 빌드 시 자동 생성됩니다.

```bash
# 로컬에서 생성 확인
bundle exec jekyll build
# _site/search.json 확인
```

---

## 6. 배포

### GitHub Pages (자동)
- `main` 브랜치에 푸시하면 자동 배포
- https://hodorii.github.io/trading-pulse

### 수동 배포
```bash
# 프로덕션 빌드 후 _site 폴더를DFFF的主力 deployed
```

---

## 7. 디렉토리 구조

```
/
├── _config.yml          # Jekyll 설정
├── _posts/              # 포스트 모음
├── js/
│   └── search.js        # 클라이언트 검색 모듈
├── search.json          # 빌드 시 생성 (검색 인덱스)
├── index.md             # 메인 페이지
└── AGENTS.md           # 이 파일
```

---

## 8. session_id 및 정렬 규칙

### session_id 형식
- **필수**: `YYYY-MM-DD-HHMM` 형식 (예: `2026-02-15-1430`)
- **중요**: YAML에서 정수로 파싱되지 않도록 항상 **따옴표**로 감싸기
- 파일명에서 시간 추출: 파일명 형식 `2026-02-15-1430_유형_종목.md`

```yaml
# Good
session_id: "2026-02-15-1430"

# Bad - YAML에서 정수로 파싱됨
session_id: 1430
```

### session_order
- 세션 내 포스트 순서를 나타내는 정수
- 1부터 시작, 오름차순으로 표시

### 정렬 로직
- **세션**: session_id 기준 내림차순 (최신 → 과거)
- **세션 내**: session_order 기준 오름차순 (1번 → 순차)

---

## 9. 중요 규칙

1. **Pull Request 전 로컬 빌드 확인**: `bundle exec jekyll build` 성공 필수
2. **검색 JS 수정 시**: Fuse.js 옵션 임의 변경 금지 (검색 정확도 영향)
3. **새 종목/유형 추가**: `js/search.js`의 `TYPES`, `STOCKS` 배열 업데이트 필요
4. **커밋 메시지**: 한국어 또는 영어로 명확하게 작성
5. **Git 반영 의무**: 모든 코드 변경은 git commit → push 필수
