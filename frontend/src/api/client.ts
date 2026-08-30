import { AgentResponse, DataQualityReport } from '../types';

const API_BASE_URL = '';

export async function sendChatMessage(message: string, sessionId?: string): Promise<AgentResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.error || 'Failed to communicate with BI Agent backend.');
  }

  return response.json();
}

export async function fetchLeadershipUpdate(sessionId?: string): Promise<AgentResponse> {
  const response = await fetch(`${API_BASE_URL}/api/leadership-update`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate leadership update report.');
  }

  return response.json();
}

export async function fetchDataQualityReport(): Promise<DataQualityReport> {
  const response = await fetch(`${API_BASE_URL}/api/data-quality`);
  if (!response.ok) {
    throw new Error('Failed to fetch data quality report.');
  }
  return response.json();
}
