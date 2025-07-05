import React, { useState, useEffect } from 'react';
import { MessageCircle, FileText, Clock, Users, Settings, Plus, Trash2, AlertTriangle, CheckCircle, Zap } from 'lucide-react';

/**
 * MACHO-GPT v3.4-mini WhatsApp Summary Application
 * HVDC Project - Samsung C&T Logistics Integration
 * Enhanced with 6 Containment Modes and Auto-Trigger System
 */
const WhatsAppSummaryApp = () => {
  // MACHO-GPT Core State
  const [currentMode, setCurrentMode] = useState('PRIME');
  const [confidence, setConfidence] = useState(0.95);
  const [systemStatus, setSystemStatus] = useState('ACTIVE');
  const [autoTriggers, setAutoTriggers] = useState([]);
  const [kpiData, setKpiData] = useState({
    success_rate: 0.95,
    processing_time: 2.1,
    error_rate: 0.05
  });

  // MACHO-GPT Modes Configuration
  const modes = {
    PRIME: { color: 'bg-blue-500', confidence_min: 0.95, auto_triggers: true },
    ORACLE: { color: 'bg-purple-500', confidence_min: 0.90, data_validation: 'strict' },
    ZERO: { color: 'bg-gray-500', confidence_min: 0.70, fallback_mode: true },
    LATTICE: { color: 'bg-green-500', confidence_min: 0.85, ocr_threshold: 0.85 },
    RHYTHM: { color: 'bg-yellow-500', confidence_min: 0.80, kpi_refresh: 3600 },
    'COST-GUARD': { color: 'bg-red-500', confidence_min: 0.90, cost_validation: true }
  };

  // Enhanced Chat Rooms with MACHO-GPT Integration
  const [chatRooms, setChatRooms] = useState([
    { id: 1, name: '마케팅팀', members: 8, lastActivity: '10분 전', active: true, priority: 'normal', confidence: 0.92 },
    { id: 2, name: '개발팀', members: 12, lastActivity: '5분 전', active: true, priority: 'high', confidence: 0.95 },
    { id: 3, name: '디자인팀', members: 6, lastActivity: '1시간 전', active: true, priority: 'normal', confidence: 0.88 },
    { id: 4, name: '영업팀', members: 15, lastActivity: '30분 전', active: true, priority: 'urgent', confidence: 0.97 },
    { id: 5, name: '경영진', members: 4, lastActivity: '2시간 전', active: true, priority: 'critical', confidence: 0.93 }
  ]);

  // Enhanced Messages with MACHO-GPT Processing
  const [messages, setMessages] = useState([
    { id: 1, room: '마케팅팀', author: '김민수', content: '내일 캠페인 론칭 준비 완료했습니다.', time: '14:30', type: 'message', confidence: 0.95, processed: true },
    { id: 2, room: '개발팀', author: '이영희', content: '긴급 버그 수정 완료. 테스트 부탁드립니다.', time: '14:25', type: 'message', confidence: 0.92, processed: true, urgent: true },
    { id: 3, room: '디자인팀', author: '박철수', content: '새로운 로고 디자인 시안 공유드립니다.', time: '13:45', type: 'file', confidence: 0.88, processed: true },
    { id: 4, room: '영업팀', author: '정미라', content: '오늘 고객 미팅 결과 보고서 작성 중입니다.', time: '14:00', type: 'message', confidence: 0.96, processed: true },
    { id: 5, room: '경영진', author: '최대표', content: '월간 실적 검토 회의 일정 조정 필요', time: '12:30', type: 'message', confidence: 0.94, processed: true }
  ]);

  // Enhanced Summary Report with MACHO-GPT Analytics
  const [summaryReport, setSummaryReport] = useState({
    date: new Date().toISOString().split('T')[0],
    totalMessages: 127,
    activeRooms: 5,
    confidence: 0.95,
    mode: 'PRIME',
    processing_time: 2.1,
    keyPoints: [
      '마케팅팀: 신규 캠페인 론칭 준비 완료 (신뢰도: 95%)',
      '개발팀: 주요 버그 수정 완료, 테스트 진행 중 (신뢰도: 92%)',
      '디자인팀: 새로운 브랜드 로고 시안 검토 중 (신뢰도: 88%)',
      '영업팀: 고객 미팅 3건 진행, 긍정적 반응 (신뢰도: 96%)',
      '경영진: 월간 실적 검토 및 향후 계획 논의 (신뢰도: 94%)'
    ],
    urgentItems: [
      '개발팀: 긴급 버그 수정 요청 (우선순위 높음) - 자동 알림 발송됨',
      '영업팀: 대형 고객사 계약 검토 필요 - 24시간 내 처리 요망'
    ],
    triggers: [
      '/logi_master urgent_processing',
      '/switch_mode LATTICE',
      '/kpi_monitor real_time'
    ]
  });

  // MACHO-GPT State Management
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [newRoomName, setNewRoomName] = useState('');
  const [isAddingRoom, setIsAddingRoom] = useState(false);
  const [manualInput, setManualInput] = useState('');
  const [isInputMode, setIsInputMode] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [commandHistory, setCommandHistory] = useState([]);

  // MACHO-GPT Auto-Trigger System
  useEffect(() => {
    const checkAutoTriggers = () => {
      const triggers = [];
      
      if (confidence < 0.90) {
        triggers.push('/switch_mode ZERO');
        setCurrentMode('ZERO');
      }
      
      if (kpiData.error_rate > 0.10) {
        triggers.push('/logi_master error_analysis');
      }
      
      if (messages.some(msg => msg.urgent && !msg.processed)) {
        triggers.push('/urgent_processor activate');
      }
      
      setAutoTriggers(triggers);
    };

    checkAutoTriggers();
    const interval = setInterval(checkAutoTriggers, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, [confidence, kpiData, messages]);

  // MACHO-GPT Enhanced Summary Processing
  const createMachoSummary = (text) => {
    const lines = text.split('\n').filter(line => line.trim());
    const messageCount = lines.length;
    
    // MACHO-GPT Keyword Classification
    const urgentKeywords = ['긴급', 'urgent', '중요', 'immediate', '빠르게', '즉시', '오늘까지', '내일까지', '위험', '경고'];
    const teamKeywords = {
      '마케팅': ['마케팅', '광고', '캠페인', '홍보', '브랜딩', '고객'],
      '개발': ['개발', '코딩', '버그', '배포', '테스트', '시스템', '서버'],
      '디자인': ['디자인', '시안', '로고', 'UI', 'UX', '브랜드'],
      '영업': ['영업', '고객', '계약', '미팅', '매출', '수주'],
      '경영': ['경영', '실적', '예산', '전략', '결정', '승인'],
      '물류': ['물류', '배송', '재고', '창고', '운송', '수입', '수출']
    };

    const keyPoints = [];
    const urgentItems = [];
    let totalConfidence = 0;
    let processedLines = 0;

    lines.forEach(line => {
      const lowerLine = line.toLowerCase();
      let lineConfidence = 0.70; // Base confidence
      
      // Calculate confidence based on content quality
      if (line.includes(':') || line.includes('-')) lineConfidence += 0.10;
      if (line.length > 20) lineConfidence += 0.05;
      if (line.length > 50) lineConfidence += 0.05;
      
      // Team classification bonus
      Object.keys(teamKeywords).forEach(team => {
        if (teamKeywords[team].some(keyword => lowerLine.includes(keyword))) {
          lineConfidence += 0.10;
        }
      });
      
      // Timestamp detection bonus
      if (line.match(/\d{2}:\d{2}|\d{4}-\d{2}-\d{2}/)) {
        lineConfidence += 0.05;
      }
      
      totalConfidence += lineConfidence;
      processedLines++;
      
      // Classify as urgent or key point
      const hasUrgent = urgentKeywords.some(keyword => 
        lowerLine.includes(keyword) || line.includes(keyword)
      );
      
      if (hasUrgent && urgentItems.length < 5) {
        urgentItems.push({
          content: line.length > 100 ? line.substring(0, 100) + '...' : line,
          confidence: lineConfidence,
          timestamp: new Date().toISOString()
        });
      } else if (keyPoints.length < 10) {
        keyPoints.push({
          content: line.length > 100 ? line.substring(0, 100) + '...' : line,
          confidence: lineConfidence,
          timestamp: new Date().toISOString()
        });
      }
    });

    const avgConfidence = processedLines > 0 ? totalConfidence / processedLines : 0.70;
    setConfidence(Math.min(avgConfidence, 1.0));

    // Auto-trigger mode switch if confidence is low
    if (avgConfidence < 0.85 && currentMode !== 'ZERO') {
      setCurrentMode('ZERO');
    }

    return {
      keyPoints: keyPoints.length > 0 ? keyPoints.map(kp => kp.content) : ['입력된 대화 내용을 확인해주세요.'],
      urgentItems: urgentItems.length > 0 ? urgentItems.map(ui => ui.content) : ['긴급 사항이 발견되지 않았습니다.'],
      totalMessages: messageCount,
      confidence: avgConfidence,
      mode: currentMode,
      processing_time: Math.random() * 2 + 1, // Simulated processing time
      triggers: generateAutoTriggers(avgConfidence, urgentItems.length)
    };
  };

  // MACHO-GPT Auto-Trigger Generation
  const generateAutoTriggers = (confidence, urgentCount) => {
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
    triggers.push('/visualize_data summary_report');
    
    return triggers;
  };

  // Enhanced Manual Input Processing with MACHO-GPT
  const processManualInput = async () => {
    if (!manualInput.trim()) {
      alert('메시지 내용을 입력해주세요.');
      return;
    }

    setIsLoading(true);
    const startTime = Date.now();

    try {
      // MACHO-GPT Processing
      const machoSummary = createMachoSummary(manualInput);
      
      // Simulate API call with enhanced processing
      const apiPayload = {
        messages: manualInput,
        mode: currentMode,
        confidence_threshold: modes[currentMode].confidence_min,
        timestamp: new Date().toISOString(),
        project: 'HVDC_SAMSUNG_CT_WHATSAPP'
      };

      // Enhanced summary with MACHO-GPT features
      const enhancedSummary = {
        ...machoSummary,
        api_response: true,
        processing_time: (Date.now() - startTime) / 1000,
        mode: currentMode,
        triggers: machoSummary.triggers
      };

      setSummaryReport(prev => ({
        ...prev,
        keyPoints: enhancedSummary.keyPoints,
        urgentItems: enhancedSummary.urgentItems,
        totalMessages: enhancedSummary.totalMessages,
        confidence: enhancedSummary.confidence,
        processing_time: enhancedSummary.processing_time,
        mode: currentMode,
        triggers: enhancedSummary.triggers
      }));

      // Update KPI Data
      setKpiData(prev => ({
        ...prev,
        success_rate: Math.min(prev.success_rate + 0.01, 1.0),
        processing_time: enhancedSummary.processing_time,
        error_rate: Math.max(prev.error_rate - 0.01, 0.0)
      }));

      // Add to command history
      setCommandHistory(prev => [...prev, {
        command: '/logi_master process_whatsapp_summary',
        timestamp: new Date().toISOString(),
        confidence: enhancedSummary.confidence,
        mode: currentMode
      }]);

      setIsInputMode(false);
      setManualInput('');
      
      alert(`✅ MACHO-GPT 처리 완료!\n신뢰도: ${(enhancedSummary.confidence * 100).toFixed(1)}%\n처리시간: ${enhancedSummary.processing_time.toFixed(1)}초\n모드: ${currentMode}`);

    } catch (error) {
      console.error('MACHO-GPT 처리 오류:', error);
      
      // Auto fail-safe to ZERO mode
      if (currentMode !== 'ZERO') {
        setCurrentMode('ZERO');
        setConfidence(0.70);
      }
      
      // Update error rate
      setKpiData(prev => ({
        ...prev,
        error_rate: Math.min(prev.error_rate + 0.05, 1.0),
        success_rate: Math.max(prev.success_rate - 0.05, 0.0)
      }));

      alert('⚠️ 처리 중 오류가 발생했습니다. ZERO 모드로 전환됩니다.');
    }

    setIsLoading(false);
  };

  // MACHO-GPT Mode Switch
  const switchMode = (newMode) => {
    setCurrentMode(newMode);
    setConfidence(modes[newMode].confidence_min);
    
    // Add to command history
    setCommandHistory(prev => [...prev, {
      command: `/switch_mode ${newMode}`,
      timestamp: new Date().toISOString(),
      confidence: modes[newMode].confidence_min,
      mode: newMode
    }]);
  };

  // Enhanced Dashboard with MACHO-GPT Features
  const DashboardTab = () => (
    <div className="space-y-6">
      {/* MACHO-GPT Status Header */}
      <div className={`${modes[currentMode].color} text-white p-6 rounded-lg`}>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">MACHO-GPT v3.4-mini</h2>
          <div className="flex items-center space-x-2">
            <Zap className="w-5 h-5" />
            <span className="text-sm">모드: {currentMode}</span>
          </div>
        </div>
        <div className="grid grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold">{(confidence * 100).toFixed(1)}%</div>
            <div className="text-sm opacity-80">신뢰도</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{summaryReport.totalMessages}</div>
            <div className="text-sm opacity-80">총 메시지</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{summaryReport.activeRooms}</div>
            <div className="text-sm opacity-80">활성 대화방</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{summaryReport.urgentItems.length}</div>
            <div className="text-sm opacity-80">긴급 사항</div>
          </div>
        </div>
      </div>

      {/* MACHO-GPT Mode Selector */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <Settings className="mr-2" size={20} />
          Containment Mode 선택
        </h3>
        <div className="grid grid-cols-3 gap-3">
          {Object.entries(modes).map(([mode, config]) => (
            <button
              key={mode}
              onClick={() => switchMode(mode)}
              className={`p-3 rounded-lg text-white font-medium transition-colors ${
                currentMode === mode ? config.color : 'bg-gray-300'
              }`}
            >
              {mode}
            </button>
          ))}
        </div>
      </div>

      {/* KPI Dashboard */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <FileText className="mr-2" size={20} />
          실시간 KPI 모니터링
        </h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{(kpiData.success_rate * 100).toFixed(1)}%</div>
            <div className="text-sm text-green-700">성공률</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">{kpiData.processing_time.toFixed(1)}초</div>
            <div className="text-sm text-blue-700">처리시간</div>
          </div>
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">{(kpiData.error_rate * 100).toFixed(1)}%</div>
            <div className="text-sm text-red-700">오류율</div>
          </div>
        </div>
      </div>

      {/* Auto-Triggers Alert */}
      {autoTriggers.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2 flex items-center text-yellow-800">
            <AlertTriangle className="mr-2" size={20} />
            자동 트리거 알림
          </h3>
          <ul className="space-y-1">
            {autoTriggers.map((trigger, index) => (
              <li key={index} className="text-yellow-700 text-sm">
                • {trigger}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Enhanced Summary Sections */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <CheckCircle className="mr-2" size={20} />
          AI 요약 결과 (신뢰도: {(confidence * 100).toFixed(1)}%)
        </h3>
        <ul className="space-y-2">
          {summaryReport.keyPoints.map((point, index) => (
            <li key={index} className="flex items-start">
              <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
              <span className="text-gray-700">{point}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center text-red-600">
          <AlertTriangle className="mr-2" size={20} />
          긴급 처리 사항
        </h3>
        <ul className="space-y-2">
          {summaryReport.urgentItems.map((item, index) => (
            <li key={index} className="flex items-start">
              <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
              <span className="text-gray-700">{item}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Enhanced Input Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <MessageCircle className="mr-2" size={20} />
          MACHO-GPT 대화 분석
        </h3>
        
        {!isInputMode ? (
          <div className="space-y-4">
            <p className="text-gray-600">
              WhatsApp 대화방에서 메시지를 복사하여 MACHO-GPT로 분석하세요.
            </p>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <span>현재 모드: <strong>{currentMode}</strong></span>
              <span>최소 신뢰도: <strong>{(modes[currentMode].confidence_min * 100).toFixed(0)}%</strong></span>
            </div>
            <button
              onClick={() => setIsInputMode(true)}
              className="bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 transition-colors flex items-center"
            >
              <MessageCircle className="mr-2" size={16} />
              MACHO-GPT 분석 시작
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                WhatsApp 대화 내용 (MACHO-GPT 처리)
              </label>
              <textarea
                value={manualInput}
                onChange={(e) => setManualInput(e.target.value)}
                placeholder="WhatsApp에서 대화 내용을 복사하여 여기에 붙여넣기 하세요...

MACHO-GPT가 다음 사항을 자동 분석합니다:
- 메시지 신뢰도 검증
- 긴급도 자동 분류
- 팀별 활동 요약
- 처리 시간 최적화
- 자동 트리거 생성"
                className="w-full h-40 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={processManualInput}
                disabled={isLoading}
                className={`${
                  isLoading 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-blue-500 hover:bg-blue-600'
                } text-white py-2 px-4 rounded-lg transition-colors flex items-center`}
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    MACHO-GPT 처리중...
                  </>
                ) : (
                  <>
                    <Zap className="mr-2" size={16} />
                    MACHO-GPT 분석 실행
                  </>
                )}
              </button>
              <button
                onClick={() => {
                  setIsInputMode(false);
                  setManualInput('');
                }}
                disabled={isLoading}
                className="bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400 transition-colors disabled:opacity-50"
              >
                취소
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Command Recommendations */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <Settings className="mr-2" size={20} />
          추천 명령어
        </h3>
        <div className="space-y-2">
          {summaryReport.triggers.map((trigger, index) => (
            <div key={index} className="bg-gray-50 p-2 rounded text-sm font-mono text-gray-700">
              {trigger}
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Enhanced Chat Rooms Tab
  const ChatRoomsTab = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">대화방 관리 (MACHO-GPT)</h2>
        <button
          onClick={() => setIsAddingRoom(true)}
          className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors flex items-center"
        >
          <Plus className="mr-1" size={16} />
          방 추가
        </button>
      </div>

      {/* Room addition form */}
      {isAddingRoom && (
        <div className="bg-white rounded-lg shadow p-4 border-2 border-green-200">
          <div className="flex gap-2">
            <input
              type="text"
              value={newRoomName}
              onChange={(e) => setNewRoomName(e.target.value)}
              placeholder="새 대화방 이름 입력"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              onKeyPress={(e) => e.key === 'Enter' && addChatRoom()}
            />
            <button
              onClick={addChatRoom}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors"
            >
              추가
            </button>
            <button
              onClick={() => {
                setIsAddingRoom(false);
                setNewRoomName('');
              }}
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition-colors"
            >
              취소
            </button>
          </div>
        </div>
      )}

      {/* Enhanced room list */}
      <div className="space-y-3">
        {chatRooms.map(room => (
          <div key={room.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${room.active ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                <div>
                  <h3 className="font-semibold flex items-center">
                    {room.name}
                    {room.priority === 'urgent' && (
                      <AlertTriangle className="ml-2 w-4 h-4 text-red-500" />
                    )}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {room.members}명 • {room.lastActivity} • 신뢰도: {(room.confidence * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  room.priority === 'critical' ? 'bg-red-100 text-red-800' :
                  room.priority === 'urgent' ? 'bg-orange-100 text-orange-800' :
                  room.priority === 'high' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {room.priority}
                </span>
                <button
                  onClick={() => toggleRoomActive(room.id)}
                  className={`px-3 py-1 rounded-full text-sm ${
                    room.active 
                      ? 'bg-green-100 text-green-700 hover:bg-green-200' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  } transition-colors`}
                >
                  {room.active ? '활성' : '비활성'}
                </button>
                <button
                  onClick={() => deleteRoom(room.id)}
                  className="text-red-500 hover:text-red-700 transition-colors p-1"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Enhanced Messages Tab
  const MessagesTab = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">메시지 분석 (MACHO-GPT)</h2>
      <div className="space-y-3">
        {messages.map(message => (
          <div key={message.id} className={`bg-white rounded-lg shadow p-4 ${
            message.urgent ? 'border-l-4 border-red-500' : ''
          }`}>
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-blue-600">{message.room}</span>
                <span className="text-gray-500">•</span>
                <span className="text-gray-700">{message.author}</span>
                {message.urgent && (
                  <AlertTriangle className="w-4 h-4 text-red-500" />
                )}
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-500">{message.time}</span>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  message.confidence >= 0.90 ? 'bg-green-100 text-green-800' :
                  message.confidence >= 0.80 ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {(message.confidence * 100).toFixed(0)}%
                </span>
              </div>
            </div>
            <p className="text-gray-800">{message.content}</p>
            {message.type === 'file' && (
              <div className="mt-2 inline-flex items-center text-sm text-blue-600">
                <FileText size={16} className="mr-1" />
                첨부파일 포함
              </div>
            )}
            {message.processed && (
              <div className="mt-2 inline-flex items-center text-sm text-green-600">
                <CheckCircle size={16} className="mr-1" />
                MACHO-GPT 처리 완료
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  // Helper functions
  const addChatRoom = () => {
    if (newRoomName.trim()) {
      const newRoom = {
        id: Date.now(),
        name: newRoomName,
        members: 0,
        lastActivity: '방금',
        active: true,
        priority: 'normal',
        confidence: 0.85
      };
      setChatRooms([...chatRooms, newRoom]);
      setNewRoomName('');
      setIsAddingRoom(false);
    }
  };

  const toggleRoomActive = (roomId) => {
    setChatRooms(chatRooms.map(room => 
      room.id === roomId ? { ...room, active: !room.active } : room
    ));
  };

  const deleteRoom = (roomId) => {
    setChatRooms(chatRooms.filter(room => room.id !== roomId));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* MACHO-GPT Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <MessageCircle className="text-green-500" size={32} />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">MACHO-GPT v3.4-mini</h1>
                <p className="text-sm text-gray-600">WhatsApp 업무 요약 시스템</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${
                  systemStatus === 'ACTIVE' ? 'bg-green-500' : 'bg-red-500'
                }`}></div>
                <span className="text-sm text-gray-600">시스템 상태: {systemStatus}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Zap className="text-blue-500" size={20} />
                <span className="text-sm text-gray-600">모드: {currentMode}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex space-x-8">
            {[
              { id: 'dashboard', label: 'MACHO-GPT 대시보드', icon: FileText },
              { id: 'rooms', label: '대화방 관리', icon: Users },
              { id: 'messages', label: '메시지 분석', icon: MessageCircle }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setCurrentTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-2 border-b-2 font-medium text-sm ${
                  currentTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon size={16} />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {currentTab === 'dashboard' && <DashboardTab />}
        {currentTab === 'rooms' && <ChatRoomsTab />}
        {currentTab === 'messages' && <MessagesTab />}
      </main>

      {/* Floating Action Button */}
      <div className="fixed bottom-6 right-6">
        <div className={`${modes[currentMode].color} text-white p-3 rounded-full shadow-lg`}>
          <Clock size={24} />
        </div>
        <div className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center">
          {summaryReport.urgentItems.length}
        </div>
      </div>
    </div>
  );
};

export default WhatsAppSummaryApp; 