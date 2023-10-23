


with sync_playwright() as p:
            print("Website 2 - "+ website)
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(website)
            api_website_name=website[27:-8]
            cookie_for_requests = context.cookies()[0]['value']
            browser.close()
            cookies = dict(Cookie=f'notice_preferences=2:; notice_gdpr_prefs=0,1,2::implied,eu; euconsent-v2={cookie_for_requests};')
            result = requests.post("https://apply.workable.com/api/v3/accounts/" + api_website_name + "/jobs#/", cookies=cookies)
            print(result.status_code)
            if result.status_code == 200:
                data = result.json()
                my_list=[]
                if 'results' in data:
                    my_list = data['results']
                next_page = data['nextPage']

                while next_page != "":
                    payload = {
                        "token": next_page,
                        "query": "",
                        "location": [],
                        "department": [],
                        "worktype": [],
                        "remote": [],
                        "workplace": []
                    }
                    headers = {
                        'Content-Type': 'application/json'
                    }
                    json_payload=json.dumps(payload)
                    result = requests.post("https://apply.workable.com/api/v3/accounts/" + api_website_name + "/jobs#/", cookies=cookies,data=json_payload,headers=headers)
                    data = result.json()
                    if 'results' in data:
                        my_list = my_list + data['results']
                    if 'nextPage' in data:
                        next_page=data['nextPage']
                    else:
                        next_page = ""
        