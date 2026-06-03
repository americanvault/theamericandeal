exports.handler = async function (event) {
  const headers = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };
  const { zip, state } = event.queryStringParameters || {};

  try {
    let url;
    if (zip) {
      url = `https://whoismyrepresentative.com/getall_mems.php?zip=${encodeURIComponent(zip)}&output=json`;
    } else if (state) {
      url = `https://whoismyrepresentative.com/getall_sens.php?state=${encodeURIComponent(state)}&output=json`;
    } else {
      return { statusCode: 400, headers, body: JSON.stringify({ error: 'Missing zip or state' }) };
    }

    const res = await fetch(url);
    const text = await res.text();
    return { statusCode: 200, headers, body: text };
  } catch (err) {
    return { statusCode: 200, headers, body: JSON.stringify({ results: [] }) };
  }
};
