#curl -X PUT http://$2/tastecard --user $1
curl -X PUT -d '{"shows": {"old": "function(doc, req) { return 'hi' }"}}' http://$2/tastecard/_design/main --user $1
