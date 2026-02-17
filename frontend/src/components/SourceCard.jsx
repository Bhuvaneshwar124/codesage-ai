export default function SourceCard({ source }) {
  return (
    <div className="bg-gray-50 dark:bg-gray-900 rounded-lg px-3 py-2 text-xs">
      <span className="font-mono text-sage-600 dark:text-sage-500">
        {source.source}
      </span>
      {source.text && (
        <p className="text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
          {source.text}
        </p>
      )}
    </div>
  );
}
