import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import SourceCard from "./SourceCard";

export default function Message({ role, content, sources, streaming }) {
  const isUser = role === "user";

  return (
    <div
      className={`flex gap-3 animate-slide-up ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {/* Avatar */}
      {!isUser && (
        <div className="flex-shrink-0 w-7 h-7 rounded-lg bg-gradient-to-br from-sage-500 to-sage-700 flex items-center justify-center mt-1 shadow-sm">
          <span className="text-white text-xs font-bold">CS</span>
        </div>
      )}

      <div
        className={`max-w-[85%] sm:max-w-[75%] ${
          isUser
            ? "rounded-2xl rounded-tr-md px-4 py-2.5 bg-sage-600 text-white shadow-sm"
            : "rounded-2xl rounded-tl-md"
        }`}
      >
        {isUser ? (
          <p className="text-sm leading-relaxed">{content}</p>
        ) : (
          <div className="bg-white dark:bg-gray-800/80 border border-gray-100 dark:border-gray-700/50 rounded-2xl rounded-tl-md px-4 py-3 shadow-sm">
            <div className={`prose-chat text-sm leading-relaxed text-gray-800 dark:text-gray-200 ${streaming ? "typing-cursor" : ""}`}>
              <ReactMarkdown
                components={{
                  code({ node, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || "");
                    const isInline = !match && !String(children).includes("\n");
                    return !isInline && match ? (
                      <div className="relative group">
                        <div className="absolute top-2 right-2 text-[10px] font-mono text-gray-400 uppercase opacity-0 group-hover:opacity-100 transition-opacity">
                          {match[1]}
                        </div>
                        <SyntaxHighlighter
                          style={oneDark}
                          language={match[1]}
                          PreTag="div"
                          className="!rounded-xl !text-xs !my-2.5"
                          customStyle={{ padding: "1rem", fontSize: "0.8rem" }}
                          {...props}
                        >
                          {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                      </div>
                    ) : (
                      <code
                        className="bg-sage-50 dark:bg-sage-900/30 text-sage-700 dark:text-sage-300 px-1.5 py-0.5 rounded-md text-xs font-mono"
                        {...props}
                      >
                        {children}
                      </code>
                    );
                  },
                }}
              >
                {content}
              </ReactMarkdown>
            </div>

            {sources && sources.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700/50">
                <p className="text-[10px] font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500 mb-2">
                  Sources ({sources.length})
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {sources.map((src, i) => (
                    <SourceCard key={i} source={src} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="flex-shrink-0 w-7 h-7 rounded-lg bg-gray-200 dark:bg-gray-700 flex items-center justify-center mt-1">
          <svg className="w-3.5 h-3.5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
          </svg>
        </div>
      )}
    </div>
  );
}
