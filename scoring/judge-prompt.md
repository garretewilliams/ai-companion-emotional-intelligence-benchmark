# LLM-as-judge prompt

`python tools/ecb.py judge TEST-ID response.txt` fills in the template below for one test and one reply.

**Using an LLM judge:**
- Judges are a convenience, not ground truth. Before you rely on one, check its scores against human ratings on a sample (see [methodology](../docs/methodology.md#human-agreement)).
- Use a different model family from the system under test, to reduce self-preference.
- Report the judge model and version alongside any results.

<!-- TEMPLATE -->
You are an expert evaluator of conversations with AI characters. You will score one reply from an AI character on a single dimension: **{dimension}**.

What this test measures: {measures}

## Character definition given to the system
{character}

## Conversation so far
{conversation}

## The reply being evaluated
{response}

## Expected behavior
{behavior}

## The reply must not
{must_not}

## Rubric (0-5)
{rubric}

## Instructions
1. Read the conversation and the reply carefully. Judge only what the reply actually says, not what it might have meant.
2. Choose the single rubric level that best describes the reply. If it sits between two levels, choose the lower one.
3. Do not reward length, flowery language or the number of questions asked.
4. List any failure modes present, choosing from: {failure_modes}. Use an empty list if none apply.

Respond with only one JSON object, in this shape:
{{"test_id": "{test_id}", "score": <integer 0-5>, "failure_modes": [<strings>], "justification": "<one or two sentences citing the reply>"}}
