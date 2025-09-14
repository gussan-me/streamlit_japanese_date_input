# Japanese Date Input Component for Streamlit

日本語表記に対応したStreamlit用のdate inputコンポーネントです。
サードパーティコンポーネントとして実装する場合、[制限事項](#制限事項)があるため、基本的には`st.date_input`の使用を推奨します。

## 特徴

- 📅 日本語の曜日表示（月、火、水、木、金、土、日）
- 📆 日本語の月表示（1月、2月、...、12月）

## インストール

```bash
pip install streamlit-japanese-date-input
```




## 使い方

### 基本的な使用例

以下のスクリプトを実行することで、アプリケーションの諸々の挙動を確認することができます。
以下のgifのような挙動になります。

```bash
streamlit run example.py
```

![demonstration](usage.gif)

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

Streamlitのカスタムコンポーネントは独立したiframe内で動作するため、Streamlitのサイドバーの中に、このコンポーネントを配置していることを自動的に検出することができません。
そのため、サイドバーで使用する場合は`sidebar_mode=True`を明示的に指定する必要があります。

```python
# サイドバーでの使用例
with st.sidebar:
    selected_date = japanese_date_input(
        "日付を選択",
        sidebar_mode=True  # サイドバーでは必ずTrueに設定
    )
```

`sidebar_mode=True`を設定すると、背景色が白色・テキストが黒色となり、サイドバーのデザインに調和します

## 制限事項

### 1. iframe内での表示制約

カスタムコンポーネントは iframe 内で動作するため、カレンダーを親ウィンドウの上に重ねて表示する「ダイアログ形式」は実現できません。
以下の制限があります。

 * 狭いコンテナやサイドバーではカレンダーが見切れる
 * iframe を超えて表示することはできない
 * 高さを動的に調整しても限界がある

一方、st.date_input は iframe ではなく Streamlit 本体のウィジェットのため、こうした制約がなく常に正しく表示されます。

### 2. サイドバーや狭いレイアウトでの自動検出不可

カスタムコンポーネントは親ウィンドウのDOMを参照できないため、
サイドバーで使う場合は手動で`sidebar_mode=True`を設定する必要があります。
これにより、背景色や文字色の調整が行えます。

### 3. メンテナンスや互換性の面

カスタムコンポーネントは React と Streamlit Components API に依存するため、Streamlit のアップデートやテーマ変更により動作が壊れる可能性があります。
また、iframe の制約を回避するために複雑な実装や高さ調整が必要になる場合があります。
