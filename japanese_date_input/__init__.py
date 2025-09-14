import os
from datetime import date, datetime
from typing import Optional, Union
import streamlit.components.v1 as components

# _RELEASE定数を作成。コンポーネントを開発中はFalse、
# パッケージ化して配布する準備ができたらTrueに設定する。
__RELEASE = True

if not __RELEASE:
    __component_func = components.declare_component(
        "japanese_date_input",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    __component_func = components.declare_component("japanese_date_input", path=build_dir)


def japanese_date_input(
    label: str,
    value: Optional[Union[date, datetime, str]] = None,
    min_value: Optional[Union[date, datetime, str]] = None,
    max_value: Optional[Union[date, datetime, str]] = None,
    format: str = "YYYY/MM/DD",
    disabled: bool = False,
    width: Union[str, int] = "stretch",
    sidebar_mode: bool = False,
    key: Optional[str] = None,
) -> Optional[date]:
    """日本語対応の日付入力コンポーネントの新しいインスタンスを作成します。

    このコンポーネントは、日本語の月・曜日名および適切な日付フォーマットをサポートする
    date_inputウィジェットを提供します。

    パラメータ
    ----------
    label : str
        ユーザーに対してこの日付入力の用途を簡潔に説明するラベル。
    value : datetime.date, datetime.datetime, str, または None
        ウィジェット初期表示時の値。Noneの場合は今日の日付がデフォルトで設定されます。
    min_value : datetime.date, datetime.datetime, str, または None
        選択可能な最小日付。Noneの場合は制限なし。
    max_value : datetime.date, datetime.datetime, str, または None
        選択可能な最大日付。Noneの場合は制限なし。
    format : str
        日付のフォーマット。サポートされる形式は "YYYY/MM/DD"、"DD/MM/YYYY"、"MM/DD/YYYY"、
        及び区切り文字が "-" または "." のバリエーション。デフォルトは "YYYY/MM/DD"。
    disabled : bool
        Trueの場合、日付入力は無効化され、ユーザーが操作できなくなります。
    width : str または int
        日付入力ウィジェットの幅。指定可能な値は以下の通り：
        - "stretch"（デフォルト）：ウィジェットの幅が親コンテナの幅に合わせられます。
        - 整数（ピクセル単位）：ウィジェットの幅を固定できます。
          指定幅が親コンテナの幅より大きい場合は、親コンテナの幅に合わせて調整されます。
    sidebar_mode : bool
        Trueの場合、サイドバー用の特別なスタイル（白背景、黒文字）が適用されます。
        st.sidebar で使用する場合は明示的に True に設定する必要があります。
        iframe による隔離のため、カスタムコンポーネントはサイドバーの文脈を自動検出できません。
        デフォルトは False。
    key : str または None
        このコンポーネントを一意に識別するための任意のキー。
        None の場合、コンポーネントの引数が変更されると
        Streamlit フロントエンドで再マウントされ、現在の状態は失われます。

    戻り値
    -------
    datetime.date または None
        選択された日付の値。日付が選択されていない場合は None を返します。
    """
    # date/datetimeオブジェクトをISO文字列形式に変換
    def to_iso_string(d: Optional[Union[date, datetime, str]]) -> Optional[str]:
        if d is None:
            return None
        if isinstance(d, str):
            return d
        if isinstance(d, datetime):
            return d.date().isoformat()
        if isinstance(d, date):
            return d.isoformat()
        return None

    # フロントエンド用の値を準備
    value_str = to_iso_string(value)
    min_value_str = to_iso_string(min_value)
    max_value_str = to_iso_string(max_value)

    # コンポーネントを呼び出し
    component_value = __component_func(
        label=label,
        value=value_str,
        min_value=min_value_str,
        max_value=max_value_str,
        format=format,
        disabled=disabled,
        width=width,
        sidebar_mode=sidebar_mode,
        key=key,
        default=None,
    )

    # 返されたISO文字列をdateオブジェクトに変換
    if component_value is not None:
        try:
            return datetime.fromisoformat(component_value).date()
        except (ValueError, TypeError, AttributeError):
            # 無効な日付形式の場合はNoneを返す
            return None
    
    return None