import { useState, useEffect, useCallback } from "react";
import { placementApi } from "../../api/placement";
import StatsBar from "./StatsBar";
import ApplicationCard from "./ApplicationCard";
import ApplicationForm from "./ApplicationForm";

const STAGES = ["applied", "oa", "interview", "offer", "rejected"];

const STAGE_COLORS = {
  applied:   "bg-blue-100 text-blue-700 border-blue-200",
  oa:        "bg-yellow-100 text-yellow-700 border-yellow-200",
  interview: "bg-purple-100 text-purple-700 border-purple-200",
  offer:     "bg-green-100 text-green-700 border-green-200",
  rejected:  "bg-red-100 text-red-700 border-red-200",
};

const STAGE_LABELS = {
  applied: "Applied", oa: "Online Assessment",
  interview: "Interview", offer: "Offer", rejected: "Rejected",
};

export default function PlacementPage() {
  const [applications, setApplications] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editRecord, setEditRecord] = useState(null);
  const [filters, setFilters] = useState({ stage: "", search: "" });

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== "")
      );
      const [appsRes, statsRes] = await Promise.all([
        placementApi.getAll(params),
        placementApi.getStats(),
      ]);
      setApplications(appsRes.data);
      setStats(statsRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleDelete = async (id) => {
    if (!confirm("Delete this application?")) return;
    await placementApi.delete(id);
    fetchData();
  };

  const handleEdit = (record) => {
    setEditRecord(record);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditRecord(null);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Placement Hub</h1>
          <p className="text-gray-500 text-sm mt-1">Track your entire placement pipeline</p>
        </div>
        <button
          onClick={() => { setEditRecord(null); setShowForm(true); }}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
        >
          + Add Application
        </button>
      </div>

      {/* Stats Dashboard */}
      {stats && <StatsBar stats={stats} />}

      {/* Filters */}
      <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6 flex gap-3 flex-wrap">
        <input
          type="text"
          placeholder="Search company..."
          value={filters.search}
          onChange={(e) => setFilters((p) => ({ ...p, search: e.target.value }))}
          className="flex-1 min-w-[200px] px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <select
          value={filters.stage}
          onChange={(e) => setFilters((p) => ({ ...p, stage: e.target.value }))}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">All Stages</option>
          {STAGES.map((s) => (
            <option key={s} value={s}>{STAGE_LABELS[s]}</option>
          ))}
        </select>
      </div>

      {/* Applications List */}
      {loading ? (
        <div className="flex justify-center py-16">
          <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : applications.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <p className="text-4xl mb-3">📋</p>
          <p className="text-lg font-medium text-gray-600">No applications yet</p>
          <p className="text-sm mt-1">Add your first company application to get started</p>
        </div>
      ) : (
        <div className="space-y-3">
          {applications.map((app) => (
            <ApplicationCard
              key={app.id}
              application={app}
              stageColors={STAGE_COLORS}
              stageLabels={STAGE_LABELS}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Form Modal */}
      {showForm && (
        <ApplicationForm
          record={editRecord}
          stageLabels={STAGE_LABELS}
          onClose={handleFormClose}
          onSaved={() => { handleFormClose(); fetchData(); }}
        />
      )}
    </div>
  );
}
