# Reference Media Workflow

Use this file when the user provides an audio file, video file, reference link, lyric sheet, transcript, or asks to "make something like this."

## What This Skill Can Extract

Extract reusable creative traits:

- genre and subgenre family
- tempo feel and groove
- meter, section lengths, and energy arc
- instrumentation and arrangement roles
- vocal tone, density, range impression, and delivery
- production texture, mix position, ambience, and sonic era
- lyric point of view, theme, narrative structure, rhyme density, and hook mechanics
- mood vocabulary that can become a Suno Style of Music prompt

Do not copy melody, lyrics, distinctive arrangement signatures, or named-artist identity. Translate references into general musical and lyric-writing traits.

## Analysis Tiers

Tier 1 metadata probe:

- Run `scripts/media_reference_probe.py <path>` for duration, streams, codecs, tags, embedded lyric metadata, and optional 16 kHz mono extraction.
- Use this first for any local audio or video path.

Tier 2 deep musical analysis:

- Run `scripts/deep_audio_analyze.py <path>` when the user asks for deeper analysis or when BPM, groove, energy arc, or arrangement pacing matters.
- The script works with `ffmpeg` only for tempo candidates, onset density, RMS energy, zero-crossing texture, rough section roles, and Suno style traits.
- If optional `librosa`, `numpy`, `scipy`, and `soundfile` dependencies are installed, it also adds key estimates, a tempo cross-check, and rough chord windows.
- Treat all BPM, key, chord, and section labels as creative guidance. Do not present them as guaranteed musicological facts.

## Intake Modes

Direct media mode:

- If the model/runtime can inspect attached audio or video, analyze it directly.
- Give timestamped observations when possible, such as `0:22 chorus lift`, `1:04 vocal harmony`, or `2:10 drop`.
- Separate audible facts from interpretation.

Local file mode:

- If the user provides a local media path, run `scripts/media_reference_probe.py <path>` to summarize duration, streams, codecs, and tags.
- If the user asks for "deep", "BPM", "key", "chords", "section", "arrangement", "energy", or stronger reference extraction, also run `scripts/deep_audio_analyze.py <path>`.
- Use `--extract-audio <out.wav>` when a clean audio file is needed for transcription or external analysis.
- If speech-to-text is available, transcribe likely vocal sections. If not, ask the user for lyrics or accept a rough transcript.

Text-only mode:

- If the user provides lyrics, subtitles, a transcript, or notes, analyze them as lyric reference and ask for audio only if musical style is important.

Video mode:

- Extract both audio traits and visual mood when available.
- Use video imagery only as creative direction, not as evidence for musical details unless it is audible.

## Reference Brief Template

Use this shape before drafting when media meaningfully affects the song:

```markdown
Reference Analysis:
- Audible style:
- Tempo/groove:
- Deep audio notes:
- Arrangement:
- Vocal:
- Production:
- Lyric reference:
- Keep:
- Avoid:

Creative Directions:
1. ...
2. ...
3. ...

Question:
Which direction should I expand, and what should be changed?
```

If the user already gave a clear target, skip the question and state the chosen direction.

## Feedback Loop

1. Extract traits and present a brief.
2. Offer 2-3 directions with distinct hook angles and style prompts.
3. Let the user select, combine, or reject traits.
4. Generate the Suno package.
5. After the user tests Suno output, adjust only one or two controls per iteration:
   - lyrics too rushed: shorten lines or remove a section
   - style too generic: sharpen the first two style descriptors
   - vocal wrong: put vocal descriptor first
   - arrangement too busy: reduce instruments and raise Style Influence
   - melody too plain: raise Weirdness moderately

## Lyric Reference Boundaries

- For copyrighted or third-party lyrics, summarize technique only: point of view, imagery type, rhyme density, refrain placement, emotional arc.
- For user-owned original lyrics, revision can be direct, but preserve the user's intended voice.
- Do not provide rewritten lyrics that are substantially similar to a reference song.
- Do not continue a known lyric from a supplied line.

## Output Contract With References

When media is used, include:

- Reference Analysis
- Creative Direction chosen or proposed
- Suno Custom Mode package
- Production Tips
- Next Feedback Questions

Keep the analysis compact enough that the user can make a decision quickly.

## Turning Analysis Into Suno Prompts

- Convert exact measurements into musical language: `92 BPM estimate` becomes `mid-tempo groove`.
- Use energy sections as arrangement guidance: `low intro -> high chorus` becomes `sparse verse, lifted chorus`.
- Use key and chord guesses only as mood hints unless confidence is high: `minor tonal center` becomes `minor-key mood`.
- Prefer the generated `suno_style_traits` and `suno_style_prompt_seed` over raw analyzer fields.
- Keep the final Style of Music field to 4-7 high-value descriptors unless the user asks for a technical prompt.