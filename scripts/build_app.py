#!/usr/bin/env python3
import pathlib, datetime, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
def read(p): return (ROOT / p).read_text(encoding="utf-8")

def main():
    # QuizEngine은 app_template.html에 인라인 정의됨(engine 주입 불필요).
    tpl = read("src/app_template.html")
    registry = read("registry.json").strip()
    bank = read("quiz_bank.json").strip()
    html = (tpl
        .replace("/*__REGISTRY__*/[]", registry)
        .replace("/*__BANK__*/[]", bank))
    if "/*__" in html:
        print("❌ 미치환 마커 존재"); sys.exit(1)
    out = ROOT / f"핵의학퀴즈앱_{datetime.date.today():%Y%m%d}.html"
    out.write_text(html, encoding="utf-8")
    print(f"✅ {out.name} ({len(html)//1024}KB)")

if __name__ == "__main__":
    main()
