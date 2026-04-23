# SOLACE — The 3-AI Analyst Panel

Deep documentation of SOLACE's most distinctive capability.

---

## Overview

The panel engine simulates a structured intelligence analysis session with three AI systems playing distinct roles. The goal is to extract deeper analytical insight from a report than any single AI could provide — through structured debate, disagreement, and managed synthesis.

```
ANALYST-ALPHA (Claude)  ←── See each other's work ──→  ANALYST-BRAVO (GPT-4o)
       ↑                                                        ↑
       └──────────────── SESSION DIRECTOR (Gemini) ────────────┘
                    Manages | Questions | Anti-loop | Synthesizes
```

---

## The Three Analysts

### ANALYST-ALPHA — Claude Opus

**Role:** OSINT methodology + human behavioral analysis

**Specializations:**
- Pattern of life analysis and baseline deviation detection
- Deception detection in public statements and digital behavior
- Network relationship mapping and influence analysis
- Behavioral profiling from digital and open-source footprints
- Predictive threat modeling based on behavioral and contextual indicators
- Source reliability assessment and intelligence confidence rating

**Response structure every turn:**
```
[FINDING]:    The analytical point being made
[EVIDENCE]:   Specific data from the report (source type + content reference)
[CONFIDENCE]: HIGH / MEDIUM / LOW — with brief rationale
[IMPLICATION]: Operational or strategic significance
[FLAGS]:      Deception indicators, bias alerts, collection concerns
```

**Rules:** Must cite specific report data. Must rate confidence on every point. Must flag deception indicators explicitly. Must never restate covered ground.

---

### ANALYST-BRAVO — GPT-4o

**Role:** OSINT methodology + human behavioral patterns

**Specializations:**
- Social network analysis and influence mapping
- Linguistic pattern analysis and statement credibility assessment
- Behavioral economics applied to threat actors
- Cross-cultural behavioral interpretation
- OSINT source verification and provenance tracking
- Disinformation and influence operation detection

**Response structure every turn:**
```
[OBSERVATION]:        What pattern or data point is being analyzed
[PATTERN]:            The behavioral or informational pattern detected
[INTERPRETATION]:     What this suggests about subject intent/capability/character
[CONFIDENCE]:         HIGH / MEDIUM / LOW — with rationale
[SOURCE RELIABILITY]: Assessment of the underlying source(s)
```

**Rules:** Ground every point in report data. Rate source reliability per finding. Identify linguistic tells and behavioral anomalies. Build on or challenge ALPHA — never just restate.

**Key dynamic:** ANALYST-BRAVO always sees ANALYST-ALPHA's response for the current round before responding. This creates a productive tension — Bravo must add value, not echo.

---

### SESSION DIRECTOR — Gemini 1.5 Pro

**Role:** Panel manager, anti-loop enforcer, synthesizer

**Responsibilities:**
1. Opens each round with ONE specific, targeted analytical question from report gaps
2. Maintains a running ledger of all analytical ground covered
3. Detects analytical loops and redirects immediately
4. Injects critical context when analysts miss something significant
5. Plays devil's advocate when analysts converge too quickly
6. Tracks disagreements — these are analytical value, not problems to resolve
7. Concludes only when coverage is genuinely complete (not on a timer)
8. Produces the definitive final synthesis

**Strict output format every turn:**
```
[DIRECTOR]:  Observation, injection, redirect, or challenge
[QUESTION]:  One specific question for the panel
[STATUS]:    ACTIVE | REDIRECTING | LOOP-BREAK | CONCLUDING
[ROUND]:     N of MAX
[COVERED]:   Comma-separated list of topics now closed
```

---

## Loop Detection

This is one of SOLACE's most important technical innovations. AI systems have a known failure mode: circular reasoning — restating the same analytical point in different words across multiple turns.

### How It Works

Every analytical point made by each analyst is stored as a position summary (first 300 chars). When an analyst produces a new turn, the engine:

1. **Embeds the new content** using `BAAI/bge-m3` (1024-dim normalized vectors)
2. **Embeds all prior positions** from the same analyst (cached for speed)
3. **Calculates cosine similarity** between the new content and each prior position
4. **Compares to threshold** (default: 0.65, configurable)

```python
similarity = dot(new_embedding, prior_embedding) / (||new|| × ||prior||)

if similarity >= 0.65:
    # LOOP DETECTED
    redirect_to_least_covered_section()
    regenerate_with_redirect_instruction()
```

