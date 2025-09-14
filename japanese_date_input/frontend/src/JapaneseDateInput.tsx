import React, { useEffect, useState, useRef } from "react"
import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps
} from "streamlit-component-lib"
import DatePicker, { registerLocale } from "react-datepicker"
import { ja } from "date-fns/locale"
import "react-datepicker/dist/react-datepicker.css"
import "./JapaneseDateInput.css"
import { JapaneseDateInputArgs, CalendarPosition } from "./types"
import {
  DEFAULT_FRAME_HEIGHT,
  BASE_CALENDAR_HEIGHT,
  DEFAULT_CALENDAR_SCALE,
  NARROW_CONTAINER_WIDTH,
  FOCUS_CHECK_INTERVAL,
  DATE_SELECT_CLOSE_DELAY,
  CLICK_HANDLER_DELAY,
  DATE_FORMAT_MAP
} from "./constants"

// 日本語ロケールを登録
registerLocale("ja", ja)

const JapaneseDateInput: React.FC<ComponentProps> = (props) => {
  // argsが未定義の場合のデフォルト値
  const args = (props.args || {}) as JapaneseDateInputArgs
  const { label = "日付を選択", value, min_value, max_value, format = "YYYY/MM/DD", disabled = false, width = "stretch", sidebar_mode = false } = args
  
  // 文字列の日付をDateオブジェクトに変換
  const [selectedDate, setSelectedDate] = useState<Date | null>(
    value ? new Date(value) : null
  )
  const [isOpen, setIsOpen] = useState(false)
  const [calendarPosition, setCalendarPosition] = useState<CalendarPosition>('auto')
  const [containerClass, setContainerClass] = useState('')
  const [isInSidebar, setIsInSidebar] = useState(false)
  const [calendarScale, setCalendarScale] = useState(DEFAULT_CALENDAR_SCALE)
  const datePickerRef = useRef<DatePicker>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  
  const minDate = min_value ? new Date(min_value) : undefined
  const maxDate = max_value ? new Date(max_value) : undefined

  useEffect(() => {
    // 初期フレーム高さを設定
    Streamlit.setFrameHeight(DEFAULT_FRAME_HEIGHT)
  }, [])

  useEffect(() => {
    // カレンダーが開いているときはフレーム高さを拡張
    if (isOpen) {
      // コンテナ幅に基づいてカレンダー位置を設定
      if (window.innerWidth < NARROW_CONTAINER_WIDTH) {
        setCalendarPosition('auto')
      }
      
      // カレンダー要素が実際にレンダリングされた後にサイズを取得
      const adjustFrameHeight = () => {
        const calendarElement = document.querySelector('.react-datepicker')
        const inputElement = document.querySelector('.date-input-container')
        
        if (calendarElement && inputElement) {
          // 実際の要素の高さを取得
          const calendarRect = calendarElement.getBoundingClientRect()
          const inputRect = inputElement.getBoundingClientRect()
          
          // カレンダーの実際の高さ（スケール後）
          const actualCalendarHeight = calendarRect.height
          const inputHeight = inputRect.height
          
          // 余白を追加（見切れ防止）
          const buffer = 20
          
          // フレーム高さを動的に設定
          const totalHeight = inputHeight + actualCalendarHeight + buffer
          Streamlit.setFrameHeight(Math.ceil(totalHeight))
        } else {
          // フォールバック：要素が見つからない場合は計算値を使用
          const scaledCalendarHeight = Math.ceil(BASE_CALENDAR_HEIGHT * calendarScale)
          const inputHeight = 80
          const buffer = 30
          Streamlit.setFrameHeight(scaledCalendarHeight + inputHeight + buffer)
        }
      }
      
      // カレンダーがレンダリングされるのを待ってから高さを調整
      setTimeout(adjustFrameHeight, 100)
      
      // スケール変更時にも再調整
      const resizeObserver = new ResizeObserver(adjustFrameHeight)
      const calendarElementForObserver = document.querySelector('.react-datepicker')
      if (calendarElementForObserver) {
        resizeObserver.observe(calendarElementForObserver)
      }
      
      // Streamlitのコンポーネントフォーカス追跡を使用
      // コンポーネントがフォーカスを失った場合、ユーザーが外側をクリックした可能性がある
      const checkFocus = setInterval(() => {
        if (!document.hasFocus()) {
          // iframeがフォーカスを失った、おそらく外側をクリックしたため
          setIsOpen(false)
          if (datePickerRef.current) {
            datePickerRef.current.setOpen(false)
          }
        }
      }, FOCUS_CHECK_INTERVAL)
      
      return () => {
        resizeObserver.disconnect()
        clearInterval(checkFocus)
      }
    } else {
      // 通常の高さに戻す
      Streamlit.setFrameHeight(DEFAULT_FRAME_HEIGHT)
    }
  }, [isOpen, calendarScale, isInSidebar])

  const handleDateChange = (date: Date | null) => {
    setSelectedDate(date)
    // 選択された日付をPythonに送信
    if (date) {
      // ローカル日付文字列としてフォーマット（UTCではない）
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      Streamlit.setComponentValue(`${year}-${month}-${day}`)
    } else {
      Streamlit.setComponentValue(null)
    }
  }

  // iframeサポートを改善した外側クリックハンドラーを追加
  useEffect(() => {
    if (!isOpen) return

    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Node
      
      // 関連するすべての要素を取得
      const container = containerRef.current
      const calendarPopper = document.querySelector('.react-datepicker-popper')
      const calendarWrapper = document.querySelector('.react-datepicker__tab-loop')
      
      // クリックが日付ピッカー要素のいずれかの内側かを確認
      const isInsideContainer = container && container.contains(target)
      const isInsidePopper = calendarPopper && calendarPopper.contains(target)
      const isInsideWrapper = calendarWrapper && calendarWrapper.contains(target)
      
      // クリックがすべての日付ピッカー要素の外側の場合、カレンダーを閉じる
      if (!isInsideContainer && !isInsidePopper && !isInsideWrapper) {
        setIsOpen(false)
        if (datePickerRef.current) {
          datePickerRef.current.setOpen(false)
        }
      }
    }

    // カレンダーが完全にレンダリングされるよう小さな遅延
    const timeoutId = setTimeout(() => {
      // より良いイベントハンドリングのためキャプチャフェーズを使用
      document.addEventListener('click', handleClickOutside, true)
      document.addEventListener('mousedown', handleClickOutside, true)
    }, CLICK_HANDLER_DELAY)
    
    // クリーンアップ
    return () => {
      clearTimeout(timeoutId)
      document.removeEventListener('click', handleClickOutside, true)
      document.removeEventListener('mousedown', handleClickOutside, true)
    }
  }, [isOpen])

  // formatパラメータに基づくカスタム日付フォーマット
  const getDateFormat = () => {
    return DATE_FORMAT_MAP[format] || DATE_FORMAT_MAP["YYYY/MM/DD"]
  }


  // コンポーネントの状態に依存する動的スタイル
  const dynamicStyles = `
    .react-datepicker {
      transform: scale(${calendarScale});
    }
  `

  // widthプロップに基づいてコンテナスタイルを決定
  const containerStyle: React.CSSProperties = {}
  if (width === "stretch") {
    containerStyle.width = "100%"
  } else if (typeof width === "number") {
    // 親コンテナより広い幅が指定された場合、親コンテナの幅に制限
    containerStyle.width = "100%"
    containerStyle.maxWidth = `${width}px`
  }
  
  useEffect(() => {
    const checkContainer = () => {
      if (containerRef.current) {
        // コンテナ幅をチェックして適切なスケールを計算
        const containerWidth = containerRef.current.offsetWidth
        const iframeWidth = window.innerWidth
        
        // より正確なカレンダー幅の計算
        // react-datepickerのカレンダーは約280px必要（曜日7つ×セル幅）
        const ACTUAL_CALENDAR_WIDTH = 280  // 実際のカレンダー幅
        
        // コンテナ幅に基づいてスケールを計算
        let scale = DEFAULT_CALENDAR_SCALE
        
        if (containerWidth > 0 && iframeWidth > 0) {
          // 利用可能な幅を計算（コンテナとiframeの小さい方）
          const effectiveWidth = Math.min(containerWidth, iframeWidth)
          
          // パディングを考慮（左右に5pxずつ）
          const padding = 10
          const availableWidth = effectiveWidth - padding
          
          // カレンダーが収まるようにスケールを計算
          if (availableWidth < ACTUAL_CALENDAR_WIDTH) {
            // 利用可能幅に合わせてスケールダウン
            scale = availableWidth / ACTUAL_CALENDAR_WIDTH
            
            // 最小スケールを適用（読みやすさを保つ）
            const minScale = sidebar_mode ? 0.95 : 0.75  // サイドバーでは95%、通常は75%まで
            scale = Math.max(minScale, scale)
          } else {
            // 十分な幅がある場合
            scale = DEFAULT_CALENDAR_SCALE
          }

        }
        
        setCalendarScale(scale)
        
        // 追加スタイリング用のクラスを設定
        if (scale < 0.8) {
          setContainerClass('very-narrow-calendar')
        } else if (scale < 0.9) {
          setContainerClass('narrow-calendar')
        } else {
          setContainerClass('')
        }
        
        // sidebar_modeパラメータで明示的に設定された場合のみサイドバーモードを使用
        // カスタムコンポーネントはサイドバー内にあるかどうかを確実に検出できない
        setIsInSidebar(sidebar_mode)
      }
    }
    
    checkContainer()
    // 適切な測定を確実にするための遅延チェック
    setTimeout(checkContainer, 100)
    setTimeout(checkContainer, 500) // 動的コンテンツ用の追加チェック
    window.addEventListener('resize', checkContainer)
    
    return () => window.removeEventListener('resize', checkContainer)
  }, [sidebar_mode, props.theme])

  const handleOverlayClick = () => {
    setIsOpen(false)
    if (datePickerRef.current) {
      datePickerRef.current.setOpen(false)
    }
  }

  return (
    <>
      <style>{dynamicStyles}</style>
      {isOpen && <div className="calendar-overlay" onClick={handleOverlayClick} />}
      <div 
        ref={containerRef}
        className={`date-input-container ${containerClass} ${isInSidebar ? 'sidebar-mode' : ''}`} 
        style={containerStyle}
      >
        {label && <label className="date-input-label">{label}</label>}
        <DatePicker
          ref={datePickerRef}
          selected={selectedDate}
          onChange={handleDateChange}
          onCalendarOpen={() => {
            setIsOpen(true)
          }}
          onCalendarClose={() => {
            setIsOpen(false)
          }}
          onSelect={() => {
            // 日付を選択した後カレンダーを閉じる
            setTimeout(() => {
              setIsOpen(false)
              if (datePickerRef.current) {
                datePickerRef.current.setOpen(false)
              }
            }, DATE_SELECT_CLOSE_DELAY)
          }}
          dateFormat={getDateFormat()}
          locale="ja"
          disabled={disabled}
          minDate={minDate}
          maxDate={maxDate}
          className="date-input-field"
          placeholderText="日付を選択"
          showMonthDropdown
          showYearDropdown
          dropdownMode="select"
          isClearable={false}
          autoComplete="off"
          popperPlacement={containerClass ? 'top-start' : calendarPosition === 'left' ? 'bottom-end' : 'bottom-start'}
          shouldCloseOnSelect={true}
          withPortal={false}
          calendarStartDay={0}
        />
      </div>
    </>
  )
}

export default withStreamlitConnection(JapaneseDateInput)