import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import axios from "axios";

function App() {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processingId, setProcessingId] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const API_URL = "http://localhost:8000";

  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API_URL}/suggestions/pending`);
      setSuggestions(res.data);
      setError(null);
    } catch (err) {
      setError("Erro ao carregar sugestões.");
    } finally {
      setLoading(false);
    }
  };

  const approve = async (id) => {
    try {
      setProcessingId(id);

      const response = await axios.post(
        `${API_URL}/suggestions/${id}/approve`
      );

      if (response.data.status === "approved") {
        setSuccessMessage("Sugestão aprovada com sucesso.");
        await fetchData();

        setTimeout(() => {
          setSuccessMessage(null);
        }, 3000);
      } else {
        alert("Não foi possível aprovar a sugestão.");
      }

    } catch (err) {
      alert("Erro ao aprovar sugestão.");
    } finally {
      setProcessingId(null);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const formatCurrency = (value) => {
    return Number(value).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  };

  return (
    <div style={{ maxWidth: "1000px", margin: "40px auto", fontFamily: "Arial" }}>
      <h1 style={{ marginBottom: "20px" }}>SmartPrice</h1>

      {successMessage && (
        <div
          style={{
            backgroundColor: "#d4edda",
            color: "#155724",
            padding: "10px",
            borderRadius: "4px",
            marginBottom: "20px"
          }}
        >
          {successMessage}
        </div>
      )}

      {loading && <p>Carregando sugestões...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && suggestions.length === 0 && (
        <p>Nenhuma sugestão pendente no momento.</p>
      )}

      {!loading && suggestions.length > 0 && (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
          }}
        >
          <thead>
            <tr style={{ backgroundColor: "#f5f5f5" }}>
              <th style={{ padding: "12px", textAlign: "left" }}>Produto</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Preço Atual</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Preço Sugerido</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Ação</th>
            </tr>
          </thead>
          <tbody>
            {suggestions.map((s) => (
              <tr key={s.id} style={{ borderTop: "1px solid #eee" }}>
                <td style={{ padding: "12px" }}>
                  <strong>{s.product_name}</strong>
                </td>
                <td style={{ padding: "12px" }}>
                  {formatCurrency(s.current_price)}
                </td>
                <td style={{ padding: "12px" }}>
                  {formatCurrency(s.suggested_price)}
                </td>
                <td style={{ padding: "12px" }}>
                  <button
                    onClick={() => approve(s.id)}
                    disabled={processingId === s.id}
                    style={{
                      padding: "8px 14px",
                      cursor: "pointer",
                      border: "none",
                      borderRadius: "4px",
                      backgroundColor:
                        processingId === s.id ? "#ccc" : "#4CAF50",
                      color: "#fff",
                    }}
                  >
                    {processingId === s.id ? "Aprovando..." : "Aprovar"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
