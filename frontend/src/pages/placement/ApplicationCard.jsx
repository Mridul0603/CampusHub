export default function ApplicationCard({ application, stageColors, stageLabels, onEdit, onDelete }) {
  const formatDate = (d) => d ? new Date(d).toLocaleDateString("en-IN", {
    day: "numeric", month: "short", year: "numeric"
  }) : null;

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-sm transition-shadow">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <h3 className="font-semibold text-gray-900">{application.company_name}</h3>
            <span className={`text-xs font-medium px-2.5 py-0.5 rounded-full border ${stageColors[application.stage]}`}>
              {stageLabels[application.stage]}
            </span>
          </div>
          <p className="text-sm text-gray-500">{application.role}</p>
          {application.applied_on && (
            <p className="text-xs text-gray-400 mt-1">Applied: {formatDate(application.applied_on)}</p>
          )}
          {application.notes && (
            <p className="text-sm text-gray-600 mt-2 bg-gray-50 rounded-lg px-3 py-2 border border-gray-100">
              {application.notes}
            </p>
          )}
        </div>

        <div className="flex gap-3 shrink-0">
          <button
            onClick={() => onEdit(application)}
            className="text-xs text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(application.id)}
            className="text-xs text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
