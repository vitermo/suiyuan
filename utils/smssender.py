import requests

def send(mobile,captcha):
    url = 'http://v.juhe.cn/sms/send'
    params = {
        'mobile':mobile,
        'tpl_id':'148343',
        'tpl_value':'#code#='+captcha,
        'key':'a4de6ee221a8f124f1e515dad33a2099',
    }
    response = requests.get(url,params=params)
    result = response.json()
    if result['error_code'] == 0:
        return True
    else:
        return False