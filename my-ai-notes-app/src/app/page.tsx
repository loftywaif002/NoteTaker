'use client';

import { TextInput, TextArea, Button } from '@carbon/react'
import { useState } from 'react'

export default function Home() {

  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [result, setResult] = useState< any | null>(null)

const handleSubmit = async () => {
  setLoading(true);
  setResult(""); // Reset
  try {
    const res = await fetch("/api/notes", {
      method: "POST",
      body: JSON.stringify({ title, content, tags: [], auto_summarize: true }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await res.json();
    const final_data = (typeof data?.summary === 'string' && data.summary.length > 0)
      ? data.summary
      : "Sorry, model returned an empty response.";
    let index = 0;
    const typeNextChar = () => {
      if (index < final_data.length) {
        const char = final_data[index];
        index++;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        setResult((prev: any) => prev + (char || ''));
        setTimeout(typeNextChar, 40);
      }
    };
    typeNextChar();
  } catch (error) {
    console.error("Error submitting:", error);
  } finally {
    setLoading(false);
  }
};


  return (
    <main style={{ maxWidth: 600, margin: '3rem auto', padding: '1rem' }}>
      <h1>AI Note Creator</h1>
      <TextInput
        id="note-title"
        labelText="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <TextArea
        id="note-content"
        labelText="Content"
        rows={5}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        style={{ marginTop: '1rem' }}
      />
      <div style={{ marginTop: '1rem' }}>
        {loading ? (
          <p>Creating new note....</p>
        ) : (
          <Button onClick={handleSubmit}>Create Note</Button>
        )}
      </div>
      {result && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Summary</h3>
          <p>{result}</p>
        </div>
      )}
    </main>
  )
}
