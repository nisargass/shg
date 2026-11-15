import React, { useState } from 'react';
import {
  Mic,
  MicOff,
  Volume2,
  Sparkles,
  Send,
  Globe,
  FileText,
  CheckCircle2,
  HelpCircle,
  ShieldCheck
} from 'lucide-react';
import { assistantApi } from '../../api/services';

const VoiceAssistantPage = () => {
  const [language, setLanguage] = useState('English');
  const [isRecording, setIsRecording] = useState(false);
  const [inputText, setInputText] = useState('');
  const [chatMessages, setChatMessages] = useState([
    {
      sender: 'saathi',
      text: 'Namaste Sunita! I am your SHG Saathi Voice Assistant. You can speak or type in Kannada, Hindi, or English. How can I help you today?',
      sources: null
    }
  ]);
  const [loading, setLoading] = useState(false);

  const sampleQuestions = {
    English: [
      "How many bags have I completed?",
      "How much money will I receive?",
      "When is my deadline for the tote bags?",
      "Has my submitted batch been approved?",
      "Tell me about Lakhpati Didi scheme benefits"
    ],
    Hindi: [
      "मैंने अब तक कितने बैग पूरे किए हैं?",
      "मुझे इस हफ्ते कितना भुगतान मिलेगा?",
      "मेरे काम की अंतिम तिथि (डेडलाइन) कब है?",
      "लखपति दीदी योजना के क्या लाभ हैं?"
    ],
    Kannada: [
      "ನಾನು ಎಷ್ಟು ಬ್ಯಾಗ್‌ಗಳನ್ನು ಹೊಲಿದಿದ್ದೇನೆ?",
      "ನನಗೆ ಎಷ್ಟು ಕೂಲಿ ಹಣ ಬರುತ್ತದೆ?",
      "ನನ್ನ ಆರ್ಡರ್ ಮುಗಿಸುವ ಕೊನೆಯ ದಿನಾಂಕ ಯಾವಾಗ?",
      "ಲಖ್‌ಪತಿ ದೀದಿ ಯೋಜನೆಯ ಅನುಕೂಲಗಳೇನು?"
    ]
  };

  const handleSend = async (queryText) => {
    const query = queryText || inputText;
    if (!query.trim()) return;

    // Add user message
    const newHistory = [...chatMessages, { sender: 'user', text: query, sources: null }];
    setChatMessages(newHistory);
    setInputText('');
    setLoading(true);

    try {
      const response = await assistantApi.queryKnowledge(query, language);
      setChatMessages([
        ...newHistory,
        {
          sender: 'saathi',
          text: response.answer,
          sources: response.sources
        }
      ]);
      setLoading(false);
    } catch (e) {
      setLoading(false);
      setChatMessages([
        ...newHistory,
        {
          sender: 'saathi',
          text: "I could not retrieve verified records right now. Please check your network or consult your SHG Leader.",
          sources: null
        }
      ]);
    }
  };

  const handleToggleRecord = () => {
    if (!isRecording) {
      setIsRecording(true);
      // Simulate speech recognition
      setTimeout(() => {
        setIsRecording(false);
        const autoVoiceQuery = language === 'Kannada'
          ? "ನಾನು ಎಷ್ಟು ಬ್ಯಾಗ್‌ಗಳನ್ನು ಹೊಲಿದಿದ್ದೇನೆ?"
          : language === 'Hindi'
          ? "मैंने अब तक कितने बैग पूरे किए हैं?"
          : "How many bags have I completed so far?";
        handleSend(autoVoiceQuery);
      }, 2500);
    } else {
      setIsRecording(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="page-title">Voice & Multilingual AI Saathi</h1>
            <span className="demo-badge">Speech AI + RAG</span>
          </div>
          <p className="page-subtitle">
            Voice-first assistant in Kannada, Hindi, and English providing instant access to your task quotas, earnings, and SOPs
          </p>
        </div>
        <div className="page-actions">
          {/* Language Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: '#FFFFFF', padding: '6px 12px', borderRadius: '8px', border: '1px solid #DCE3E8' }}>
            <Globe size={16} color="#168B80" />
            <select
              style={{ border: 'none', background: 'transparent', fontWeight: '600', fontSize: '13px', outline: 'none', cursor: 'pointer' }}
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="English">English</option>
              <option value="Hindi">हिंदी (Hindi)</option>
              <option value="Kannada">ಕನ್ನಡ (Kannada)</option>
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-12" style={{ gap: '24px' }}>
        {/* Left Column: Interactive Chat Interface */}
        <div style={{ gridColumn: 'span 8' }}>
          <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '620px', padding: 0 }}>
            {/* Chat header */}
            <div style={{ padding: '16px 20px', borderBottom: '1px solid #EEF2F5', background: '#F8FAFC', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: '#168B80', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#FFFFFF' }}>
                  <Sparkles size={18} />
                </div>
                <div>
                  <strong style={{ fontSize: '14px', color: '#123B5D' }}>SHG Saathi Verified Assistant</strong>
                  <div style={{ fontSize: '11px', color: '#168B80' }}>&bull; Connected to FastAPI RAG Knowledge Base</div>
                </div>
              </div>
              <span className="badge badge-neutral" style={{ fontSize: '11px' }}>
                Active Language: {language}
              </span>
            </div>

            {/* Chat Messages Log */}
            <div style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {chatMessages.map((msg, idx) => (
                <div
                  key={idx}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                    maxWidth: '85%',
                    alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start'
                  }}
                >
                  <div
                    style={{
                      padding: '12px 16px',
                      borderRadius: '12px',
                      fontSize: '13.5px',
                      lineHeight: '1.5',
                      background: msg.sender === 'user' ? '#123B5D' : '#f1f8f7',
                      color: msg.sender === 'user' ? '#FFFFFF' : '#243746',
                      borderBottomRightRadius: msg.sender === 'user' ? '2px' : '12px',
                      borderBottomLeftRadius: msg.sender === 'saathi' ? '2px' : '12px',
                      boxShadow: 'var(--shadow-sm)'
                    }}
                  >
                    {msg.text}
                  </div>

                  {/* Referenced RAG Source Citation */}
                  {msg.sources && msg.sources.length > 0 && (
                    <div style={{ marginTop: '6px', background: '#FFFFFF', border: '1px solid #DCE3E8', borderRadius: '6px', padding: '8px 10px', fontSize: '11.5px', color: '#5e7386' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontWeight: '700', color: '#168B80', marginBottom: '2px' }}>
                        <FileText size={12} /> Verified Reference Source:
                      </div>
                      <strong>{msg.sources[0].title}</strong> ({msg.sources[0].category})
                      <div style={{ fontStyle: 'italic', marginTop: '2px' }}>"{msg.sources[0].excerpt}"</div>
                    </div>
                  )}
                </div>
              ))}
              {loading && (
                <div style={{ alignSelf: 'flex-start', background: '#f1f8f7', padding: '10px 16px', borderRadius: '12px', fontSize: '13px', color: '#168B80' }}>
                  Consulting SHG Knowledge Base...
                </div>
              )}
            </div>

            {/* Voice Recording / Input Bar */}
            <div style={{ padding: '16px', borderTop: '1px solid #EEF2F5', background: '#FFFFFF' }}>
              {isRecording && (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', padding: '8px', background: '#fef4e8', borderRadius: '6px', marginBottom: '10px', color: '#ab711b', fontSize: '12.5px', fontWeight: '700' }}>
                  <span className="demo-dot" style={{ backgroundColor: '#C83D43' }}></span>
                  Listening in {language}... Speak your question clearly into the microphone.
                </div>
              )}

              <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                <button
                  type="button"
                  className={`btn ${isRecording ? 'btn-danger' : 'btn-accent'}`}
                  style={{ width: '48px', height: '48px', borderRadius: '50%', padding: 0 }}
                  onClick={handleToggleRecord}
                  title="Click to speak (Voice Recognition)"
                >
                  <Mic size={22} color={isRecording ? '#FFFFFF' : '#000000'} />
                </button>

                <input
                  type="text"
                  className="form-control"
                  style={{ height: '48px', fontSize: '14px' }}
                  placeholder={`Type or ask something in ${language}...`}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                />

                <button
                  type="button"
                  className="btn btn-primary"
                  style={{ height: '48px', width: '48px', borderRadius: 'var(--radius-sm)', padding: 0 }}
                  onClick={() => handleSend()}
                >
                  <Send size={18} />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Suggested One-Tap Questions */}
        <div style={{ gridColumn: 'span 4' }}>
          <div className="card">
            <h3 style={{ fontSize: '15px', color: '#123B5D', marginBottom: '8px' }}>
              Suggested Voice Queries ({language})
            </h3>
            <p style={{ fontSize: '12px', color: '#5e7386', marginBottom: '16px' }}>
              Tap any button below to trigger the verified voice query instantly:
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {(sampleQuestions[language] || sampleQuestions.English).map((q, qIdx) => (
                <button
                  key={qIdx}
                  className="btn btn-outline"
                  style={{ textAlign: 'left', justifyContent: 'flex-start', fontSize: '12.5px', padding: '10px 12px', lineHeight: '1.3' }}
                  onClick={() => handleSend(q)}
                >
                  <Volume2 size={15} color="#168B80" style={{ flexShrink: 0 }} />
                  <span>{q}</span>
                </button>
              ))}
            </div>

            <div style={{ marginTop: '24px', padding: '14px', background: '#F8FAFC', borderRadius: '8px', border: '1px solid #EEF2F5', fontSize: '12px', color: '#5e7386' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#123B5D', fontWeight: '700', marginBottom: '4px' }}>
                <ShieldCheck size={16} color="#168B80" /> Privacy & Accuracy
              </div>
              All answers are sourced directly from verified workshop production ledgers and official NRLM government gazettes.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VoiceAssistantPage;

