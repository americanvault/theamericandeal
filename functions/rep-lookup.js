/**
 * rep-lookup.js — NSRA Delegation Resolver
 * Primary:  Google Civic Information API v2 (GOOGLE_CIVIC_API_KEY env var)
 * Fallback: whoismyrepresentative.com
 * Returns: { results: [{ name, role, email, url }] }
 */
exports.handler = async function (event) {
    var headers = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };
    var params = event.queryStringParameters || {};
    var zip = params.zip;

    if (!zip) {
          return { statusCode: 400, headers: headers, body: JSON.stringify({ error: 'Missing zip' }) };
    }

    var civicKey = process.env.GOOGLE_CIVIC_API_KEY;
    if (civicKey) {
          try {
                  var civicUrl = 'https://www.googleapis.com/civicinfo/v2/representatives?address=' +
                            encodeURIComponent(zip) + '&roles=legislatorUpperBody&roles=legislatorLowerBody&key=' + civicKey;
                  var res = await fetch(civicUrl, { signal: AbortSignal.timeout(8000) });
                  if (res.ok) {
                            var data = await res.json();
                            var officials = data.officials || [];
                            var offices = data.offices || [];
                            var results = [];
                            offices.forEach(function(office) {
                                        var isSen = office.roles && office.roles.includes('legislatorUpperBody');
                                        var role = isSen ? 'sen' : 'rep';
                                        (office.officialIndices || []).forEach(function(idx) {
                                                      var o = officials[idx];
                                                      if (!o) return;
                                                      var email = (o.emails && o.emails.length) ? o.emails[0] : null;
                                                      var url = (o.urls && o.urls.length) ? o.urls[0] : null;
                                                      results.push({ name: o.name, role: role, email: email, url: url });
                                        });
                            });
                            if (results.length) {
                                        return { statusCode: 200, headers: headers, body: JSON.stringify({ results: results }) };
                            }
                  }
          } catch(e) {}
    }

    // Fallback: whoismyrepresentative.com
    try {
          var repUrl = 'https://whoismyrepresentative.com/getall_mems.php?zip=' + encodeURIComponent(zip) + '&output=json';
          var repRes = await fetch(repUrl, {
                  headers: { 'User-Agent': 'Mozilla/5.0 (compatible; NSRALookup/2.0)', 'Accept': 'application/json', 'Referer': 'https://whoismyrepresentative.com/' },
                  signal: AbortSignal.timeout(8000)
          });
          if (repRes.ok) {
                  var repData = await repRes.json();
                  if (repData.results && repData.results.length) {
                            var state = repData.results[0].state;
                            var senators = [];
                            try {
                                        var senRes = await fetch('https://whoismyrepresentative.com/getall_sens.php?state=' + encodeURIComponent(state) + '&output=json', {
                                                      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; NSRALookup/2.0)', 'Accept': 'application/json' },
                                                      signal: AbortSignal.timeout(8000)
                                        });
                                        if (senRes.ok) {
                                                      var senData = await senRes.json();
                                                      senators = (senData.results || []).map(function(s) {
                                                                      return { name: s.name, role: 'sen', email: s.email || null, url: s.link || null };
                                                      });
                                        }
                            } catch(e) {}
                            var reps = repData.results.map(function(r) {
                                        return { name: r.name, role: 'rep', email: r.email || null, url: r.link || null };
                            });
                            return { statusCode: 200, headers: headers, body: JSON.stringify({ results: reps.concat(senators) }) };
                  }
          }
    } catch(e) {}

    return { statusCode: 200, headers: headers, body: JSON.stringify({ results: [] }) };
};
