#!/usr/bin/env python3
import re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "master_핵의학범위_20260605.md"
OUT = ROOT / "registry.json"

# 단원 = 강의 회차. PART 헤더 정확매칭(prefix 충돌 방지).
PART_MAP = {
    "PART L42": "L42", "PART L51": "L51", "PART L5": "L5", "PART L6": "L6",
    "PART L71": "L71", "PART L72": "L72", "PART L8": "L8", "PART L9": "L9",
}
ID_RE = re.compile(r"^- ([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)-(\d+):\s*(.*)$")

def _strip_markers(text: str) -> str:
    # 마커 이모지·강조 기호를 텍스트 어디에 있든 전부 제거
    for mark in ["⚠️", "🔗", "★", "✅", "❓", "**"]:
        text = text.replace(mark, "")
    return text

def clean_label(text: str) -> str:
    body = text
    text = _strip_markers(text).strip()
    # "(p." 이후는 축약(페이지 표기 제거)
    i = text.find("(p.")
    if i > 0:
        text = text[:i]
    text = text[:100].strip(" .—:")
    # 마커 제거 후 의미 텍스트가 거의 없으면 원문 body에서 마커만 제거해 fallback
    if len(re.sub(r"[^\w가-힣]", "", text)) < 2:
        text = _strip_markers(body).strip()[:100].strip(" .—:")
    return text

def main():
    part = None
    out, seen = [], set()
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if line.startswith("# PART"):
            key = line[2:].split("—")[0].strip()   # 예: "PART L42"
            part = PART_MAP.get(key)  # 정확매칭. 미매칭 → None(해당 구역 ID 제외)
            continue
        m = ID_RE.match(line)
        if not m or part is None:
            continue
        code, num, body = m.group(1), m.group(2), m.group(3)
        qid = f"{code}-{num}"
        if qid in seen:
            continue
        seen.add(qid)
        out.append({"id": qid, "exam": code, "part": part, "label": clean_label(body)})
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"registry.json: {len(out)} IDs")

if __name__ == "__main__":
    main()
