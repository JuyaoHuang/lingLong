---
title: JWT令牌
published: 2025-09-28
description: 探讨JWT令牌的定义与实现
tags: [JWT]
first_level_category: '编程'
second_level_category: '后端开发'
author: JuyaoHuang
draft: false
---

# JWT标准

## JWT介绍

### 形式化定义

​	**JWT (JSON Web Token)** 是一个开放的行业标准（**RFC 7519**），它定义了一种紧凑且自包含的方式，用于在各方之间安全地传输信息。这个信息是一个 JSON 对象，由于它经过了数字签名，因此可以被验证和信任。JWT 可以使用密钥（通过 **HMAC** 算法）或公/私钥对（通过 **RSA** 或 **ECDSA**）进行签名。

​	从工程角度看，JWT 的本质是一个**带有防伪签名的、标准化的、有有效期的声明字符串**。

### 设计目标：解决什么问题？

在理解 JWT 之前，必须先理解它要解决的核心问题：**HTTP 协议的无状态性）**。

在传统的基于 **Session-Cookie** 的认证模型中，服务器需要存储每个登录用户的 Session 信息。

- **流程：** 用户登录 -> 服务器创建 Session -> 将 Session ID 存入 Cookie 发给客户端 -> 客户端每次请求都携带 Cookie -> 服务器通过 Session ID 查找对应的 Session 数据以确认用户身份。
- **工程痛点：**
  1. **服务端状态存储：** 服务器需要开辟内存或数据库空间来存储大量 Session，增加了服务器的负载。
  2. **可扩展性差：** 在分布式或微服务架构中，如果一个请求被负载均衡到另一台没有该用户 Session 信息的服务器上，认证就会失败。解决方案（如 Session 共享、Session 粘连）会引入新的架构复杂度。
  3. **跨域/跨设备限制：** Cookie 机制在跨域认证和非浏览器客户端（如移动 App、IoT 设备）上存在天然的限制。

​	**JWT 的设计目标就是实现一种无状态的、可移植的认证授权机制，将状态信息从服务端转移到客户端。**

### 技术解构：JWT 的解剖学

一个 JWT 字符串由三部分组成，通过点（.）分隔，其结构为：
`Header.Payload.Signature`，  即 `xxxxx.yyyyy.zzzzz`

#### 第一部分：Header (头部)

- **内容：** 一个包含元数据的 JSON 对象，描述了关于该 JWT 的最基本信息。

- **标准字段：**

  - `typ (Type)`: 令牌的类型，对于 JWT 来说，其值固定为 "JWT"。
  - `alg (Algorithm)`: 用于生成签名的加密算法。这是极其重要的字段，它告诉接收方应该用哪种算法来验证签名。常见的有 HS256 (HMAC using SHA-256) 和 RS256 (RSA using SHA-256)。

- 生成过程：

  ​	 将该 JSON 对象进行 **Base64Url** 编码，形成 JWT 的第一部分。

  - 工程注意： Base64Url 是一种 URL 安全的 Base64 编码，它不会产生 +, /, = 等在 URL 中有特殊含义的字符。

  - 示例：

    ```json
    {
      "alg": "HS256",
      "typ": "JWT"
    }
    ```

    编码后 -> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

#### 第二部分：Payload (载荷)

- **内容：** 一个包含声明（Claims）的 JSON 对象。声明是关于实体（通常是用户）和其他附加元数据的陈述。
- **声明的三种类型：**
  1. **Registered Claims (注册声明):** 这些是预定义的一组声明，虽然不是强制性的，但推荐使用，以提供一套有用的、可互操作的声明。
     - `iss (Issuer)`: 令牌的签发者。
     - `sub (Subject)`: 令牌的主题（通常是用户的唯一标识符，如 user_id）。
     - `aud (Audience)`: 令牌的接收者。
     - `exp (Expiration Time)`: **极其重要的安全字段**。定义了令牌的过期时间戳。在此时间之后，该令牌将不再被接受。
     - `nbf (Not Before)`: 定义了令牌开始生效的时间戳。
     - `iat (Issued At)`: 令牌的签发时间戳。
  2. **Public Claims (公共声明):** 使用方可以自由定义，但为了避免冲突，应该在 [IANA JSON Web Token Registry](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.iana.org%2Fassignments%2Fjson-web-token%2Fjson-web-token.xhtml) 中定义它们，或为其加上包含命名空间的 URI。
  3. **Private Claims (私有声明):** 这是签发方和接收方共同商定使用的声明，用于在它们之间共享信息。例如，可以包含用户的角色、权限等级等。
- 生成过程： 将该 JSON 对象进行 **Base64Url** 编码，形成 JWT 的第二部分。

- 示例：

  ```json
  {
    "sub": "1234567890",
    "name": "John Doe",
    "role": "admin",
    "iat": 1516239022,
    "exp": 1516242622
  }
  ```

  编码后 -> eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyNDI2MjJ9

#### 第三部分：Signature (签名)

