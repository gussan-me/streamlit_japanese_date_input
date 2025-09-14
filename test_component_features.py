import streamlit as st
from datetime import date, timedelta
from japanese_date_input import japanese_date_input

st.set_page_config(
    page_title="Japanese Date Input コンポーネントテスト",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Japanese Date Input コンポーネント機能テスト")

# タブでテストを整理
tab1, tab2, tab3, tab4 = st.tabs(["基本機能", "レイアウト", "幅パラメータ", "セッション状態"])

with tab1:
    st.header("基本機能テスト")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("通常の日付入力")
        date1 = japanese_date_input(
            "日付を選択",
            key="basic_date"
        )
        if date1:
            st.success(f"選択された日付: {date1}")
    
    with col2:
        st.subheader("範囲制限あり")
        date2 = japanese_date_input(
            "今後30日以内",
            min_value=date.today(),
            max_value=date.today() + timedelta(days=30),
            key="limited_date"
        )
        if date2:
            days_from_today = (date2 - date.today()).days
            st.info(f"{days_from_today}日後")
    
    st.divider()
    
    # フォーマットテスト
    st.subheader("日付フォーマット")
    formats_col1, formats_col2, formats_col3 = st.columns(3)
    
    with formats_col1:
        japanese_date_input(
            "YYYY/MM/DD",
            format="YYYY/MM/DD",
            key="format1"
        )
    
    with formats_col2:
        japanese_date_input(
            "YYYY-MM-DD",
            format="YYYY-MM-DD",
            key="format2"
        )
    
    with formats_col3:
        japanese_date_input(
            "YYYY.MM.DD",
            format="YYYY.MM.DD",
            key="format3"
        )

with tab2:
    st.header("レイアウトテスト")
    
    # サイドバーテスト
    with st.sidebar:
        st.subheader("サイドバーでの表示")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = japanese_date_input(
                "開始日",
                value=date.today(),
                sidebar_mode=True,
                key="sidebar_start"
            )
        
        with col2:
            end_date = japanese_date_input(
                "終了日",
                value=date.today() + timedelta(days=7),
                min_value=start_date if start_date else date.today(),
                sidebar_mode=True,
                key="sidebar_end"
            )
        
        if start_date and end_date:
            st.info(f"期間: {(end_date - start_date).days + 1}日間")
    
    # メインエリアでの複数列
    st.subheader("複数列レイアウト")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        japanese_date_input("列1", key="col1_date")
    with col2:
        japanese_date_input("列2", key="col2_date")
    with col3:
        japanese_date_input("列3", key="col3_date")
    
    # フォーム内での使用
    st.subheader("フォーム内での使用")
    with st.form("test_form"):
        form_col1, form_col2 = st.columns(2)
        with form_col1:
            st.text_input("名前")
            japanese_date_input("生年月日", key="form_birthday")
        with form_col2:
            st.text_input("メール")
            japanese_date_input("希望日", key="form_preferred_date")
        st.form_submit_button("送信", use_container_width=True)

with tab3:
    st.header("幅パラメータテスト")
    
    # デフォルト（stretch）
    st.subheader("デフォルト - width='stretch'")
    japanese_date_input(
        "ストレッチ幅（親コンテナに合わせる）",
        key="width_stretch"
    )
    
    st.divider()
    
    # 固定幅
    st.subheader("固定幅")
    width_col1, width_col2, width_col3 = st.columns(3)
    
    with width_col1:
        japanese_date_input(
            "200px",
            width=200,
            key="width_200"
        )
    
    with width_col2:
        japanese_date_input(
            "300px",
            width=300,
            key="width_300"
        )
    
    with width_col3:
        japanese_date_input(
            "400px",
            width=400,
            key="width_400"
        )
    
    st.divider()
    
    # 狭いコンテナでの動作
    st.subheader("狭いコンテナでの動作")
    narrow_col1, narrow_col2, narrow_col3 = st.columns([1, 2, 1])
    
    with narrow_col1:
        st.caption("狭いカラムで500px指定")
        japanese_date_input(
            "500px（親より大きい）",
            width=500,
            key="width_overflow"
        )
        st.caption("→ 親の幅に制限される")

with tab4:
    st.header("セッション状態テスト")
    
    # セッション状態の確認
    selected_date = japanese_date_input(
        "日付を選択",
        key="session_test_date"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("戻り値")
        st.write(f"selected_date: {selected_date}")
        st.write(f"Type: {type(selected_date)}")
    
    with col2:
        st.subheader("Session State")
        if "session_test_date" in st.session_state:
            st.success(f"st.session_state['session_test_date'] = {st.session_state['session_test_date']}")
        else:
            st.warning("'session_test_date'はsession_stateに存在しません")
    
    # 再実行ボタン
    if st.button("ページを再実行"):
        st.rerun()
    
    # Session State全体の表示
    with st.expander("Session State全体を表示"):
        st.json({k: str(v) for k, v in st.session_state.items()})

# フッター
st.divider()
st.caption("Japanese Date Input Component - 機能テストページ")