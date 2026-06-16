export interface Rule {
  meta_data_key: string;
  value: any;
  operator: string;
  actions: string[];
}

export interface Event {
  id: string;
  event_name: string;
  next_state_name: string;
  rules: Rule[];
  version: number;
}

export interface NewRule {
  rule_type: string;   
  meta_data_key: string;
  value: any;
  operator: string;
  actions: string[];   
}