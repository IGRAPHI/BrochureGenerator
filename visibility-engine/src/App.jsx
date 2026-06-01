import { useState } from 'react';
import Sidebar from './layout/Sidebar.jsx';
import Header from './layout/Header.jsx';
import DashboardView from './views/DashboardView.jsx';
import AnalyzerView from './views/AnalyzerView.jsx';
import KeywordStrategyView from './views/KeywordStrategyView.jsx';
import CalendarView from './views/CalendarView.jsx';
import BlogGeneratorView from './views/BlogGeneratorView.jsx';
import LinkedInGeneratorView from './views/LinkedInGeneratorView.jsx';
import CaseStudyBuilderView from './views/CaseStudyBuilderView.jsx';
import PublishingQueueView from './views/PublishingQueueView.jsx';
import SettingsView from './views/SettingsView.jsx';

const VIEWS = {
  dashboard: DashboardView,
  analyzer:  AnalyzerView,
  strategy:  KeywordStrategyView,
  calendar:  CalendarView,
  blog:      BlogGeneratorView,
  linkedin:  LinkedInGeneratorView,
  casestudy: CaseStudyBuilderView,
  queue:     PublishingQueueView,
  settings:  SettingsView,
};

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileOpen, setMobileOpen] = useState(false);

  const View = VIEWS[activeTab] ?? DashboardView;

  return (
    <div className="flex h-screen bg-slate-50 font-sans selection:bg-blue-100 overflow-hidden">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        mobileOpen={mobileOpen}
        setMobileOpen={setMobileOpen}
      />

      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header activeTab={activeTab} setMobileOpen={setMobileOpen} />

        <div className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-[#F8FAFC]">
          <View key={activeTab} />
        </div>
      </main>
    </div>
  );
}
