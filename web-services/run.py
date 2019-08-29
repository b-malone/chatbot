import requests

new_json = df.to_json()
post_url = 'http://127.0.0.1:5000/api/v1'
post_r = requests.post(url=post_url, data=new_json_orient)

print(post_r.json())