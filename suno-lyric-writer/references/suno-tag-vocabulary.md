# Suno Tag Vocabulary

Use this file when choosing bracketed arrangement tags, vocal effects, spoken-word cues, or bilingual music terminology. It is curated from the user's `suno提示音乐术语中英文对照表.txt` and tightened for Suno use.

## Arrangement Tags

Use these inside the Lyrics field only when they guide section structure:

| Tag | Meaning | Use |
| --- | --- | --- |
| `[intro]` | 前奏 | Start texture, motif, or spoken setup |
| `[verse]` | 主歌 | Story/detail section |
| `[pre-chorus]` | 预副歌 | Tension before chorus |
| `[chorus]` | 副歌 | Main hook |
| `[post-chorus]` | 后副歌 | Repeated chant or instrumental hook after chorus |
| `[bridge]` | 过渡段 | New angle, harmony, or lyrical turn |
| `[interlude]` | 间奏 | Short instrumental or atmospheric break |
| `[solo]` | 独奏 | Instrumental feature |
| `[guitar riff]` | 吉他重复段 | Guitar motif cue |
| `[outro]` | 尾奏 | Ending section |
| `[end]` | 结束 | Clean stop |
| `[fade out]` | 渐弱结束 | Trailing ending |

Use title case (`[Chorus]`) or lower case consistently. Keep tags sparse.

## Musical Terms For Style Prompts

Use these in `Style of Music`, not inside sung lyrics:

- melody: 旋律
- harmony: 和声
- rhythm: 节奏
- tempo: 速度
- beat: 拍子
- bassline: 低音线
- chord progression: 和弦进行
- hook: 钩子, memorable refrain
- accompaniment: 伴奏
- modulation: 转调
- dynamics: 力度
- syncopation: 切分音
- improvisation: 即兴演奏
- key signature: 调号
- time signature: 拍号
- scale: 音阶
- arpeggio: 琶音
- motif: 动机
- crescendo: 渐强
- diminuendo: 渐弱

## Vocal Effects

Use vocal effects carefully. Too many can make the generation unstable.

| Cue | Chinese | Best Use |
| --- | --- | --- |
| reverb | 混响 | Spacious or cinematic vocal |
| delay | 延迟 | Echoed phrase or dream texture |
| echo | 回声 | Sparse call into space |
| auto-tune | 自动调音 | Modern pop, trap, hyperpop |
| vibrato | 颤音 | Soul, ballad, opera, expressive styles |
| pitch shift | 音高变化 | Hyperpop, experimental, character voice |
| harmonizer | 和声器 | Layered hook or robotic harmony |
| distortion | 失真 | Rock, industrial, aggressive vocals |
| compression | 压缩 | Upfront polished vocal |
| de-esser | 去齿音 | Production note, usually not needed in prompt |
| flanger | 镶边效果 | Psychedelic or 80s vocal color |
| phaser | 移相效果 | Psychedelic movement |
| doubling | 加倍效果 | Wider chorus vocal |
| megaphone effect | 扩音器效果 | Punk, indie, broadcast voice |
| robotic voice | 机器人声音 | Cyberpunk, electro, AI character |
| reverse reverb | 反向混响 | Ghostly lead-in |
| vocal fry | 低喉音 | Intimate or gritty vocal detail |
| growl | 咆哮 | Metal, aggressive vocal |
| scream | 尖叫 | Hardcore, metalcore, punk |
| whisper | 耳语 | Intimate, eerie, ASMR-like sections |
| falsetto | 假声 | R&B, pop, airy chorus |
| head voice | 头声 | Light high register |
| chest voice | 胸声 | Strong grounded vocal |
| belting | 强唱 | Broadway, pop climax, power ballad |
| overdrive | 过载 | Rock vocal grit |
| formant shift | 共振峰变化 | Character voice, experimental pop |
| gating | 噪声门 | Chopped vocal effect |

## Spoken Cues

Use these for intros, bridges, and narrative moments:

- narration: 叙述
- dialogue: 对话
- monologue: 独白
- voice-over: 画外音
- intonation: 语调
- diction: 发音
- accent: 口音
- inflection: 语调变化
- articulation: 发音清晰度
- projection: 声音投射
- pause: 停顿
- emphasis: 强调
- cadence: 抑扬顿挫
- tone: 音调
- pitch: 音高
- pace: 速度

## Practical Rules

- Put section tags on their own lines.
- Parentheses are usually sung; do not put production directions in parentheses.
- Put vocal effects in `Style of Music` unless a local section cue is needed.
- Use no more than 1-3 performance cues per section.
- Prefer descriptive language over obscure technical terms unless the user wants precision.
