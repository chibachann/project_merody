# メロディ採譜ソフト 開発計画書

## 1. 目的

音楽ファイルを入力として受け取り、まずは**単旋律メロディを抽出して MIDI 化する**ソフトを開発する。

初期段階では以下をスコープとする。

- 入力: wav / mp3 などの音声ファイル
- 出力: メロディ 1 本の MIDI ファイル
- 対象: 鼻歌、歌、単音楽器などの**単旋律音源**
- 非対象: 和音、複数楽器同時採譜、ドラム採譜、完全な浄書品質の譜面生成

本プロジェクトでは、まず **「動く最小構成」→「精度改善」→「譜面化」** の順で進める。

---

## 2. 開発方針

### 2.1 基本方針

最初から高機能化しない。以下の順で段階的に実装する。

1. 音声を読み込めるようにする
2. フレーム単位で基本周波数（F0）を推定する
3. 連続した F0 から音符区間を作る
4. MIDI に出力する
5. 精度検証しやすいようにログ・可視化を整備する
6. 必要に応じてテンポ推定・量子化・譜面化に進む

### 2.2 最初の成功条件

以下を満たせば MVP とみなす。

- 単旋律 wav を入力できる
- メロディを MIDI として出力できる
- 出力 MIDI を DAW や MIDI プレイヤーで再生すると、おおよそ元メロディとして認識できる

### 2.3 初期技術方針

初期実装では Python を用いる。

- 音声読み込み・前処理: `librosa`
- ピッチ推定: `librosa.pyin`
- MIDI 出力: `pretty_midi`
- 将来的な譜面処理候補: `music21`
- 可視化: `matplotlib`
- テスト: `pytest`

理由:

- 音声処理ライブラリが揃っている
- 試作速度が速い
- 後からアルゴリズムの差し替えがしやすい

---

## 3. 実装順序

## 3.1 Phase 1: プロジェクト土台構築

### 目的
開発しやすい最小構成を整える。

### 実装内容

- Python プロジェクト作成
- 仮想環境構築
- 依存パッケージ管理
- ディレクトリ構成作成
- CLI の入口を作成
- サンプル音源配置ルールを決める

### 完了条件

- `python -m app.main --help` が動く
- サンプル音源を指定して実行できる枠だけある

---

## 3.2 Phase 2: 音声入力と前処理

### 目的
音源を安定して処理できる状態にする。

### 実装内容

- 音声ファイル読み込み
- モノラル化
- サンプリングレート統一
- 音量正規化
- 必要に応じた無音除去
- 入力メタ情報の取得

### 完了条件

- 対象ファイルを読み込み、長さ・サンプリング周波数・波形サイズをログ出力できる
- 不正ファイル時に明確なエラーを返せる

---

## 3.3 Phase 3: ピッチ推定

### 目的
時間ごとのメロディ候補を得る。

### 実装内容

- `librosa.pyin` による F0 推定
- voiced / unvoiced 判定取得
- フレーム列データとして保存
- デバッグ用 CSV 出力

### 保存したい情報

- 時刻
- 周波数
- MIDI ノート番号換算値
- voiced フラグ
- 信頼度が取れる場合は信頼度

### 完了条件

- フレームごとの F0 推定結果を CSV で確認できる
- 単純な音源でおおよその高さが追えている

---

## 3.4 Phase 4: ノート区間生成

### 目的
フレーム列を音符列に変換する。

### 実装内容

- 無声音を休符扱いにする
- 近い音高の連続区間を 1 音としてまとめる
- 短すぎる区間を除去する
- ビブラート等の揺れを平滑化する
- 音高を MIDI ノート番号へ丸める

### 最初に入れるルール

- 最小音長しきい値を設定する
- 一定フレーム数未満の変動はノイズとみなす
- 半音未満の微小揺れは同一音とみなす

### 完了条件

- `start_time, end_time, midi_note` のノート列が作れる
- 人が見て理解できる単純なノート列になる

---

## 3.5 Phase 5: MIDI 出力

### 目的
ノート列を標準的な MIDI として保存する。

### 実装内容

- `pretty_midi` による MIDI ファイル生成
- テンポは初期版では固定値でも可
- velocity は固定値でも可
- Instrument はメロディ用に 1 本だけ生成

### 完了条件

- `.mid` ファイルが出力される
- 外部ツールで再生確認できる

---

