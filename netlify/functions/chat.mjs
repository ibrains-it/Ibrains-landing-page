// Netlify Serverless Function: POST /api/chat
// Netlify deployment handler for IBrains AI Assistant.

const SYSTEM_PROMPT = `You are the website assistant for IBrains, an AI engineering studio (ibrains.pages.dev).

IBrains builds AI systems end-to-end: conversational voice agents, industrial IoT systems, cross-platform mobile apps, and EduFlex (an adaptive learning platform for schools and training providers).

IBrains has 11 live production AI agents available to adopt or adapt:
- HR Voice Agent (first-round screening, policy questions, scheduling)
- Resume Shortlisting Agent (parses resumes against a job description)
- Technical Interviewer Agent (voice-based technical interviews)
- Coding Round Interviewer Agent (live coding interviews)
- System Design Interview Agent (architecture & trade-offs)
- Screen Tracker Agent (watches shared screen, answers questions conversationally)
- Real Estate Voice Agent (property Q&A, lead qualification)
- CRM Agent (call logging, CRM record updates)
- Ortho Medical Agent (patient calls & appointment booking)
- Loan Agent (loan options & eligibility by voice)
- Insurance Agent (policy questions, claims, coverage)

Contact channels: WhatsApp (+91 9390425742), email (ibrains.it@gmail.com), LinkedIn (linkedin.com/company/ibrains-ai).

Answer visitor questions about IBrains' services, agents, and engagements in 2-4 friendly, specific sentences. Never invent unverified pricing or statistics — direct custom pricing queries to WhatsApp or email.`;

export default async (req, context) => {
  if (req.method !== "POST" && req.method !== "post") {
    return new Response(JSON.stringify({ error: "Method Not Allowed" }), {
      status: 405,
      headers: { "content-type": "application/json" },
    });
  }

  // Support Netlify / Node environment variables
  const apiKey = process.env.GROQ_API_KEY || process.env.GROK_API_KEY || process.env.GROQ_KEY;

  if (!apiKey) {
    return new Response(
      JSON.stringify({
        error: "GROQ_API_KEY is not configured in Netlify Environment Variables. Please set GROQ_API_KEY in Netlify Site Configuration -> Environment Variables and trigger a re-deploy."
      }),
      { status: 500, headers: { "content-type": "application/json" } }
    );
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON request body." }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }

  const incoming = Array.isArray(body.messages) ? body.messages : [];
  const trimmed = incoming
    .slice(-8)
    .filter((m) => m && typeof m.content === "string" && (m.role === "user" || m.role === "assistant"))
    .map((m) => ({ role: m.role, content: m.content.slice(0, 1000) }));

  if (trimmed.length === 0) {
    return new Response(JSON.stringify({ error: "No messages provided." }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }

  const models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"];
  let lastError = null;

  for (const model of models) {
    try {
      const groqResponse = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "authorization": `Bearer ${apiKey.trim()}`,
          "user-agent": "IBrains-NetlifyFunction/1.0",
        },
        body: JSON.stringify({
          model: model,
          messages: [{ role: "system", content: SYSTEM_PROMPT }, ...trimmed],
          temperature: 0.4,
          max_tokens: 400,
        }),
      });

      if (groqResponse.ok) {
        const data = await groqResponse.json();
        const reply = data.choices?.[0]?.message?.content?.trim();
        if (reply) {
          return new Response(JSON.stringify({ reply }), {
            headers: { "content-type": "application/json" },
          });
        }
      } else {
        const errText = await groqResponse.text();
        lastError = `Groq API (${model}) returned status ${groqResponse.status}: ${errText}`;
      }
    } catch (err) {
      lastError = `Fetch exception: ${err.message}`;
    }
  }

  return new Response(
    JSON.stringify({ error: lastError || "Failed to reach AI assistant service." }),
    { status: 502, headers: { "content-type": "application/json" } }
  );
};

export const config = {
  path: "/api/chat"
};
