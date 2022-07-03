# 原神自动签到

## 中文 | [English](README_EN.md)

## 简介

- 原神米游社每日自动签到（使用 Github Actions）

## 准备

### 1. 获取 Cookie

1. 浏览器打开 <a href="https://bbs.mihoyo.com/ys/" target="_blank">米游社</a> 并登录账号

#### 1.1 方法一

1. 按`F12`，打开`开发者工具`，找到`网络`并点击

2. 按`F5`刷新页面，复制`Cookie`

    - *当触发`Debugger`时，可尝试按`Ctrl + F8`关闭，然后再次刷新页面，最后复制`Cookie`*

#### 1.2 方法二

```javascript
var cookie = document.cookie;
var ask = confirm('Cookie:' + cookie + '\n\n是否复制内容到剪切板？');
if (ask == true) {
    copy(cookie);
    msg = cookie;
} else {
    msg = 'Cancel';
}
```

1. 复制上面的代码

2. 按`F12`，打开`开发者工具`，找到`控制台`并点击

3. 命令行粘贴代码并运行，获得类似`Cookie:xxxxxx`的输出信息，`xxxxxx`部分即为需要复制的`Cookie`，点击确定复制

### 2. 添加 Cookie 至 Secrets

1. 在项目主页面，依次点击`Settings` -> `Secrets` -> `Actions` -> `New repository secret`

2. 建立名为`COOKIE`的 secret，值为`步骤1`中复制的`Cookie`内容，最后点击`Add secret`

    - *多个账号的`Cookie`值之间用`#`号隔开，例如：A#B#C#D*

### 3. 启用 Actions

1. 在项目主页面，依次点击`Actions` -> `Genshin Impact Auto Sign-in` -> `Run workflow`

    - *Action 默认为关闭状态，需要手动执行一次，若成功运行其才会激活*
    
### 4. 一些可能导致 Actions 运行失败的原因

1. 修改密码会导致Cookie失效。重新获取Cookie并更新`Secrets`下的`COOKIE`即可。

2. 移动端或网页端米游社重新输入账号密码登录后，原Cookie会失效。重新获取Cookie并更新`Secrets`下的`COOKIE`即可。

3. 登录账号获取Cookie后，请不要退出登录，否则获取的Cookie会失效。如果要获取多个账号的Cookie，尝试使用浏览器的无痕模式打开米游社，登录账号并获取Cookie。获取Cookie后不要退出登录，直接关闭整个无痕模式浏览器窗口即可。

*Cookie 样例：_MHYUUID=?; _ga=?; CNZZDATA???=?; cookie_token=?; account_id=?; ltoken=?; ltuid=?;*

## 感谢以下项目

- y1ndan - [genshin-impact-helper](https://github.com/y1ndan/genshin-impact-helper)

- sirodeneko - [genshin-sign](https://github.com/sirodeneko/genshin-sign)