## 3.6 Phase 6: 検証・可視化

### 目的
精度改善のための観測基盤を作る。

### 実装内容

- 波形表示
- 推定 F0 の折れ線可視化
- ノート区間の可視化
- 入力音源と出力ノート数の比較ログ
- テスト用サンプル音源セット整備

### 完了条件

- どこで失敗しているかを目視で追える

---

## 3.7 Phase 7: 精度改善

### 候補

- ノート境界判定改善
- onset 検出の導入
- 平滑化アルゴリズム改善
- Basic Pitch との比較
- 前処理改善
- 入力音源の条件別チューニング

---

## 3.8 Phase 8: 譜面化

### 目的
MIDI だけでなく譜面に近い表現へ進める。

### 実装内容

- テンポ推定
- 拍位置推定
- 音価の量子化
- 小節線処理
- `music21` 等による譜面データ生成

### 注意

ここは別フェーズとして扱う。MIDI が安定する前に手を出さない。

---

## 4. 推奨ディレクトリ構成

```text
melody-transcriber/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .env.example
├── docs/
│   ├── architecture.md
│   ├── development-rules.md
│   ├── roadmap.md
│   └── experiment-notes.md
├── data/
│   ├── raw/
│   │   └── sample_melody.wav
│   ├── interim/
│   │   └── sample_melody_f0.csv
│   └── output/
│       └── sample_melody.mid
├── scripts/
│   ├── run_sample.sh
│   └── inspect_csv.py
├── src/
│   └── melody_transcriber/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── logger.py
│       ├── pipeline/
│       │   ├── __init__.py
│       │   └── transcribe.py
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── loader.py
│       │   └── preprocess.py
│       ├── pitch/
│       │   ├── __init__.py
│       │   ├── estimator.py
│       │   └── smoothing.py
│       ├── notes/
│       │   ├── __init__.py
│       │   ├── segmenter.py
│       │   └── quantizer.py
│       ├── midi/
│       │   ├── __init__.py
│       │   └── writer.py
│       ├── visualization/
│       │   ├── __init__.py
│       │   └── plotter.py
│       └── models/
│           ├── __init__.py
│           ├── frame_pitch.py
│           └── note_event.py
├── tests/
│   ├── test_loader.py
│   ├── test_estimator.py
│   ├── test_segmenter.py
│   └── test_writer.py
└── notebooks/
    └── analysis.ipynb
```

---

## 5. 各ディレクトリの役割

### `docs/`
仕様、設計、ルール、検証メモを置く。

### `data/raw/`
元音源を置く。編集しない。

### `data/interim/`
F0 推定結果や中間 CSV を置く。

### `data/output/`
MIDI や将来的な譜面出力を置く。

### `scripts/`
補助スクリプトを置く。本体ロジックは置かない。

### `src/melody_transcriber/audio/`
音声読み込みと前処理。

### `src/melody_transcriber/pitch/`
ピッチ推定と平滑化。

### `src/melody_transcriber/notes/`
フレーム列を音符列にする処理。

### `src/melody_transcriber/midi/`
MIDI 出力。

### `src/melody_transcriber/models/`
データ構造定義。

### `tests/`
単体テスト。

### `notebooks/`
実験・検証用。検証後にロジックは `src/` へ戻す。

---

## 6. プロジェクト内ルール

## 6.1 設計ルール

### ルール1: 1 モジュール 1 役割

- `loader.py` は読み込みだけ
- `estimator.py` は F0 推定だけ
- `writer.py` は MIDI 出力だけ

責務を混ぜない。

### ルール2: パイプラインとロジックを分離する

`main.py` や `pipeline/transcribe.py` は処理の流れだけを担当し、個別アルゴリズムは各モジュールへ分離する。

### ルール3: 中間データを捨てない

初期段階では特に、以下を保存する。

- 前処理後音声情報
- F0 推定 CSV
- ノート列 CSV
- 出力 MIDI

ブラックボックス化を防ぐ。

### ルール4: 実験コードを本番コードに混ぜない

試行錯誤は `notebooks/` や `scripts/` で行い、採用した処理だけ `src/` に戻す。

---

## 6.2 命名ルール

### Python ファイル

- 小文字 + スネークケース
- 例: `note_event.py`, `pitch_estimator.py`

### クラス名

- パスカルケース
- 例: `FramePitch`, `NoteEvent`

### 関数名

