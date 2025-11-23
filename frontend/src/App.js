import { useState, useEffect } from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import { 
  Sun, 
  Moon, 
  ChevronRight, 
  Search, 
  Check, 
  X, 
  Video, 
  FileText, 
  BookOpen, 
  ExternalLink 
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Icon components - using inline SVG for consistent rendering
const IconCode = ({ size = 32, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color || "currentColor"} strokeWidth="2">
    <polyline points="16 18 22 12 16 6"></polyline>
    <polyline points="8 6 2 12 8 18"></polyline>
  </svg>
);

const IconShield = ({ size = 32, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color || "currentColor"} strokeWidth="2">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
  </svg>
);

const IconBrain = ({ size = 32, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color || "currentColor"} strokeWidth="2">
    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"></path>
    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"></path>
  </svg>
);

const IconChart = ({ size = 32, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color || "currentColor"} strokeWidth="2">
    <line x1="18" y1="20" x2="18" y2="10"></line>
    <line x1="12" y1="20" x2="12" y2="4"></line>
    <line x1="6" y1="20" x2="6" y2="14"></line>
  </svg>
);

const IconCube = ({ size = 32, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color || "currentColor"} strokeWidth="2">
    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
    <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
    <line x1="12" y1="22.08" x2="12" y2="12"></line>
  </svg>
);

const IconCloud = ({ size = 32, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color || "currentColor"} strokeWidth="2">
    <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"></path>
  </svg>
);

const ICON_MAP = {
  code: IconCode,
  shield: IconShield,
  brain: IconBrain,
  chart: IconChart,
  cube: IconCube,
  cloud: IconCloud
};

const RESOURCE_ICONS = {
  video: Video,
  article: FileText,
  course: BookOpen
};

const Home = () => {
  const [careerPaths, setCareerPaths] = useState([]);
  const [selectedPath, setSelectedPath] = useState(null);
  const [selectedMilestone, setSelectedMilestone] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isDark, setIsDark] = useState(true);
  const [userProgress, setUserProgress] = useState({});
  const [userId] = useState('demo-user');
  const [showWelcome, setShowWelcome] = useState(true);

  useEffect(() => {
    fetchCareerPaths();
  }, []);

  useEffect(() => {
    if (selectedPath) {
      fetchProgress(selectedPath.id);
    }
  }, [selectedPath]);

  const fetchCareerPaths = async () => {
    try {
      const response = await axios.get(`${API}/career-paths`);
      setCareerPaths(response.data);
    } catch (e) {
      console.error('Error fetching career paths:', e);
    }
  };

  const fetchProgress = async (pathId) => {
    try {
      const response = await axios.get(`${API}/progress/${userId}/${pathId}`);
      setUserProgress(response.data);
    } catch (e) {
      console.error('Error fetching progress:', e);
    }
  };

  const toggleMilestoneComplete = async (milestoneId) => {
    const isCompleted = userProgress.completed_milestones?.includes(milestoneId);
    
    try {
      await axios.post(`${API}/progress/${userId}/${selectedPath.id}`, {
        milestone_id: milestoneId,
        completed: !isCompleted
      });
      
      await fetchProgress(selectedPath.id);
    } catch (e) {
      console.error('Error updating progress:', e);
    }
  };

  const filteredPaths = careerPaths.filter(path => 
    path.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    path.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const calculateProgress = () => {
    if (!selectedPath || !userProgress.completed_milestones) return 0;
    return Math.round((userProgress.completed_milestones.length / selectedPath.milestones.length) * 100);
  };

  const totalDays = selectedPath?.milestones.reduce((sum, m) => sum + m.estimated_days, 0) || 0;
  const completedDays = selectedPath?.milestones
    .filter(m => userProgress.completed_milestones?.includes(m.id))
    .reduce((sum, m) => sum + m.estimated_days, 0) || 0;

  return (
    <div className={`app-container ${isDark ? 'dark' : 'light'}`}>
      {/* Theme Toggle */}
      <button
        data-testid="theme-toggle-btn"
        className="theme-toggle"
        onClick={() => setIsDark(!isDark)}
      >
        {isDark ? <Sun size={20} /> : <Moon size={20} />}
      </button>

      {/* Welcome Screen */}
      {showWelcome && !selectedPath && (
        <div className="welcome-screen">
          <div className="welcome-content">
            <div className="logo-pulse">
              <div className="pulse-ring"></div>
              <div className="pulse-ring delay-1"></div>
              <div className="pulse-ring delay-2"></div>
              <span className="logo-text">⚡</span>
            </div>
            <h1 className="welcome-title" data-testid="app-title">
              SUPERCHARGE
            </h1>
            <p className="welcome-subtitle">
              Your Interactive Career Journey Starts Here
            </p>
            <p className="welcome-description">
              Choose your path, unlock milestones, and level up your engineering career with curated resources and visual progress tracking
            </p>
            <Button
              data-testid="explore-paths-btn"
              className="explore-btn"
              onClick={() => setShowWelcome(false)}
            >
              Explore Career Paths
              <ChevronRight className="ml-2" size={20} />
            </Button>
          </div>
        </div>
      )}

      {/* Main Content */}
      {!showWelcome && (
        <div className="main-content">
          {/* Header */}
          <header className="app-header">
            <div className="header-content">
              <div className="logo-section">
                <span className="logo">⚡</span>
                <h2 className="app-name" data-testid="header-title">SUPERCHARGE</h2>
              </div>
              
              {!selectedPath && (
                <div className="search-container">
                  <Search className="search-icon" size={18} />
                  <Input
                    data-testid="search-input"
                    type="text"
                    placeholder="Search career paths..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="search-input"
                  />
                </div>
              )}

              {selectedPath && (
                <Button
                  data-testid="back-to-paths-btn"
                  variant="outline"
                  onClick={() => {
                    setSelectedPath(null);
                    setSelectedMilestone(null);
                  }}
                  className="back-btn"
                >
                  ← Back to Paths
                </Button>
              )}
            </div>
          </header>

          {/* Career Paths Grid */}
          {!selectedPath && (
            <div className="paths-grid">
              {filteredPaths.map((path) => {
                const IconComponent = ICON_MAP[path.icon];
                return (
                  <div
                    key={path.id}
                    data-testid={`career-path-card-${path.id}`}
                    className="path-card"
                    onClick={() => setSelectedPath(path)}
                    style={{ '--accent-color': path.color }}
                  >
                    <div className="path-icon" style={{ backgroundColor: path.color + '20' }}>
                      {IconComponent && <IconComponent size={32} color={path.color} />}
                    </div>
                    <h3 className="path-name">{path.name}</h3>
                    <p className="path-description">{path.description}</p>
                    <div className="path-stats">
                      <span className="stat-badge">
                        {path.milestones.length} Milestones
                      </span>
                      <span className="stat-badge">
                        {path.milestones.reduce((sum, m) => sum + m.estimated_days, 0)} Days
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Roadmap View */}
          {selectedPath && (
            <div className="roadmap-container">
              {/* Progress Header */}
              <div className="progress-header">
                <div className="path-info">
                  <div className="path-icon-large" style={{ backgroundColor: selectedPath.color + '20' }}>
                    {(() => {
                      const IconComponent = ICON_MAP[selectedPath.icon];
                      return IconComponent && <IconComponent size={40} color={selectedPath.color} />;
                    })()}
                  </div>
                  <div>
                    <h2 className="path-title" data-testid="selected-path-title">{selectedPath.name}</h2>
                    <p className="path-subtitle">{selectedPath.description}</p>
                  </div>
                </div>
                <div className="progress-stats">
                  <div className="stat-item">
                    <span className="stat-value">{calculateProgress()}%</span>
                    <span className="stat-label">Complete</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{completedDays}/{totalDays}</span>
                    <span className="stat-label">Days</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{userProgress.completed_milestones?.length || 0}/{selectedPath.milestones.length}</span>
                    <span className="stat-label">Milestones</span>
                  </div>
                </div>
              </div>

              <Progress value={calculateProgress()} className="progress-bar" />

              {/* Milestone Map */}
              <div className="milestone-map">
                <svg className="path-svg" viewBox="0 0 100 600" preserveAspectRatio="none">
                  <path
                    d="M 50 0 Q 80 100 50 200 Q 20 300 50 400 Q 80 500 50 600"
                    className="milestone-path"
                    strokeDasharray="1000"
                    strokeDashoffset={1000 - (calculateProgress() * 10)}
                  />
                </svg>

                <div className="milestones-list">
                  {selectedPath.milestones.map((milestone, index) => {
                    const isCompleted = userProgress.completed_milestones?.includes(milestone.id);
                    const isActive = selectedMilestone?.id === milestone.id;
                    
                    return (
                      <div
                        key={milestone.id}
                        data-testid={`milestone-${milestone.id}`}
                        className={`milestone-node ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`}
                        onClick={() => setSelectedMilestone(milestone)}
                        style={{
                          '--node-color': selectedPath.color,
                          animationDelay: `${index * 0.1}s`
                        }}
                      >
                        <div className="node-checkpoint">
                          {isCompleted ? (
                            <LucideIcons.Check size={20} className="check-icon" />
                          ) : (
                            <span className="node-number">{index + 1}</span>
                          )}
                        </div>
                        <div className="node-content">
                          <h4 className="node-title">{milestone.title}</h4>
                          <p className="node-description">{milestone.description}</p>
                          <div className="node-footer">
                            <span className="node-badge">{milestone.estimated_days} days</span>
                            <span className="node-badge">{milestone.resources.length} resources</span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* Milestone Detail Panel */}
          {selectedMilestone && (
            <div className="detail-overlay" onClick={() => setSelectedMilestone(null)}>
              <div className="detail-panel" onClick={(e) => e.stopPropagation()}>
                <button
                  data-testid="close-panel-btn"
                  className="close-panel"
                  onClick={() => setSelectedMilestone(null)}
                >
                  <LucideIcons.X size={24} />
                </button>

                <div className="panel-header">
                  <h3 className="panel-title" data-testid="milestone-detail-title">{selectedMilestone.title}</h3>
                  <p className="panel-description">{selectedMilestone.description}</p>
                  <div className="panel-meta">
                    <span className="meta-badge">📅 {selectedMilestone.estimated_days} days</span>
                    <span className="meta-badge">📚 {selectedMilestone.resources.length} resources</span>
                  </div>
                </div>

                <div className="completion-toggle">
                  <Button
                    data-testid="toggle-complete-btn"
                    className={`complete-btn ${userProgress.completed_milestones?.includes(selectedMilestone.id) ? 'completed' : ''}`}
                    onClick={() => toggleMilestoneComplete(selectedMilestone.id)}
                  >
                    {userProgress.completed_milestones?.includes(selectedMilestone.id) ? (
                      <><LucideIcons.Check size={18} className="mr-2" /> Completed</>
                    ) : (
                      <>Mark as Complete</>
                    )}
                  </Button>
                </div>

                <div className="resources-section">
                  <h4 className="resources-title">Learning Resources</h4>
                  <div className="resources-list">
                    {selectedMilestone.resources.map((resource, idx) => {
                      const ResourceIcon = RESOURCE_ICONS[resource.type];
                      return (
                        <a
                          key={idx}
                          href={resource.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="resource-card"
                          data-testid={`resource-${idx}`}
                        >
                          <div className="resource-icon">
                            {ResourceIcon && <ResourceIcon size={20} />}
                          </div>
                          <div className="resource-content">
                            <h5 className="resource-title">{resource.title}</h5>
                            <span className="resource-type">{resource.type}</span>
                          </div>
                          <LucideIcons.ExternalLink size={18} className="external-icon" />
                        </a>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;