- 目的： 

  ​	验证令牌的完整性（Integrity）和真实性（Authenticity）。即确保令牌在传输过程中没有被篡改，并且它确实是由可信的签发者签发的。

- 生成过程：

  1. 取编码后的 Header。
  2. 取编码后的 Payload。
  3. 用点（.）将这两部分连接起来，形成一个字符串：base64UrlEncode(header) + "." + base64UrlEncode(payload)。
  4. 使用 Header 中指定的 alg 算法，和**一个只有服务器知道的密钥（Secret）**，对上述字符串进行加密签名。

- 公式：以 HS256 为例：

  ```py
  Signature = HMACSHA256(
    base64UrlEncode(header) + "." + base64UrlEncode(payload),
    your-256-bit-secret
  )
  ```

- 最终产物： 将生成的签名再进行 **Base64Url** 编码，得到 JWT 的第三部分。

### 核心工作流

1. **认证 (Authentication):**

   - 客户端使用用户名和密码向服务器的 /login 接口发起请求。
   - 服务器验证凭据。
   - 验证成功后，服务器创建一个包含用户标识（如 user_id）和过期时间（exp）的 Payload，然后用**私钥（Secret）**生成签名，组装成一个完整的 JWT。
   - 服务器将此 JWT 返回给客户端。

2. **授权 (Authorization):**

   - 客户端收到 JWT 后，通常将其存储在 localStorage 或 sessionStorage 中。

   - 当客户端需要访问受保护的 API 接口时，它会在 HTTP 请求的 Authorization 头中携带该 JWT，格式为 `Bearer <token>`。

     ```
     Authorization: Bearer eyJhbGciOiJIUzI1Ni...
     ```

     服务器收到请求后，首先提取 `Authorization` 头中的 JWT。

   - 服务器**不信任** Payload 中的任何内容，而是进行**签名验证**：

     1. 读取 JWT 的 Header 和 Payload。
     2. 使用与签发时**相同的算法和密钥**，根据 Header 和 Payload 重新计算一次签名。
     3. 将新计算出的签名与 JWT 中自带的第三部分（Signature）进行**严格比对**。
     4. 如果二者完全一致，证明令牌未被篡改且来源可信。
     5. 服务器**必须**检查 Payload 中的 exp 声明，确保令牌未过期。

   - 所有验证通过后，服务器才信任 Payload 中的信息（如 sub 字段里的 user_id），并处理该 API 请求。

### 工程上的权衡

- **优点：**

  - **无状态与可扩展性：** 

    ​	服务器无需存储会话信息，极大地降低了内存消耗，并天然支持分布式和微服务架构。

  - **自包含性：** 

    ​	载荷中可以包含必要的用户信息，减少了后续查询数据库的次数。

  - **解耦与可移植性：** 

    ​	令牌的生成和验证逻辑是独立的，适用于多种客户端（Web, Mobile, IoT）和跨域场景。

- **缺点与安全考量：**

  - **不可撤销性：** 

    ​	一旦签发，JWT 在其有效期内始终有效。如果令牌泄露，攻击者可以在过期前一直使用它。解决方案包括：设置较短的有效期、使用刷新令牌（Refresh Token）机制、维护一个黑名单（但这又违背了无状态的初衷）。

  - **数据暴露：** 

    ​	Payload 部分只是 Base64Url 编码，并非加密。**任何敏感信息都绝对不能存放在 Payload 中**。

  - **令牌体积：** 

    ​	如果在 Payload 中存放过多信息，会导致 JWT 字符串变得很长，增加每次 HTTP 请求的开销。

  - **密钥安全：** 

    ​	签名用的密钥（Secret）是整个安全体系的命脉，**必须妥善保管，绝不能泄露到客户端**。算法选择也很重要，绝不能使用 alg: "none"。

## FastAPI实现方式

### 1. 核心依赖库

在动手之前，明确工具集。

1. **FastAPI**:  Web 框架。
2. **python-jose**: 一个实现了 JOSE（JavaScript 对象签名与加密）标准的库，FastAPI 官方文档推荐用它来处理 JWT。它比 PyJWT 支持更多加密算法。
3. **passlib**: 用于安全地哈希和验证密码。**工程红线：绝不能在数据库中存储明文密码。**=>使用 bcrypt 算法。

### 2. 整体设计思路

把认证逻辑分为三个独立但相互协作的模块：

1. **密码处理模块 (security.py)**: 负责密码的哈希生成与验证，功能单一且明确。
2. **认证核心模块 (auth.py)**: 负责 JWT 的创建、解析和验证。这是整个认证体系的大脑。
3. **API 路由模块 (main.py)**: 负责提供公开的登录接口，以及受 JWT 保护的业务接口。

这种分层设计使得代码高内聚、低耦合，易于测试和未来的扩展。

### 3. 工程化实现步骤(示例)

#### 步骤一：配置与基础设置

首先，需要一个地方来管理密钥和算法等配置信息。硬编码是绝对不可取。

**config.py**

