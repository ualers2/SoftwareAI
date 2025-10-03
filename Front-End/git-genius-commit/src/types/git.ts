// src\types\git.ts
export interface GitConfig {
  lines_threshold: number;
  files_threshold: number;
  time_threshold: number; 
  auto_push: boolean;
  auto_commit: boolean;
  require_tests: boolean;
  api_endpoint: string;
  api_key: string;
  ai_model?: string;
}

export interface CommitMessage {
  commit_message: string;
  status: 'READY' | 'NO_CHANGES' | 'ERROR';
}
export interface AnalyzeRequest {
  repo_diff: string;
  modified_files: string[];
  repo_path: string;
  api_key: string;
  ai_model: string;
}

export interface AnalyzeResponse {
  status: 'SUCCESS' | 'NO_CHANGES' | 'ERROR';
  commit_message: string;
  detail: string;
  lines_changed: number;
}

export interface GitStatus {
  modified_files: string[];
  lines_changed: number;
  has_changes: boolean;
  last_check: Date;
  is_monitoring: boolean;
}
