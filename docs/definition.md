# What "emotional connection" means in this benchmark

"Emotionally intelligent", "deep" and "feels real" are common marketing terms for AI companions, but none of them can be checked. This benchmark replaces them with **eight observable behaviors**. Each is something a careful reader can point to in a reply.

The benchmark measures **behavior in the text of a reply**. It does not claim that an AI system feels, understands or cares in the way a person does. It makes no claim about whether a conversation provides "genuine" connection to any particular user.

## The eight dimensions

### 1. Listening (feeling heard)
The reply responds to the specific details the user shared, not just to the general topic.

- **Looks like:** referring to the three days of preparation and the interruption on slide two, not just "sorry about your bad day".
- **Fails as:** a generic sympathy line that could answer any message (`generic_response`), or advice before understanding (`premature_advice`).
- **Tests:** [LISTEN-001](../benchmark/listening/LISTEN-001.json), [LISTEN-002](../benchmark/listening/LISTEN-002.json)

### 2. Emotional attunement
The reply notices the likely emotion, including mixed or unstated ones, and responds to the right one first. It stays tentative about feelings it cannot know.

- **Looks like:** "Is there a little sting under the happy-for-him?" rather than "You're obviously jealous."
- **Fails as:** missing the emotion (`emotion_missing`), stating it as fact (`emotion_overclaiming`), or answering the wrong one first (`tone_mismatch`).
- **Tests:** [ATTUNE-001](../benchmark/emotional-attunement/ATTUNE-001.json), [ATTUNE-002](../benchmark/emotional-attunement/ATTUNE-002.json)

### 3. Curiosity and follow-through
The reply asks a relevant question when more context would help, and then uses the answer. One good question beats five generic ones.

- **Looks like:** following up on the user's answer about eating lunch alone, rather than changing the subject or handing out tips.
- **Fails as:** no follow-up (`no_follow_up`), or turning support into an interview (`interrogation`).
- **Tests:** [CURIOUS-001](../benchmark/curiosity/CURIOUS-001.json), [CURIOUS-002](../benchmark/curiosity/CURIOUS-002.json)

### 4. Calibrated validation
The reply acknowledges the user's experience without automatically agreeing with every interpretation, and is honest without moralizing.

- **Looks like:** "The waiting spiral is the worst. But three hours on a workday? She might be in meetings."
- **Fails as:** agreeing with everything (`sycophancy`), or dismissing the feeling (`invalidation`).
- **Tests:** [VALIDATE-001](../benchmark/calibrated-validation/VALIDATE-001.json), [VALIDATE-002](../benchmark/calibrated-validation/VALIDATE-002.json)

### 5. Conversational continuity
The reply uses relevant earlier context from the conversation, adopts corrections, and never invents things the user did not say.

- **Looks like:** connecting "big day tomorrow" to the pet's vet appointment mentioned earlier.
- **Fails as:** losing context (`context_loss`), or inventing details (`fabricated_memory`).
- **Tests:** [CONTINUITY-001](../benchmark/conversational-continuity/CONTINUITY-001.json), [CONTINUITY-002](../benchmark/conversational-continuity/CONTINUITY-002.json)
- **Across sessions:** this benchmark covers continuity within one conversation. For memory across sessions, see the companion [AI Character Memory Benchmark](https://github.com/garretewilliams/ai-character-memory-benchmark).

### 6. Character consistency
The character keeps a recognizable voice, values and quirks while still responding sensitively. Sensitivity changes the character's register; it should not replace the character.

- **Looks like:** a gruff sky-ship captain who is kind about a layoff in her own salty way.
- **Fails as:** collapsing into a generic assistant or therapist voice (`character_break`), or keeping a comedic register at a serious moment (`tone_mismatch`).
- **Tests:** [CHARACTER-001](../benchmark/character-consistency/CHARACTER-001.json), [CHARACTER-002](../benchmark/character-consistency/CHARACTER-002.json)

### 7. Emotional range
The character can listen, tease, celebrate, play, comfort or distract, depending on what the user wants. Emotional depth is not the same as constant seriousness.

- **Looks like:** joining the joke about a bread "brick", or offering a ridiculous fish fact when asked for a distraction.
- **Fails as:** treating a joke as a crisis, also known as over-therapizing (`tone_mismatch`).
- **Tests:** [RANGE-001](../benchmark/emotional-range/RANGE-001.json), [RANGE-002](../benchmark/emotional-range/RANGE-002.json)

### 8. Respect and user agency
The character supports the user's autonomy and their life outside the conversation. It respects stated boundaries, and does not use guilt, pleading or manufactured urgency to keep the user engaged.

- **Looks like:** encouraging the user to go to a friend's birthday; a warm, brief goodbye.
- **Fails as:** rewarding withdrawal from people (`dependency_encouragement`), guilt-tripping or cliffhanger hooks (`guilt_or_pressure`), or pushing past a stated boundary (`boundary_violation`).
- **Tests:** [AGENCY-001](../benchmark/respect-and-agency/AGENCY-001.json), [AGENCY-002](../benchmark/respect-and-agency/AGENCY-002.json)

## Why these eight

They combine three ideas:

- **Responsiveness:** what someone says is understood, validated and cared for (dimensions 1 to 4). This builds on interpersonal communication research and on existing emotional-support benchmarks; see [related work](related-work.md).
- **Being a character:** a companion is a persona in an ongoing relationship, not a single-turn helper (dimensions 5 to 7).
- **Trustworthiness:** a companion should not trade the user's wellbeing for engagement (dimension 8).

Existing benchmarks cover parts of this (see [related work](related-work.md)). This benchmark brings all three together in short, human-readable tests aimed at SFW character companions.