- 動詞始まり
- 例: `load_audio`, `estimate_pitch`, `write_midi`

### 変数名

- 単位や意味を含める
- 例: `start_time_sec`, `sample_rate`, `midi_note_number`

---

## 6.3 データ構造ルール

中間データはできるだけ明示的な構造で持つ。

### `FramePitch` の例

- `time_sec`
- `frequency_hz`
- `midi_note`
- `is_voiced`

### `NoteEvent` の例

- `start_time_sec`
- `end_time_sec`
- `midi_note`
- `velocity`

辞書の多用を避け、型のある構造を優先する。

---

## 6.4 ログルール

以下は最低限ログに残す。

- 入力ファイル名
- サンプリング周波数
- 音声長
- F0 推定フレーム数
- 抽出ノート数
- 出力 MIDI パス
- 警告: 無音が多い、推定不能区間が多い等

---

## 6.5 テストルール

### 初期テスト対象

- 音声ファイル読み込み
- F0 推定関数の出力形式
- ノート分割ロジック
- MIDI 出力でファイル生成されること

### ポイント

音声系は完全一致ではなく、以下のような性質を検証する。

- 空でないこと
- 時系列が昇順であること
- 異常値が少ないこと
- 期待したノート数に近いこと

---

## 6.6 Git 運用ルール

### ブランチ方針

- `main`: 安定版
- `develop`: 開発統合
- `feature/*`: 個別機能

例:

- `feature/audio-loader`
- `feature/f0-estimator`
- `feature/midi-writer`

### コミット方針

1 コミット 1 意図を基本とする。

例:

- `feat: add wav loader`
- `feat: implement pyin pitch estimation`
- `fix: correct note segmentation threshold`
- `test: add midi writer tests`
- `docs: update architecture notes`

---

## 7. 最初に作る CLI 仕様

```bash
python -m melody_transcriber.main \
  --input data/raw/sample_melody.wav \
  --output data/output/sample_melody.mid
```

### 将来的なオプション候補

- `--save-f0-csv`
- `--save-note-csv`
- `--plot`
- `--tempo`
- `--min-note-duration`
- `--fmin`
- `--fmax`

---

## 8. 最初のマイルストーン

## Milestone 1

### 目標
音声読込から F0 推定 CSV 出力まで。

### 成果物

- wav 読み込み
- `pyin` 実行
- CSV 保存

---

## Milestone 2

### 目標
F0 からノート列を作る。

### 成果物

- ノート統合ロジック
- ノート CSV 保存

---

## Milestone 3

### 目標
MIDI を出力して再生確認する。

### 成果物

- MIDI writer
- CLI 一発実行

---

## Milestone 4

### 目標
可視化と精度確認基盤を作る。

### 成果物

- F0 プロット
- ノート区間可視化
- サンプル比較

---

## 9. 当面やらないこと

初期フェーズでは以下を後回しにする。

- 複数音同時採譜
- コード推定
- ドラム譜生成
- 高度な楽器分類
- 商用曲フルミックスからの完全採譜
- 高品質な五線譜浄書

スコープを守ることを優先する。

---

## 10. 開発開始時にまずやること

以下の順で着手する。

1. プロジェクト雛形を作る
2. 音声読み込みを実装する
3. `pyin` で F0 を CSV 出力する
4. ノート分割処理を入れる
5. MIDI 出力する
6. 可視化を追加する
7. サンプル音源で検証する

---

## 11. 直近の実装タスク

### Task 1

- `pyproject.toml` 作成
- `src/` 構成作成
- `main.py` 作成

### Task 2

- `audio/loader.py` 実装
- wav 読み込み確認

### Task 3

- `pitch/estimator.py` 実装
- `pyin` による F0 推定
- CSV 保存

### Task 4

- `notes/segmenter.py` 実装
- F0 → ノート列変換

### Task 5

- `midi/writer.py` 実装
- MIDI 出力

### Task 6

- `visualization/plotter.py` 実装
- F0 とノートの可視化

---

## 12. 最終コメント

このプロジェクトで重要なのは、最初から「完璧な採譜」を狙わないこと。
まずは **単旋律の MIDI 化を安定して成功させる**。その後、観測可能な構造を維持しながら改善していく。

この順番で進めれば、後から

- Basic Pitch との比較
- 楽器別対応
- 譜面生成
- Web アプリ化 / デスクトップアプリ化

へ発展させやすい。

