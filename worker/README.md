# Chat Worker

Powers the "Ask me anything" chat on the website. The site sends the visitor's
messages here; this Worker calls Claude with your Anthropic API key, so the key
never appears in the public website code.

## One-time setup

1. Create an Anthropic API key at https://console.anthropic.com (Settings → API keys).
   Set a monthly spend limit there, since anyone visiting the site can use the chat.
2. Create a free Cloudflare account at https://dash.cloudflare.com/sign-up.
3. From this `worker` folder:

   ```bash
   npm install
   npx wrangler login
   npx wrangler secret put ANTHROPIC_API_KEY
   npx wrangler deploy
   ```

   `secret put` asks you to paste the key. `deploy` prints the Worker's address,
   for example `https://jurgen-chat.<your-subdomain>.workers.dev`.
4. Put that address in `assets/site.js` as `CHAT_ENDPOINT`, then commit and push.
   The chat button appears on every page once it is set.

## Notes

- Only requests from `https://gameovercheeseburger.github.io` are accepted
  (`ALLOWED_ORIGINS` in `src/index.js`). Add your own domain there if you get one.
- The assistant's knowledge of the company lives in the `SYSTEM` text in `src/index.js`.
- Model: Claude Opus 5.5 at low effort, replies capped at 1,024 tokens.
