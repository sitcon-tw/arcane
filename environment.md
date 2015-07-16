#如何建立 arcane 開發環境

1. 安裝 `python3` 跟 `django`
  * 如 Ubuntu/Debian: `sudo apt-get install python3 && sudo pip install django`
2. git clone repo:
  * `git clone git@github.com:sitcon-tw/arcane`
3. 設置db:
  * `python3 manage.py migrate`
4. 設置管理帳號:
  * `python3 createsuperuser`
4. 設置範例資料(就只是個範例資料 你可以自己改):
```
from app.models import *
from django.contrib.auth.models import User
u = User.objects.create_user("seadog007", "", "777777")
u.first_name = "seadog"
u.last_name = "007"
a = Card(name="這是一張點數卡", long_desc="<3", cid="seadog_and_denny")
b = Player(user=u,team=Team(name="第零小隊", tid="team0"))
u.save()
a.save()
b.save()
b.team.save()
```
5. 開啟 local server
  * `python3 manage.py runserver`

# 其他東西

* 範例帳號: `seadog007`
  * 密碼 `777777`
* 範例點數卡: `seadog_and_denny`


* 靜態頁面都在 /app/templates/ 下面
  * 母頁 `base.html`
  * 頂欄 `topbar.html`
* 一些 URL：
  * 學員用
    * [學員登入 /user/login/\[username\]](http://localhost:8000/user/login/seadog007)
      * `user/login.html`
    * [學員頁面 /player](http://localhost:8000/player/)
      * `player/player.html`
      * 首頁也會是這個
    * [學員拿點數頁面 /card/get/\[card id\]](http://localhost:8000/card/get/seadog_and_denny)
      * `card/get.html`
    * [學員改名子頁面](http://localhost:8000/user/chgname)
      * `user/chgname.html`
    * [學員改PIN頁面](http://localhost:8000/user/chgpin)
      * `user/chgpin.html`
  * 工人用
    * 請用管理帳號來試
    * [工人登入 /user/staff_login](http://localhost:8000/user/staff_login)
      * `/user/staff_login.html`
    * [看學員資料 /player/\[username\]](http://localhost:8000/player/seadog007)
      * `/player/player.html`
    * [看點數卡資料 /card/\[card id\]](http://localhost:8000/card/seadog_and_denny)
      * `/card/card.html`
    * [改點數卡資料 /card/edit/\[card id\]](http://localhost:8000/card/edit/seadog_and_denny)
      * `/card/card.html`
    * [生成點數卡 /card/generate](http://localhost:8000/card/generate)
      * `/card/generate.html`
    * [總覽頁面 /staff/](http://localhost:8000/staff/)
      * `/staff/staff.html`
