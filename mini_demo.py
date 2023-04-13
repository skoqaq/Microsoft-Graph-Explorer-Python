import requests
import msal

# 配置应用程序参数
CLIENT_ID = "{应用程序ID}"
AUTHORITY = "<https://login.microsoftonline.com/common>"
SCOPE = ["User.Read"]
REDIRECT_URI = "<http://localhost:8000>"

# 创建MSAL应用程序对象
app = msal.PublicClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY,
    redirect_uri=REDIRECT_URI
)

# 通过浏览器登录
result = app.acquire_token_interactive(scopes=SCOPE)

# 获取访问令牌
access_token = result["access_token"]

# 使用访问令牌调用Microsoft Graph API
graph_url = "<https://graph.microsoft.com/v1.0/me>"
headers = {
    "Authorization": "Bearer {0}".format(access_token)
}
response = requests.get(graph_url, headers=headers)

# 输出用户信息
if response.status_code == 200:
    data = response.json()
    print("Hello, {0}!".format(data["displayName"]))
else:
    print("An error occurred: {0}".format(response.text))