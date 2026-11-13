export default function StatCard({ title, value, accent = 'primary' }) {
  return (
    <div className="col-md-3">
      <div className={`card border-0 shadow-sm h-100 bg-${accent}-subtle`}>
        <div className="card-body">
          <div className="text-uppercase small text-muted">{title}</div>
          <div className="display-6 fw-bold mt-2">{value}</div>
        </div>
      </div>
    </div>
  );
}
