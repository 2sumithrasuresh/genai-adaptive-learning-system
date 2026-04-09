import { useState } from "react";

const API = "http://localhost:8000";

export default function App() {
  const [studentId] = useState("student_" + Math.random().toString(36).slice(2, 8));
  const [topic, setTopic] = useState("");
  const [started, setStarted] = useState(false);
  const [difficulty, setDifficulty] = useState(1);
  const [question, setQuestion] = useState("");
  const [expectedAnswer, setExpectedAnswer] = useState("");
  const [studentAnswer, setStudentAnswer] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [mastery, setMastery] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [questionCount, setQuestionCount] = useState(0);
  const [explanation, setExplanation] = useState("");

  // Step 2: Generate a question
  async function fetchQuestion(diff) {
    setLoading(true);
    setError("");
    setEvaluation(null);
    setStudentAnswer("");
    try {
      const res = await fetch(`${API}/generate-question`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, difficulty: diff })
      });
      const data = await res.json();
      setQuestion(data.question);
      setExpectedAnswer(data.expected_answer);
      setQuestionCount(c => c + 1);
    } catch {
      setError("Could not generate question. Is the backend running?");
    }
    setLoading(false);
  }

  // Start session — fetch first question
  async function handleStart() {
    if (!topic.trim()) return;
    setStarted(true);
    setDifficulty(1);
    setMastery(0);
    setQuestionCount(0);
    await fetchQuestion(1);
  }

  // Steps 4–6: Evaluate → Update → Next Action
  async function handleSubmit() {
    if (!studentAnswer.trim()) return;
    setLoading(true);
    setError("");
    try {
      // Step 4: evaluate-answer
      const evalRes = await fetch(`${API}/evaluate-answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, expected_answer: expectedAnswer, student_answer: studentAnswer })
      });
      const evalData = await evalRes.json();
      setEvaluation(evalData);

      // Step 5: update-student
      const updateRes = await fetch(`${API}/update-student`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: studentId, topic, evaluation_result: evalData })
      });
      const updatedState = await updateRes.json();
      setMastery(updatedState.mastery_score);

      // Step 6: next-action
      const actionRes = await fetch(`${API}/next-action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student_id: studentId,
            topic,
            question,
            student_answer: studentAnswer,
            expected_answer: expectedAnswer,
            evaluation_result: evalData
        })
    });
      const action = await actionRes.json();
      setDifficulty(action.next_difficulty || 1);
      setExplanation(action.explanation || "");
    } catch {
      setError("Something went wrong. Check the backend.");
    }
    setLoading(false);
  }

  // Step 8: Repeat — fetch next question
  async function handleNext() {
    await fetchQuestion(difficulty);
  }

  const masteryPercent = Math.round((mastery || 0) * 100);

  const resultColor = {
    correct: "#22c55e",
    partial: "#f59e0b",
    wrong: "#ef4444"
  };

  return (
    <div style={{ minHeight: "100vh", background: "#f1f5f9", fontFamily: "sans-serif", padding: "2rem" }}>
      <div style={{ maxWidth: 640, margin: "0 auto" }}>

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2rem" }}>
          <h1 style={{ fontSize: "1.8rem", fontWeight: 700, color: "#1e293b" }}>
            Adaptive Learning Engine
          </h1>
          <p style={{ color: "#64748b" }}>Person 1 — Core Loop</p>
        </div>

        {/* Topic Input */}
        {!started && (
          <div style={{ background: "white", borderRadius: 12, padding: "2rem", boxShadow: "0 2px 8px rgba(0,0,0,0.08)" }}>
            <h2 style={{ marginBottom: "1rem", color: "#1e293b" }}>Enter a Topic</h2>
            <input
              value={topic}
              onChange={e => setTopic(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleStart()}
              placeholder="e.g. Photosynthesis, Deadlocks, Newton's Laws"
              style={{
                width: "100%", padding: "0.75rem 1rem", fontSize: "1rem",
                border: "1.5px solid #e2e8f0", borderRadius: 8, outline: "none",
                boxSizing: "border-box"
              }}
            />
            <button
              onClick={handleStart}
              disabled={!topic.trim()}
              style={{
                marginTop: "1rem", width: "100%", padding: "0.75rem",
                background: topic.trim() ? "#3b82f6" : "#cbd5e1",
                color: "white", border: "none", borderRadius: 8,
                fontSize: "1rem", fontWeight: 600, cursor: topic.trim() ? "pointer" : "not-allowed"
              }}
            >
              Start Session
            </button>
          </div>
        )}

        {/* Session UI */}
        {started && (
          <>
            {/* Stats bar */}
            <div style={{
              display: "flex", gap: "1rem", marginBottom: "1rem"
            }}>
              {[
                { label: "Topic", value: topic },
                { label: "Difficulty", value: `${difficulty} / 5` },
                { label: "Questions", value: questionCount },
                { label: "Mastery", value: `${masteryPercent}%` }
              ].map(s => (
                <div key={s.label} style={{
                  flex: 1, background: "white", borderRadius: 10, padding: "0.75rem",
                  textAlign: "center", boxShadow: "0 1px 4px rgba(0,0,0,0.06)"
                }}>
                  <div style={{ fontSize: "0.7rem", color: "#94a3b8", textTransform: "uppercase", fontWeight: 600 }}>{s.label}</div>
                  <div style={{ fontSize: "1.1rem", fontWeight: 700, color: "#1e293b" }}>{s.value}</div>
                </div>
              ))}
            </div>

            {/* Mastery bar */}
            <div style={{ background: "white", borderRadius: 10, padding: "0.75rem 1rem", marginBottom: "1rem", boxShadow: "0 1px 4px rgba(0,0,0,0.06)" }}>
              <div style={{ fontSize: "0.75rem", color: "#64748b", marginBottom: 4 }}>Mastery Progress</div>
              <div style={{ background: "#e2e8f0", borderRadius: 99, height: 10 }}>
                <div style={{
                  width: `${masteryPercent}%`, background: masteryPercent >= 80 ? "#22c55e" : masteryPercent >= 50 ? "#f59e0b" : "#3b82f6",
                  height: "100%", borderRadius: 99, transition: "width 0.5s"
                }} />
              </div>
            </div>

            {/* Question card */}
            <div style={{ background: "white", borderRadius: 12, padding: "1.5rem", boxShadow: "0 2px 8px rgba(0,0,0,0.08)", marginBottom: "1rem" }}>
              {loading && !question ? (
                <p style={{ color: "#94a3b8" }}>Generating question...</p>
              ) : (
                <>
                  <div style={{ fontSize: "0.75rem", color: "#94a3b8", fontWeight: 600, marginBottom: 8 }}>
                    QUESTION {questionCount} · DIFFICULTY {difficulty}
                  </div>
                  <p style={{ fontSize: "1.1rem", color: "#1e293b", fontWeight: 500, marginBottom: "1.25rem" }}>
                    {question}
                  </p>

                  {/* Answer input — only show if not yet evaluated */}
                  {!evaluation && (
                    <>
                      <textarea
                        value={studentAnswer}
                        onChange={e => setStudentAnswer(e.target.value)}
                        placeholder="Type your answer here..."
                        rows={3}
                        style={{
                          width: "100%", padding: "0.75rem", fontSize: "0.95rem",
                          border: "1.5px solid #e2e8f0", borderRadius: 8,
                          outline: "none", resize: "vertical", boxSizing: "border-box"
                        }}
                      />
                      <button
                        onClick={handleSubmit}
                        disabled={loading || !studentAnswer.trim()}
                        style={{
                          marginTop: "0.75rem", width: "100%", padding: "0.75rem",
                          background: studentAnswer.trim() ? "#3b82f6" : "#cbd5e1",
                          color: "white", border: "none", borderRadius: 8,
                          fontSize: "1rem", fontWeight: 600,
                          cursor: studentAnswer.trim() ? "pointer" : "not-allowed"
                        }}
                      >
                        {loading ? "Evaluating..." : "Submit Answer"}
                      </button>
                    </>
                  )}

                  {/* Evaluation result */}
                  {evaluation && (
                    <div style={{
                      marginTop: "1rem", padding: "1rem", borderRadius: 8,
                      background: resultColor[evaluation.correctness] + "18",
                      border: `1.5px solid ${resultColor[evaluation.correctness]}`
                    }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                        <span style={{ fontWeight: 700, color: resultColor[evaluation.correctness], textTransform: "uppercase" }}>
                          {evaluation.correctness}
                        </span>
                        <span style={{ color: "#64748b", fontSize: "0.9rem" }}>
                          Score: {Math.round(evaluation.score * 100)}%
                        </span>
                      </div>
                      {evaluation.mistake_type !== "none" && (
                        <p style={{ color: "#64748b", fontSize: "0.85rem", margin: 0 }}>
                          Mistake type: <strong>{evaluation.mistake_type}</strong>
                        </p>
                      )}
                      <p style={{ color: "#475569", fontSize: "0.85rem", marginTop: 6, marginBottom: 0 }}>
                        <strong>Expected:</strong> {expectedAnswer}
                      </p>
                        {explanation && (
  <div style={{
    marginTop: "1rem",
    padding: "1rem",
    background: "#eff6ff",
    borderRadius: 8,
    fontSize: "0.9rem",
    color: "#1e40af"
  }}>
    <strong>Explanation:</strong>
    <p>{explanation}</p>
  </div>
)}

                      <button
                        onClick={handleNext}
                        disabled={loading}
                        style={{
                          marginTop: "1rem", width: "100%", padding: "0.65rem",
                          background: "#3b82f6", color: "white", border: "none",
                          borderRadius: 8, fontSize: "0.95rem", fontWeight: 600, cursor: "pointer"
                        }}
                      >
                        {loading ? "Loading..." : "Next Question →"}
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>

            {error && (
              <div style={{ background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 8, padding: "0.75rem", color: "#dc2626" }}>
                {error}
              </div>
            )}

            {/* Mastery complete */}
            {mastery >= 0.9 && (
              <div style={{ background: "#f0fdf4", border: "1.5px solid #22c55e", borderRadius: 12, padding: "1.5rem", textAlign: "center" }}>
                <div style={{ fontSize: "2rem" }}>🏆</div>
                <h3 style={{ color: "#15803d", margin: "0.5rem 0" }}>Mastery Achieved!</h3>
                <p style={{ color: "#166534", margin: 0 }}>You've mastered {topic}!</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
