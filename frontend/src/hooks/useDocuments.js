import { useState, useEffect, useCallback } from "react";
import { fetchDocuments, deleteDocument } from "../services/api";

export function useDocuments() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchDocuments();
      setDocuments(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const removeDocument = useCallback(
    async (id) => {
      try {
        await deleteDocument(id);
        setDocuments((prev) => prev.filter((d) => d.id !== id));
      } catch (err) {
        setError(err.message);
      }
    },
    []
  );

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { documents, loading, error, refresh, removeDocument };
}

