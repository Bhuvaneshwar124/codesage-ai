import { useState } from "react";
import ChatInterface from "./components/ChatInterface";
import DocumentList from "./components/DocumentList";
import FileUpload from "./components/FileUpload";
import ThemeToggle from "./components/ThemeToggle";
import { useTheme } from "./hooks/useTheme";

export default function App() {
  const [activeTab, setActiveTab] = useState("chat");
  const { theme, toggleTheme } = useTheme();

  return (
    <div className={theme === "dark" ? "dark" : ""}>
      <div className="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 flex flex-col">
        {/* Header */}
        <header className="border-b border-gray-200 dark:border-gray-800 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-sage-600 dark:text-sage-500">
              🧠 CodeSage AI
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <nav className="flex gap-1">
              {["chat", "documents", "upload"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-colors ${
                    activeTab === tab
                      ? "bg-sage-100 dark:bg-sage-900 text-sage-700 dark:text-sage-200"
                      : "text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
                  }`}
                >
                  {tab}
                </button>
              ))}
            </nav>
            <ThemeToggle theme={theme} onToggle={toggleTheme} />
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 max-w-5xl w-full mx-auto p-6">
          {activeTab === "chat" && <ChatInterface />}
          {activeTab === "documents" && <DocumentList />}
          {activeTab === "upload" && <FileUpload />}
        </main>
      </div>
    </div>
  );
}
