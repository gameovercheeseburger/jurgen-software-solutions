// Shared behaviour for every page: header shadow, scroll reveals, quote form, copy email, chat.
(function () {
  var EMAIL = 'patrik.j.santiago@gmail.com';
  var FORM_ENDPOINT = 'https://formsubmit.co/ajax/' + EMAIL;
  // Set this to the Cloudflare Worker URL once it is deployed. The chat button stays hidden until then.
  var CHAT_ENDPOINT = '';

  document.documentElement.classList.add('js');

  /* Header shadow once the page scrolls */
  var header = document.querySelector('header.site');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Fade sections up as they come into view */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* Copy email button */
  var copyBtn = document.getElementById('copy-email');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      function done() { copyBtn.textContent = 'Copied'; setTimeout(function () { copyBtn.textContent = 'Copy email'; }, 1800); }
      function fallback() {
        var r = document.createRange(); r.selectNodeContents(document.getElementById('email'));
        var s = getSelection(); s.removeAllRanges(); s.addRange(r);
        copyBtn.textContent = 'Press Ctrl+C to copy';
      }
      try { navigator.clipboard.writeText(EMAIL).then(done, fallback); } catch (e) { fallback(); }
    });
  }

  /* Quote form: one template, used in the popup and on the Contact page */
  var formCount = 0;
  function formHTML() {
    var n = ++formCount;
    function id(name) { return 'q' + n + '-' + name; }
    return '' +
      '<form class="qform" novalidate>' +
      '<div class="field"><label for="' + id('first') + '">First name</label><input id="' + id('first') + '" name="First name" autocomplete="given-name" required></div>' +
      '<div class="field"><label for="' + id('last') + '">Last name</label><input id="' + id('last') + '" name="Last name" autocomplete="family-name" required></div>' +
      '<div class="field"><label for="' + id('email') + '">Email</label><input id="' + id('email') + '" name="email" type="email" autocomplete="email" required></div>' +
      '<div class="field"><label for="' + id('phone') + '">Phone <span class="opt">(optional)</span></label><input id="' + id('phone') + '" name="Phone" type="tel" autocomplete="tel"></div>' +
      '<div class="field full"><label for="' + id('subject') + '">Subject</label><input id="' + id('subject') + '" name="Subject" required></div>' +
      '<div class="field full"><label for="' + id('body') + '">Message</label><textarea id="' + id('body') + '" name="Message" required placeholder="What do you need built, and by when?"></textarea></div>' +
      '<div class="hp" aria-hidden="true"><label for="' + id('honey') + '">Leave empty</label><input id="' + id('honey') + '" name="_honey" tabindex="-1" autocomplete="off"></div>' +
      '<div class="form-actions full"><button type="submit" class="btn solid">Send request</button><p class="form-status" role="status" aria-live="polite"></p></div>' +
      '</form>' +
      '<div class="sent" hidden><h3>Thank you. Your request was sent.</h3><p class="muted sent-msg"></p><button type="button" class="btn solid again">Send another</button></div>';
  }

  function wireForm(root, onDone) {
    var form = root.querySelector('form');
    var sent = root.querySelector('.sent');
    var status = root.querySelector('.form-status');
    var send = form.querySelector('button[type=submit]');
    root.querySelector('.again').addEventListener('click', function () {
      if (onDone) { onDone(); return; }
      sent.hidden = true; form.hidden = false;
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        var bad = form.querySelector(':invalid');
        status.className = 'form-status err';
        status.textContent = bad && bad.type === 'email' && bad.value ? 'Enter a valid email address.' : 'Please fill in every required field.';
        if (bad) bad.focus();
        return;
      }
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      data._subject = 'Quote request: ' + data.Subject;
      data._replyto = data.email;
      data._template = 'table';
      data._captcha = 'false';
      send.disabled = true; send.textContent = 'Sending...';
      status.className = 'form-status'; status.textContent = '';
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!(res.ok && String(res.j.success) === 'true')) throw new Error(res.j.message || 'not sent');
          root.querySelector('.sent-msg').textContent = 'We will reply to ' + data.email + ' within one business day.';
          form.reset(); form.hidden = true; sent.hidden = false;
        })
        .catch(function () {
          status.className = 'form-status err';
          status.textContent = 'Your request could not be sent. Please try again, or email ' + EMAIL + ' directly.';
        })
        .then(function () { send.disabled = false; send.textContent = 'Send request'; });
    });
  }

  // Inline form on the Contact page
  document.querySelectorAll('[data-quote-form]').forEach(function (slot) {
    slot.innerHTML = formHTML();
    wireForm(slot);
  });

  // Popup form opened by every "Request a quote" button
  var dlg = document.createElement('dialog');
  dlg.className = 'quote-dlg';
  dlg.setAttribute('aria-labelledby', 'quote-title');
  dlg.innerHTML = '<div class="dlg-inner"><div class="dlg-head"><div style="display:grid;gap:6px"><span class="eyebrow">Request a quote</span><h2 id="quote-title">Tell us about your project</h2></div><button type="button" class="dlg-close" aria-label="Close">&times;</button></div><div class="dlg-body">' + formHTML() + '</div></div>';
  document.body.appendChild(dlg);
  var dlgBody = dlg.querySelector('.dlg-body');
  dlgBody.querySelector('.again').textContent = 'Close';
  wireForm(dlgBody, function () { dlg.close(); });
  dlg.querySelector('.dlg-close').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  document.querySelectorAll('[data-quote]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (typeof dlg.showModal !== 'function') return; // old browsers follow the link to the Contact page
      e.preventDefault();
      dlgBody.querySelector('form').hidden = false;
      dlgBody.querySelector('.sent').hidden = true;
      dlgBody.querySelector('.form-status').textContent = '';
      dlg.showModal();
      dlgBody.querySelector('input').focus();
    });
  });

  /* Ask-me-anything chat, powered by Claude through the Worker */
  if (!CHAT_ENDPOINT) return;
  var history = [];
  var fab = document.createElement('button');
  fab.type = 'button';
  fab.className = 'chat-fab';
  fab.setAttribute('aria-expanded', 'false');
  fab.innerHTML = '<span class="dot" aria-hidden="true"></span><span class="label">Ask me anything</span><span class="visually-hidden" style="position:absolute;left:-9999px">Open chat</span>';
  var panel = document.createElement('section');
  panel.className = 'chat-panel';
  panel.hidden = true;
  panel.setAttribute('aria-label', 'Chat with our assistant');
  panel.innerHTML = '<div class="chat-head"><div><strong>Ask me anything</strong><small>AI assistant · Powered by Claude</small></div><button type="button" class="dlg-close" aria-label="Close chat">&times;</button></div>' +
    '<div class="chat-log" aria-live="polite"></div>' +
    '<form class="chat-form"><label for="chat-input" style="position:absolute;left:-9999px">Your question</label><input id="chat-input" autocomplete="off" maxlength="2000" placeholder="Ask about our services..."><button type="submit" class="btn solid">Send</button></form>';
  document.body.appendChild(panel);
  document.body.appendChild(fab);
  var log = panel.querySelector('.chat-log');
  var input = panel.querySelector('input');
  var chatSend = panel.querySelector('.chat-form button');

  function add(text, cls) {
    var m = document.createElement('div');
    m.className = 'msg ' + cls;
    m.textContent = text;
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
    return m;
  }
  add('Hi! I can answer questions about Jurgen Software Solutions, our services, or your project idea. What would you like to know?', 'bot');

  function toggle(open) {
    panel.hidden = !open;
    fab.setAttribute('aria-expanded', String(open));
    if (open) input.focus();
  }
  fab.addEventListener('click', function () { toggle(panel.hidden); });
  panel.querySelector('.dlg-close').addEventListener('click', function () { toggle(false); fab.focus(); });

  panel.querySelector('.chat-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var text = input.value.trim();
    if (!text || chatSend.disabled) return;
    input.value = '';
    add(text, 'me');
    history.push({ role: 'user', content: text });
    var typing = add('Typing...', 'bot typing');
    chatSend.disabled = true;
    fetch(CHAT_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ messages: history.slice(-20) }) })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (j) {
        typing.remove();
        if (j.reply) {
          add(j.reply, 'bot');
          history.push({ role: 'assistant', content: j.reply });
        } else {
          history.pop();
          add(j.error || 'Something went wrong. Please try again.', 'bot err');
        }
      })
      .catch(function () {
        typing.remove();
        history.pop();
        add('The assistant could not be reached. Please try again, or email ' + EMAIL + '.', 'bot err');
      })
      .then(function () { chatSend.disabled = false; input.focus(); });
  });
})();
