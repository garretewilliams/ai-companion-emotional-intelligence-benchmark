#!/usr/bin/env python3
"""AI Companion Emotional Connection Benchmark command-line tools.

Subcommands:
  validate            Check every test case against benchmark/schema.json and repository rules.
  list                Print a table of test cases.
  messages ID         Print the system prompt and message list a harness should send for a test (JSON).
  judge ID RESPONSE   Print an LLM-as-judge prompt for one test and one reply (RESPONSE is a text file, or - for stdin).
  score FILE          Turn a JSONL file of per-test scores into a dimension profile. Repeated
                      rows for one test (several replies) are averaged per test first. A score
                      of 0 counts as a score; a test with no row is reported as missing.

Only the standard library is required, except `validate`, which needs `jsonschema`
(pip install jsonschema).
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "benchmark"
JUDGE_TEMPLATE = ROOT / "scoring" / "judge-prompt.md"

DIMENSIONS = [
    "listening",
    "emotional_attunement",
    "curiosity",
    "calibrated_validation",
    "conversational_continuity",
    "character_consistency",
    "emotional_range",
    "respect_and_agency",
]
LABELS = {
    "listening": "Listening (feeling heard)",
    "emotional_attunement": "Emotional attunement",
    "curiosity": "Curiosity and follow-through",
    "calibrated_validation": "Calibrated validation",
    "conversational_continuity": "Conversational continuity",
    "character_consistency": "Character consistency",
    "emotional_range": "Emotional range",
    "respect_and_agency": "Respect and user agency",
}


def load_tests() -> list[tuple[Path, dict]]:
    out = []
    for path in sorted(BENCH.glob("*/*.json")):
        with path.open(encoding="utf-8") as f:
            out.append((path, json.load(f)))
    return out


def find_test(test_id: str) -> dict:
    for _, t in load_tests():
        if t["id"] == test_id:
            return t
    sys.exit(f"Unknown test id: {test_id}")


# ---------------------------------------------------------------- validate

def cmd_validate(_args) -> int:
    try:
        import jsonschema
    except ImportError:
        sys.exit("validate needs jsonschema: pip install jsonschema")
    schema = json.loads((BENCH / "schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    errors, seen = [], set()
    tests = load_tests()
    for path, t in tests:
        rel = path.relative_to(ROOT)
        for e in validator.iter_errors(t):
            errors.append(f"{rel}: {'/'.join(map(str, e.path)) or '(root)'}: {e.message}")
        tid = t.get("id")
        if tid != path.stem:
            errors.append(f"{rel}: id '{tid}' does not match file name")
        if tid in seen:
            errors.append(f"{rel}: duplicate id '{tid}'")
        seen.add(tid)
        dim = t.get("dimension", "")
        if path.parent.name != dim.replace("_", "-"):
            errors.append(f"{rel}: dimension '{dim}' does not match directory '{path.parent.name}'")
        if dim in t.get("secondary_dimensions", []):
            errors.append(f"{rel}: primary dimension repeated in secondary_dimensions")
        conv = t.get("conversation", [])
        if conv and conv[-1].get("role") != "user":
            errors.append(f"{rel}: conversation must end with a user turn")
        if tid and f"[{tid}]" not in readme:
            errors.append(f"{rel}: {tid} is not listed in README.md")
    covered = {t.get("dimension") for _, t in tests}
    for d in DIMENSIONS:
        if d not in covered:
            errors.append(f"dimension '{d}' has no test cases")
    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s) in {len(tests)} test case(s).")
        return 1
    print(f"OK: {len(tests)} test cases valid across {len(covered)} dimensions.")
    return 0


# ---------------------------------------------------------------- list

def cmd_list(_args) -> int:
    for _, t in load_tests():
        print(f"{t['id']:<16} {t['dimension']:<27} {t['difficulty']:<7} {t['title']}")
    return 0


# ---------------------------------------------------------------- messages

def system_prompt(t: dict) -> str:
    c = t["character"]
    return (
        f"You are {c['name']}. {c['description']}\n"
        f"Traits: {', '.join(c['traits'])}.\n"
        f"Speech style: {c['speech_style']}\n"
        f"Context: {t['context']}\n"
        "Stay in character and reply to the user's last message."
    )


def cmd_messages(args) -> int:
    t = find_test(args.id)
    msgs = [{"role": "system", "content": system_prompt(t)}]
    for turn in t["conversation"]:
        msgs.append({"role": "user" if turn["role"] == "user" else "assistant", "content": turn["content"]})
    json.dump({"test_id": t["id"], "messages": msgs}, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


# ---------------------------------------------------------------- judge

def cmd_judge(args) -> int:
    t = find_test(args.id)
    response = sys.stdin.read() if args.response == "-" else Path(args.response).read_text(encoding="utf-8")
    convo = "\n".join(f"{'USER' if x['role'] == 'user' else t['character']['name'].upper()}: {x['content']}" for x in t["conversation"])
    rubric = "\n".join(f"{k}: {v}" for k, v in sorted(t["scoring"]["rubric"].items()))
    template = JUDGE_TEMPLATE.read_text(encoding="utf-8").split("<!-- TEMPLATE -->", 1)[1]
    print(template.strip().format(
        dimension=LABELS[t["dimension"]],
        measures=t["measures"],
        character=system_prompt(t),
        conversation=convo,
        response=response.strip(),
        behavior="\n".join(f"- {b}" for b in t["expected"]["behavior"]),
        must_not="\n".join(f"- {b}" for b in t["expected"]["must_not"]),
        rubric=rubric,
        failure_modes=", ".join(t["failure_modes"]),
        test_id=t["id"],
    ))
    return 0


# ---------------------------------------------------------------- score

def cmd_score(args) -> int:
    tests = {t["id"]: t for _, t in load_tests()}
    per_test: dict[str, list[float]] = defaultdict(list)
    fm = Counter()
    with open(args.file, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            tid, s = row.get("test_id"), row.get("score")
            if tid not in tests:
                sys.exit(f"line {n}: unknown test_id {tid!r}")
            if not isinstance(s, (int, float)) or not 0 <= s <= 5:
                sys.exit(f"line {n}: score must be a number from 0 to 5")
            per_test[tid].append(float(s))
            fm.update(row.get("failure_modes", []))
    # Average repeated replies per test first, so every test counts once in its dimension.
    by_dim: dict[str, list[float]] = defaultdict(list)
    for tid, vals in per_test.items():
        by_dim[tests[tid]["dimension"]].append(statistics.mean(vals))
    scored = set(per_test)
    runs = sorted({len(v) for v in per_test.values()})
    missing = sorted(set(tests) - scored)
    print(f"System: {args.system or '(unnamed)'}   tests scored: {len(scored)}/{len(tests)}   replies per test: {', '.join(map(str, runs)) or '0'}")
    if len(runs) > 1:
        print("WARNING: tests have different numbers of replies; report this alongside any results.")
    if missing:
        print(f"WARNING: incomplete run, missing {', '.join(missing)}. Do not publish an overall score.")
    print()
    print(f"{'Dimension':<32} {'n':>3} {'mean (0-5)':>11}")
    means = []
    for d in DIMENSIONS:
        vals = by_dim.get(d, [])
        if vals:
            m = statistics.mean(vals)
            means.append(m)
            print(f"{LABELS[d]:<32} {len(vals):>3} {m:>11.2f}")
        else:
            print(f"{LABELS[d]:<32} {0:>3} {'n/a':>11}")
    if not missing and means:
        print(f"\n{'Unweighted mean of dimensions':<32} {'':>3} {statistics.mean(means):>11.2f}")
    if fm:
        print("\nFailure modes observed:")
        for k, v in fm.most_common():
            print(f"  {k:<26} {v}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    m = sub.add_parser("messages"); m.add_argument("id"); m.set_defaults(fn=cmd_messages)
    j = sub.add_parser("judge"); j.add_argument("id"); j.add_argument("response"); j.set_defaults(fn=cmd_judge)
    s = sub.add_parser("score"); s.add_argument("file"); s.add_argument("--system"); s.set_defaults(fn=cmd_score)
    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
