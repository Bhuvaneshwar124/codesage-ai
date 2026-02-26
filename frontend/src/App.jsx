import { useState } from "react";
import ChatInterface from "./components/ChatInterface";
import DocumentList from "./components/DocumentList";
import FileUpload from "./components/FileUpload";
import ThemeToggle from "./components/ThemeToggle";
import { useTheme } from "./hooks/useTheme";

const TABS = [
  { id: "chat", label: "Chat", icon: "💬" },
  { id: "documents", label: "Documents", icon: "📄" },
  { id: "upload", label: "Upload", icon: "📤" },
];

export default function App() {
  const [activeTab, setActiveTab] = useState("chat");
  const { theme, toggleTheme } = useTheme();

  return (
    <div className={theme === "dark" ? "dark" : ""}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 flex flex-col">
        {/* Header */}
        <header className="glass-header sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 border-b border-gray-200/60 dark:border-gray-800/60 px-4 sm:px-6 py-3">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sage-500 to-sage-700 flex items-center justify-center shadow-sm">
                <span className="text-white text-sm font-bold">CS</span>
              </div>
              <div>
                <h1 className="text-base font-bold text-gray-900 dark:text-white leading-tight">
                  CodeSage AI
                </h1>
                <p className="text-[10px] text-gray-400 dark:text-gray-500 leading-tight">
                  RAG-Powered Code Intelligence
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <nav className="flex bg-gray-100 dark:bg-gray-800 rounded-xl p-1 gap-0.5">
                {TABS.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                      activeTab === tab.id
                        ? "bg-white dark:bg-gray-700 text-sage-700 dark:text-sage-400 shadow-sm"
                        : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
                    }`}
                  >
                    <span className="text-sm">{tab.icon}</span>
                    <span className="hidden sm:inline">{tab.label}</span>
                  </button>
                ))}
              </nav>
              <div className="w-px h-6 bg-gray-200 dark:bg-gray-700 mx-1 hidden sm:block" />
              <ThemeToggle theme={theme} onToggle={toggleTheme} />
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 w-full">
          <div className="tab-content h-full" key={activeTab}>
            {activeTab === "chat" && <ChatInterface />}
            {activeTab === "documents" && (
              <div className="max-w-4xl mx-auto p-4 sm:p-6">
                <DocumentList />
              </div>
            )}
            {activeTab === "upload" && (
              <div className="max-w-3xl mx-auto p-4 sm:p-6">
                <FileUpload />
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