```py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT 配置
    SECRET_KEY: str = "a_very_secret_and_long_string_for_jwt" # 生产环境中必须从环境变量读取
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 访问令牌有效期30分钟

    class Config:
        env_file = ".env" # 可以通过 .env 文件覆盖配置

settings = Settings()
```

#### 步骤二：密码处理模块

这个模块只做一件事：处理密码。

#### 步骤三：JWT 令牌的构建与验证

**auth.py**

```py
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from .config import settings
# 假设有一个 Pydantic 模型来表示用户
# from .schemas import User

# 定义令牌载荷的数据结构
class TokenData(BaseModel):
    username: Optional[str] = None

# 创建 OAuth2 密码流实例
# tokenUrl 指向获取令牌的 API 路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# 令牌的构建函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    构建 JWT 访问令牌

    :param data: 需要编码到令牌中的数据 (payload)
    :param expires_delta: 令牌的有效期
    :return: 编码后的 JWT 字符串
    """
    to_encode = data.copy()
    
    # 计算过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 如果未提供有效期，则使用配置中的默认值
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 向 payload 中添加 'exp' (过期时间) 声明
    to_encode.update({"exp": expire})

    # 使用 python-jose 库进行编码
    encoded_jwt = jwt.encode(
        claims=to_encode, 
        key=settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

# 创建一个 FastAPI 依赖项，用于保护接口
def get_current_user(token: str = Depends(oauth2_scheme)): # -> User:
    """
    解析并验证令牌，返回当前用户信息。
    这是一个 FastAPI 依赖项，可以注入到任何需要保护的路由中。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码 JWT
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # 从 payload 中提取 'sub' (主题，通常是用户名或用户ID)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        # 使用 Pydantic 模型验证 payload 结构
        token_data = TokenData(username=username)

    except JWTError:
        # 如果解码失败 (令牌无效、过期等)，抛出异常
        raise credentials_exception

    # 在实际应用中，这里应该从数据库中根据 username 查询用户对象
    # user = get_user_from_db(username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user
    
    # 为了演示，直接返回 token_data
    return token_data
```

#### 步骤四：在 API 路由中使用

将以上所有模块组合起来，构建 API 接口

**main.py**

```py
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from . import auth, password_utils
# from .schemas import User # 假设的用户模型

app = FastAPI()

# --- 公开接口：用于登录和获取令牌 ---
@app.post("/api/auth/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 在实际应用中，这里应该从数据库查询用户
    # user = authenticate_user(form_data.username, form_data.password)
    
    # --- 模拟用户认证 ---
    # 假设只有一个 'admin' 用户，密码是 'password'
    # 实际密码哈希应该是从数据库读取的
    hashed_password = password_utils.get_password_hash("password")
    
    is_password_correct = password_utils.verify_password(form_data.password, hashed_password)
    
    if not (form_data.username == "admin" and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # --- 认证结束 ---
    
    # 构建令牌的 payload，'sub' 是标准字段，用于存放唯一标识
    access_token_payload = {"sub": form_data.username}
    
    # 创建 JWT
    access_token = auth.create_access_token(data=access_token_payload)
    
    return {"access_token": access_token, "token_type": "bearer"}


# --- 受保护的接口：必须携带有效令牌才能访问 ---
@app.get("/api/users/me")
def read_users_me(current_user: auth.TokenData = Depends(auth.get_current_user)):
    """
    获取当前登录用户的信息。
    FastAPI 会自动处理：
    1. 检查 Authorization header。
    2. 调用 get_current_user 依赖。
    3. 如果验证失败，依赖会抛出 HTTP 401 异常，此处的代码不会执行。
    4. 如果验证成功，将返回值注入到 current_user 参数中。
    """
    return {"username": current_user.username}

@app.post("/api/admin/posts")
def create_new_post(current_user: auth.TokenData = Depends(auth.get_current_user)):
    # 只有通过了 get_current_user 验证的用户才能执行这里的逻辑
    # 在这里实现创建新文章（操作 md 文件）的逻辑
    return {"message": f"Hello {current_user.username}, you are authorized to create a post."}
```

#### 总结与回顾

1. **令牌构建方式**:
   - 通过 create_access_token 函数构建。
   - 输入是一个包含**声明**的字典。最重要的私有声明是 sub，用于唯一标识用户。
   - 函数内部会自动添加一个**注册声明** exp，用于控制令牌的生命周期。
   - 最后，使用 jose.jwt.encode 方法，传入**载荷（playload）、密钥（key）和算法**，生成最终的 JWT 字符串。
2. **实现思路**:
   - **分层解耦**：将密码、认证、路由的逻辑分离，使代码结构清晰。
   - **依赖注入**：利用 FastAPI 的 Depends，创建了一个可复用的 get_current_user 依赖项。任何需要认证的接口，只需在函数签名中声明这个依赖，即可实现自动化的令牌验证。
   - **配置驱动**：将敏感信息和可变配置（如密钥、算法、有效期）外部化到配置文件中，增强了安全性和灵活性。
   - **安全第一**：强制使用密码哈希，并严格处理令牌的验证错误和过期情况。
