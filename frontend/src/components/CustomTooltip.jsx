function CustomTooltip({ active, payload }) {
  if (!active || !payload) return null;

  return (
    <div style={{ background: "white", border: "1px solid #ccc", padding: "8px" }}>
      <p>{payload[0].value}</p>
    </div>
  );
}

export default CustomTooltip;