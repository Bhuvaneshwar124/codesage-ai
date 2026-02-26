export default function LoadingSpinner({ size = "sm" }) {
  const sizeClass = size === "sm" ? "h-4 w-4" : size === "md" ? "h-5 w-5" : "h-6 w-6";
  return (
    <div className="flex items-center gap-1.5">
      <span className="w-1.5 h-1.5 bg-sage-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
      <span className="w-1.5 h-1.5 bg-sage-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
      <span className="w-1.5 h-1.5 bg-sage-500 rounded-full animate-bounce"></span>
    </div>
  );
}
