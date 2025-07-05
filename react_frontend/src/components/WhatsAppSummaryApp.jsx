import React, { useState, useEffect } from 'react';
import { MessageCircle, FileText, Clock, Users, Send, Settings, Plus, Trash2, Edit3, Download, Upload, CheckSquare, FileSignature, Wand2, Key, AlertTriangle, ListChecks } from 'lucide-react';

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
    { id: 1, name: '마케팅팀', members: 8, lastActivity: '10분 전', active: true },
    { id: 2, name: '개발팀', members: 12, lastActivity: '5분 전', active: true },
    { id: 3, name: '디자인팀', members: 6, lastActivity: '1시간 전', active: true },
    { id: 4, name: '영업팀', members: 15, lastActivity: '30분 전', active: true },
    { id: 5, name: '경영진', members: 4, lastActivity: '2시간 전', active: true }
  ]);

  // Enhanced Messages with MACHO-GPT Processing
  const [messages, setMessages] = useState([
    { id: 1, room: '마케팅팀', author: '김민수', content: '내일 캠페인 론칭 준비 완료했습니다.', time: '14:30', type: 'message' },
    { id: 2, room: '개발팀', author: '이영희', content: '버그 수정 완료. 테스트 부탁드립니다.', time: '14:25', type: 'message' },
    { id: 3, room: '디자인팀', author: '박철수', content: '새로운 로고 디자인 시안 공유드립니다.', time: '13:45', type: 'file' },
    { id: 4, room: '영업팀', author: '정미라', content: '오늘 고객 미팅 결과 보고서 작성 중입니다.', time: '14:00', type: 'message' },
    { id: 5, room: '경영진', author: '최대표', content: '월간 실적 검토 회의 일정 조정 필요', time: '12:30', type: 'message' }
  ]);

  // Enhanced Summary Report with MACHO-GPT Analytics
  const [summaryReport, setSummaryReport] = useState({
    date: '2025-07-05',
    totalMessages: 127,
    activeRooms: 5,
    keyPoints: [
      '마케팅팀: 신규 캠페인 론칭 준비 완료',
      '개발팀: 주요 버그 수정 완료, 테스트 진행 중',
      '디자인팀: 새로운 브랜드 로고 시안 검토 중',
      '영업팀: 고객 미팅 3건 진행, 긍정적 반응',
      '경영진: 월간 실적 검토 및 향후 계획 논의'
    ],
    urgentItems: [
      '개발팀: 긴급 버그 수정 요청 (우선순위 높음)',
      '영업팀: 대형 고객사 계약 검토 필요'
    ],
    todoItems: [],
    meetingMinutes: null
  });

  // MACHO-GPT State Management
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [newRoomName, setNewRoomName] = useState('');
  const [isAddingRoom, setIsAddingRoom] = useState(false);
  const [manualInput, setManualInput] = useState('');
  const [isInputMode, setIsInputMode] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isTodoLoading, setIsTodoLoading] = useState(false);
  const [isMinutesLoading, setIsMinutesLoading] = useState(false);

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

  useEffect(() => {
    const savedData = localStorage.getItem('whatsappSummaryData');
    if (savedData) {
      try {
        const data = JSON.parse(savedData);
        if (data.manualInput) setManualInput(data.manualInput);
        if (data.summaryReport) setSummaryReport(data.summaryReport);
      } catch (error) {
        console.warn('로컬 스토리지 데이터 로드 실패:', error);
      }
    }
  }, []);

  const saveToLocalStorage = () => {
    const dataToSave = {
      manualInput,
      summaryReport,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('whatsappSummaryData', JSON.stringify(dataToSave));
  };

  const callGeminiAPI = async (prompt, schema) => {
    const apiKey = "";
    if (!apiKey) {
      throw new Error('API 키가 설정되지 않았습니다.');
    }

    const payload = {
      contents: [{ role: "user", parts: [{ text: prompt }] }],
      generationConfig: {
        responseMimeType: "application/json",
        responseSchema: schema
      }
    };

    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API 요청 실패: ${response.statusText}`);
    }

    const result = await response.json();
    if (result.candidates && result.candidates[0].content && result.candidates[0].content.parts[0].text) {
      return JSON.parse(result.candidates[0].content.parts[0].text);
    } else {
      throw new Error('API 응답에서 유효한 데이터를 찾을 수 없습니다.');
    }
  };

  const createBasicSummary = (text) => {
    const lines = text.split('\n').filter(line => line.trim());
    const messageCount = lines.length;
    
    const urgentKeywords = ['긴급', 'urgent', '중요', 'immediate', '빠르게', '즉시', '오늘까지', '내일까지'];
    
    const keyPoints = [];
    const urgentItems = [];

    lines.forEach(line => {
      const lowerLine = line.toLowerCase();
      
      const hasUrgent = urgentKeywords.some(keyword => 
        lowerLine.includes(keyword) || line.includes(keyword)
      );
      
      if (hasUrgent && urgentItems.length < 5) {
        urgentItems.push(line.length > 100 ? line.substring(0, 100) + '...' : line);
      } else if (keyPoints.length < 10) {
        keyPoints.push(line.length > 100 ? line.substring(0, 100) + '...' : line);
      }
    });

    return {
      keyPoints: keyPoints.length > 0 ? keyPoints : ['입력된 대화 내용을 확인해주세요.'],
      urgentItems: urgentItems.length > 0 ? urgentItems : ['긴급 사항이 발견되지 않았습니다.'],
      totalMessages: messageCount
    };
  };

  const processManualInput = async () => {
    if (!manualInput.trim()) {
      alert('메시지 내용을 입력해주세요.');
      return;
    }

    setIsLoading(true);
    const basicSummary = createBasicSummary(manualInput);

    try {
      const prompt = `다음 WhatsApp 대화 내용을 분석하여 주요 내용과 긴급 처리 사항을 요약해주세요. 응답은 반드시 한국어로 해주세요.\n\n대화 내용:\n---\n${manualInput}\n---\n\n다음 JSON 형식으로만 응답해주세요:\n{"keyPoints": ["주요 활동 요약 (3~5개)"], "urgentItems": ["긴급 처리 사항 (1~3개)"]}`;
      
      const schema = {
        type: "OBJECT",
        properties: {
          "keyPoints": { type: "ARRAY", items: { type: "STRING" } },
          "urgentItems": { type: "ARRAY", items: { type: "STRING" } }
        },
        required: ["keyPoints", "urgentItems"]
      };

      const aiSummary = await callGeminiAPI(prompt, schema);
      
      setSummaryReport(prev => ({
        ...prev,
        keyPoints: aiSummary.keyPoints || basicSummary.keyPoints,
        urgentItems: aiSummary.urgentItems || basicSummary.urgentItems,
        totalMessages: basicSummary.totalMessages
      }));
      
      setIsInputMode(false);
      alert('AI 요약이 성공적으로 생성되었습니다!');
      
    } catch (error) {
      console.warn('AI 요약 실패, 기본 요약 사용:', error);
      
      setSummaryReport(prev => ({
        ...prev,
        keyPoints: basicSummary.keyPoints,
        urgentItems: basicSummary.urgentItems,
        totalMessages: basicSummary.totalMessages
      }));
      
      setIsInputMode(false);
      alert('기본 키워드 분석으로 대화 내용을 정리했습니다.');
    }

    setIsLoading(false);
    saveToLocalStorage();
  };

  const generateTodoList = async () => {
    if (!manualInput.trim()) {
      alert('먼저 대화 내용을 입력하고 요약을 생성해주세요.');
      return;
    }

    setIsTodoLoading(true);

    try {
      const prompt = `다음 대화 내용에서 실행 가능한 할 일(Action Item)을 추출해주세요. 각 할 일에 대해 담당자가 언급되었다면 함께 찾아주세요. 응답은 반드시 한국어로 해주세요.\n\n대화 내용:\n---\n${manualInput}\n---\n\n다음 JSON 형식으로만 응답해주세요:\n{"tasks": [{"task": "실행할 구체적인 내용", "person": "담당자 이름 (없으면 '미지정')"}, ...]}`;
      
      const schema = {
        type: "OBJECT",
        properties: {
          "tasks": {
            type: "ARRAY",
            items: {
              type: "OBJECT",
              properties: {
                "task": { type: "STRING" },
                "person": { type: "STRING" }
              },
              required: ["task", "person"]
            }
          }
        },
        required: ["tasks"]
      };

      const todoData = await callGeminiAPI(prompt, schema);
      
      setSummaryReport(prev => ({
        ...prev,
        todoItems: todoData.tasks || []
      }));
      
      alert('AI 할 일 목록이 생성되었습니다!');
      
    } catch (error) {
      console.error('할 일 목록 생성 실패:', error);
      alert('AI 할 일 목록 생성에 실패했습니다. 기본 기능을 사용합니다.');
      
      const lines = manualInput.split('\n').filter(line => line.trim());
      const taskKeywords = ['해야', '필요', '요청', '부탁', '완료', '진행', '준비'];
      const basicTasks = lines
        .filter(line => taskKeywords.some(keyword => line.includes(keyword)))
        .slice(0, 5)
        .map(line => ({
          task: line.length > 80 ? line.substring(0, 80) + '...' : line,
          person: '미지정'
        }));
      
      setSummaryReport(prev => ({
        ...prev,
        todoItems: basicTasks
      }));
    }

    setIsTodoLoading(false);
    saveToLocalStorage();
  };

  const generateMeetingMinutes = async () => {
    if (!manualInput.trim()) {
      alert('먼저 대화 내용을 입력하고 요약을 생성해주세요.');
      return;
    }

    setIsMinutesLoading(true);

    try {
      const prompt = `다음 대화 내용을 바탕으로 공식적인 회의록 초안을 작성해주세요. 참석자, 주요 안건, 논의 내용 요약, 결정 사항, 실행 항목(Action Item)을 포함해주세요. 응답은 반드시 한국어로 해주세요.\n\n대화 내용:\n---\n${manualInput}\n---\n\n다음 JSON 형식으로만 응답해주세요:\n{"title": "회의 제목", "attendees": ["참석자 이름 목록"], "agenda": ["주요 안건 목록"], "discussion": "전체 논의 내용 요약", "decisions": ["주요 결정 사항 목록"], "actionItems": [{"task": "실행할 내용", "owner": "담당자"}]}`;
      
      const schema = {
        type: "OBJECT",
        properties: {
          "title": { type: "STRING" },
          "attendees": { type: "ARRAY", items: { type: "STRING" } },
          "agenda": { type: "ARRAY", items: { type: "STRING" } },
          "discussion": { type: "STRING" },
          "decisions": { type: "ARRAY", items: { type: "STRING" } },
          "actionItems": {
            type: "ARRAY",
            items: {
              type: "OBJECT",
              properties: { "task": { type: "STRING" }, "owner": { type: "STRING" } },
              required: ["task", "owner"]
            }
          }
        },
        required: ["title", "attendees", "agenda", "discussion", "decisions", "actionItems"]
      };

      const minutesData = await callGeminiAPI(prompt, schema);
      
      setSummaryReport(prev => ({
        ...prev,
        meetingMinutes: minutesData
      }));
      
      alert('AI 회의록 초안이 생성되었습니다!');
      
    } catch (error) {
      console.error('회의록 생성 실패:', error);
      alert('AI 회의록 생성에 실패했습니다.');
    }

    setIsMinutesLoading(false);
    saveToLocalStorage();
  };

  const downloadReport = () => {
    const reportData = {
      ...summaryReport,
      manualInput,
      generatedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `whatsapp-summary-${summaryReport.date}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const uploadReport = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          if (data.manualInput !== undefined) {
            setManualInput(data.manualInput);
            setSummaryReport(data);
            alert('데이터를 성공적으로 불러왔습니다.');
          } else {
            alert('올바른 형식의 파일이 아닙니다.');
          }
        } catch (error) {
          alert('파일을 읽는 중 오류가 발생했습니다.');
        }
      };
      reader.readAsText(file);
    } else {
      alert('JSON 파일을 선택해주세요.');
    }
    event.target.value = null;
  };

  const clearAll = () => {
    if (window.confirm('정말로 모든 내용을 지우시겠습니까?')) {
      setManualInput('');
      setSummaryReport({
        date: new Date().toISOString().split('T')[0],
        totalMessages: 0,
        activeRooms: 5,
        keyPoints: [],
        urgentItems: [],
        todoItems: [],
        meetingMinutes: null
      });
      setIsInputMode(false);
      localStorage.removeItem('whatsappSummaryData');
    }
  };

  const addChatRoom = () => {
    if (newRoomName.trim()) {
      const newRoom = {
        id: Date.now(),
        name: newRoomName,
        members: 0,
        lastActivity: '방금',
        active: true
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

  const DashboardTab = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-green-500 via-blue-500 to-purple-600 text-white p-8 rounded-xl relative overflow-hidden">
        <div className="absolute inset-0 bg-white opacity-10 transform -skew-y-1"></div>
        <div className="relative z-10">
          <h1 className="text-3xl font-bold mb-2 flex items-center">
            <Wand2 className="mr-3" size={32} />
            WhatsApp 업무 요약 도우미 ✨
          </h1>
          <p className="text-green-100 text-lg">AI로 WhatsApp 대화를 분석하여 요약, 할 일, 회의록까지 한번에!</p>
          <div className="grid grid-cols-3 gap-4 mt-6">
            <div className="text-center bg-white bg-opacity-20 rounded-lg p-4">
              <div className="text-2xl font-bold">{summaryReport.totalMessages}</div>
              <div className="text-sm text-green-100">총 메시지</div>
            </div>
            <div className="text-center bg-white bg-opacity-20 rounded-lg p-4">
              <div className="text-2xl font-bold">{summaryReport.activeRooms}</div>
              <div className="text-sm text-green-100">활성 대화방</div>
            </div>
            <div className="text-center bg-white bg-opacity-20 rounded-lg p-4">
              <div className="text-2xl font-bold">{summaryReport.urgentItems.length}</div>
              <div className="text-sm text-green-100">긴급 사항</div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-xl font-bold mb-4 flex items-center">
          <MessageCircle className="mr-3 text-green-500" size={24} />
          WhatsApp 대화 내용 입력
        </h3>
        
        {!isInputMode ? (
          <div className="space-y-4">
            <p className="text-gray-600">
              WhatsApp 대화방에서 메시지를 복사하여 붙여넣기 하세요.
            </p>
            <button
              onClick={() => setIsInputMode(true)}
              className="bg-green-500 text-white py-3 px-6 rounded-lg hover:bg-green-600 transition-colors flex items-center font-semibold"
            >
              <Edit3 className="mr-2" size={18} />
              대화 내용 입력하기
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                WhatsApp 대화 내용 (복사-붙여넣기)
              </label>
              <textarea
                value={manualInput}
                onChange={(e) => setManualInput(e.target.value)}
                placeholder={`예시:\n[2025. 7. 5. 오전 9:15] 김민수: 마케팅팀 신규 캠페인 론칭 준비 완료.\n[2025. 7. 5. 오전 9:20] 이영희: 개발팀 주요 버그 수정 완료, 테스트 진행 중.\n[2025. 7. 5. 오전 9:25] 박철수: 디자인팀 새로운 브랜드 로고 시안 검토 요청드립니다.`}
                className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
              />
            </div>
            <div className="flex gap-3">
              <button
                onClick={processManualInput}
                disabled={isLoading}
                className={`${
                  isLoading 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-blue-500 hover:bg-blue-600'
                } text-white py-2 px-6 rounded-lg transition-colors flex items-center font-semibold`}
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    분석 중...
                  </>
                ) : (
                  <>
                    <Wand2 className="mr-2" size={16} />
                    ✨ 요약 생성
                  </>
                )}
              </button>
              <button
                onClick={() => {
                  setIsInputMode(false);
                }}
                disabled={isLoading}
                className="bg-gray-400 text-white py-2 px-4 rounded-lg hover:bg-gray-500 transition-colors disabled:opacity-50"
              >
                취소
              </button>
            </div>
          </div>
        )}
      </div>

      {summaryReport.keyPoints.length > 0 && (
        <>
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <Wand2 className="mr-2 text-purple-500" size={20} />
              AI 추가 기능
            </h3>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={generateTodoList}
                disabled={isTodoLoading}
                className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center font-semibold"
              >
                {isTodoLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    생성 중...
                  </>
                ) : (
                  <>
                    <CheckSquare className="mr-2" size={16} />
                    ✨ 할 일 목록 추출
                  </>
                )}
              </button>
              <button
                onClick={generateMeetingMinutes}
                disabled={isMinutesLoading}
                className="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors flex items-center font-semibold"
              >
                {isMinutesLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    생성 중...
                  </>
                ) : (
                  <>
                    <FileSignature className="mr-2" size={16} />
                    ✨ 회의록 초안 작성
                  </>
                )}
              </button>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <h3 className="text-xl font-bold mb-4 flex items-center border-b pb-2">
              <Key className="mr-3 text-blue-500" size={24} />
              주요 내용 요약
            </h3>
            <ul className="space-y-3">
              {summaryReport.keyPoints.map((point, index) => (
                <li key={index} className="flex items-start">
                  <span className="w-3 h-3 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span className="text-gray-700 leading-relaxed">{point}</span>
                </li>
              ))}
            </ul>
          </div>

          {summaryReport.urgentItems.length > 0 && (
            <div className="bg-white rounded-xl shadow-lg p-6 border border-red-200">
              <h3 className="text-xl font-bold mb-4 flex items-center text-red-600 border-b pb-2">
                <AlertTriangle className="mr-3" size={24} />
                긴급 처리 사항
              </h3>
              <ul className="space-y-3">
                {summaryReport.urgentItems.map((item, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-3 h-3 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    <span className="text-gray-700 leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {summaryReport.todoItems && summaryReport.todoItems.length > 0 && (
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h3 className="text-xl font-bold mb-4 flex items-center border-b pb-2">
                <ListChecks className="mr-3 text-indigo-500" size={24} />
                ✨ AI 추천 할 일 목록
              </h3>
              <div className="space-y-3">
                {summaryReport.todoItems.map((item, index) => (
                  <div key={index} className="flex items-start p-3 rounded-lg hover:bg-indigo-50 transition-colors">
                    <input 
                      type="checkbox" 
                      className="mt-1 mr-3 h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                    />
                    <div className="flex-1">
                      <span className="text-gray-800">{item.task}</span>
                      <span className="text-xs ml-2 font-semibold text-white bg-indigo-400 px-2 py-0.5 rounded-full">
                        {item.person}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {summaryReport.meetingMinutes && (
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h3 className="text-xl font-bold mb-4 flex items-center border-b pb-2">
                <FileSignature className="mr-3 text-teal-500" size={24} />
                ✨ AI 회의록 초안
              </h3>
              <div className="prose prose-sm max-w-none bg-gray-50 p-4 rounded-md border">
                <h4 className="font-bold">회의 제목: {summaryReport.meetingMinutes.title}</h4>
                <p><strong>참석자:</strong> {summaryReport.meetingMinutes.attendees.join(', ')}</p>
                <p><strong>주요 안건:</strong></p>
                <ul className="list-disc pl-5">
                  {summaryReport.meetingMinutes.agenda.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
                <p className="mt-4"><strong>논의 내용:</strong><br />{summaryReport.meetingMinutes.discussion}</p>
                <p className="mt-4"><strong>결정 사항:</strong></p>
                <ul className="list-disc pl-5">
                  {summaryReport.meetingMinutes.decisions.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
                <p className="mt-4"><strong>실행 항목:</strong></p>
                <ul className="list-disc pl-5">
                  {summaryReport.meetingMinutes.actionItems.map((item, index) => (
                    <li key={index}>{item.task} (담당: {item.owner})</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <Settings className="mr-2 text-gray-500" size={20} />
              데이터 관리
            </h3>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={downloadReport}
                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center"
              >
                <Download className="mr-2" size={16} />
                파일로 저장
              </button>
              <label className="bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600 transition-colors cursor-pointer flex items-center">
                <Upload className="mr-2" size={16} />
                파일 불러오기
                <input
                  type="file"
                  onChange={uploadReport}
                  accept=".json"
                  className="hidden"
                />
              </label>
              <button
                onClick={clearAll}
                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors flex items-center"
              >
                <Trash2 className="mr-2" size={16} />
                전체 초기화
              </button>
            </div>
          </div>
        </>
      )}

      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
        <p className="text-yellow-800 text-sm">
          <strong>참고:</strong> AI 기능이 작동하지 않을 경우, 기본 키워드 분석으로 전환됩니다. 
          정확한 분석을 위해 대화 내용에 날짜, 시간, 발신자 이름이 포함되도록 복사해주세요.
        </p>
      </div>
    </div>
  );

  const ChatRoomsTab = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">대화방 관리</h2>
        <button
          onClick={() => setIsAddingRoom(true)}
          className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors flex items-center"
        >
          <Plus className="mr-1" size={16} />
          방 추가
        </button>
      </div>

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

      <div className="space-y-3">
        {chatRooms.map(room => (
          <div key={room.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${room.active ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                <div>
                  <h3 className="font-semibold">{room.name}</h3>
                  <p className="text-sm text-gray-600">{room.members}명 • {room.lastActivity}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
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

  const MessagesTab = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">최근 메시지</h2>
      <div className="space-y-3">
        {messages.map(message => (
          <div key={message.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-blue-600">{message.room}</span>
                <span className="text-gray-500">•</span>
                <span className="text-gray-700">{message.author}</span>
              </div>
              <span className="text-sm text-gray-500">{message.time}</span>
            </div>
            <p className="text-gray-800">{message.content}</p>
            {message.type === 'file' && (
              <div className="mt-2 inline-flex items-center text-sm text-blue-600">
                <FileText size={16} className="mr-1" />
                첨부파일 포함
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <MessageCircle className="text-green-500" size={32} />
              <h1 className="text-2xl font-bold text-gray-900">WhatsApp 업무 요약</h1>
            </div>
            <div className="flex items-center space-x-2">
              <Settings className="text-gray-500" size={20} />
              <span className="text-sm text-gray-600">자동 요약 ON</span>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex space-x-8">
            {[
              { id: 'dashboard', label: '대시보드', icon: FileText },
              { id: 'rooms', label: '대화방 관리', icon: Users },
              { id: 'messages', label: '메시지', icon: MessageCircle }
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

      <main className="max-w-4xl mx-auto px-4 py-8">
        {currentTab === 'dashboard' && <DashboardTab />}
        {currentTab === 'rooms' && <ChatRoomsTab />}
        {currentTab === 'messages' && <MessagesTab />}
      </main>

      <div className="fixed bottom-6 right-6">
        <div className="bg-blue-500 text-white p-3 rounded-full shadow-lg">
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