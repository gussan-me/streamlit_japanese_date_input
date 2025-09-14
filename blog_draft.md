# Streamlitカスタムコンポーネント開発で直面したiframeの制限と対策

## はじめに

Streamlitで日本語対応の日付選択コンポーネントを開発しました。標準の`st.date_input`は英語表記のみのため、日本のユーザー向けに曜日や月を日本語で表示するカスタムコンポーネントが必要でした。

開発は順調に進んでいましたが、実装を進める中でStreamlitのカスタムコンポーネントアーキテクチャに起因する様々な制限に直面しました。本記事では、これらの制限とその対策について共有します。

## Streamlitカスタムコンポーネントの仕組み

Streamlitのカスタムコンポーネントは、セキュリティとアイソレーションのためにiframe内で動作します。これにより以下のような構造になっています：

```
┌─────────────────────────────────┐
│  Streamlitアプリ（親ウィンドウ） │
│  ┌─────────────────────────┐   │
│  │  iframe                 │   │
│  │  ┌───────────────────┐ │   │
│  │  │ カスタム         │ │   │
│  │  │ コンポーネント   │ │   │
│  │  └───────────────────┘ │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

## 直面した制限事項

### 1. カレンダーポップアップの表示領域制限

最も大きな課題は、日付選択カレンダーがiframeの境界を越えて表示できないことでした。

**問題点：**
- 通常の日付ピッカーは、入力フィールドの下にポップアップとして表示される
- iframeの高さが固定されていると、カレンダーが見切れてしまう
- 親ウィンドウの領域にカレンダーを表示することは不可能

**対策：**
```typescript
// カレンダーが開いた時にiframeの高さを動的に拡張
useEffect(() => {
  if (isOpen) {
    const adjustFrameHeight = () => {
      const calendarElement = document.querySelector('.react-datepicker')
      const inputElement = document.querySelector('.date-input-container')
      
      if (calendarElement && inputElement) {
        const calendarRect = calendarElement.getBoundingClientRect()
        const inputRect = inputElement.getBoundingClientRect()
        const totalHeight = inputHeight + actualCalendarHeight + buffer
        
        // Streamlit APIを使用してiframeの高さを変更
        Streamlit.setFrameHeight(Math.ceil(totalHeight))
      }
    }
    
    setTimeout(adjustFrameHeight, 100)
  } else {
    // カレンダーを閉じた時は元の高さに戻す
    Streamlit.setFrameHeight(DEFAULT_FRAME_HEIGHT)
  }
}, [isOpen])
```

### 2. 狭い幅での表示問題

サイドバーなど狭い領域でコンポーネントを使用する際の課題です。

**問題点：**
- 幅200px未満の極端に狭いコンテナでは、カレンダーが収まらない
- 横スクロールも親ウィンドウに影響を与えられない
- モバイルアプリのような縦長レイアウトへの変更は大規模な改修が必要

**対策：**
```typescript
// コンテナ幅に応じてカレンダーをスケールダウン
if (availableWidth < ACTUAL_CALENDAR_WIDTH) {
  scale = availableWidth / ACTUAL_CALENDAR_WIDTH
  // 最小スケールを設定（読みやすさを保つ）
  const minScale = sidebar_mode ? 0.95 : 0.75
  scale = Math.max(minScale, scale)
}

// CSSでtransform: scaleを適用
const dynamicStyles = `
  .react-datepicker {
    transform: scale(${calendarScale});
    transform-origin: top left;
  }
`
```

### 3. サイドバー検出の不可能性

**問題点：**
- iframe内からは親ウィンドウのDOM構造にアクセスできない
- コンポーネントが自動的にサイドバー内にあることを検出できない
- 背景色などのスタイルを自動調整できない

**対策：**
```python
def japanese_date_input(
    label: str,
    sidebar_mode: bool = False,  # 明示的なパラメータとして追加
    # ... 他のパラメータ
):
    """
    sidebar_mode : bool
        サイドバーで使用する場合はTrueに設定。
        カスタムコンポーネントは自動検出できないため手動設定が必要。
    """
```

使用例：
```python
# サイドバーでの使用
with st.sidebar:
    date = japanese_date_input(
        "日付を選択",
        sidebar_mode=True  # 必須
    )
```

### 4. クロスオリジン制限

**問題点：**
- localStorageへのアクセスが制限される
- 親ウィンドウとの直接的な通信ができない
- window.parentへのアクセスが制限される

**対策：**
- Streamlit提供のComponent APIのみを使用
- `Streamlit.setComponentValue()`でデータを送信
- `Streamlit.setFrameHeight()`でサイズ調整

## なぜダイアログ的な実装ができないのか

理想的には、カレンダーを独立したダイアログやモーダルとして表示したいところですが、以下の理由で実現できませんでした：

1. **Streamlit本体のCSS変更が必要**
   - ダイアログを親ウィンドウに表示するには、Streamlit自体のCSSを変更する必要がある
   - これはカスタムコンポーネントの範囲を超えている

2. **セキュリティモデルの制約**
   - iframeのサンドボックス化はセキュリティ上重要
   - 親ウィンドウへの自由なアクセスを許可することはリスクが高い

3. **アーキテクチャの制約**
   - StreamlitとReactコンポーネント間の通信は限定的
   - 非同期通信のみで、リアルタイムな相互作用は困難

## 学んだこと

### 1. 制限を前提とした設計の重要性

カスタムコンポーネント開発では、最初から以下を考慮すべきです：
- iframe内での動作を前提とした設計
- 親ウィンドウへのアクセスが不要な実装
- 動的なサイズ変更への対応

### 2. ドキュメントの重要性

制限事項を明確にドキュメント化することで、ユーザーの混乱を防げます：

```markdown
## 制限事項

### iframe内での動作による制限

1. **極端に狭い幅での表示制限**
   - 幅が200px未満では、カレンダーが見切れる可能性があります
   - これはiframeの技術的制限によるもので、完全な解決は困難です

2. **サイドバー検出の制限**
   - `sidebar_mode`パラメータを手動で設定する必要があります
```

### 3. 既存のStreamlit APIを最大限活用

制限がある中でも、Streamlit Component APIを活用することで多くの課題を解決できました：
- `setFrameHeight()`による動的な高さ調整
- `setComponentValue()`によるデータ通信
- `theme`プロパティによるテーマ情報の取得

## まとめ

Streamlitカスタムコンポーネントの開発では、iframeによる制限を理解し、その範囲内で最適な解決策を見つけることが重要です。完璧な解決策がない場合でも、ユーザビリティを最大化する工夫は可能です。

今回開発した日本語日付入力コンポーネントは、これらの制限と向き合いながらも、日本のユーザーにとって使いやすいインターフェースを提供できたと考えています。

カスタムコンポーネント開発を検討している方は、ぜひこれらの制限事項を事前に把握し、設計段階から考慮することをお勧めします。

## 参考リンク

- [Streamlit Components API](https://docs.streamlit.io/library/components)
- [Japanese Date Input Component (GitHub)](https://github.com/...)
- [Streamlit公式ドキュメント](https://docs.streamlit.io)

---

*この記事で紹介したコンポーネントはオープンソースで公開予定です。*