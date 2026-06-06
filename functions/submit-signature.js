exports.handler = async function (event) {
    var headers = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };
    if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers: headers };
    if (event.httpMethod !== 'POST') {
          return { statusCode: 405, headers: headers, body: JSON.stringify({ success: false, error: 'Method not allowed' }) };
    }

    var netlifyToken  = process.env.NETLIFY_ACCESS_TOKEN;
    var siteId        = process.env.NETLIFY_SITE_ID;
    var formSubmitUrl = 'https://formsubmit.co/ajax/americandealvault@proton.me';
    var counterUrl    = 'https://api.counterapi.dev/v1/theamericandeal/nsra/up';

    try {
          var fields = {};
          var ct = (event.headers['content-type'] || '');
          if (ct.includes('application/json')) {
                  fields = JSON.parse(event.body || '{}');
          } else {
                  var params = new URLSearchParams(event.body || '');
                  params.forEach(function(v, k) { fields[k] = v; });
          }

      var email = (fields.email || '').trim().toLowerCase();
          var name  = (fields.name  || '').trim();
          var zip   = (fields.zip   || '').trim();

      if (!email || !name) {
              return { statusCode: 400, headers: headers, body: JSON.stringify({ success: false, error: 'Name and email are required.' }) };
      }

      // Server-side dedup via Netlify Forms API
      if (netlifyToken && siteId) {
              try {
                        var formsRes = await fetch('https://api.netlify.com/api/v1/sites/' + siteId + '/forms', {
                                    headers: { 'Authorization': 'Bearer ' + netlifyToken }
                        });
                        var forms = await formsRes.json();
                        var form = Array.isArray(forms) && forms.find(function(f) { return f.name === 'nsra-signatures'; });
                        if (form) {
                                    var subRes = await fetch('https://api.netlify.com/api/v1/forms/' + form.id + '/submissions?per_page=1000', {
                                                  headers: { 'Authorization': 'Bearer ' + netlifyToken }
                                    });
                                    var subs = await subRes.json();
                                    var isDuplicate = Array.isArray(subs) && subs.some(function(s) {
                                                  var d = s.data || {};
                                                  return (d.email || '').toLowerCase() === email;
                                    });
                                    if (isDuplicate) {
                                                  return {
                                                                  statusCode: 200,
                                                                  headers: headers,
                                                                  body: JSON.stringify({ success: false, duplicate: true })
                                                  };
                                    }
                        }
              } catch (_) {}
      }

      // Forward to FormSubmit.co
      try {
              await fetch(formSubmitUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                        body: JSON.stringify({
                                    name: name,
                                    email: email,
                                    zip: zip,
                                    _subject: 'New NSRA Signature',
                                    _replyto: 'contact@theamericandeal.org',
                                    _autoresponse: 'Thank you for signing the National Sovereignty and Resilience Act. Your signature has been recorded and added to the public record of citizen demand.\n\nThe NSRA is a movement built on honest math, constitutional architecture, and the belief that America owes its people a return on the investment they\'ve made in this country. Share the movement with someone who deserves to know — TheAmericanDeal.org.\n\nWhat America Owes You™\nTheAmericanDeal.org\ncontact@theamericandeal.org'
                        }),
                        signal: AbortSignal.timeout(8000)
              });
      } catch (_) {}

      // Record in Netlify Forms (dedup store)
      try {
              var formBody = 'form-name=nsra-signatures&name=' + encodeURIComponent(name) + '&email=' + encodeURIComponent(email) + '&zip=' + encodeURIComponent(zip);
              await fetch('https://theamericandeal.org/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: formBody,
                        signal: AbortSignal.timeout(8000)
              });
      } catch (_) {}

      // Increment counter server-side
      var newCount = null;
          try {
                  var cr = await fetch(counterUrl, { signal: AbortSignal.timeout(5000) });
                  if (cr.ok) {
                            var cd = await cr.json();
                            newCount = typeof cd.count === 'number' ? cd.count : null;
                  }
          } catch (_) {}

      return {
              statusCode: 200,
              headers: headers,
              body: JSON.stringify({ success: true, count: newCount })
      };

    } catch (err) {
          return {
                  statusCode: 500,
                  headers: headers,
                  body: JSON.stringify({ success: false, error: 'Server error. Please try again.' })
          };
    }
};
