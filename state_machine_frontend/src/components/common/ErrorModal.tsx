import { useError } from "../../context/ErrorContext";

export const ErrorModal = () => {
  const { errorMessage, clearError } = useError();

  if (!errorMessage) return null;

  return (
    <div style={{
      position: "fixed",
      inset: 0,
      backgroundColor: "rgba(0,0,0,0.4)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 9999,
    }}>
      <div style={{
        background: "white",
        borderRadius: 8,
        padding: "28px 32px",
        minWidth: 400,
        maxWidth: 560,
        boxShadow: "0 8px 24px rgba(0,0,0,0.12)",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 14 }}>
          <span style={{ fontWeight: 600, fontSize: 15, color: "#1a1a18" }}>Error</span>
          <button
            onClick={clearError}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              fontSize: 18,
              lineHeight: 1,
              color: "#6b6b68",
              padding: "0 0 0 16px",
            }}
            aria-label="Cerrar"
          >
            ×
          </button>
        </div>
        <p style={{ color: "#6b6b68", fontSize: 14, lineHeight: 1.6, marginBottom: 20 }}>
          {errorMessage}
        </p>
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button
            onClick={clearError}
            style={{
              height: 34,
              padding: "0 16px",
              background: "#2563eb",
              color: "#fff",
              border: "none",
              borderRadius: 6,
              fontSize: 13,
              fontWeight: 500,
              cursor: "pointer",
            }}
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};
