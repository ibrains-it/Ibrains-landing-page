// Netlify Serverless Function: POST /api/chat
// Netlify deployment handler for IBrains AI Assistant.

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

### CONTACT & WHATSAPP BUTTON LINKS:
- NEVER display plain text phone numbers or raw email addresses.
- When the user asks for contact information, to talk to a person, or for custom pricing, include interactive Markdown buttons/links:
  - 💬 **[Chat on WhatsApp](https://wa.me/919390425742?text=Hi%20IBrains!%20I%20was%20chatting%20with%20your%20website%20assistant)**
  - ✉️ **[Email Engineering Team](mailto:ibrains.it@gmail.com)**

### HUMAN CONSULTANT BEHAVIOR & LEAD CAPTURE:
- Act like a senior human AI solution architect: warm, persuasive, articulate.
- As the conversation progresses, naturally ask for their Name, Company/Project Idea, or Email so we can follow up with a tailored proposal.
`;

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
};

export const config = {
  path: "/api/chat"
};
