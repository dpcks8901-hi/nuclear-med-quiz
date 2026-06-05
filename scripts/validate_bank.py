#!/usr/bin/env python3
import json, argparse, pathlib, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", default="quiz_bank.json")
    ap.add_argument("--registry", default="registry.json")
    a = ap.parse_args()
    bank = json.loads(pathlib.Path(a.bank).read_text(encoding="utf-8"))
    reg_ids = {r["id"] for r in json.loads(pathlib.Path(a.registry).read_text(encoding="utf-8"))}

    errors, ids = [], set()
    dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for i, q in enumerate(bank):
        tag = q.get("id", f"#{i}")
        if not q.get("id"): errors.append(f"{tag}: id 없음")
        if q.get("id") in ids: errors.append(f"{tag}: id 중복")
        ids.add(q.get("id"))
        sids = q.get("source_ids") or []
        if not sids: errors.append(f"{tag}: source_ids 비어있음")
        for s in sids:
            if s not in reg_ids: errors.append(f"{tag}: source_id '{s}' registry에 없음")
        opts = q.get("options") or []
        if len(opts) != 5: errors.append(f"{tag}: options 5개 아님({len(opts)})")
        ans = q.get("answers") or []
        if not (1 <= len(ans) <= 5): errors.append(f"{tag}: answers 개수 이상({len(ans)})")
        if len(set(ans)) != len(ans): errors.append(f"{tag}: answers 중복")
        if any(not (0 <= x <= 4) for x in ans): errors.append(f"{tag}: answers 범위(0~4) 벗어남")
        if not q.get("explanation"): errors.append(f"{tag}: explanation 없음")
        if len(ans) in dist: dist[len(ans)] += 1

    total = sum(dist.values())
    if total:
        four_ratio = dist[4] / total
        print(f"문항수={total} 정답개수분포={dist} (4개비율={four_ratio:.0%})")
        if four_ratio > 0.25:
            errors.append(f"정답 4개 비율 {four_ratio:.0%} > 25% 상한(6규칙①)")
        # 분포 권고(경고만)
        target = {1: .25, 2: .25, 3: .25, 4: .20, 5: .05}
        skew = [f"{k}개 {dist[k]/total:.0%}(목표{int(target[k]*100)}%)" for k in dist if abs(dist[k]/total - target[k]) > 0.12]
        if skew: print("⚠️ 분포 권고이탈:", ", ".join(skew))

    if errors:
        print(f"❌ 검증 실패 {len(errors)}건:")
        for e in errors[:50]: print("  -", e)
        sys.exit(1)
    print("✅ 검증 통과")
    sys.exit(0)

if __name__ == "__main__":
    main()
