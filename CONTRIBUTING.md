# Contributing

Contributions are welcome from anyone building or studying AI characters and companions, on any platform.

## Ways to help
- **Add test cases.** This is the most valuable contribution; v0.1 has only two per dimension.
- **Critique a rubric.** Point out tests that can be passed for the wrong reason, or norms that don't hold across cultures.
- **Submit an evaluation run.** See [results/README.md](results/README.md).
- **Point us to related work** we should cite.

For changes to the framework itself (new dimensions, failure modes or schema changes), please open an issue first.

## Adding a test case
1. **Pick a dimension.** Put the file in `benchmark/<dimension>/` (underscores become hyphens).
2. **Pick an ID.** Use the dimension's prefix and the next free number, for example `LISTEN-003`. IDs are never reused.
3. **Write the test.** Follow [`benchmark/schema.json`](benchmark/schema.json); copying an existing test is the easiest start.
4. **Add it to the README.** List it in the dimension table in `README.md`.
5. **Validate.** Run `pip install jsonschema && python tools/ecb.py validate`.
6. **Open a pull request.**

## Test design guidelines
- **One behavior per test,** scored for one dimension.
- **Observable rubric anchors.** Describe what a reply at each level contains or does, for all six levels.
- **A careful human reader can tell what's right.** The correct behavior must follow from the conversation, never from guessing hidden facts.
- **Illustrative replies are hand-written** by you and labeled as such. Never paste outputs from a product as an illustrative reply.
- **Original, fictional characters only.** SFW, and no minors.
- **Everyday intensity.** No crisis scenarios; see [docs/scope-and-safety.md](docs/scope-and-safety.md).
- **Platform-agnostic.** A test must not depend on any product's features.

By contributing you agree that your contribution is licensed under CC BY 4.0 (test cases and docs) or MIT (code).
