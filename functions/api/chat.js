// Cloudflare Pages Function: POST /api/chat
// Keeps GROQ_API_KEY server-side (set it in Cloudflare Pages → Settings → Environment variables).
// Never call Groq directly from the browser — that would expose the key to anyone viewing source.

const SYSTEM_PROMPT = `You are the website assistant for IBrains, an AI automation studio.

IBrains builds AI systems end to end: conversational voice agents, industrial IoT systems, cross-platform mobile apps, and EduFlex (an adaptive learning platform for schools and training providers).

IBrains has already built and operates these production AI agents, available to adopt or adapt:
- HR Voice Agent (screening, policy questions, interview scheduling)
- Resume Shortlisting Agent (matches resumes against a job description)
- Technical Interviewer Agent (first-round technical interviews by voice)
- Coding Round Interviewer Agent (live coding interviews)
- System Design Interview Agent
- Screen Tracker Agent (watches a shared screen, answers questions about it conversationally)
- Real Estate Voice Agent (property Q&A, lead qualification)
- CRM Agent (call logging, CRM record updates)
- Ortho Medical Agent (patient calls for orthopedic clinics)
- Loan Agent (loan options and eligibility by voice)
- Insurance Agent (policy questions, claims, renewals)

Contact: WhatsApp +91 9390425742, email ibrains.it@gmail.com, LinkedIn at linkedin.com/company/ibrains-ai.

Answer visitor questions about IBrains' services, agents, and how engagements work, in 2-4 sentences, friendly and specific. Never invent client names, case studies, statistics, or exact pricing you were not given here — if asked about pricing or something you don't know, tell them to reach out directly via WhatsApp or email. If a question is unrelated to IBrains or automation, briefly redirect to what IBrains can help with.`;

export async function onRequestPost(context) {
  const { request, env } = context;

  if (!env.GROQ_API_KEY) {
    return new Response(JSON.stringify({ error: "Chat is not configured yet." }), {
      status: 500,
      headers: { "content-type": "application/json" },
    });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid request." }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }

  const incoming = Array.isArray(body.messages) ? body.messages : [];
  // Keep only the last few turns and cap message length — controls cost and blocks trivial abuse.
  const trimmed = incoming
    .slice(-8)
    .filter((m) => m && typeof m.content === "string" && (m.role === "user" || m.role === "assistant"))
    .map((m) => ({ role: m.role, content: m.content.slice(0, 1000) }));

  if (trimmed.length === 0) {
    return new Response(JSON.stringify({ error: "No message provided." }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }

  let groqResponse;
  try {
    groqResponse = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${env.GROQ_API_KEY}`,
      },
      body: JSON.stringify({
        model: "llama-3.3-70b-versatile",
        messages: [{ role: "system", content: SYSTEM_PROMPT }, ...trimmed],
        temperature: 0.4,
        max_tokens: 400,
      }),
    });
  } catch {
    return new Response(JSON.stringify({ error: "The assistant is temporarily unavailable." }), {
      status: 502,
      headers: { "content-type": "application/json" },
    });
  }

  if (!groqResponse.ok) {
    return new Response(JSON.stringify({ error: "The assistant is temporarily unavailable." }), {
      status: 502,
      headers: { "content-type": "application/json" },
    });
  }

  const data = await groqResponse.json();
  const reply = data.choices?.[0]?.message?.content?.trim() || "Sorry, I didn't catch that — could you rephrase?";

  return new Response(JSON.stringify({ reply }), {
    headers: { "content-type": "application/json" },
  });
}
