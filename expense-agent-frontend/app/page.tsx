"use client";

import { useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    const text = question.trim();

    if (!text || loading) return;

    setQuestion("");
    setError("");

    setMessages((previous) => [
      ...previous,
      { role: "user", content: text },
    ]);

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/assistant/chat/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: text,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "The request failed."
        );
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main
      style={{
        maxWidth: "700px",
        margin: "40px auto",
        padding: "20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>AI Expense Assistant</h1>

      <p>
        Ask questions about your recorded expenses.
      </p>

      <section
        aria-live="polite"
        style={{
          minHeight: "300px",
          border: "1px solid #ddd",
          borderRadius: "8px",
          padding: "16px",
          marginBottom: "16px",
        }}
      >
        {messages.map((message, index) => (
          <div key={index} style={{ marginBottom: "16px" }}>
            <strong>
              {message.role === "user"
                ? "You"
                : "Assistant"}
              :
            </strong>

            <p>{message.content}</p>
          </div>
        ))}

        {loading && <p>Assistant is thinking...</p>}

        {error && (
          <p role="alert">
            Error: {error}
          </p>
        )}
      </section>

      <form onSubmit={sendMessage}>
        <input
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder="Ask about your expenses..."
          maxLength={1000}
          disabled={loading}
          style={{
            width: "100%",
            padding: "12px",
            boxSizing: "border-box",
            marginBottom: "12px",
          }}
        />

        <button
          type="submit"
          disabled={loading || !question.trim()}
          style={{
            padding: "10px 20px",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </form>
    </main>
  );
}