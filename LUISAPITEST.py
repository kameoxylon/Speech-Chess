import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '{subscription key}',
}

params = urllib.urlencode({
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("GET", "/luis/v1.0/prog/apps/{appId}/actionChannels?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))