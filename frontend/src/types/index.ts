export interface QueryPlan {
  intent: string;
  boards_required: string[];
  filters: {
    sector?: string | null;
    date_range?: string | null;
    stage?: string | null;
    status?: string | null;
  };
  sector?: string | null;
  date_range?: string | null;
  metrics: string[];
  comparison_required: boolean;
  clarification_required: boolean;
  clarification_question?: string | null;
}

export interface DataQualityReport {
  total_records: number;
  valid_records: number;
  records_with_missing_values: number;
  invalid_dates: number;
  missing_monetary_values: number;
  normalization_actions: string[];
  records_excluded_from_calculations: string[];
  important_caveats: string[];
}

export interface ChartDataItem {
  name: string;
  value: number;
  count?: number;
}

export interface AgentResponse {
  session_id: string;
  query_plan: QueryPlan;
  metrics: Record<string, any>;
  insights: string;
  data_quality_report: DataQualityReport;
  chart_data: ChartDataItem[];
  clarification_required: boolean;
  clarification_question?: string | null;
}

export interface ChatMessageItem {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  responsePayload?: AgentResponse;
}