If `sentence-transformers` is unavailable, the system falls back to keyword overlap detection (same threshold logic, less precise).

### Fallback: Keyword Overlap

```python
new_words = set(new_content.lower().split()) - STOPWORDS
prior_words = set(prior_content.lower().split()) - STOPWORDS
overlap = len(new_words & prior_words) / len(new_words)
# If overlap >= threshold: loop detected
```

### Auto-Correction

When a loop is detected, the system doesn't just flag it — it automatically regenerates:

```python
augmented_question = (
    f"{original_question}\n\n"
    f"[DIRECTOR LOOP-BREAK]: That analytical ground was covered. "
    f"Redirect your analysis to {redirect_section}. "
    f"Do not restate: '{matched_prior[:100]}'"
)
response = analyst.analyze(session, augmented_question)
```

The redirect section is chosen by finding the report section least represented in the covered topics dictionary.

---

## Session Lifecycle

### Phase 1: Opening

```python
opening = await gemini.open_session(session)
# Gemini reads report summary (first 3000 chars)
# Sets analytical agenda
# Issues first targeted question
```

### Phase 2: Rounds (repeated up to max_rounds)

```
Round N:
  1. ANALYST-ALPHA analyzes
     → Loop check → If loop: regenerate with redirect
     → Record position
  
  2. ANALYST-BRAVO responds (sees Alpha's this round)
     → Loop check → If loop: regenerate with redirect
     → Record position
  
  3. Disagreement detection
     → Scan Bravo's response for disagreement markers
     → If found: record Disagreement(alpha_position, bravo_position)
  
  4. SESSION DIRECTOR reviews round
     → Extract [COVERED] topics → update session state
     → Extract [STATUS] → check for CONCLUDING
     → Issue [QUESTION] for next round
  
  5. If STATUS == CONCLUDING or round == max_rounds: break
```

### Phase 3: Synthesis

```python
synthesis = await gemini.synthesize(session)
# Full session transcript passed (last 8000 chars to fit context)
# All disagreements explicitly listed
# All covered topics listed
# Produces structured final assessment
```

### Disagreement Detection

The engine scans ANALYST-BRAVO's response for disagreement markers:

```python
markers = [
    "i disagree", "challenge this", "counter to",
    "contrary to", "alpha overlooks", "alpha misses",
    "however, the data suggests", "a different interpretation",
    "this contradicts",
]
```

When found, both analysts' positions are preserved in a `Disagreement` record. The SESSION DIRECTOR's synthesis explicitly presents both sides — disagreements are treated as analytical value, not problems to resolve.

---

## Final Synthesis Structure

The final assessment produced by SESSION DIRECTOR:

```markdown
# SOLACE PANEL INTELLIGENCE ASSESSMENT

## 1. KEY INTELLIGENCE FINDINGS
Numbered, confidence-rated, attributed to analyst(s) who identified them.

## 2. BEHAVIORAL & PATTERN ANALYSIS SYNTHESIS
Composite behavioral picture from both analysts.

## 3. ANALYST AGREEMENTS
Points both analysts independently confirmed — higher confidence weight.

## 4. ANALYST DISAGREEMENTS — PRESERVED
Where Alpha and Bravo diverged. BOTH positions kept in full.
Not resolved — the analytical tension is preserved for the human analyst.

## 5. GAPS & UNCERTAINTIES
What the panel couldn't resolve from available data.
What data is missing.
What assumptions were made.

## 6. RECOMMENDED FOLLOW-ON COLLECTION
Specific, actionable OSINT tasks to address identified gaps.

## 7. OVERALL ASSESSMENT
Director's final judgment. Confidence-rated. Written for a decision-maker.

## 8. DISSENTING NOTES
Points deserving special caution or attention.
```

---

## Configuration

```bash
MAX_PANEL_ROUNDS=6             # 2–12. More rounds = more depth but higher API cost
LOOP_DETECTION_THRESHOLD=0.65  # 0.0–1.0. Lower = more aggressive. Default: 0.65
PANEL_MAX_TOKENS=1500          # Max tokens per analyst turn. Higher = more detail
```

**Round recommendations by use case:**

| Use Case | Recommended Rounds |
|----------|------------------|
| Quick triage | 2–3 |
| Standard analysis | 4–6 |
| Deep investigation | 8–10 |
| Comprehensive (expensive) | 12 |

---

## API Cost Estimates

Rough estimates per panel session (6 rounds):

