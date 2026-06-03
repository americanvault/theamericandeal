exports.handler = async function () {
  const headers = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };
  const token = process.env.NETLIFY_ACCESS_TOKEN;
  const siteId = process.env.NETLIFY_SITE_ID;

  if (!token || !siteId) {
    return { statusCode: 200, headers, body: JSON.stringify({ count: 0 }) };
  }

  try {
    const res = await fetch(`https://api.netlify.com/api/v1/sites/${siteId}/forms`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const forms = await res.json();
    const form = forms.find(f => f.name === 'nsra-signatures');
    const count = form ? form.submission_count : 0;
    return { statusCode: 200, headers, body: JSON.stringify({ count }) };
  } catch (err) {
    return { statusCode: 200, headers, body: JSON.stringify({ count: 0 }) };
  }
};
