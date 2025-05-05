import time
import random
from curl_cffi import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

authorization = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9nYXRld2F5LmdvbGlrZS5uZXRcL2FwaVwvbG9naW4iLCJpYXQiOjE3NDY0MzIxMDEsImV4cCI6MTc3Nzk2ODEwMSwibmJmIjoxNzQ2NDMyMTAxLCJqdGkiOiJ1SXRoTVVnYkhZWW9pbGcxIiwic3ViIjoyNjYxNDcyLCJwcnYiOiJiOTEyNzk5NzhmMTFhYTdiYzU2NzA0ODdmZmYwMWUyMjgyNTNmZTQ4In0.7tTaiQU-c7G5bZslDQM9OJmn-wAzvzbgDlCfKP4QeGY'
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': authorization,
    'content-type': 'application/json;charset=utf-8',
    'origin': 'https://app.golike.net',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="135", "Safari";v="18"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"iOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    't': 'VFZSak1FNXFVWHBPVkVGNVRsRTlQUT09',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
}

def getrequests(requeseturl, params=None):
    try:
        with requests.Session(impersonate="safari_ios") as s:
            response = s.get(requeseturl, headers=headers, params=params).json()
        return response
    except Exception as e:
        print(f"Lỗi khi gửi yêu cầu: {str(e)}")
        return None

def TIKTOK_INFO():
    response = getrequests('https://gateway.golike.net/api/tiktok-account')
    if not response or 'data' not in response:
        print("Không thể lấy danh sách tài khoản TikTok")
        return None, None
    
    account = []
    ID = []
    print("=====================")
    for i in response['data']:
        account.append(i['unique_username'])
        ID.append(i['id'])
    
    print('Danh sách các tài khoản TikTok hiện có:')
    for i in range(len(ID)):
        print('STT  ', i, '. ', ID[i], account[i])
    
    try:
        choose = int(input("Chọn tài khoản (nhập số): "))
        if choose < 0 or choose >= len(ID):
            raise ValueError("Lựa chọn không hợp lệ")
    except ValueError:
        print("Lựa chọn không hợp lệ, thoát tool.")
        exit()
    
    account_id = ID[choose]
    account_name = account[choose]
    print(account_id, account_name)
    return account_id, account_name

def tiktok_job(id):
    params = {
        'account_id': id,
        'data': 'null',
    }
    try:
        with requests.Session(impersonate="safari_ios") as s:
            response = s.get('https://gateway.golike.net/api/advertising/publishers/tiktok/jobs', params=params, headers=headers).json()
        if not response or 'data' not in response:
            print("Không thể lấy công việc")
            return None
        
        info_job = {
            'id': response['data']['id'],
            'link': response['data']['link'],
            'object_id': response['data']['object_id'],
            'type': response['data']['type'],
        }
        return info_job
    except Exception as e:
        print(f"Lỗi khi lấy công việc: {str(e)}")
        return None

def skip_job(ads_id, object_id, account_id, job_type):
    json_data = {
        'ads_id': ads_id,
        'object_id': object_id,
        'account_id': account_id,
        'type': job_type,
    }
    try:
        with requests.Session(impersonate="safari_ios") as s:
            response = s.post(
                'https://gateway.golike.net/api/advertising/publishers/tiktok/skip-jobs',
                headers=headers,
                json=json_data,
            ).json()
        print(f"Đã bỏ qua công việc {job_type}: {response.get('message', 'No message')}")
        return response
    except Exception as e:
        print(f"Lỗi khi bỏ qua công việc: {str(e)}")
        return None

def complete_job(ads_id, account_id):
    json_data = {
        'ads_id': ads_id,
        'account_id': account_id,
        'async': True,
        'data': None,
    }
    try:
        with requests.Session(impersonate="safari_ios") as s:
            response = s.post(
                'https://gateway.golike.net/api/advertising/publishers/tiktok/complete-jobs',
                headers=headers,
                json=json_data,
            ).json()
        print(f"Hoàn thành công việc: {response.get('message', 'No message')}")
        return response
    except Exception as e:
        print(f"Lỗi khi hoàn thành công việc: {str(e)}")
        return None

def UI():
    response = getrequests('https://gateway.golike.net/api/users/me')
    if not response or 'data' not in response:
        print("Không thể lấy thông tin người dùng")
        return
    
    print("TOOL DEMO AUTO TIKTOK")
    print('-- Thông tin người dùng --')
    account = {
        'id': response['data'].get('id', ''),
        'username': response['data'].get('username', ''),
        'coin': response['data'].get('coin', ''),
    }
    print("ID:", account['id'])
    print("TÊN: ", account['username'])
    print("TIỀN: ", account['coin'])

def main():
    UI()
    account_id, account_name = TIKTOK_INFO()
    if not account_id:
        return
    
    # Input number of follow and like jobs
    try:
        max_follow_jobs = min(int(input("Nhập số lượng job follow (tối đa 150): ")), 150)
        max_like_jobs = min(int(input("Nhập số lượng job like (tối đa 300): ")), 300)
    except ValueError:
        print("Số lượng không hợp lệ, thoát tool.")
        exit()
    
    follow_count = 0
    like_count = 0
    print(f"Bắt đầu thực hiện {max_follow_jobs} job follow và {max_like_jobs} job like...")
    
    while follow_count < max_follow_jobs or like_count < max_like_jobs:
        # Check if both targets are met
        if follow_count >= max_follow_jobs and like_count >= max_like_jobs:
            break
        
        # Fetch job
        job = tiktok_job(account_id)
        if not job:
            print("Không lấy được công việc, thử lại sau 30 giây...")
            time.sleep(30)
            continue
        
        job_type = job['type']
        ads_id = job['id']
        object_id = job['object_id']
        link = job['link']
        
        # Skip comment jobs
        if job_type == 'comment':
            skip_job(ads_id, object_id, account_id, job_type)
            time.sleep(random.uniform(30, 60))  # Delay between jobs
            continue
        
        # Handle follow or like jobs
        if job_type == 'follow' and follow_count < max_follow_jobs:
            print(f"Thực hiện job follow: {link}")
            # Simulate accessing TikTok link (in practice, use a browser automation tool)
            time.sleep(7)  # Wait 7 seconds to mimic interaction
            complete_job(ads_id, account_id)
            follow_count += 1
            print(f"Đã hoàn thành {follow_count}/{max_follow_jobs} job follow")
        elif job_type == 'like' and like_count < max_like_jobs:
            print(f"Thực hiện job like: {link}")
            time.sleep(7)  # Wait 7 seconds to mimic interaction
            complete_job(ads_id, account_id)
            like_count += 1
            print(f"Đã hoàn thành {like_count}/{max_like_jobs} job like")
        else:
            # Skip if job type doesn't match remaining quota
            skip_job(ads_id, object_id, account_id, job_type)
        
        # Random delay between jobs to avoid detection
        time.sleep(random.uniform(30, 60))
    
    print("Hoàn thành tất cả công việc yêu cầu!")

if __name__ == "__main__":
    main()
