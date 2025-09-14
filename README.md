# Japanese Date Input Component for Streamlit

日本語表記に対応したStreamlit用のdate inputコンポーネントです。

## 特徴

- 📅 日本語の曜日表示（月、火、水、木、金、土、日）
- 📆 日本語の月表示（1月、2月、...、12月）
- 🗾 週の開始を月曜日に設定
- 🎌 日本で一般的な日付フォーマット（YYYY/MM/DD）をデフォルトに

## インストール

```bash
pip install streamlit-japanese-date-input
```

![demonstration](usage.gif)


## 使い方

### 基本的な使用例

以下のスクリプトを実行することで、アプリケーションの諸々の挙動を確認することができます。

```bash
streamlit run example.py
```

### パラメータ

- `label` (str): 入力フィールドのラベル
- `value` (date/datetime/str, optional): 初期値
- `min_value` (date/datetime/str, optional): 選択可能な最小日付
- `max_value` (date/datetime/str, optional): 選択可能な最大日付
- `format` (str): 日付フォーマット（デフォルト: "YYYY/MM/DD"）
- `disabled` (bool): 入力を無効化するかどうか
- `width` (str or int): ウィジェットの幅（"stretch"または固定ピクセル値）
- `sidebar_mode` (bool): サイドバーでの表示に最適化するかどうか（デフォルト: False）
- `key` (str, optional): コンポーネントの一意のキー

### サイドバーでの使用について

Streamlitのカスタムコンポーネントは独立したiframe内で動作するため、自動的にサイドバーコンテキストを検出することができません。そのため、サイドバーで使用する場合は`sidebar_mode=True`を明示的に指定する必要があります。

```python
# サイドバーでの使用例
with st.sidebar:
    selected_date = japanese_date_input(
        "日付を選択",
        sidebar_mode=True  # サイドバーでは必ずTrueに設定
    )
```

`sidebar_mode=True`を設定すると
- 背景色が白になり、サイドバーのデザインに調和します
- テキストカラーが黒になります

## 制限事項

### 1. iframe内での表示制約

カスタムコンポーネントは iframe 内で動作するため、カレンダーを親ウィンドウの上に重ねて表示する「ダイアログ形式」は実現できません。

 * 狭いコンテナやサイドバーではカレンダーが見切れる
 * iframe を超えて表示することはできない
 * 高さを動的に調整しても限界がある

一方で`st.date_input`はiframeではなくStreamlit本体のウィジェットなので、こうした制約がなく常にきれいに表示されます。


### 2. サイドバーや狭いレイアウトでの自動検出不可

カスタムコンポーネントは親ウィンドウのDOMを参照できないため、
サイドバーで使う場合は手動で`sidebar_mode=True`を設定する必要があります。
これにより、背景色や文字色の調整が行えます。

### 3. メンテナンスや互換性の面

カスタムコンポーネントはReactとStreamlit Components APIに依存するため、
Streamlitのアップデートやテーマ変更によって動作が壊れるリスクがあります。

また、前述したiframeの制約を回避するために複雑な実装や高さ調整が必要になります。

