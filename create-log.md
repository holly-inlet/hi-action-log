# HI Action Log製作日誌

<!-- omit in toc -->
## 目次

- [2022/02/01(Tue)](#20220201tue) —— 環境構築
- [2022/02/02(Wen)](#20220202wen) —— 環境構築，FlaskでHello World
- [2022/02/03(Thu)](#20220203thu) —— FlaskでToDoアプリ写経
- [2022/02/04(Fri)](#20220204fri) —— オブジェクト化＆MySQL使用断念
- [2022/02/05(Sat)](#20220205sat) —— Bootstrap＆Heroku
- [2022/02/06(Sun)](#20220206sun) —— Herokuでデプロイ
- [2022/02/07(Mon)](#20220207mon) —— 写経したToDoアプリをベースに独自機能実装開始
- [2022/02/08(Tue)](#20220208tue) —— HTML変更
- [2022/02/09(Wen)](#20220209wen) —— HTML変更
- [2022/02/10(Thu)](#20220210thu)
- [2022/02/11(Fri)](#20220211fri) —— 経過時間算出機能実装

---

### 2022/02/01(Tue)

使用時間：195分

- Githubにリポジトリを作成
- Docker上で環境構築
- Docker imageからubuntu:latestのimageをpull
- ubuntu imageをrunし，hi-action-logコンテナを作成
  - しかし，hi-action-logコンテナが起動しない
- 一度作成したコンテナを消去し，`$ docker run --name hi-action-log -it ubuntu bash`で再度コンテナを作成・コンテナの中に入ってみる
  - 無事コンテナが起動し，コンテナの中に入ることに成功
- コンテナの中でaptにより`update`と`-y upgared`
  - cf. [Python 3をインストールしUbuntu 20.04サーバーにプログラミング環境を設定する方法](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server-ja)
  - なぜか`sudo`が使えなかったが，aptはできたので一旦は無視することにした
- コンテナの中で`# apt install python3-pip`でコンテナにPythonをインストール
  - Python 3.8.10インストール完了

### 2022/02/02(Wen)

使用時間：245分

- cf. 参考記事  
(1) [【保存版】30分でFlask入門！Webアプリの作り方をPythonエンジニアが解説——テックダイアリー](https://tech-diary.net/flask-introduction/)  
(2) [VS CodeとFlaskによるWebアプリ開発「最初の一歩」——＠IT](https://atmarkit.itmedia.co.jp/ait/articles/1807/24/news024.html)  
(3) [チュートリアル——Flask](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/index.html)
- dockerコンテナに入り`$ pip install flask`でFlask 2.0.2をインストール。`$ pip freeze`でインストールの確認
- (2)の始めの通りに最小のFlaskアプリを書いて`$ set FLASK_APP=app.py`→`$ flask run`してみる。しかしエラー。

    ~~~bash
    Error: Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.
    ~~~

- もう一度dockerコンテナを作成し直してみる。今度はポートのマッピングやファイルにマウントも行った  
    cf. [Docker、ボリューム(Volume)について真面目に調べた——@gounx2｜Qiita](https://qiita.com/gounx2/items/23b0dc8b8b95cc629f32)  
    cf. [Docker の Volume がよくわからないから調べた——@aki_55p｜Qiita](https://qiita.com/aki_55p/items/63c47214cab7bcb027e0)
  - `$ docker run -p 8888:8888 -v ~/hi-action-log:/workspace --name hi-action-log -it ubuntu bash`
  - aptの`update`と`-y upgrade`
  - `$ apt install python3-pip`。`$ python3 --version`でPython 3.8.10のインストール確認
  - `$ pip install flask`。`$ pip freeze`でFlask 2.0.2のインストール確認
  - `$ set FLASK_APP=app.py`→`$ flask run`
  - 再度同じエラー
- dockerコンテナを出て，ホームディレクトリで`$ python3 --version`してみると何故かPython 3.9.5が入っていた
- 取り敢えず(2)に従ってvenvで仮想環境を構築してみる
  - `$ cd hi-action-log` → `$ python3 -m venv myenv`でhi-action-logフォルダ内に仮想環境作成
  - `$ source ~/hi-action-log/myenv/bin/activate`  
    cf. [【Python3×VSCode】実行環境を分ける必要が出たら行う手順（仮想環境作成）——@some-nyan｜Qiita](https://qiita.com/some-nyan/items/7f20fa5fa0b6e451a42b)
    - 仮想環境には入れたが，VSCodeでインタプリタに設定できない
  - [VSCode にPython仮想環境を追加する——@coffeebeater｜Qiita](https://qiita.com/coffeebeater/items/ebe2d7802e64e3af3027)を参考に設定してみる
    - できない
  - VSCodeの「Python: Venv Path」設定から仮想環境管理用ディレクトリのパスを設定  
    cf. [【Python3×VSCode】実行環境を分ける必要が出たら行う手順（仮想環境作成）——@some-nyan｜Qiita](https://qiita.com/some-nyan/items/7f20fa5fa0b6e451a42b)
    - インタプリタに仮想環境が表示される。成功
- もう一度Flaskでapp.pyを実行
  - 再度同じエラー
  - (1)に従い，すでに書いたapp.pyに以下のコードを追加

    ~~~python
    if __name__ == "__main__":
        app.run(debug=True)
    ~~~

  - `$ python app.py`を実行し，表示されたローカルホストにアクセス
    - 成功。ブラウザ上で「Hello World」が表示される

> dockerでもvenvでも同じエラーが出ており，これならdockerでも同じようにすれば解決できたかもしれない。ただ，ここまで来るとvenvの方が速く作業に入れるので，これからはvenvの仮想環境で進める

- venvで仮想環境を構築したときに作られたmyenvのgitステージング待ちが膨大な量になっているので，gitignoreした方が良さそう  
    cf. [.gitignoreについて——@sf213471118｜Qiita](https://qiita.com/sf213471118/items/efbc0abf028a3ead72e7)  
    cf. [.gitignore の書き方——@inabe49｜Qiita](https://qiita.com/inabe49/items/16ee3d9d1ce68daa9fff)
- hi-action-logディレクトリに.gitignoreフォルダを作成。`/myenv`を記入
  - gitのステージング待ちが解消

### 2022/02/03(Thu)

使用時間：225分

- (1) [【保存版】30分でFlask入門！Webアプリの作り方をPythonエンジニアが解説——テックダイアリー](https://tech-diary.net/flask-introduction/)に従って進める
  - `$ pip install flask-sqlalchemy`でSQLalchemyをインストール
  - (3-1)の「5-2 データベースの項目定義」の箇所で`>>> from app import db`→`>>> db.create_all()`するとImport Error
  - SQLAlchemyがインストールできているか確認。`>>> imoprt sqlalchemy` → `>>> sqlalchemy.__version__`  
    cf. [Sqlalchemy-introduction](https://www.finddevguides.com/Sqlalchemy-introduction)
    - 1.4.31が入っていることを確認
  - もう一度`>>> from app import db`
    - AttributeError: 'Flask' object has no attribute 'comfig'
  - app.pyの`app.config["SQLALCHEMY_DATABASE_URI"]`の箇所にスペルミスがあった。修正
  - `>>> from app import db` → `>>> db.create_all()`
    - 成功。hi-action-logディレクトリ内にtodo.dbが作成された
- (1)の「STEP11」まで完了
- (2) [VS CodeとFlask-SQLAlchemyでデータベース操作——@IT](https://atmarkit.itmedia.co.jp/ait/articles/1808/07/news029.html)を参考にこれまでに書いたコードをオブジェクト化してみる

### 2022/02/04(Fri)

使用時間：135分

- 昨日に引き続き(4) [VS CodeとFlask-SQLAlchemyでデータベース操作——@IT](https://atmarkit.itmedia.co.jp/ait/articles/1808/07/news029.html)を参考にこれまでに書いたコードをオブジェクト化してみる
  - どうも上手くできないので，ひとまずオブジェクト化は後回しにする。
- データベースをMySQLに変更する
  - cf. 参考記事
    - [Flask-SQLAlchemyの基本的な使い方。MySQLを使います](https://www.tcom242242.net/entry/python-basic/flask-sqlalchemy%E3%81%AE%E5%9F%BA%E6%9C%AC%E7%9A%84%E3%81%AA%E4%BD%BF%E3%81%84%E6%96%B9%E3%80%82mysql%E3%82%92%E4%BD%BF%E3%81%84%E3%81%BE%E3%81%99/)
    - [FlaskでMySQLを使う方法](https://masublog.net/flask/flask%E3%81%A7mysql%E3%82%92%E4%BD%BF%E3%81%86%E6%96%B9%E6%B3%95/)
    - [Flask SQLAlchemyを使用したSQLiteからMySQLへの切り替え](https://jpcodeqa.com/q/fc556b073a8c3a4b79a7746c978804b7)
    - [Python3でMySQLを操作する](https://kzhishu.hatenablog.jp/entry/2017/06/03/162911)
    - [MySQLに接続してデータ操作を行う](https://www.yoheim.net/blog.php?q=20151102)
    - [MySQLの使い方](https://www.dbonline.jp/mysql/)
    - [【初心者でもわかるMySQL入門】MySQLの使い方を基礎からマスター](https://26gram.com/mysql)
  - 何から始めればよいのか全くわからず動けなくなってしまったので，ひとまずMySQLの使用は後回しにする。

### 2022/02/05(Sat)

使用時間：230分

- (1) [【保存版】30分でFlask入門！Webアプリの作り方をPythonエンジニアが解説——テックダイアリー](https://tech-diary.net/flask-introduction/)のSTEP12以降を実施
  - Herokuアカウントを作成し，Heroku CLIをインストールしようとしたがエラー `Error: Your Command Line Tools are too outdated.`
    - OSをアップデートするが，変わらずエラー
    - [brew upgrade でのエラー対処からCommand Line Toolsについてまとめてみる](https://techracho.bpsinc.jp/wingdoor/2021_04_09/104821)を参考にコマンドラインツールをアップデート
      - `sudo rm -rf /Library/Developer/CommandLineTools`
      - `sudo xcode-select --install`
      - 再度Heroku CLIをインストール。成功
  - [heroku 初級編 - GitHub から deploy してみよう -](https://qiita.com/sho7650/items/ebd87c5dc2c4c7abb8f0)を参考にHerokuとGithubリポジトリを連携させ，アプリをデプロイする
    - デプロイしたページを見ようとしたがエラー`at=error code=H14 desc="No web processes running"`
      - [【Heroku】デプロイ後にcode=H14 desc="No web processes running"](https://qiita.com/rebi/items/efd1c36f0a9e46222d80)を参考に解決を試みる
        - `$ heroku ps:scale web=1`したが`Error: Missing required flag:`
          - [［Herokuエラー］Error: Missing required flagが出た](https://qiita.com/hirokik-0076/items/71c104158fa8b963ba85)を参考に対処
          - `$ heroku git:remote -a hi-aciton-log`しエラー解消
        - もう一度`$ heroku ps:scale web=1`したが`Scaling dynos... !　Couldn't find that process type (web).`と表示されできず
          - heroku.ymlを作成。`$ heroku stack:set container`を実行
          - `$ git push heroku main`をするがエラー，`error: failed to push some refs to`
    - 今日は解決できずに一時中断

### 2022/02/06(Sun)

使用時間：120分

- 昨日に引き続き[【Heroku】デプロイ後にcode=H14 desc="No web processes running"](https://qiita.com/rebi/items/efd1c36f0a9e46222d80)を参考にエラーの解決を試みる
  - `$ heroku stack:set heroku-18`を実行。`$ git push heroku main`し上手く行ったように見える
  - `$ heroku ps:scale web=1`を実行したが変わらず`Scaling dynos... !　Couldn't find that process type (web).`
  - HerokuのダッシュボードでActivity FeedのBuild Logを確認すると，Build Succeedとなっている
  - Heroku 20 stackがあるようなので，そちらにアップデートし，`$ git push heroku main`→ ビルド
    - Build Succeedになり，リリースされているようだが，アプリにアクセスするとエラー。ログを見るとまだcode=H14エラーのまま。
  - [【Heroku × Flask】No web processes runningエラーの対処](https://yuki.world/heroku-h14-error/)を参考にHerokuダッシュボードからResourcesを見てみると，Free Dynosの箇所に何も表示されていない。Procfileに問題があると思われる。
    - [Herokuに必要なProcfileの書き方についてまとめておく](https://creepfablic.site/2019/06/15/heroku-procfile-matome/)に  
      > Procfileは「P」が大文字であるが，「p」と小文字でファイルを作ると見事に動かない。  

      との記述。確認してみるとファイル名が「procfile」になっていた。修正。
      - デプロイしてみるが変わらずH14エラー
    - Procfileに`web: gunicorn app:app --log-file=-`と書いていたが，`--log-file=-`の箇所で`=`を使っている例が見当たらないので，消してみる。
      - 変わらず失敗
    - gitに反映されているかActivity Feedから飛んで確認してみる。
      - ファイル名が「Procfile」に変更されていない
      - 一度procfileを削除しコミット。その後Prcofileを作成し直しコミット。デプロイ。
        - Githubリモートリポジトリを確認すると変更できていた
    - アプリにアクセスすると，Internal Server Error 500に変わった。
      - `$ heroku logs --tail`を見ると`(Background on this error at: https://sqlalche.me/e/14/e3q8)`との記述があり
      - gitignoreしていたtodo.dbを外し，gitにコミットしてやり直す
        - 成功。無事Herokuサーバー上でアプリが表示された
- これで(1) [【保存版】30分でFlask入門！Webアプリの作り方をPythonエンジニアが解説——テックダイアリー](https://tech-diary.net/flask-introduction/)で説明されている内容を全て終えた

### 2022/02/07(Mon)

使用時間：150分

- (3) [チュートリアル——Flask](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/index.html)
  > 途中まで読み，これまでに参考にしていた記事よりも説明が詳細に感じた反面，やろうとしていることの複雑さが増していて，アプリを公開するなら最低限このくらいは行う必要があるだろうと考えたが，今からこのチュートリアルを実施していると自分の実装したい機能を実装する時間が無くなりそうなので，これまでに作ったアプリをベースに改編して自分で機能を考えて実装を試みたほうが，拙い部分は多くなりそうでも後々の学びになるかと思い，後者を選択した。Flaskチュートリアルは一度今回の計画を終えてからでも行えるだろう。
- これまで記事に従って作ってきた部分から，自分で機能を考えて実装するに当たり，わかりやすくするためGitでブランチを切る
  - 「HI Action Log Ver.1」ブランチ作成
  - アプリページのヘッドとタイトルを「HI Action Log」に変更
- これまでに実装したTodoのCURD機能の部分を，1日の行動データの入力形式に変更する
  - データベースに必要なカラムは実施時間・タスク名・タグ名・使用時間。使用時間の計算は新たに考える必要があるのでひとまず後回しにし，実施時間・タスク名・タグ名をデータベースに設定する
  - 全てのファイルで実施時間として，「due」としていた箇所を「time」に変更
  - 全てのファイルでタグ名として，「detail」としていた箇所を「tag」に変更
  - データベースファイルを新たに「action-log.db」として作成
  - デバックして現在の状態を確認する
  - timeのインプットに時間も入力できるようにする。  
  cf. [\<input>: 入力欄 (フォーム入力) 要素](https://developer.mozilla.org/ja/docs/Web/HTML/Element/input)
  - インプットで受け取った日付と時間をデータベースのtimeカラムに入れる
  - ルートページで時間も表示されるようにする

### 2022/02/08(Tue)

使用時間：105分

- ルートページで新しいデータをcreateできるようにする
- create.htmlのformの内容をindex.htmlにコピペする
  - 変わらず機能が実行できた。よってcreate.htmlを削除
- 新しいデータの入力フォームのレイアウトを一列になるよう変える
  - cf. [空白ユーティリティ（Spacing）](https://v4.bootstrap-guide.com/utilities/spacing)
- Tagの入力フォームを選択式にする

> 中々きれいなレイアウトにならず，Bootstrapのドキュメントを読み込んでいたら時間が過ぎてしまった。実装したい機能のイメージを掴むために見た目から変えているが，あまりこだわりすぎるとバックエンドの処理に割ける時間がなくなってしまうので程々にしよう。

### 2022/02/09(Wen)

使用時間：140分

- ルートページでタスク一覧の表示をカード形式からリスト形式に変更
- Tagの種類ごとにタスク名に色付けして表示させる
- タスクをupdateするときに日付だけでなく時間も反映させる
- タスクを新しくcreateするときにdateとtimeの入力を分ける

### 2022/02/10(Thu)

使用時間：40分

- 入力フォームのラベルを「Time」から「Crete New Task」に変更。サイズを大きくして目立たせる
- ナビゲーションバーにアプリのGithubリポジトリへのリンクボタンを追加
- Create New Taskの日付フォームに今日の日付を予め入力させる

### 2022/02/11(Fri)

使用時間：305分

- 現状tag.htmlを使わないのでindex.htmlからtag.htmlへのリンクを消す
- app.py内のcreate関数は使っていなかったので消す
- なぜかまたdatetimeモジュールが使えなくなっている。
  - Gitで正常に動いていた前のコミットを参照しながら1つずつ変更を加え，どこでモジュールが認識されなくなるか確認していった
  - 変数名に同名のdatetimeを使用していたためモジュールが認識されなくなていた。変数名の方を「start_time」に変更することで解決
- 経過時間を計算する
  - データベースのカラムに「duration」を追加。「title」カラムを「task」に変更。「time」カラムを「start_time」に変更。データベースを作り直す。
  - formで入力したタスクの前にタスクがあった場合。前のタスクと今回入力したタスクの経過時間を計算する

    ~~~python
    before_task = Post.query.order_by(Post.start_time.desc()).filter(Post.start_time < start_time).first()
    if before_task:
        before_task.duration = start_time - before_task.start_time
    ~~~

  - 同様に，formで入力したタスクの次にタスクがあった場合，次のタスクと今回入力したタスクの経過時間を計算する
    - sqlalchemy.exc.StatementError: (builtins.TypeError) SQLite Time type only accepts Python time objects as input.
    - durationを計算したときにデータ型がtimedelta型であったためデータベースのdurationカラムの型と合わずエラーになっていたようだ。
  - 算出した経過時間をtimedelta型からtime型に変換する

    ~~~python
    if before_task:
        before_time = start_time - before_task.start_time
        before_task.duration = datetime.time(datetime.strptime(str(before_time), "%H:%M:%S"))
     ~~~

    cf. [Pythonで秒数と分・時間・日数を相互に変換](https://note.nkmk.me/python-datetime-timedelta-conversion/)
    - 新しいタスクを既存のタスクの前後どちらに挿入してもエラーが出なくなった
  - ルートページに経過時間も表示する
  - タスクリストの表示にヘッダーを付ける
