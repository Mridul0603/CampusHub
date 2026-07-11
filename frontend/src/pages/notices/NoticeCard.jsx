import { useState } from "react";
import { noticesApi } from "../../api/notices";

const CATEGORY_COLORS = {
  general: "bg-gray-100 text-gray-700",
  academic: "bg-blue-100 text-blue-700",
  placement: "bg-green-100 text-green-700",
  club: "bg-purple-100 text-purple-700",
  exam: "bg-red-100 text-red-700",
};

export default function NoticeCard({ notice, currentUser, onDelete, onUpdated }) {
  const [expanded, setExpanded] = useState(false);
  const [summary, setSummary] = useState("");
  const [summarizing, setSummarizing] = useState(false);
  const [summaryError, setSummaryError] = useState("");

  const canModify =
    currentUser?.id === notice.author.id || currentUser?.role === "admin";

  const handleSummarize = async () => {
    if (summary) {
      // Already fetched — just toggle
      setSummary("");
      return;
    }
    setSummarizing(true);
    setSummaryError("");
    try {
      const res = await noticesApi.summarize(notice.id);
      setSummary(res.data.summary);
    } catch (err) {
      setSummaryError("Could not generate summary. Please try again.");
    } finally {
      setSummarizing(false);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString("en-IN", {
      day: "numeric", month: "short", year: "numeric",
    });
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-sm transition-shadow">
      {/* Top row */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-2">
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${CATEGORY_COLORS[notice.category]}`}>
              {notice.category.charAt(0).toUpperCase() + notice.category.slice(1)}
            </span>
            {notice.department && (
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                {notice.department}
              </span>
            )}
            {notice.semester && (
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                Sem {notice.semester}
              </span>
            )}
          </div>
          <h3 className="font-semibold text-gray-900 text-base leading-snug">{notice.title}</h3>
          <p className="text-xs text-gray-400 mt-1">
            By {notice.author.full_name} · {formatDate(notice.created_at)}
          </p>
        </div>

        {/* Actions */}
        {canModify && (
          <button
            onClick={() => onDelete(notice.id)}
            className="text-xs text-red-500 hover:text-red-700 shrink-0"
          >
            Delete
          </button>
        )}
      </div>

      {/* Content */}
      <div className="mt-3">
        <p className={`text-sm text-gray-600 leading-relaxed ${!expanded ? "line-clamp-3" : ""}`}>
          {notice.content}
        </p>
        {notice.content.length > 200 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-indigo-600 mt-1 hover:text-indigo-700"
          >
            {expanded ? "Show less" : "Read more"}
          </button>
        )}
      </div>

      {/* AI Summary Section */}
      <div className="mt-4 pt-3 border-t border-gray-100">
        <button
          onClick={handleSummarize}
          disabled={summarizing}
          className="flex items-center gap-1.5 text-xs font-medium text-indigo-600 hover:text-indigo-700 disabled:opacity-50"
        >
          <span>✨</span>
          {summarizing ? "Summarizing..." : summary ? "Hide Summary" : "AI Summarize"}
        </button>

        {summaryError && (
          <p className="mt-2 text-xs text-red-500">{summaryError}</p>
        )}

        {summary && (
          <div className="mt-3 bg-indigo-50 rounded-lg p-3 border border-indigo-100">
            <p className="text-xs font-semibold text-indigo-700 mb-2">AI Summary</p>
            <div className="text-sm text-gray-700 whitespace-pre-line">{summary}</div>
          </div>
        )}
      </div>
    </div>
  );
}
