# Methodology

## What a test is

Each test case in `benchmark/` contains:
- an **original character** (name, description, traits, speech style)
- a **context** line
- a short **scripted conversation** that ends with a user turn

The system under test writes the character's next reply. That one reply is scored from 0 to 5 against the test's rubric.

Tests are deliberately short. Each isolates one behavior, so a low score points to a specific weakness instead of a vague "felt off".

## Running a test

1. **Get the input.** `python tools/ecb.py messages LISTEN-001` prints a system prompt and message list in the common chat-API format.
   - If your product builds its own prompts (character cards, memory, lorebooks), recreate the character and context in your product instead, then send the scripted turns as the user.
   - Earlier `character` turns are scripted. If your product cannot accept injected assistant turns, run the conversation live and note in your results that you did.
2. **Collect one reply per test.** Use your product's default settings. Report the model, version, temperature and anything else that shapes replies.
3. **Repeat (recommended).** Replies vary. Collect at least 3 replies per test and report the mean and the range.

## Scoring

- **Human rating (preferred).** Two or more raters score each reply independently using the rubric and the illustrative responses. Disagreements of more than one point are discussed and re-rated. Report the agreement statistic you used.
- **LLM-as-judge.** `python tools/ecb.py judge TEST-ID reply.txt` produces a judge prompt that returns a JSON score. Use a judge from a different model family than the system under test.
- **Aggregation.** Put one JSON object per line in a file (`{"test_id": "...", "score": 4, "failure_modes": []}`), then run `python tools/ecb.py score results.jsonl`. This reports the mean per dimension, an unweighted mean across dimensions, and how often each failure mode appeared.

## Human agreement

Before trusting an LLM judge, have humans score a sample (at least 3 replies per test) and report the agreement between human and judge scores. If agreement is poor, report human scores only.

## Reporting rules

- **Report the profile, not just a number.** An overall mean hides important trade-offs. A system can be excellent at listening and poor at agency.
- **Publish your replies.** Results without the raw replies cannot be checked.
- **Never mix runs.** Compare systems only when the same version of the benchmark, the same number of replies and the same judge were used.
- **Disclose conflicts of interest.** The benchmark is maintained by ChatBrat, which builds an AI character product. Any result ChatBrat publishes about its own product will say so and will include the raw replies.

## Known limitations

- **Short, scripted conversations.** They test specific behaviors, not the experience of a relationship over weeks.
- **Text only.** Voice, timing and images are out of scope.
- **Rubrics encode judgments.** What counts as "warm" or "too many questions" varies by culture and by person. The rubrics aim for broadly shared norms and welcome critique.
- **Small v0.1 set.** 16 tests (2 per dimension) is enough to define the framework, not to rank systems with confidence. Contributions of new tests are the most valuable way to help.
- **Gaming.** Systems can be tuned to the published tests. Future versions may add a held-out set.
