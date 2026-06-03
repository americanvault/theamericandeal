exports.handler = async function (event) {
  const headers = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };

  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers };
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ success: false, error: 'Method not allowed' }) };
  }

  const token  = process.env.NETLIFY_ACCESS_TOKEN;
  const siteId = process.env.NETLIFY_SITE_ID;

  try {
    // Parse form fields
    let fields = {};
    const ct = (event.headers['content-type'] || '');
    if (ct.includes('application/json')) {
      fields = JSON.parse(event.body || '{}');
    } else {
      const params = new URLSearchParams(event.body || '');
      for (const [k, v] of params.entries()) fields[k] = v;
    }

    const email = (fields.email || fields['sig-email'] || '').trim().toLowerCase();
    const name  = (fields.name  || fields['sig-name']  || '').trim();
    const zip   = (fields.zip   || fields['sig-zip']   || '').trim();
    const phone = (fields.phone || fields['sig-phone'] || '').trim();

    if (!email || !name) {
      return { statusCode: 400, headers, body: JSON.stringify({ success: false, error: 'Name and email are required.' }) };
    }

    // ── Deduplication via Netlify Forms API ──────────────────────
    if (token && siteId) {
      try {
        // Get the nsra-signatures form ID
        const formsRes = await fetch(`https://api.netlify.com/api/v1/sites/${siteId}/forms`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const forms = await formsRes.json();
        const form = forms.find(f => f.name === 'nsra-signatures');

        if (form) {
          // Search submissions for this email (page through if needed)
          const subRes = await fetch(
            `https://api.netlify.com/api/v1/forms/${form.id}/submissions?per_page=100`,
            { headers: { Authorization: `Bearer ${token}` } }
          );
          const subs = await subRes.json();
          const duplicate = Array.isArray(subs) && subs.some(s => {
            const d = s.data || {};
            return (d.email || '').toLowerCase() === email;
          });

          if (duplicate) {
            return {
              statusCode: 200,
              headers,
              body: JSON.stringify({ success: false, duplicate: true, error: 'This email address has already signed the NSRA.' }),
            };
          }
        }
      } catch (_) {
        // Non-fatal — proceed with submission if dedup check fails
      }
    }

    // ── Submit to Netlify Forms (native) ─────────────────────────
    const formBody = new URLSearchParams({
      'form-name': 'nsra-signatures',
      name, email, zip, phone,
    });

    await fetch('https://theamericandeal.org/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formBody.toString(),
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ success: true }),
    };
  } catch (err) {
    console.error('submit-signature error:', err);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ success: false, error: 'Server error. Please try again.' }),
    };
  }
};
