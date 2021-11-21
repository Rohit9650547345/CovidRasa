import requests
url = 'https://rasa-server-rohit9650547345.cloud.okteto.net/webhooks/rest/webhook' ##change rasablog with your app name
myobj = {
"message": "haryana",
"sender": "Ashish",
}
x = requests.post(url, json = myobj)
print(x.text)
