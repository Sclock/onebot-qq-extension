## 对 OneBot_QQ 实现的要求

!!! tip "提示"
    所有实现应尽可能满足本标准规定的字段，如有扩展字段可在此基础上进行额外扩展。

### 接口

建议先实现所有 [**OneBot 标准事件**](https://12.onebot.dev/interface/meta/events/)、[**OneBot 标准动作**](https://12.onebot.dev/interface/meta/actions/)、[**OneBot 标准消息**](https://12.onebot.dev/interface/message/type/)

OneBot QQ 实现建议实现所有  **QQ基础接口**，这些事件是适配 QQ 平台的必要条件，如果未能全部实现，则无法称之为一个完整的 QQ 平台的 OneBot 实现。同时也建议所有字段按照本标准定义的所有参数实现。

自行决定是否实现 **QQ可选接口** 或其他没有列举的扩展事件，如果实现了一个本标准中列举的扩展事件，建议遵守本标准列出的相关字段要求。
