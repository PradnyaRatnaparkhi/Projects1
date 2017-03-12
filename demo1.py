import elasticsearch
import requests
import base64
url = 'http://www.cbu.edu.zm/downloads/pdf-sample.pdf'
response = requests.get(url)
with open('Downloads', 'wb') as f:
    f.write(response.content)

es = elasticsearch.Elasticsearch()
print(es.cat.health())
body = {
  "description" : "Extract attachment information",
  "processors" : [
    {
      "attachment" : {
        "field" : "data"
      }
    }
  ]
}
es.index(index='_ingest', doc_type='pipeline', id='attachment', body=body)

result1 = es.index(index='my_index', doc_type='my_type', pipeline='attachment',
                  body={'data': "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0="})
print(result1)

url = 'http://www.cbu.edu.zm/downloads/pdf-sample.pdf'
response = requests.get(url)

data = base64.b64encode(response.content).decode('ascii')
result2 = es.index(index='my_index', doc_type='my_type', pipeline='attachment',
                  body={'data': data})
print(result2)
