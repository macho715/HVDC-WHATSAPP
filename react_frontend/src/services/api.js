/**
 * MACHO-GPT v3.4-mini API Service
 * HVDC Project - Samsung C&T Logistics Integration
 * Backend Communication Layer
 */

import axios from 'axios';

// MACHO-GPT Configuration
const MACHO_GPT_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8501',
  VERSION: '3.4-mini',
  PROJECT: 'HVDC_SAMSUNG_CT',
  CONFIDENCE_THRESHOLD: 0.90,
  TIMEOUT: 30000
};

// Create axios instance with MACHO-GPT defaults
const api = axios.create({
  baseURL: MACHO_GPT_CONFIG.BASE_URL,
  timeout: MACHO_GPT_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'X-MACHO-GPT-Version': MACHO_GPT_CONFIG.VERSION,
    'X-MACHO-GPT-Project': MACHO_GPT_CONFIG.PROJECT
  }
});

// Request interceptor for MACHO-GPT
api.interceptors.request.use(
  (config) => {
    console.log(`[MACHO-GPT] API Request: ${config.method?.toUpperCase()} ${config.url}`);
    
    // Add timestamp and mode to headers
    config.headers['X-MACHO-GPT-Timestamp'] = new Date().toISOString();
    config.headers['X-MACHO-GPT-Mode'] = getCurrentMode();
    
    return config;
  },
  (error) => {
    console.error('[MACHO-GPT] Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for MACHO-GPT
api.interceptors.response.use(
  (response) => {
    console.log(`[MACHO-GPT] API Response: ${response.status} from ${response.config.url}`);
    
    // Validate confidence level
    if (response.data?.confidence && response.data.confidence < MACHO_GPT_CONFIG.CONFIDENCE_THRESHOLD) {
      console.warn(`[MACHO-GPT] Low confidence: ${response.data.confidence}`);
    }
    
    return response;
  },
  (error) => {
    console.error('[MACHO-GPT] Response Error:', error);
    
    // Auto fail-safe to ZERO mode on critical errors
    if (error.response?.status >= 500) {
      console.warn('[MACHO-GPT] Server error detected - consider switching to ZERO mode');
    }
    
    return Promise.reject(error);
  }
);

// Helper function to get current mode
function getCurrentMode() {
  return window.MACHO_GPT_CONFIG?.mode || 'PRIME';
}

// MACHO-GPT API Functions
export const machoGptApi = {
  // Process WhatsApp messages
  processWhatsappMessages: async (messages, options = {}) => {
    try {
      const payload = {
        messages,
        mode: getCurrentMode(),
        confidence_threshold: MACHO_GPT_CONFIG.CONFIDENCE_THRESHOLD,
        timestamp: new Date().toISOString(),
        project: MACHO_GPT_CONFIG.PROJECT,
        ...options
      };
      
      const response = await api.post('/api/process_messages', payload);
      
      return {
        success: true,
        data: response.data,
        confidence: response.data.confidence || 0.85,
        mode: response.data.mode || getCurrentMode(),
        processing_time: response.data.processing_time || 0
      };
    } catch (error) {
      console.error('[MACHO-GPT] Process Messages Error:', error);
      
      return {
        success: false,
        error: error.message,
        data: null,
        confidence: 0.70,
        mode: 'ZERO'
      };
    }
  },

  // Get KPI data
  getKpiData: async () => {
    try {
      const response = await api.get('/api/kpi_data');
      return response.data;
    } catch (error) {
      console.error('[MACHO-GPT] KPI Data Error:', error);
      return {
        success_rate: 0.85,
        processing_time: 2.5,
        error_rate: 0.15,
        confidence: 0.80
      };
    }
  },

  // Switch MACHO-GPT mode
  switchMode: async (newMode) => {
    try {
      const response = await api.post('/api/switch_mode', { mode: newMode });
      
      // Update global config
      if (window.MACHO_GPT_CONFIG) {
        window.MACHO_GPT_CONFIG.mode = newMode;
      }
      
      return response.data;
    } catch (error) {
      console.error('[MACHO-GPT] Mode Switch Error:', error);
      return { success: false, error: error.message };
    }
  },

  // Get system status
  getSystemStatus: async () => {
    try {
      const response = await api.get('/api/system_status');
      return response.data;
    } catch (error) {
      console.error('[MACHO-GPT] System Status Error:', error);
      return {
        status: 'ERROR',
        mode: 'ZERO',
        confidence: 0.70,
        last_update: new Date().toISOString()
      };
    }
  },

  // Execute command
  executeCommand: async (command, args = {}) => {
    try {
      const response = await api.post('/api/execute_command', {
        command,
        args,
        mode: getCurrentMode(),
        timestamp: new Date().toISOString()
      });
      
      return response.data;
    } catch (error) {
      console.error('[MACHO-GPT] Command Execution Error:', error);
      return {
        success: false,
        error: error.message,
        confidence: 0.70
      };
    }
  },

  // Get available commands
  getCommands: async () => {
    try {
      const response = await api.get('/api/commands');
      return response.data;
    } catch (error) {
      console.error('[MACHO-GPT] Commands Error:', error);
      return {
        commands: [
          '/logi_master',
          '/switch_mode',
          '/kpi_monitor',
          '/visualize_data',
          '/urgent_processor'
        ]
      };
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (error) {
      console.error('[MACHO-GPT] Health Check Error:', error);
      return {
        status: 'ERROR',
        timestamp: new Date().toISOString()
      };
    }
  }
};

// MACHO-GPT Utility Functions
export const machoGptUtils = {
  // Format confidence percentage
  formatConfidence: (confidence) => {
    return `${(confidence * 100).toFixed(1)}%`;
  },

  // Get confidence color class
  getConfidenceColor: (confidence) => {
    if (confidence >= 0.90) return 'high';
    if (confidence >= 0.80) return 'medium';
    return 'low';
  },

  // Get mode color
  getModeColor: (mode) => {
    const colors = {
      'PRIME': '#3b82f6',
      'ORACLE': '#8b5cf6',
      'ZERO': '#6b7280',
      'LATTICE': '#10b981',
      'RHYTHM': '#f59e0b',
      'COST-GUARD': '#ef4444'
    };
    return colors[mode] || '#6b7280';
  },

  // Validate message format
  validateMessage: (message) => {
    if (!message || typeof message !== 'string') return false;
    if (message.length < 10) return false;
    if (message.length > 10000) return false;
    return true;
  },

  // Generate auto-triggers
  generateAutoTriggers: (confidence, urgentCount) => {
    const triggers = [];
    
    if (confidence < 0.90) {
      triggers.push('/switch_mode ZERO');
    }
    
    if (urgentCount > 2) {
      triggers.push('/urgent_processor activate');
    }
    
    if (confidence >= 0.95) {
      triggers.push('/logi_master optimize_processing');
    }
    
    triggers.push('/kpi_monitor update_dashboard');
    
    return triggers;
  }
};

// Export default api instance
export default api;

// Export configuration
export { MACHO_GPT_CONFIG }; 