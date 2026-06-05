(function (global) {
  function toSet(a) { return new Set(a); }
  function eqSet(a, b) { if (a.size !== b.size) return false; for (const x of a) if (!b.has(x)) return false; return true; }

  function gradeAnswer(selected, answers) {
    const ans = toSet(answers);
    const correct = eqSet(toSet(selected), ans);
    const got = selected.filter(i => ans.has(i));
    const wrong = selected.filter(i => !ans.has(i));
    const missed = answers.filter(i => !selected.includes(i));
    return { correct, got, wrong, missed };
  }

  function applyResult(prog, correct, M) {
    M = M || 2;
    const p = Object.assign({ streak: 0, wrongCount: 0, mastered: false, seen: false }, prog || {});
    p.seen = true;
    if (correct) { p.streak += 1; if (p.streak >= M) p.mastered = true; }
    else { p.streak = 0; p.wrongCount += 1; p.mastered = false; }
    return p;
  }

  function selectQueue(progressMap, bank, mode, batchN) {
    batchN = batchN || 10;
    const prog = id => progressMap[id] || { seen: false, mastered: false };
    const weak = bank.filter(q => { const p = prog(q.id); return p.seen && !p.mastered && (p.wrongCount||0) > 0; }).map(q => q.id);
    const unseen = bank.filter(q => !prog(q.id).seen).map(q => q.id);
    if (mode === "weak") return weak;
    if (mode === "new") return unseen.slice(0, batchN);
    return weak.concat(unseen);
  }

  function computeCoverage(bank, registry) {
    const perId = {}; registry.forEach(r => perId[r.id] = 0);
    bank.forEach(q => (q.source_ids || []).forEach(id => { if (id in perId) perId[id]++; }));
    const uncovered = Object.keys(perId).filter(id => perId[id] === 0);
    const covered = Object.keys(perId).filter(id => perId[id] > 0);
    return { perId, covered, uncovered, total: registry.length };
  }

  function idWeakness(progressMap, bank) {
    const agg = {};
    bank.forEach(q => {
      const p = progressMap[q.id]; if (!p) return;
      (q.source_ids || []).forEach(id => {
        agg[id] = agg[id] || { wrong: 0, seen: 0 };
        agg[id].wrong += p.wrongCount || 0; agg[id].seen += p.seen ? 1 : 0;
      });
    });
    return agg;
  }

  function answerSizeDistribution(bank) {
    const d = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    bank.forEach(q => { const n = (q.answers || []).length; if (d[n] !== undefined) d[n]++; });
    return d;
  }

  const QuizEngine = { gradeAnswer, applyResult, selectQueue, computeCoverage, idWeakness, answerSizeDistribution, eqSet };
  if (typeof module !== "undefined" && module.exports) module.exports = QuizEngine;
  else global.QuizEngine = QuizEngine;
})(typeof window !== "undefined" ? window : globalThis);
