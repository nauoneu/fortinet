# fortinet
How to use:

1. Github ユーザーの設定
git config --global user.name <name>
git config --global user.email <email>

2. ローカルリポジトリの初期化
cd path\to\repo
git init
git branch -M main

3. リモートリポジトリを追加
git remote set-url origin git@github.com:nauoneu/fortinet.git

4. リポジトリを取得
git pull origin main

5. 新規作成/変更をプッシュ
git add <ファイル名>
git commit -m <コメント>
git push origin main

6. ブランチ関連
ローカルに作成 - git branch <ブランチ名>
ローカルで移動 - git checkout <ブランチ名>
リモートを更新 - git push origin <ブランチ名>
