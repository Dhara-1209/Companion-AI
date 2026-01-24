// API Service for CompanionAI Backend

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';

export interface SourceInfo {
  filename: string;
  page?: number;
  brand?: string;
  model?: string;
  relevance_score: number;
}

export interface AnswerResponse {
  answer: string;
  safety_flag: boolean;
  safety_level: string;
  safety_message?: string;
  sources: SourceInfo[];
  chunks_used: number;
  processing_time: number;
  search_time: number;
  llm_time: number;
  confidence_score: number;
}

export interface QueryRequest {
  query: string;
  brand?: string;
  model?: string;
  k?: number;
}

export interface HealthResponse {
  status: string;
  companion_ai_loaded: boolean;
  safety_checker_loaded: boolean;
  timestamp: string;
  version: string;
}

export interface UploadResponse {
  filename: string;
  status: string;
  chunks_processed: number;
  processing_time: number;
}

class CompanionAIService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Check if the backend is healthy and ready
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Send a query to the CompanionAI backend
   */
  async getAnswer(request: QueryRequest): Promise<AnswerResponse> {
    const response = await fetch(`${this.baseUrl}/answer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: request.query,
        brand: request.brand,
        model: request.model,
        k: request.k || 10,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Failed to get answer: ${response.statusText}`
      );
    }

    return response.json();
  }

  /**
   * Send a device-specific query (brand and model pre-filled)
   */
  async getDeviceSpecificAnswer(
    query: string,
    brand: string,
    model: string,
    k: number = 10
  ): Promise<AnswerResponse> {
    return this.getAnswer({
      query,
      brand,
      model,
      k,
    });
  }

  /**
   * Upload a file (image, PDF, etc.) for processing
   */
  async uploadFile(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Failed to upload file: ${response.statusText}`
      );
    }

    return response.json();
  }

  /**
   * Process text extracted from QR code or other sources
   */
  async processQRCode(text: string): Promise<AnswerResponse> {
    return this.getAnswer({ query: `Information from QR code: ${text}` });
  }

  /**
   * Get metrics about the system performance
   */
  async getMetrics(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/metrics`);
    if (!response.ok) {
      throw new Error(`Failed to get metrics: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Process voice input (if speech-to-text is implemented in backend)
   */
  async processVoiceInput(audioBlob: Blob): Promise<AnswerResponse> {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'voice.webm');

    const response = await fetch(`${this.baseUrl}/voice`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Failed to process voice: ${response.statusText}`
      );
    }

    return response.json();
  }
}

// Export a singleton instance
export const apiService = new CompanionAIService();

// Export the class for custom instances
export default CompanionAIService;
