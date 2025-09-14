// フレーム高さの定数
export const DEFAULT_FRAME_HEIGHT = 80
export const BASE_CALENDAR_HEIGHT = 330

// カレンダースケーリング
export const DEFAULT_CALENDAR_SCALE = 0.9
export const MIN_CALENDAR_SCALE_SIDEBAR = 0.85
export const MIN_CALENDAR_SCALE_MAIN = 0.75

// 幅のブレークポイント
export const NARROW_CONTAINER_WIDTH = 350
export const SIDEBAR_WIDTH_THRESHOLD = 400
export const CALENDAR_BASE_WIDTH = 280

// タイミング定数
export const FOCUS_CHECK_INTERVAL = 100
export const MOUSE_LEAVE_DELAY = 300
export const DATE_SELECT_CLOSE_DELAY = 100
export const CLICK_HANDLER_DELAY = 100

// 日付フォーマットのマッピング
export const DATE_FORMAT_MAP = {
  "YYYY/MM/DD": "yyyy/MM/dd",
  "DD/MM/YYYY": "dd/MM/yyyy",
  "MM/DD/YYYY": "MM/dd/yyyy",
  "YYYY-MM-DD": "yyyy-MM-dd",
  "DD-MM-YYYY": "dd-MM-yyyy",
  "MM-DD-YYYY": "MM-dd-yyyy",
  "YYYY.MM.DD": "yyyy.MM.dd",
  "DD.MM.YYYY": "dd.MM.yyyy",
  "MM.DD.YYYY": "MM.dd.yyyy"
} as const