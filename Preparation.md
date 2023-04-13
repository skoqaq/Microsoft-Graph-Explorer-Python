## 步骤1：安装必要的库

在开始编写程序之前，需要确保已经安装了以下库：

- requests
- msal

这些库可以使用pip命令进行安装。

## 步骤2：注册应用程序

在使用Microsoft Graph API之前，需要在Azure门户上注册应用程序。具体步骤请参考[Microsoft官方文档](https://docs.microsoft.com/en-us/graph/auth-register-app-v2)。
在注册应用程序时，需要注意以下几点：

- 应用程序类型选择“Public client (mobile & desktop)”。
- 重定向 URI指定为http://localhost:8000。
- API权限需要添加“User.Read”。