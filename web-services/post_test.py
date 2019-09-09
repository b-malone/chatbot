import requests

# WIKIPEDIA
# curl --header "Content-Type: application/json" 
#     --request POST 
#         --data '{"query": "real time face recognition using deep learning"}' 
#         http://localhost:5000/topics/lda

# ONLINE HELP
# curl --header "Content-Type: application/json" 
#     --request POST 
#         --data '{"query": "how do I schedule an event?"}' 
#         http://localhost:5000/topics/lda


headers = {
    'Content-Type': 'application/json',
}

data = '{"query": "real time face recognition using deep learning"}'

response = requests.post('http://localhost:5000/topics/lda', headers=headers, data=data)

print(response)