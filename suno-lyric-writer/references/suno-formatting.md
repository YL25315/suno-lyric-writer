# Suno Formatting Reference

Use this file when preparing copy-paste fields for Suno Custom Mode.

## Field Separation

- Put sung words only in the Lyrics field.
- Put genre, instrumentation, production, vocal tone, and energy in Style of Music.
- Put unwanted traits in Exclude Styles.
- Put operational notes, generation strategy, and rationale outside the Suno fields.
- Assume Suno may sing anything that is not a valid bracketed tag. Keep stage directions out of lyrics.

## Lyrics Tags

Use tags as hints, not as a programming language. Too many tags can make the generation unstable. Add 1-3 performance cues per section at most.

Common tags:

- `[Intro]`
- `[Verse 1]`, `[Verse 2]`
- `[Pre-Chorus]`
- `[Chorus]`
- `[Post-Chorus]`
- `[Hook]`
- `[Bridge]`
- `[Breakdown]`
- `[Build]`
- `[Drop]`
- `[Instrumental Break]`
- `[Solo]`
- `[Outro]`
- `[End]`

Use `[End]` when the user wants a clean stop. Use `[Fade Out]` when the user wants a trailing ending.

Vocal and performance tags:

- `[Spoken]`
- `[Whispered]`
- `[Call and Response]`
- `[Group Vocals]`
- `[Harmony]`
- `[Ad-lib]`

Use parentheses for short sung ad-libs:

```text
I keep the porch light on
(come back, come back)
```

Parentheses are sung. Keep ad-libs short, usually 1-5 words. Do not put production directions like `(drums explode)` or `(instrumental break)` in parentheses.

## Chorus And Structure Control

- Keep chorus lyrics identical on repeats when a recognizable repeated hook matters.
- Number verses as `[Verse 1]`, `[Verse 2]` so they occupy related but distinct slots.
- Use section modifiers sparingly: `[Verse 1: quiet, close vocal]`.
- Bar-count tags such as `[VERSE 1 8]` may be useful in some Suno versions, but treat them as approximate guidance.
- For instrumental tracks, omit sung lyrics and provide an arrangement outline:

```text
[Instrumental Intro]
[Build]
[Drop]
[Breakdown]
[Final Drop]
[Outro]
[End]
```

## Suno Practical Notes

- Custom Mode supports using original lyrics and separate context fields.
- Recent Suno models can generate longer full songs than older models, but exact duration and field limits change. Verify the current UI when limits matter.
- Use Extend for a better ending or a longer arrangement instead of overcrowding the first lyric draft.
- Personas can carry a saved vocal/style identity; note the persona name in Parameters when the user has one.
- Exclude Styles is useful for unwanted instruments, vocal artifacts, mix qualities, or genre bleed.
- Uploading or creating songs can consume credits. Show the package and ask for explicit approval before any automated submission.

## Strong Lyrics Field Pattern

```text
[Verse 1]
...

[Pre-Chorus]
...

[Chorus]
...

[Verse 2]
...

[Bridge]
...

[Final Chorus]
...

[Outro]
...
```

## Avoid

- Putting "make it catchy" or "female vocals" inside the lyrics field.
- Long prose paragraphs instead of lyric lines.
- Four or five full verses for a first generation.
- Multiple contradictory vocal identities.
- Real artist names in Style of Music when a descriptive equivalent will work better.
- Long parenthetical stage directions that become accidental lyrics.
