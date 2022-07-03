# Genshin Auto Sign-in

## [中文](README.md) | English

## Introduction

- Genshin Impact BBS automatic daily sign-in (use Github Actions)

## Setup

### 1. Get Cookie

1. Open [Mihoyo BBS](https://bbs.mihoyo.com/ys/) in your browser and log into your account

#### 1.1 Method A

1. Press `F12`, open `Developer Tools`, click `Network`

2. Press `F5` to refresh the page, copy the `Cookie`

    - *If `Debugger` is triggered, try to disable it by pressing `Ctrl + F8`, then refresh the page again, finally copy the `Cookie`*

#### 1.2 Method B

```javascript
var cookie = document.cookie;
var ask = confirm('Cookie:' + cookie + '\n\nCopy to clipboard?');
if (ask == true) {
    copy(cookie);
    msg = cookie;
} else {
    msg = 'Cancel';
}
```

1. Copy the code above

2. Press `F12`, open `Developer Tools`, click `Console`

3. Paste the code and run, you will get an output like `Cookie:xxxxxx`, `xxxxxx` is the `Cookie` you need to copy, click confirm to copy

### 2. Add Cookie to Secrets

1. Go to the repo's main page, click the following `Settings` -> `Secrets` -> `Actions` -> `New repository secret`

2. Create a secret named `COOKIE`, the value is the cookie you copied in `Step 1 - Get Cookie`, finally click `Add secret`

    - *Multiple `Cookie` of different accounts should be separated with `#`, for example: A#B#C#D*
    
### 3. Enable Github Actions

1. Go to the repo's main page, click the following `Actions` -> `Genshin Impact Auto Sign-in` -> `Run workflow`

    - *The Action is disabled by default. You have to manually run it for the first time, the action will be enabled if it runs successfully*

### 4. Some possible reasons for Actions to fail

1. The Cookie will be invalid after changing the password. In this case, you need to update the `COOKIE` under `Secrets`.

2. The Cookie will be invalid after new log-in. In this case, you need to update the `COOKIE` under `Secrets`.

3. After getting the Cookie, do not log out; otherwise, the Cookie will be invalid. If you want to obtain the Cookies of multiple accounts, try using the incognito mode of the browser to obtain the Cookies. Do not log out after obtaining the Cookie, just close the incognito browser window.

*Cookie example: _MHYUUID=?; _ga=?; CNZZDATA???=?; cookie_token=?; account_id=?; ltoken=?; ltuid=?;*

## Thanks to the following projects

- y1ndan - [genshin-impact-helper](https://github.com/y1ndan/genshin-impact-helper)

- sirodeneko - [genshin-sign](https://github.com/sirodeneko/genshin-sign)
