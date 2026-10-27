// Chat proxy for the Jurgen Software Solutions website.
// The site calls this Worker; the Worker calls Claude with the secret API key,
// so the key never reaches the browser.
import Anthropic from "@anthropic-ai/sdk";

const ALLOWED_ORIGINS = ["https://gameovercheeseburger.github.io"];
const MAX_TURNS = 20;
const MAX_CHARS = 2000;

const SYSTEM = `You are the website assistant for Jurgen Software Solutions, a custom software firm owned by Patrik Santiago. Visitors chat with you from the company website.

About the company:
- Services: custom software development (C#/.NET, Java/Spring Boot, Python, Node.js); AI and automation (LLM integration, OpenAI and Claude APIs, agentic workflows, Python automation); web and front-end (React, TypeScript, custom CMS); APIs and systems integration (REST, SOAP, GraphQL, Kafka, RabbitMQ, ERP integrations); cloud and DevOps (AWS, Azure, Oracle Cloud, OpenShift, Docker, CI/CD); data, BI and reporting (Power BI, ETL pipelines, SSIS, AWS Glue, Crystal Reports); database design (SQL Server, Oracle, PostgreSQL, MySQL); legacy modernization; security (OAuth, JWT, encryption, secure coding); testing and quality; support and maintenance; IT consulting and analysis.
- Industries: oil and gas, retail, ERP, finance, banking, insurance and enterprise reporting.
- Way of working: Agile delivery in short iterations with a working demo at every step. Clients work directly with the owner and engineers.
- Owner: Patrik Santiago, Founder and Owner, full-stack software engineer with 5+ years at IBM, Infor and Accenture. Diploma in Software Development (SAIT) and B.S. Computer Engineering (Adamson University). Certifications include IBM Generative & Agentic AI Foundation, AWS Generative AI Essentials and Oracle Cloud Infrastructure AI Foundations Associate.
- Contact: patrik.j.santiago@gmail.com, or the "Request a quote" button on the website.

How to answer:
- Be friendly, clear and brief: usually two to four short sentences. Write plain text with no Markdown, headings or bullet symbols.
- You may answer general technology questions, then relate them to how the company can help when it fits.
- Never quote prices, timelines or guarantees. Say they depend on the project and suggest the "Request a quote" button or emailing patrik.j.santiago@gmail.com.
- If you do not know something about the company, say so and point to the email address. Do not invent clients, projects or facts.`;

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders(origin) },
  });
}

function cleanMessages(input) {
  if (!Array.isArray(input) || input.length === 0) return null;
  const turns = input.slice(-MAX_TURNS).map((m) => ({
    role: m && m.role === "assistant" ? "assistant" : "user",
    content: String((m && m.content) || "").slice(0, MAX_CHARS),
  }));
  // The conversation must start and end with the visitor.
  while (turns.length && turns[0].role !== "user") turns.shift();
  if (!turns.length || turns[turns.length - 1].role !== "user") return null;
  if (turns.some((t) => !t.content.trim())) return null;
  return turns;
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }
    if (request.method !== "POST") {
      return json({ error: "Use POST." }, 405, origin);
    }
    if (!ALLOWED_ORIGINS.includes(origin)) {
      return json({ error: "This chat only works from the company website." }, 403, origin);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: "Invalid request." }, 400, origin);
    }
    const messages = cleanMessages(body.messages);
    if (!messages) return json({ error: "Invalid conversation." }, 400, origin);

    const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
    try {
      const response = await client.beta.messages.create({
        model: "claude-opus-5-5",
        max_tokens: 1024, // short website replies; caps cost per message
        system: SYSTEM,
        output_config: { effort: "low" },
        betas: ["server-side-fallback-2026-07-01"],
        fallbacks: "default",
        messages,
      });

      if (response.stop_reason === "refusal") {
        return json({ reply: "Sorry, I can't help with that. For anything about our services, email patrik.j.santiago@gmail.com." }, 200, origin);
      }
      const reply = response.content
        .filter((block) => block.type === "text")
        .map((block) => block.text)
        .join("")
        .trim();
      return json({ reply: reply || "Sorry, I didn't catch that. Could you rephrase?" }, 200, origin);
    } catch (err) {
      if (err instanceof Anthropic.RateLimitError) {
        return json({ error: "The assistant is busy. Please try again in a minute." }, 429, origin);
      }
      if (err instanceof Anthropic.APIStatusError) {
        console.error("Claude API error", err.status, err.message);
        return json({ error: "The assistant is unavailable right now." }, 502, origin);
      }
      if (err instanceof Anthropic.APIConnectionError) {
        return json({ error: "The assistant could not be reached. Please try again." }, 502, origin);
      }
      throw err;
    }
  },
};
