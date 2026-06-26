# Suno Lyric Writer

Suno Lyric Writer is a Codex skill for turning song ideas, lyrics, and reference audio or video into Suno-ready song packages. It writes original lyrics, extracts usable style traits from references, and produces copy-paste fields for Suno Custom Mode.

## What It Does

- Writes original lyrics with clear section tags such as `[Verse 1]`, `[Chorus]`, `[Bridge]`, and `[End]`.
- Builds focused Suno `Style of Music` prompts instead of long, conflicting genre lists.
- Suggests `Exclude Styles`, `Weirdness`, `Style Influence`, `Audio Influence`, vocal notes, persona notes, and production tips.
- Analyzes reference audio, video, lyrics, subtitles, or transcripts for reusable creative traits.
- Performs deeper local audio analysis for BPM candidates, groove density, energy sections, texture, and optional key/chord hints.
- Includes curated genre prompts, Suno tags, vocal effects, rap/rock style maps, and tag-combination guidance.
- Offers 2-3 creative directions, then turns feedback into a finished Suno prompt and lyric package.
- Supports Chinese lyric writing and revision with natural Mandarin phrasing, compact singable lines, hook checks, and anti-cliche passes.
- Keeps copyrighted references safe by borrowing traits, not melody, lyrics, or named-artist identity.

## Skill Layout

```text
suno-lyric-writer/
  SKILL.md
  agents/openai.yaml
  references/
    quality-review.md
    chinese-lyric-craft.md
    genre-prompt-library.md
    rap-rock-style-map.md
    reference-media.md
    songwriting-craft.md
    style-parameters.md
    suno-formatting.md
    suno-tag-vocabulary.md
    tag-combination-guide.md
  scripts/
    build_suno_prompt.py
    deep_audio_analyze.py
    media_reference_probe.py
```

## Typical Workflow

1. Give the skill a song idea, reference file, lyric draft, or mood.
2. The skill extracts the creative brief: theme, style, vocal identity, structure, and Suno constraints.
3. If reference media is provided, it summarizes genre, groove, instrumentation, vocal tone, production texture, lyric mechanics, and energy arc.
4. It proposes creative directions and waits for feedback when the direction is not obvious.
5. It writes a Suno-ready package with title, style prompt, lyrics, exclusions, parameters, and iteration notes.

## Example Request

```text
Use $suno-lyric-writer. I want a Mandarin indie-pop song for Suno.
Theme: leaving a city but not a person.
Reference: use this audio for mood and arrangement pacing, but do not copy melody or lyrics.
Vocal: warm female alto.
```

## Example Output Shape

```markdown
Reference Analysis:

Title:

Style of Music:

Lyrics:

Exclude Styles:

Parameters:
- Model:
- Weirdness:
- Style Influence:
- Audio Influence:
- Vocal:
- Persona:

Production Tips:

Iteration Notes:
```

## Scripts

`scripts/build_suno_prompt.py` packages finished lyrics and style choices into a Markdown or JSON Suno bundle.

```powershell
python .\suno-lyric-writer\scripts\build_suno_prompt.py `
  --title "Morning Breaks" `
  --style "Warm alto vocal, synth-pop, hopeful mid-tempo, analog pads and tight drums, polished modern mix" `
  --exclude "muddy mix, harsh autotune" `
  --weirdness 45 `
  --style-influence 72 `
  --lyrics-file lyrics.txt
```

For Chinese lyrics, use a UTF-8 lyric file instead of piping text through PowerShell:

```powershell
python .\suno-lyric-writer\scripts\build_suno_prompt.py `
  --title "别回头" `
  --style "Mandarin indie pop, warm male vocal, mid-tempo, clean guitars and soft synth pads, bittersweet city-night mood" `
  --lyrics-file .\lyrics-zh.txt
```

`scripts/media_reference_probe.py` uses `ffprobe` and `ffmpeg` to inspect local audio/video and optionally extract 16 kHz mono WAV for transcription or additional analysis.

```powershell
python .\suno-lyric-writer\scripts\media_reference_probe.py .\reference.mp4 --extract-audio reference.wav
```

`scripts/deep_audio_analyze.py` estimates tempo candidates, onset density, energy sections, dynamics, brightness, and Suno-ready style traits. It works with `ffmpeg` only; installing `librosa`, `numpy`, `scipy`, and `soundfile` adds optional key and rough chord analysis.

```powershell
python .\suno-lyric-writer\scripts\deep_audio_analyze.py `
  "C:\Users\21905\Downloads\reference.mp3" `
  --out reference-analysis.md
```

## Design Principles

- Traits over copying: extract style, structure, mood, and production cues, not protected lyrics or melodies.
- Fewer stronger descriptors: most style prompts should use 4-7 high-value descriptors.
- Separate fields: lyrics go in Lyrics, production and genre go in Style of Music, unwanted traits go in Exclude Styles.
- Feedback-first iteration: change one or two controls at a time after hearing Suno output.
- Upload safety: any automated Suno submission must be explicitly approved because it can consume credits.

## Validation

The skill validates with the Codex skill validator:

```text
Skill is valid!
```

The helper scripts have also been smoke-tested for Markdown output, JSON output, media probing, and audio extraction.