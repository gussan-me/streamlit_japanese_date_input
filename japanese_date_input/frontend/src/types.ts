export interface JapaneseDateInputArgs {
  label?: string
  value?: string | null
  min_value?: string | null
  max_value?: string | null
  format?: DateFormat
  disabled?: boolean
  width?: "stretch" | number
  sidebar_mode?: boolean
}

export type DateFormat = 
  | "YYYY/MM/DD" 
  | "DD/MM/YYYY" 
  | "MM/DD/YYYY"
  | "YYYY-MM-DD" 
  | "DD-MM-YYYY" 
  | "MM-DD-YYYY"
  | "YYYY.MM.DD" 
  | "DD.MM.YYYY" 
  | "MM.DD.YYYY"

export type CalendarPosition = 'auto' | 'left' | 'right'