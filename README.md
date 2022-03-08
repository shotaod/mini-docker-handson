# Mini Docker ハンズオン
学習用のなんちゃってDockerのハンズオンです

## セットアップ

### vagrantのインストールとセットアップ

https://www.vagrantup.com/downloads

```bash
vagrant up
vagrant ssh
```

#### ※ m1macの方へ
m1macではvagrantが利用できないようです。その場合は他のソフトウェア（UTMなど）を利用し、ubuntu-20.x（20.4推奨）の環境を用意してください。
環境ができたら、本来は `vagrant up` の中で行われるprovisioner.sh内の処理を実行してください。（cd /vagrant...のコードを消して実行するなどの対応をお願いします🙇‍♀️）
また、ハンズオンを進めるにあたりコードが書きやすい環境になっていると良いと思います。（ubuntu desktopを入れてeditorを起動する、ディレクトリのマウントをするなど）

参考: https://gihyo.jp/admin/serial/01/ubuntu-recipe/0672

### VMの動作確認
以下の動作確認はVM内で実施してください。

- OSの確認

```bash
cat /etc/os-release

# --->
# NAME="Ubuntu"
# VERSION="20.10 (Groovy Gorilla)" 
```

- コマンドの確認

```bash
cd /vagrant

./mini-docker pull
# ---> pull command called!

./mini-docker images
# ---> images command called!

./mini-docker run
# ---> run command called!
```

お疲れさまです。
事前に実施していただきたいセットアップはこれで以上となります。


## ハンズオン
---> [ハンズオン資料](./LESSONS.md) (当日はこちらの資料を使用してハンズオン形式で進めます。)
