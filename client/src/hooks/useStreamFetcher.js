import { useState } from "react";

export const useStreamFetcher = (apiUrl) => {
  const [streamData, setStreamData] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const fetchStream = async (endpoint, body) => {
    if (isStreaming) return;

    setIsStreaming(true);

    try {
      const response = await fetch(`${apiUrl}/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.body) {
        throw new Error("Readable stream not supported in response.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        setStreamData((prev) => [...prev, chunk]);
      }
    } catch (error) {
      console.error("Error fetching stream:", error);
    } finally {
      setIsStreaming(false);
    }
  };

  return { streamData, isStreaming, fetchStream };
};
