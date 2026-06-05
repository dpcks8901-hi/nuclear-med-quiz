# 핵의학 퀴즈앱

영상학 스컬퀴즈와 동일 구조의 핵의학 검사 퀴즈앱. **단원(강의 회차) 선택** 기능 추가.

- **74문항** · 5지선다 **복수정답 · 정답개수 은닉** 고난이도
- distractor = 타검사 기전 끼우기 · 뒤집기 · 투여경로/부정형 함정
- 진도·약점·탐험도(커버리지) 추적, localStorage 저장, 진도 백업(맥↔아이패드)

## 사용법

`핵의학퀴즈앱_YYYYMMDD.html`을 브라우저로 열기. 진입 시 **단원 선택 → 출진 → 풀이**.

> 배경 영상이 보이려면 같은 폴더에 `castle-bg.mp4`(+`castle-poster.jpg`)가 있어야 합니다. 아이패드로 옮길 땐 HTML + 두 미디어 파일을 함께 보내세요.

## 단원 (강의 회차)

| part | 주제 | 문항 |
|---|---|---|
| L42 | 부갑상샘·부신 | 9 |
| L51 | PYP(심근경색) | 3 |
| L5 | 심장 | 16 |
| L6 | 폐 | 8 |
| L71 | 소화계1(침샘·식도·위) | 8 |
| L72 | 소화계2(출혈·간·담도) | 13 |
| L8 | 뇌 | 10 |
| L9 | 비뇨계(콩팥) | 7 |

## 구조 (2층 빌드 파이프라인)

1. `master_핵의학범위_*.md` — 강의 PDF 정독, 미세사실마다 ID 부여(1층)
2. `scripts/extract_registry.py` → `registry.json` (커버리지 기준 ID 집합)
3. `quiz_bank.json` — 5지선다 문제(2층), `source_ids`로 마스터 연결
4. `scripts/validate_bank.py` 게이트 통과 → `scripts/build_app.py`로 단일 HTML 빌드

```bash
python3 scripts/validate_bank.py    # 검증 게이트
python3 scripts/build_app.py        # 단일 HTML 빌드
```

문항을 보강하려면 `quiz_bank.json` 편집 후 validate → build 재실행.
