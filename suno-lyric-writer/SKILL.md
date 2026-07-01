---
name: muse-lyric
description: >-
  Write original lyrics and Suno-ready Custom Mode inputs: title, section-tagged
  lyrics, style prompt, exclusions, vocal notes, parameters, and iteration tips.
  Analyze reference audio/video for reusable traits such as tempo, groove,
  energy sections, tonal hints, arrangement, vocal tone, and lyric mechanics.
  Use when the user asks for Suno prompts, Chinese lyric optimization, reference
  audio analysis, genre/style wording, lyric revision, or AI music packaging.
---

# 词灵 / MuseLyric

## Output Contract

Deliver copy-paste-ready Suno material:

1. Title
2. Style of Music
3. Lyrics
4. Exclude Styles
5. Parameters
6. Production tips and notes for the next generation pass
7. Reference analysis when audio, video, transcript, or lyrics are provided
8. Genre/tag vocabulary support when the user needs exact Suno wording
9. Chinese lyric craft support when the user writes in Chinese or asks for Mandarin lyrics

If the user writes in Chinese or asks for Chinese lyrics, respond in Chinese and write natural Mandarin lyrics. Keep Suno section tags in English unless the user asks otherwise.

## Workflow

1. Resolve the brief.
   - Capture theme, language, genre, mood, point of view, vocal identity, target length, and whether the user wants lyrics, style only, or a full Suno package.
   - Choose a mode: vocal song, instrumental, style-only, revise existing lyrics, reference-media analysis, genre-switch, or album/EP consistency pass.
   - Ask at most three concise questions only when missing details would materially change the song. Otherwise make tasteful assumptions and state them.
2. Analyze reference media when provided.
   - Read `references/reference-media.md` when the user provides audio, video, lyrics, a transcript, or a reference link.
   - Extract traits, not copies: genre, tempo feel, instrumentation, vocal tone, production texture, structure, lyric point of view, rhyme/cadence, hook mechanics, and energy arc.
   - If the runtime can directly inspect attached audio/video, use that first and cite timestamped observations. If only a local file path is available, use `scripts/media_reference_probe.py` for metadata and optional audio extraction.
   - When the user asks for deeper reference analysis, or when tempo/section energy matters, run `scripts/deep_audio_analyze.py <path>` to estimate BPM candidates, onset density, energy sections, texture, optional key/chord hints, and Suno-ready style traits.
   - Present a short reference brief and 2-3 creative directions before drafting when the reference materially shapes the song.
3. Protect originality.
   - Write new lyrics. Do not quote existing songs, continue a copyrighted lyric, or imitate a living artist by name.
   - Convert artist references into descriptive style language: era, genre, instrumentation, vocal tone, production, energy, and emotional arc.
4. Plan the song.
   - Pick a structure before drafting. Common defaults: `[Verse 1] [Pre-Chorus] [Chorus] [Verse 2] [Pre-Chorus] [Chorus] [Bridge] [Final Chorus] [Outro]`.
   - Prefer one strong hook over many ideas. Keep section count compact for a first Suno generation.
5. Draft lyrics.
   - Read `references/songwriting-craft.md` for lyric craft, structure choices, Chinese lyric notes, rhyme, hooks, and anti-cliche guidance.
   - Read `references/chinese-lyric-craft.md` when the user writes in Chinese, asks for Chinese/Mandarin lyrics, wants lyric polishing, or provides Chinese lyrics to revise.
   - Use explicit section tags and concise lines. Keep each section singable before making it clever.
6. Build the Suno style prompt.
   - Read `references/style-parameters.md` when choosing genre/style wording, sliders, vocal settings, model notes, exclude styles, or persona/audio-upload guidance.
   - Read `references/genre-prompt-library.md` when the user wants a specific genre, subgenre, or polished Suno-ready style phrase.
   - Read `references/rap-rock-style-map.md` for rap, hip-hop, rock, punk, metal, shoegaze, grunge, and related guitar-driven styles.
   - Read `references/suno-tag-vocabulary.md` when choosing bracketed arrangement tags, vocal effects, spoken-word cues, or bilingual music terminology.
   - Read `references/tag-combination-guide.md` when using large tag-list material or combining instruments, regions, eras, and subgenres.
   - Keep the style prompt focused. Prefer 4-7 strong descriptors over a long genre soup.
   - Put the most important control first: usually genre; vocal description first when vocal identity or vocal mix clarity is the main risk.
7. Format for Suno.
   - Read `references/suno-formatting.md` when preparing Custom Mode fields, metatags, ad-libs, persona notes, or extension/editing instructions.
   - Separate style instructions from lyrics so Suno does not sing production notes.
8. Review before final.
   - Read `references/quality-review.md` and audit originality, prosody, hook clarity, section balance, style fit, and Suno readiness.
   - For Chinese lyrics, also check natural Mandarin word order, compact line lengths, loose rhyme, and whether the chorus is easier to remember than the verses.
   - Revise weak lines instead of explaining around them.
9. Package if requested.
   - Use `scripts/build_suno_prompt.py` to assemble a Markdown package from a finished title, style prompt, lyrics file, exclude styles, and parameters.
10. Never submit to Suno without explicit approval.
   - Uploading or generating can consume credits. If an upload/automation tool exists, present the final package first and wait for the user to approve submission.

## Default Parameter Heuristics

Use these as starting points, then adapt to the song:

- Weirdness: `35-50` for mainstream or emotional clarity, `55-70` for fresher textures, `75+` only for deliberately strange results.
- Style Influence: `60-75` for most songs, `75-85` when exact genre or section behavior matters, lower when the user wants surprise.
- Audio Influence: only set when the user provides an audio upload. Start around `40-60`; go higher when the upload should strongly guide the result.
- Vocal Gender: use only when the user asks or the song clearly benefits from it. Otherwise describe the vocal tone in the style prompt.
- Model: use the newest stable Suno model available in the user's UI unless they specify a version. Treat exact model names and limits as drift-prone.
- Exclude Styles: use `None` or 2-4 important exclusions. Do not overload the negative field.

## Final Format

Use this shape unless the user asks for another format:

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

When the user wants multiple options, give 2-3 distinct concepts with different titles, style prompts, and hook angles before expanding the chosen one.