# 词灵 / MuseLyric

词灵（MuseLyric）是一个 Codex skill，用来把歌曲想法、歌词草稿、参考音频或视频整理成 Suno Custom Mode 可直接使用的创作包。它会写原创歌词，提取参考素材里的可复用风格特征，并输出标题、歌词、Style of Music、Exclude Styles、参数建议和迭代提示。

> 安装注意：本仓库根目录不是 skill 根目录。真正的 skill 在 `suno-lyric-writer/` 子目录下。

## 能做什么

- 写中文/英文原创歌词，并使用 `[Verse 1]`、`[Chorus]`、`[Bridge]`、`[End]` 等 Suno 友好的段落标签。
- 优化中文歌词，让它更像自然普通话歌词，而不是翻译腔。
- 生成聚焦的 `Style of Music`，避免堆太多互相冲突的曲风词。
- 分析参考音频、视频、歌词、字幕或转写文本，提取可借鉴的风格特征。
- 做深度本地音频分析：BPM 候选、groove 密度、能量段落、质感、可选调性/粗略和弦。
- 给出 `Exclude Styles`、`Weirdness`、`Style Influence`、`Audio Influence`、vocal/persona 建议。
- 从参考素材中借"特征"，不复制旋律、歌词或特定艺人身份。

## 目录结构

```text
.
  README.md
  pyproject.toml
  requirements.txt
  requirements-dev.txt
  LICENSE
  suno-lyric-writer/        # skill 根目录
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
      build_suno_prompt.py
      media_reference_probe.py
      deep_audio_analyze.py
  tests/
  .github/workflows/ci.yml
```

## 安装依赖

Python 依赖：

```powershell
py -3.14 -m pip install -r requirements.txt
```

开发和测试依赖：

```powershell
py -3.14 -m pip install -r requirements-dev.txt
```

如果你的 `python` 命令正常指向目标解释器，也可以把下面所有 `py -3.14` 换成 `python`。在 Windows 上如果 `python` 命中了 WindowsApps 的 Store shim，优先使用 `py -3.14`。

外部命令依赖：

- `ffmpeg`
- `ffprobe`

`media_reference_probe.py` 和 `deep_audio_analyze.py` 需要能在 PATH 中找到这两个命令。深度音频分析在没有 `librosa/numpy/scipy/soundfile` 时仍可用 `ffmpeg-only` 模式运行；安装 `requirements.txt` 后会启用调性和粗略和弦分析。

当前测试过的核心版本：

- Python 3.14.4
- librosa 0.11.0
- numpy 2.4.6
- scipy 1.18.0
- soundfile 0.14.0

## 安装 Skill

把 `suno-lyric-writer/` 这个子目录安装或复制到你的 Codex skills 目录。不要只指向仓库根目录。

示例：

```powershell
Copy-Item .\suno-lyric-writer "$env:USERPROFILE\.codex\skills\" -Recurse -Force
```

使用时可以这样说：

```text
Use $muse-lyric. 写一首中文 indie pop，主题是离开城市但不是离开那个人。
```

## 常用脚本

打包 Suno 提示词：

```powershell
py -3.14 .\suno-lyric-writer\scripts\build_suno_prompt.py `
  --title "别回头" `
  --style "Mandarin indie pop, warm male vocal, mid-tempo, clean guitars and soft synth pads, bittersweet city-night mood" `
  --lyrics-file .\lyrics-zh.txt
```

中文歌词建议用 UTF-8 文件传入，不建议在 PowerShell 里直接管道输入中文文本。

探测参考媒体：

```powershell
py -3.14 .\suno-lyric-writer\scripts\media_reference_probe.py `
  "C:\Users\21905\Downloads\reference.mp3"
```

抽取适合转写/分析的 16 kHz 单声道 WAV：

```powershell
py -3.14 .\suno-lyric-writer\scripts\media_reference_probe.py `
  "C:\Users\21905\Downloads\reference.mp4" `
  --extract-audio reference.wav `
  --start 30 `
  --duration 60
```

`--start` 和 `--duration` 在这个脚本里只作用于 `--extract-audio`，metadata probe 会读取整个文件。

深度音频分析：

```powershell
py -3.14 .\suno-lyric-writer\scripts\deep_audio_analyze.py `
  "C:\Users\21905\Downloads\reference.mp3" `
  --out reference-analysis.md
```

`deep_audio_analyze.py` 默认最多解码 600 秒音频到内存中。长音频请用 `--duration` 或调整 `--max-duration`。

## 验证

语法检查：

```powershell
py -3.14 -m py_compile `
  .\suno-lyric-writer\scripts\build_suno_prompt.py `
  .\suno-lyric-writer\scripts\media_reference_probe.py `
  .\suno-lyric-writer\scripts\deep_audio_analyze.py
```

测试：

```powershell
py -3.14 -m ruff check .
py -3.14 -m pytest --cov=suno-lyric-writer/scripts --cov-report=term-missing -q
```

Codex skill validator：

```powershell
py -3.14 C:\Users\21905\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\suno-lyric-writer
```

如果缺少 `yaml`：

```powershell
py -3.14 -m pip install PyYAML
```

## English Summary

词灵（MuseLyric）is a Codex skill for turning song ideas, lyrics, and reference audio/video into Suno-ready Custom Mode packages. It writes original lyrics, analyzes reusable musical traits, builds focused style prompts, and suggests parameters for iteration.

The skill root is the `suno-lyric-writer/` subdirectory, not the repository root.

Core scripts:

- `build_suno_prompt.py`: package finished lyrics and style choices.
- `media_reference_probe.py`: inspect local media and optionally extract WAV audio.
- `deep_audio_analyze.py`: estimate BPM, groove density, energy sections, texture, optional key/chord hints, and Suno style traits.
