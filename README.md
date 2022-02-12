# hi-action-log

<!-- omit in toc -->
## 目次

- [概要](#概要)
- [製作期間](#製作期間)
- [使用技術と選択理由](#使用技術と選択理由)
- [背景/課題/目的](#背景課題目的)
- [使用方法](#使用方法)
- [実装要件](#実装要件)
- [振り返り](#振り返り)

---

### 概要

- アプリ名：HI Action Log  
  毎日の行動記録を集計・可視化するアプリ  
- デプロイ先URL：<https://hi-action-log.herokuapp.com/>

### 製作期間

- 制作開始日：2022/02/01
- Ver 1　公開日：2022/02/12  
  製作日誌：[create-log.md](create-log.md)

### 使用技術と選択理由

- Python3 / Flask
    > 元々データ分析に興味がありPythonを学習していたので使用しました。今回のプロジェクトはデータを集計・分析・可視化するものであり，かつWebアプリケーションとして実装したいので，どちらも行える汎用性からPythonは適していると考えました。また，Webアプリケーション開発フレームワークとしてFlaskを選択した理由は，事前知識が不足している状態で短期間の制作を行う状況において，必要最低限の機能のみを行え学習コストが低く，必要があれば自分で拡張機能を選択し追加できることから，今回のプロジェクトで必要な知識のみを一歩ずつ学びながら実装するのに適していると考えたからです。
- HTML&CSS / Bootstrap
    > 短期間の制作という行えることが限られる中で，今回はバックエンドの処理に集中したいと思い，フロントエンドは最低限見やすい表示にするため，フロントエンドのWebアプリケーションフレームワークであるBootstrapを使用することにしました。
- SQLight
    > 今回は小規模な開発であり，かつ学習コストが低く初動を速くできると考えたことからデータベースとして選択しました。当初はMySQLの使用も検討しましたが，今回はスケジュールの観点から断念しました。
- Heroku
    > インターネット上に情報が多く，簡単にデプロイできるという理由から使用することにしました。より実務に活かせる技術を考えるとAWSも候補に挙がりましたが，今回は学習コストの高さから選択しませんでした。

### 背景/課題/目的

- 背景：
  - 限られた時間を有効に使えるように学習計画を立てていました。
  - 実行した計画を客観的に振り返り評価・改善するため，自分の行動を「何時：何分　タスク名」という形で記録していました。
  - そこから毎日手計算で，1日の行動を睡眠時間・休憩時間・学習時間・その他に分類や，タスクごとに予想時間と所用時間を比較していました。
- 課題：
  - 毎日手計算で集計するため，日々時間的・労力的なコストが高く，余裕がない時は集計ができないことも多くありました。
  - 計算の負担が増えるため，新たな分析や複雑な分析ができていませんでした。
  - 行動データを様々な角度から可視化し，直感的に行動の実態を把握しやすくしたいと思いました。
- 目的：
  - 「何時：何分　タスク名」の形で行動の記録を入力するだけで，必要な集計・可視化が行われるようにする。

### 使用方法

![how-to-use](https://github.com/holly-inlet/hi-action-log/blob/imeges/hi-action-log-how-to-use.png)

1. 新しくタスクを登録する。左から
   1. タスクを行った日付を入力。デフォルトでは当日が入力されている
   2. タスクを開始した時刻を入力
   3. タスク名を入力
   4. タスクをどのように分類したいかを選択。Sleep・Rest・Task・Otherから選べる
   5. 「Create」で登録
2. これまでに登録したタスクの一覧を確認できる。左から
   1. タスクを行った日付と開始時間。時系列順に並んでいる
   2. 行ったタスク名。選択したタグによって色がつけられる
      1. Sleep：ブルー
      2. Rest：グリーン
      3. Task：イエロー
      4. Other：グレー
   3. タスクに要した時間が自動で計算される。登録内容を変更しても反映される。一番新しいタスクは次のタスクが始まるまで終了時間がわからないため，未記入になる
   4. 登録したタスクの情報を変更・削除したい場合それぞれの列のボタンから実行できる

### 実装要件

- CURD機能
  - 新規行動データ入力機能
  - 行動スケジュール表示機能
  - 行動データ削除機能
  - 行動データ編集機能

### 振り返り

#### こだわった点

タスクごとの経過時間を計算しデータベースに入れ，表示する点をこだわりました。  
タスクを新規登録する時点ではそのタスクに要した時間がわからず，また新規登録後，前後に新しくタスクが挿入されると経過時間の計算結果が変化することが考えられるので，新しいタスクが登録される度関連するタスクの経過時間が計算され，更新されるようにしました。  
[app.py](/hi-action-log/app.py) > def index() > 38~50行

~~~python
# 時系列順に並べ，新規登録したタスクの1つ前のタスクを取り出す
before_task = Post.query.order_by(Post.start_time.desc()).filter(
    Post.start_time < start_time).first()
if before_task:
    # 前にタスクがある場合，その差を計算し，
    # Time型に変換してから前のタスクの経過時間を更新する
    before_time = start_time - before_task.start_time
    before_task.duration = datetime.time(
        datetime.strptime(str(before_time), "%H:%M:%S"))

# 時系列順に並べ，新規登録したタスクの1つ後のタスクを取り出す
next_task = Post.query.order_by(Post.start_time).filter(
    Post.start_time > start_time).first()
if next_task:
    # 後ろにタスクがある場合，その差を計算し，
    # Time型に変換してから新規登録したタスクの経過時間に登録する
    duration = next_task.start_time - start_time
    duration = datetime.time(
        datetime.strptime(str(duration), "%H:%M:%S"))
~~~

#### 苦労した点

こだわった点と同じ箇所で以下のような苦労がありました。

- 新規登録するタスクの1つ前・1つ後という特定のデータを，どのような条件にすればデータベースから取り出せるかを考える時
- 経過時間を計算した後，その計算結果をそのままデータベースに登録してもエラーになってしまったので，その原因を突き止める時
- 計算結果をtimedelta型からtime型に変換する方法を探す時

また，全体の中で最も時間を要した箇所は環境構築でした。仮想環境の構築・デバック・Herokuでのデプロイでそれぞれエラーが多発し，その解明に時間がかかりました。

#### 今後追加したい機能など

- 集計/可視化：
  - 1日ごと・1週間ごと・1ヶ月ごとの行動分類の割合の集計とグラフ表示
  - 1日ごと・1週間ごと・1ヶ月ごとのタスク所用時間の集計とグラフ表示
- ユーザー認証：
  - ユーザログイン機能
  - ユーザログアウト機能
- 例外処理：エラー画面が表示されないようにする
- ユニットテスト
- ソースコードにコメントを書き，可読性を高める
