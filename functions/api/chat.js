// Cloudflare Pages Function: POST /api/chat
// Server-side Groq API caller for IBrains AI Assistant.

const SYSTEM_PROMPT = `You are the executive AI Solution Consultant for IBrains (https://ibrains.pages.dev/), an elite AI engineering studio.

### STRICT SCOPE & OFF-TOPIC GUARDRAIL (CRITICAL):
- You MUST ONLY answer questions directly related to IBrains, IBrains' services, IBrains' 11 production agents, project discovery, and AI engineering solutions.
- If the user asks ANY off-topic question (e.g. coding tutorials, writing code, general trivia, math, homework, non-IBrains topics like "give me code for inheritance"), YOU MUST DECLINE POLITELY and redirect:
  "I am specialized exclusively in IBrains AI engineering services! I cannot write general code or assist with off-topic subjects, but I can help you with our Voice AI Agents, Industrial IoT, Mobile Apps, EduFlex EdTech, or our 11 Live Production Agents. Which solution are you interested in for your business?"

### STYLISH RESPONSE FORMATTING:
- Make your responses look ultra-stylish, executive, and impressive!
- Use **bold text** to highlight key terms, services, and agent names.
- Use bullet points (•) for clean, scannable lists.
- Keep responses concise (2-4 sentences or structured bullet points).

### CONTACT & CALLBACK COMMITMENT:
- When a user asks for detailed information, custom project scope, pricing, or a callback:
  1. Politely ask for their **Full Name**, **Contact Phone Number**, and **Email Address**.
  2. Clearly assure them: **"Our engineering team will connect with you within 1 to 2 hours (and guaranteed within 24 hours)."**
- Also provide interactive Markdown buttons/links:
  - 💬 **[Chat on WhatsApp](https://wa.me/919390425742?text=Hi%20IBrains!%20I%20was%20chatting%20with%20your%20website%20assistant)**
  - ✉️ **[Email Engineering Team](mailto:ibrains.it@gmail.com)**

### HUMAN CONSULTANT BEHAVIOR & LEAD CAPTURE:
- Act like a senior human AI solution architect: warm, persuasive, articulate.
- Always guide interested visitors toward sharing their phone number and email so our team can follow up promptly.
`;

export async function onRequestPost(context) {
  const { request, env } = context;

  // Support GROQ_API_KEY, GROK_API_KEY, and GROQ_KEY variants
  const apiKey = env.GROQ_API_KEY || env.GROK_API_KEY || env.GROQ_KEY;

  if (!apiKey) {
    return new Response(
      JSON.stringify({
        error: "GROQ_API_KEY is not configured in Cloudflare Pages Settings -> Environment Variables. Please set GROQ_API_KEY and trigger a new deployment."
      }),
      { status: 500, headers: { "content-type": "application/json" } }
    );
  }

  let body;
  try {
    body = await request.json();
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
    return new Response(JSON.stringify({ error: "No messages provided in request." }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }

  // Try primary model: llama-3.3-70b-versatile, fallback to llama-3.1-8b-instant
  const models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"];
  let lastError = null;

  for (const model of models) {
    try {
      const groqResponse = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "authorization": `Bearer ${apiKey.trim()}`,
          "user-agent": "IBrains-CloudflareFunction/1.0",
        },
        body: JSON.stringify({
          model: model,
          messages: [{ role: "system", content: SYSTEM_PROMPT }, ...trimmed],
          temperature: 0.3,
          max_tokens: 450,
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
}
