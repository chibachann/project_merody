# melody-transcriber

単旋律の音声ファイル（WAV / MP3）を MIDI ファイルへ変換する Python CLI ツール。

鼻歌・歌声・単音楽器などのモノフォニック音源を入力として受け取り、ピッチ推定を経て MIDI を出力します。

## 特徴

- `librosa.pyin` による高精度な基本周波数（F0）推定
- フレーム列からノートイベントへの自動変換（短音除去・平滑化つき）
- `pretty_midi` による標準 MIDI ファイル出力
- 中間データ（F0 CSV / ノート CSV / 可視化プロット）の出力に対応

## インストール

```bash
# Python 3.9 以上が必要
python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

## 使い方

```bash
python -m melody_transcriber.main \
  --input  data/raw/sample.wav \
  --output data/output/sample.mid
```

### オプション

| フラグ | 説明 | デフォルト |
|---|---|---|
| `--input` | 入力音声ファイルパス（必須） | — |
| `--output` | 出力 MIDI ファイルパス（必須） | — |
| `--save-f0-csv` | F0 推定結果を CSV 保存 | off |
| `--save-note-csv` | ノートイベントを CSV 保存 | off |
| `--plot` | 波形・F0・ノートの可視化を保存 | off |
| `--tempo BPM` | テンポ（BPM） | 120 |
| `--min-note-duration SEC` | 最小音符長（秒） | 0.05 |
| `--fmin HZ` | ピッチ検出の最低周波数 | 65.0（C2） |
| `--fmax HZ` | ピッチ検出の最高周波数 | 2093.0（C7） |

### 実行例（中間データも全出力）

```bash
python -m melody_transcriber.main \
  --input data/raw/sample.wav \
  --output data/output/sample.mid \
  --save-f0-csv --save-note-csv --plot --tempo 100
```

中間ファイルは `data/interim/` に保存されます。

## プロジェクト構成

```
melody-transcriber/
├── src/melody_transcriber/
│   ├── main.py              # CLI エントリポイント
│   ├── config.py            # パラメータ設定
│   ├── logger.py            # ロガー
│   ├── pipeline/
│   │   └── transcribe.py    # パイプライン全体の制御
│   ├── audio/
│   │   ├── loader.py        # 音声読込（モノラル化・リサンプリング）
│   │   └── preprocess.py    # ピーク正規化
│   ├── pitch/
│   │   ├── estimator.py     # pyin による F0 推定・CSV 出力
│   │   └── smoothing.py     # メジアンフィルタによる平滑化
│   ├── notes/
│   │   ├── segmenter.py     # フレーム列→ノートイベント変換
│   │   └── quantizer.py     # リズムグリッドへの量子化
│   ├── midi/
│   │   └── writer.py        # MIDI ファイル生成
│   ├── visualization/
│   │   └── plotter.py       # 波形・F0・ノートのプロット
│   └── models/
│       ├── frame_pitch.py   # FramePitch データクラス
│       └── note_event.py    # NoteEvent データクラス
├── tests/                   # pytest テスト
├── data/
│   ├── raw/                 # 入力音源（編集しない）
│   ├── interim/             # 中間ファイル（CSV・プロット）
│   └── output/              # 出力 MIDI
└── pyproject.toml
```

## 処理パイプライン

```
音声ファイル
  → [1] 読込・正規化      audio/loader.py + preprocess.py
  → [2] F0 推定           pitch/estimator.py  (librosa.pyin)
  → [3] ピッチ平滑化      pitch/smoothing.py  (メジアンフィルタ)
  → [4] ノート分割        notes/segmenter.py
  → [5] MIDI 出力         midi/writer.py      (pretty_midi)
  → [6] 可視化（任意）    visualization/plotter.py
```

## テスト

```bash
# 全テスト実行
pytest

# ファイル指定
pytest tests/test_segmenter.py

# テスト関数指定
pytest tests/test_segmenter.py::test_segment_notes_basic_two_notes
```

## 依存ライブラリ

| ライブラリ | 用途 |
|---|---|
| `librosa` | 音声読込・F0 推定（pyin） |
| `pretty_midi` | MIDI ファイル生成 |
| `matplotlib` | 可視化 |
| `numpy` | 数値処理 |
| `soundfile` | WAV 読み書き |

## スコープ

**対象:** 単旋律音源（鼻歌・歌声・単音楽器）
**非対象:** 和音・複数楽器同時採譜・ドラム・浄書品質の譜面生成

## 今後の予定

- Phase 7: 精度改善（onset 検出・平滑化改善・Basic Pitch 比較）
- Phase 8: 譜面化（テンポ推定・拍位置推定・`music21` 連携）
