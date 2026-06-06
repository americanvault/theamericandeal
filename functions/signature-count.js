exports.handler = async function () {
      const headers = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };
      try {
              const r = await fetch('https://api.counterapi.dev/v1/theamericandeal/nsra/');
              if (!r.ok) throw new Error('counterapi unreachable');
              const d = await r.json();
              const count = typeof d.count === 'number' ? d.count : 0;
              return { statusCode: 200, headers, body: JSON.stringify({ count }) };
      } catch (err) {
              return { statusCode: 200, headers, body: JSON.stringify({ count: 0 }) };
      }
};
