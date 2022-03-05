# Mini Docker ハンズオン
学習用のなんちゃってDockerのハンズオンです

## セットアップ

### vagrantのインストール

https://www.vagrantup.com/downloads

※ m1macの方はvagrantが利用できないかもしれません。その場合は他のソフトウェア（UTMなど）を利用し、ubuntu-20.xの環境が立ち上がればOKです。
環境ができたら `vagrant up` で行われるprovisioner.sh内の処理を実行してください。

参考: https://gihyo.jp/admin/serial/01/ubuntu-recipe/0672

### VMの作成と起動

```bash
vagrant up
vagrant ssh
```

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
