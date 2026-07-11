export default function StatsBar({ stats }) {
  const cards = [
    { label: "Total Applied", value: stats.total, color: "text-gray-900", bg: "bg-gray-50" },
    { label: "In Progress", value: stats.in_progress, color: "text-blue-600", bg: "bg-blue-50" },
    { label: "Offers", value: stats.offers, color: "text-green-600", bg: "bg-green-50" },
    { label: "Rejections", value: stats.rejections, color: "text-red-500", bg: "bg-red-50" },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {cards.map((card) => (
        <div key={card.label} className={`${card.bg} rounded-xl p-4 border border-gray-100`}>
          <p className="text-sm text-gray-500 font-medium">{card.label}</p>
          <p className={`text-3xl font-bold mt-1 ${card.color}`}>{card.value}</p>
        </div>
      ))}
    </div>
  );
}
