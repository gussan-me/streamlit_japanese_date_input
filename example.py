import streamlit as st
from datetime import date, timedelta
from japanese_date_input import japanese_date_input

# ページの設定
st.set_page_config(
    page_title="Japanese Date Input Component Demo",
    page_icon="🗾",
    layout="wide"
)

st.title("🗾 Japanese Date Input Component")
st.markdown("日本語表記に対応したdate inputコンポーネントのデモです。")

# サイドバーに説明を追加
st.sidebar.header("特徴")
st.sidebar.markdown("""
- 📅 日本語の曜日表示（月、火、水...）
- 📆 日本語の月表示（1月、2月...）
- 🗾 週の開始は月曜日
- 🎌 日本で一般的な日付フォーマット対応
""")

st.sidebar.markdown("---")

# サイドバーでの使用例
st.sidebar.subheader("サイドバーでの使用例")
sidebar_date = japanese_date_input(
    "サイドバーで日付選択",
    sidebar_mode=True,  # サイドバーでは必須
    key="sidebar_example"
)
if sidebar_date:
    st.sidebar.info(f"選択: {sidebar_date}")

st.sidebar.caption("💡 サイドバーで使用する場合は`sidebar_mode=True`を設定してください")

st.markdown("---")

# 基本的な使用例
st.subheader("1. 基本的な使用例")
col1, col2 = st.columns(2)

with col1:
    selected_date1 = japanese_date_input(
        "日付を選択してください",
        key="basic_example"
    )
    if selected_date1:
        st.success(f"選択された日付: {selected_date1}")

with col2:
    st.code("""
selected_date = japanese_date_input(
    "日付を選択してください"
)
""", language="python")

st.markdown("---")

# デフォルト値の設定
st.subheader("2. デフォルト値の設定")
col1, col2 = st.columns(2)

with col1:
    selected_date2 = japanese_date_input(
        "誕生日",
        value=date(2000, 1, 1),
        key="default_value_example"
    )
    if selected_date2:
        age = (date.today() - selected_date2).days // 365
        st.info(f"選択された日付: {selected_date2} (約{age}歳)")

with col2:
    st.code("""
selected_date = japanese_date_input(
    "誕生日",
    value=date(2000, 1, 1)
)
""", language="python")

st.markdown("---")

# 日付範囲の制限
st.subheader("3. 日付範囲の制限")
col1, col2 = st.columns(2)

with col1:
    min_date = date.today() - timedelta(days=365)
    max_date = date.today() + timedelta(days=365)
    
    selected_date3 = japanese_date_input(
        "予約日（1年以内）",
        value=date.today(),
        min_value=date.today(),
        max_value=max_date,
        key="date_range_example"
    )
    if selected_date3:
        days_from_today = (selected_date3 - date.today()).days
        st.info(f"選択された日付: {selected_date3} (今日から{days_from_today}日後)")

with col2:
    st.code("""
selected_date = japanese_date_input(
    "予約日（1年以内）",
    value=date.today(),
    min_value=date.today(),
    max_value=date.today() + timedelta(days=365)
)
""", language="python")

st.markdown("---")

# 異なるフォーマット
st.subheader("4. 異なる日付フォーマット")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("YYYY/MM/DD (デフォルト)")
    date_fmt1 = japanese_date_input(
        "標準フォーマット",
        format="YYYY/MM/DD",
        key="format1"
    )
    if date_fmt1:
        st.write(f"選択: {date_fmt1}")

with col2:
    st.write("YYYY-MM-DD")
    date_fmt2 = japanese_date_input(
        "ハイフン区切り",
        format="YYYY-MM-DD",
        key="format2"
    )
    if date_fmt2:
        st.write(f"選択: {date_fmt2}")

with col3:
    st.write("YYYY.MM.DD")
    date_fmt3 = japanese_date_input(
        "ドット区切り",
        format="YYYY.MM.DD",
        key="format3"
    )
    if date_fmt3:
        st.write(f"選択: {date_fmt3}")

st.markdown("---")

# ヘルプテキストと無効化
st.subheader("5. ヘルプテキストと無効化")
col1, col2 = st.columns(2)

with col1:
    st.write("ヘルプテキスト付き")
    date_help = japanese_date_input(
        "開始日",
        key="help_example"
    )
    
with col2:
    st.write("無効化された入力")
    date_disabled = japanese_date_input(
        "終了日（編集不可）",
        value=date.today() + timedelta(days=30),
        disabled=True,
        key="disabled_example"
    )

st.markdown("---")

# 複数の日付入力の連携
st.subheader("6. 複数の日付入力の連携例")

start_date = japanese_date_input(
    "開始日",
    value=date.today(),
    key="start_date"
)

end_date = japanese_date_input(
    "終了日",
    value=date.today() + timedelta(days=7),
    min_value=start_date if start_date else date.today(),
    key="end_date"
)

if start_date and end_date:
    duration = (end_date - start_date).days
    if duration >= 0:
        st.success(f"期間: {duration + 1}日間 ({start_date} から {end_date})")
    else:
        st.error("終了日は開始日より後の日付を選択してください")

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Japanese Date Input Component for Streamlit</p>
    <p>Made with ❤️ using Streamlit Components</p>
</div>
""", unsafe_allow_html=True)