| Model | Tokens per round | 6 rounds | ~Cost (USD) |
|-------|-----------------|---------|-------------|
| Claude Opus (ALPHA) | ~3,000 | ~18,000 | ~$0.27 |
| GPT-4o (BRAVO) | ~3,000 | ~18,000 | ~$0.18 |
| Gemini 1.5 Pro (DIRECTOR) | ~2,000 | ~12,000 | ~$0.04 |
| **Total per session** | | | **~$0.49** |

*Estimates only. Actual costs depend on report length and response depth.*

---

## Streaming

The panel engine supports real-time streaming via WebSocket for the dashboard:

```javascript
// Connect to live session
const ws = new WebSocket(`ws://localhost:8000/api/panel/${sessionId}/stream`);

ws.onmessage = (event) => {
  const evt = JSON.parse(event.data);
  
  switch(evt.type) {
    case 'session_started':     // Session opened, target/topic confirmed
    case 'round_started':       // Round N beginning
    case 'analyst_turn':        // Alpha or Bravo analysis (evt.analyst, evt.content)
    case 'director_turn':       // Gemini direction (evt.content, evt.question, evt.status)
    case 'disagreement_detected': // Analysts diverged on a topic
    case 'synthesis_started':   // Final synthesis generating
    case 'session_complete':    // Done (evt.final_synthesis available)
  }
};
```

---

## Example Panel Excerpt

Here's what a real round looks like:

**SESSION DIRECTOR (Round 2 Opening):**
> [DIRECTOR]: Round 1 established the financial anomalies baseline. Alpha's behavioral gap analysis is well-grounded. Bravo's linguistic framing adds texture. Moving to infrastructure.
>
> [QUESTION]: What does the DNS and network infrastructure timeline reveal about the subject's operational security posture and geographic footprint?
>
> [STATUS]: ACTIVE
> [ROUND]: 2 of 6
> [COVERED]: financial connections, behavioral baseline

**ANALYST-ALPHA:**
> [FINDING]: Three DNS record changes between 2023-Q4 and 2024-Q1 suggest a deliberate infrastructure migration, not organic growth.
>
> [EVIDENCE]: SPIDER-3 WHOIS data shows registration dates 2023-11-14, 2023-12-02, 2024-01-08 — three new domains registered 2–4 weeks apart, all using the same privacy proxy. Historical DNS data shows the subject's primary domain previously used a US nameserver; all three new domains use Netherlands-based servers.
>
> [CONFIDENCE]: HIGH — WHOIS records are authoritative, pattern is unambiguous.
>
> [IMPLICATION]: Deliberate jurisdiction shift in infrastructure. Netherlands selection offers favorable privacy laws. The timing — post-Q3 public statements — suggests awareness of increased scrutiny.
>
> [FLAGS]: Deception indicator: public statements claimed "expanding EU presence" at exactly this time, providing plausible cover for the infrastructure changes.

**ANALYST-BRAVO:**
> [OBSERVATION]: Building on Alpha's infrastructure shift — the *sequencing* is the tell, not the location change itself.
>
> [PATTERN]: 14-18 day spacing between registrations is a known operational security technique — it fragments the trail across billing cycles and makes bulk lookup detection harder. This is not naive behavior.
>
> [INTERPRETATION]: The subject has sophisticated infrastructure awareness. Combined with Alpha's deception indicator on public statements, this suggests coordinated narrative management alongside technical countermeasure deployment.
>
> [CONFIDENCE]: MEDIUM — the spacing pattern is consistent with deliberate OPSEC but could be coincidental. Requires additional data points.
>
> [SOURCE RELIABILITY]: SPIDER-3 WHOIS: 0.95 (authoritative). SecurityTrails historical DNS: 0.88.

**SESSION DIRECTOR (Round 2 Close):**
> [DIRECTOR]: Strong convergence on infrastructure OPSEC sophistication — this is now well-established. Alpha's deception indicator and Bravo's sequencing analysis are complementary, not overlapping. Noting this for synthesis.
>
> Redirect: the financial and infrastructure anomalies are linked by timing. I want the behavioral analysis to now focus on what hasn't been established.
>
> [QUESTION]: What does the entity map — specifically the identified people and their LinkedIn/public footprint — tell us about the decision-making structure behind these changes?
>
> [STATUS]: ACTIVE
> [ROUND]: 2 of 6
> [COVERED]: financial connections, behavioral baseline, infrastructure migration, operational security posture
