# Quality Review Reference

Use this file before final delivery and when revising user lyrics.

## Review Checklist

- Originality: no copied lyric, no near-quote, no living-artist imitation.
- Brief fit: language, theme, genre, mood, vocal, and target use are honored.
- Hook: title or hook phrase is memorable and repeatable.
- Structure: sections are clear and not overcrowded.
- Prosody: lines can be sung without awkward stress or too many syllables.
- Verse movement: verse 2 adds a new image, event, or emotional turn.
- Chorus lift: chorus is simpler, clearer, and more repeatable than verses.
- Bridge purpose: bridge changes perspective, stakes, or harmony.
- Suno readiness: production notes are outside lyrics; tags are useful and sparse.
- Parameters: sliders match the risk level of the requested style.
- Exclusions: `None` or a short, purposeful list. No overloaded negative prompt.
- Iteration: final answer tells the user what to test first and what to adjust if Suno misses.

## Fast Cliche Pass

Search for stock phrases and replace with scene-specific language:

- lost in the night
- chasing dreams
- broken wings
- fire inside
- heart of stone
- shadows in my mind
- dancing in the rain
- never let go

Do not ban common words. Ban lazy combinations.

## Prosody Pass

- Read each line aloud.
- Mark any line that needs a rushed breath.
- Shorten lines before adding punctuation.
- Put important nouns or verbs near strong beats.
- Keep repeated chorus lines rhythmically consistent.

## Suno Pass

- Remove dense stage directions from the lyrics field.
- Keep tags on their own lines.
- Avoid contradictory tags in the same section.
- If the lyric is long, cut a verse or shorten the bridge.
- If a genre switch is requested, make the switch earned by lyrical or rhythmic escalation.
- Keep Style of Music to 4-7 high-value descriptors unless the user explicitly needs a more detailed prompt.
- Add `[End]` or `[Fade Out]` when endings matter.

## What To Reject

- Exact imitation of a named living artist.
- Existing copyrighted lyrics, even if the user wants "just formatting."
- Unattended Suno submission or upload without user approval.
- Claims that exact duration, model behavior, or slider percentages are guaranteed.
