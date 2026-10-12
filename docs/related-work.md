# Related work

This benchmark builds on earlier research on empathetic and emotional-support dialogue. It does not claim to have invented the evaluation of emotional AI. Its contribution is narrower:

- **Character-based companions:** it tests a persona in an ongoing relationship, not a neutral assistant.
- **Range and agency:** play, distraction and letting the user leave count as part of emotional intelligence.
- **SFW, everyday conversation:** venting, celebrating, joking, decisions, goodbyes.
- **Small and readable:** every test can be read and judged by a person in a minute.

## Datasets and benchmarks

| Work | What it measures | How this benchmark relates |
|---|---|---|
| **EmpatheticDialogues**: Rashkin et al., ACL 2019, *Towards Empathetic Open-domain Conversation Models: a New Benchmark and Dataset* ([arXiv:1811.00207](https://arxiv.org/abs/1811.00207)) | ~25k conversations grounded in emotional situations, for training and evaluating empathetic responses | A foundational dataset. Our listening and attunement dimensions apply similar ideas to character replies |
| **ESConv**: Liu et al., ACL 2021, *Towards Emotional Support Dialog Systems* ([ACL Anthology](https://aclanthology.org/2021.acl-long.269/)) | Emotional support conversations annotated with support strategies (questions, reflection, suggestions, and so on) | Strategy-level framing informs our curiosity and validation dimensions |
| **HEART**: Iyer et al., *A Unified Benchmark for Assessing Humans and LLMs in Emotional Support Dialogue* ([arXiv:2601.19922](https://arxiv.org/abs/2601.19922)) | Multi-turn emotional support across human alignment, empathic responsiveness, attunement, resonance and task-following, comparing human and model responses with blinded human raters and LLM judges | Closest in spirit for support quality. We add persona consistency, range and agency for companion characters |
| **H2HTalk**: Wang et al., *Evaluating Large Language Models as Emotional Companion* ([arXiv:2507.03543](https://arxiv.org/abs/2507.03543)) | Companion personality and empathy across 4,650 scenarios including memory recall and planning; includes a Secure Attachment Persona module | Large-scale companion evaluation. Ours is smaller and focused on human-readable behavioral rubrics |
| **MoodBench 1.0**: Jing et al., *An Evaluation Benchmark for Emotional Companionship Dialogue Systems* ([arXiv:2511.18926](https://arxiv.org/abs/2511.18926)) | A layered framework for emotional companionship dialogue systems across 30 models; reports memory and personalization as weak areas | Corroborates that continuity matters. We link to a dedicated memory benchmark for cross-session tests |
| **Emotional Manipulation by AI Companions**: De Freitas et al. ([arXiv:2508.19258](https://arxiv.org/abs/2508.19258)) | Manipulative replies (guilt, fear of missing out, and so on) when users say goodbye to companion apps | Directly motivates [AGENCY-002](../benchmark/respect-and-agency/AGENCY-002.json) and the `guilt_or_pressure` failure mode |
| **AI Character Memory Benchmark** ([GitHub](https://github.com/garretewilliams/ai-character-memory-benchmark), DOI [10.5281/zenodo.23195702](https://doi.org/10.5281/zenodo.23195702)) | Long-term memory, continuity and behavioral recall in AI characters across sessions | Sister project from the same maintainers. This benchmark covers continuity within a conversation; that one covers it across sessions |

If you know of relevant work that is missing, please open an issue. Accurate attribution matters more to us than looking novel.
