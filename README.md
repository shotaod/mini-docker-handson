# Mini Docker ハンズオン
学習用のなんちゃってDockerのハンズオンです

## セットアップ

### vagrantのインストール

https://www.vagrantup.com/downloads

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

./mini-docker pull hello-world
# ---> pull command called! image: hello-world

./mini-docker images
# ---> images command called!

./mini-docker run hello-world
# ---> run command called! image: hello-world
```

お疲れさまです。
事前に実施していただきたいセットアップはこれで以上となります。


## ハンズオン
---> [ハンズオン資料](./LESSONS.md) (当日はこちらの資料を使用してハンズオン形式で進めます。)
