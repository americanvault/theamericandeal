exports.handler = async function (event) {
  var headers = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };
    if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers: headers };
      var url = event.httpMethod === 'POST'
          ? 'https://api.counterapi.dev/v1/theamericandeal/nsra/up'
              : 'https://api.counterapi.dev/v1/theamericandeal/nsra/get';
                try {
                    var res = await fetch(url, { signal: AbortSignal.timeout(5000) });
                        var data = await res.json();
                            var count = typeof data.count === 'number' ? data.count : 0;
                                return { statusCode: 200, headers: headers, body: JSON.stringify({ count: count }) };
                                  } catch (err) {
                                      return { statusCode: 200, headers: headers, body: JSON.stringify({ count: 0 }) };
                                        }
                                        };
