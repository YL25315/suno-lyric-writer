# Tag Combination Guide

Use this file when drawing from large tag-list material such as `Suno_音乐流派提示词.xlsx`. The spreadsheet contains hundreds of possible combinations; this guide explains how to use that kind of list without producing chaotic prompts.

## Combination Formula

Build combinations from one anchor and up to three modifiers:

`anchor genre + instrument or sound source + region/era + mood/production`

Examples:

- `acid house + TB-303 + hypnotic + club energy`
- `accordion + tango + intimate vocal + vintage room`
- `acoustic blues + glitch hop + dusty drums + late-night mood`
- `drill + sliding 808s + dark synths + tense vocal`

## Anchors

Pick one anchor genre first:

- pop, rock, hip-hop, trap, drill, house, techno, trance, ambient
- jazz, blues, soul, funk, R&B, reggae, country, folk
- metal, punk, grunge, shoegaze, dream pop
- cinematic, orchestral, trailer, anime, K-pop, J-pop

## Modifier Types

Instrument or sound source:

- accordion, acoustic guitar, banjo, brass, piano, Rhodes, strings
- 808 bass, TB-303, analog synths, drum machine, live drums
- choir, group vocals, spoken narration, robotic voice

Region or tradition:

- Celtic, African folk, Afrobeat, Hawaiian, tango, mariachi
- Chicago blues, Delta blues, Motown, roots reggae
- Carnatic, Bollywood, Latin pop, flamenco

Era or texture:

- 16-bit, 80s, vintage, modern, lo-fi, glossy, analog, cyberpunk
- dusty vinyl, bitcrushed, distorted, clean, cinematic, cathedral reverb

Mood or energy:

- dark, bright, tense, euphoric, reflective, intimate, aggressive
- meditative, nostalgic, playful, heroic, nocturnal, gritty

## Good Combinations

- `acoustic blues glitch hop`: use when the user wants rootsy guitar plus electronic broken-beat texture.
- `acid house boom bap`: useful for experimental rap over squelchy club bass.
- `accordion tango`: useful for theatrical, intimate, European or Latin dance color.
- `ambient techno`: useful for hypnotic electronic music without a hard pop hook.
- `afro trap`: useful for syncopated percussion and modern 808 bounce.
- `city pop funk`: useful for nostalgic, polished, bright bass-and-brass songs.
- `dream pop shoegaze`: useful for hazy guitar textures and soft vocals.
- `industrial metal`: useful for mechanical aggression and cold distorted texture.

## Bad Combinations To Avoid

- More than three anchor genres in one prompt.
- Contradictory vocal identities, such as `whispered screamed choir lead`.
- Exact BPM plus unrelated tempo adjectives, such as `slow ballad, 180 BPM`.
- Adding many regional tags as decoration without audible instrument or rhythm choices.
- Combining aggressive genres with soft production notes unless the contrast is intentional.

## Search Strategy

When the user asks for a niche style:

1. Identify the anchor genre.
2. Add one instrument or production modifier.
3. Add one mood or era modifier.
4. Turn the result into a natural Suno phrase.

Example:

User: "想要手风琴、有点赛博、但还是流行副歌"

Style phrase:

`cyberpunk pop, accordion hook, glossy synth bass, tight electronic drums, bright Mandarin vocal, wide catchy chorus`

## Use With Existing References

- Use `genre-prompt-library.md` for polished genre stems.
- Use `rap-rock-style-map.md` for rap, rock, punk, and metal hybrids.
- Use `suno-tag-vocabulary.md` for bracketed arrangement tags and vocal effects.
