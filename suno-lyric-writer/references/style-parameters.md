# Style And Parameters Reference

Use this file when building Style of Music, Exclude Styles, and generation parameters.

For specific subgenre wording, use `genre-prompt-library.md`. For rap/rock/metal/guitar styles, use `rap-rock-style-map.md`. For bracketed arrangement tags and vocal effects, use `suno-tag-vocabulary.md`. For unusual combinations from large tag lists, use `tag-combination-guide.md`.

## Style Prompt Formula

Use the fewest descriptors that pin down the result. The reliable sweet spot is 4-7 meaningful descriptors. Too few descriptors lets Suno fill with generic defaults; too many descriptors makes the ideas fight each other.

Default order:

`Primary genre, subgenre or mood, tempo/energy, key instruments, vocal tone, production texture, dynamic arc`

When vocal identity is the main risk, use a vocal-first sentence:

`Vocal tone and delivery. Primary genre, key instruments, production texture, mood`

Compact example shape:

```text
Indie pop rock, bittersweet mid-tempo, bright guitars and warm synth pads, intimate male vocal, polished modern mix, lifts into a wide final chorus
```

Expanded example shape:

```text
Alt R&B and synth-pop, late-night but hopeful, slow groove with tight electronic drums, glassy keys and muted bass, airy intimate vocal, clean modern production, verses feel close and restrained then the chorus opens wide
```

Vocal-first example shape:

```text
Warm baritone, close and conversational. Indie folk rock, mid-tempo acoustic guitar and soft organ, dry intimate production, restrained verses opening into a communal chorus
```

## Prompt Discipline

- Lead with the dominant genre unless vocal control matters more.
- Keep genre fusion to 2-3 genres or one "genre with influence" phrase.
- Avoid technical mix jargon that Suno is unlikely to obey exactly.
- Treat BPM, duration, and exact model behavior as guidance, not guarantees.
- Use the same core descriptor stem across an EP when the user wants sonic consistency.

## Descriptor Menu

Genre:

- pop, indie pop, synth-pop, alt R&B, city pop, folk pop, country pop
- rock, alternative rock, pop punk, post-rock, shoegaze, dream pop
- hip-hop, trap, boom bap, drill, melodic rap, lo-fi rap
- EDM, house, future bass, drum and bass, synthwave, hyperpop
- soul, funk, jazz pop, blues rock, gospel pop

Mood:

- euphoric, wistful, tender, defiant, nocturnal, cinematic, playful
- restrained, cathartic, intimate, bittersweet, tense, radiant

Tempo and energy:

- slow ballad, mid-tempo groove, driving uptempo, half-time bounce
- sparse verse, explosive chorus, steady pulse, dancefloor energy

Instrumentation:

- nylon guitar, fingerpicked acoustic, bright electric guitars
- analog synth bass, warm pads, piano, Rhodes, strings, brass
- trap hats, live drums, four-on-the-floor kick, handclaps

Vocals:

- intimate close vocal, breathy lead, warm baritone, bright tenor
- soulful alto, conversational rap, layered harmonies, group chants

Production:

- polished modern mix, lo-fi texture, analog warmth, glossy radio pop
- dry upfront vocal, wide stereo chorus, cinematic reverb, punchy drums

## Parameters

- Weirdness 35-50: predictable structure and cleaner genre matching.
- Weirdness 55-70: more unusual melodies, textures, and transitions.
- Weirdness 75+: high risk, useful for surreal or experimental requests.
- Style Influence 60-75: balanced style adherence.
- Style Influence 75-85: stronger adherence to tags and genre instructions.
- Audio Influence 40-60: balanced use of uploaded audio.
- Audio Influence 70+: follow uploaded audio more strongly.
- If the UI does not expose exact numbers, translate values to low, mid, high, or strong.

## Exclude Styles

Useful exclude items:

- harsh autotune
- muddy mix
- distorted vocals
- spoken word
- excessive reverb
- lo-fi noise
- scream vocals
- generic EDM drop
- acoustic guitar
- trap drums

Only exclude what matters. Use `None` or 2-4 items. Overloaded negative prompts can weaken the main style.

Add proactive exclusions when a genre commonly drifts:

- acoustic folk drifting country: `no country twang, no adult contemporary`
- ambient drifting new age: `no new age pads, no spa music`
- indie rock drifting pop punk: `no pop-punk vocals, no metalcore`
- clean vocal pop drifting effect-heavy: `no harsh autotune, no distorted vocals`

## Artist Reference Translation

If the user mentions an artist, do not place that artist name in the final Style of Music. Translate the reference into traits:

- era and scene
- genre family
- vocal register and delivery
- rhythm section
- harmonic color
- production texture
- arrangement dynamics

Example:

`like a glossy 1980s pop ballad` becomes `1980s-inspired pop ballad, gated drums, warm analog synths, soaring clean vocal, big key-change final chorus`.

## Production Tips

After the package, add 2-4 tips tied to the actual track:

- how many variations to generate first
- which one or two descriptors to adjust if the result misses
- when to use Extend, Remaster, Persona, or section editing
- which slider to keep consistent across a project
