# 原神自动签到

```javascript
var cookie = document.cookie;
var ask = confirm('Cookie:' + cookie + '\n\n复制？');
if (ask == true) {
    copy(cookie);
    msg = cookie;
} else {
    msg = 'Cancel';
}
```
