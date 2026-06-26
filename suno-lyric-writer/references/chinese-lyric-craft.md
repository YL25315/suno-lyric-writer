# Chinese Lyric Craft Reference

Use this file when writing, revising, localizing, or polishing Mandarin Chinese lyrics for Suno.

## Goals

- Write lyrics that sound born in Chinese, not translated from English.
- Keep the language singable first, literary second.
- Preserve the user's intent, speaker, and emotional temperature during revision.
- Make each section do a job: verses reveal scenes, pre-choruses tighten pressure, choruses repeat a clear hook.

## Chinese Prosody

- Prefer compact lines. For most C-pop, ballad, indie, and rock songs, aim for 6-13 Chinese characters per sung line.
- Keep chorus lines shorter and more repeatable than verse lines. A strong hook often fits in 4-9 Chinese characters.
- For rap, allow longer lines, but place clear pauses with commas, spaces, or line breaks so the flow can breathe.
- Put important nouns and verbs near the end of a line when the melody needs lift.
- Avoid cramming too many modifiers before one noun. Chinese lyrics usually sing better with image + action.
- Read every line aloud. If it needs a rushed breath, split it or cut one image.

## Natural Mandarin

- Prefer spoken but shaped Mandarin: direct enough to sing, specific enough to remember.
- Use "我/你/他/她/我们" deliberately. If the subject changes, make the emotional camera clear.
- Let Chinese word order stay natural. Avoid English-style patterns such as "在我的心里我找到..." when a simpler Chinese sentence works.
- Use classical or poetic diction only when the genre asks for it, such as guofeng, wuxia, or cinematic ballad.
- Keep rare characters, dense idioms, and ornate four-character phrases sparse. Suno may sing them stiffly.

## Rhyme And Repetition

- Use loose rhyme families instead of forcing exact rhyme every line.
- Favor stable vowel colors in the chorus, such as `ang`, `an`, `ai`, `ao`, `ong`, or `ei`.
- Repeat one key phrase with small emotional changes rather than inventing a new slogan each time.
- Internal echoes work well in Chinese: repeated verbs, mirrored sentence shapes, or a recurring object.
- Do not sacrifice a natural phrase just to rhyme. Awkward rhyme sounds cheaper than no rhyme.

## Hook Design

- Make the title phrase singable, short, and repeatable.
- Let the chorus answer one emotional question from the verse.
- Put the strongest hook at the first or last line of the chorus.
- Use one concrete object or action as the memory anchor: a platform, raincoat, receipt, old phone, elevator, window light.
- If the song is sad, avoid explaining the sadness in the hook. Let a simple action carry it.

## Section Templates

### Mandarin Pop Or Ballad

```text
[Verse 1]
scene, time, object, quiet conflict

[Pre-Chorus]
pressure rises, the speaker nearly says the truth

[Chorus]
short hook phrase, repeatable emotional thesis

[Verse 2]
new detail, consequence, or changed distance

[Bridge]
confession, reversal, or one-line decision

[Final Chorus]
same hook with one sharper changed line
```

### Chinese Rap Or Melodic Rap

```text
[Intro]
short spoken setup or atmosphere

[Verse 1]
clear flow pocket, concrete claims, inner rhyme

[Hook]
simple repeated Mandarin phrase

[Verse 2]
denser images, stronger stance, one memorable punchline

[Bridge]
half-time, sung switch, or beat-change setup

[Final Hook]
repeat hook with ad-libs
```

### Guofeng Or Cinematic Chinese

- Use restraint. A few traditional images are stronger than a pile of antique words.
- Balance old imagery with clear modern emotion.
- Keep references understandable without footnotes.
- Prefer sensory images: sleeve, lamp, river, dust, bell, snow, ink, courtyard.

## Revision Moves

- Translationese pass: replace English-shaped sentence order with natural Mandarin.
- Singability pass: shorten lines over 13 Chinese characters unless rap flow needs them.
- Image pass: replace abstract emotion with a scene, object, or action.
- Hook pass: make the chorus simpler and more repeatable than the verses.
- Second-verse pass: add new information instead of restating verse 1.
- Rhyme pass: loosen forced rhyme, then strengthen cadence and repeated sounds.

## Common Problems To Fix

| Problem | Fix |
| --- | --- |
| Too abstract | Add time, place, object, or action. |
| Too literary | Use one poetic phrase, then return to plain speech. |
| Too translated | Rewrite the sentence from the speaker's mouth, not from the source text. |
| Too many metaphors | Keep one image family per song. |
| Chorus too clever | Make it shorter, plainer, and easier to repeat. |
| Verse 2 repeats verse 1 | Add consequence, memory, distance, or a new choice. |

## Chinese Cliche Watchlist

Do not ban these words, but avoid lazy combinations:

- 星空, 梦想, 人海, 孤单, 心碎, 温柔, 余生, 遗憾
- 黑夜, 眼泪, 远方, 等待, 拥抱, 放手, 世界
- "我在黑夜里追逐梦想"
- "你的温柔照亮我的世界"
- "在人海中寻找你的身影"
- "破碎的心还在等待"

Make them specific:

| Generic | Stronger Direction |
| --- | --- |
| 我很想你 | Show the habit that remains after the person leaves. |
| 我走在人海里 | Name the street, station, elevator, or last train. |
| 你的温柔 | Show what the person did, said, or forgot to take away. |
| 我的心碎了 | Show the speaker avoiding a place, object, or message. |

## Suno Formatting For Chinese

- Keep section tags in English: `[Verse 1]`, `[Chorus]`, `[Bridge]`, `[Outro]`, `[End]`.
- Put only sung Chinese words and useful bracket tags in the Lyrics field.
- Keep production notes in Style of Music or Production Tips, not inside lyrics.
- Use punctuation lightly. Too many commas can make phrasing choppy.
- Use short ad-libs in parentheses only when they should be sung, such as `(别回头)` or `(再一次)`.
- Add `[End]` when a clean stop matters.

## Quality Checklist

- The lyric can be read aloud without awkward breath.
- The chorus has one phrase the listener can remember after one listen.
- Verse 2 adds a new image or emotional turn.
- The rhyme feels natural in Mandarin.
- The style prompt and lyrics do not fight each other.
- No line feels like a direct translation unless the user explicitly wants translation.