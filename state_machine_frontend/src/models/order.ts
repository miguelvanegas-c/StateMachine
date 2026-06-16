export interface Transition {
  event: string
  new_state: string
  timestamp: string
}

export interface Order {
  id: string
  products_id: string[]
  amount: number
  state: string
  created_at: string
  updated_at: string
  transitions: Transition[]
}