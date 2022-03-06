# Lessons

## Lesson 0. Lessonで使用するファイルを眺めてみよう

```
/
├── commands
│    ├── __init__.py
│    ├── config.py
│    ├── data.py
│    ├── format.py
│    ├── images.py
│    ├── pull.py
│    └── run.py
├── LESSONS.md
└── mini-docker
```

- mini-docker ファイル

mini-docker コマンド受け付けるpythonファイルです。
このファイルが、コマンドを各関数にマッピングしています。

- commands ディレクトリ
コマンドラインの操作の実装ファイルが置いてあります。

コマンドとの対応関係 (詳細は、mini-docker ファイルを参照)

|       command        |      .py file      |
|----------------------|--------------------|
| ./mini-docker images | commands/images/py |
| ./mini-docker pull   | commands/pull.py   |
| ./mini-docker run    | commands/run.py    |


以下は、Lessonを進めるときに使用するヘルパーファイルです (参照するレッスンで後述します)
- commands/config.py
- commands/data.py
- commands/fetch.py
- commands/format.py
- commands/local.py


## Lesson 1. 子プロセスを立ち上げてみよう

※ 以降のレッスンでのコマンドラインの実行に関して
- コマンドラインの操作はvagrant環境の中で実行することとします (`vagrant ssh`)
- vagrant内で、root権限を有していることとします (`sudo su -`)

### clone システムコールとはなにか確認してみよう

- ドキュメント https://linuxjm.osdn.jp/html/LDP_man-pages/man2/clone.2.html

### 1-1. clone システムコールを呼び出してみよう

#### 実装
- ファイル `commands/run.py`
- 使用するモジュール `linux`
- 使用する関数 
  ```
  linux.clone(
    callback: Callable[[], None], 
    flags: int, 
    *callback_args
  )
  ```

#### 確認 (VM)
```shell
cd /vagrant

./mini-docker run
```

### 1-2.子プロセスでコマンドを受け取れるようにしてみよう

#### 実装①
- ファイル `mini-docker`
- 使用するモジュール `click`
  - 参照: https://click.palletsprojects.com
- 使用する関数アノテーション `@click.argument`


#### 実装② 〜子プロセスで任意のコマンドを実行する〜
- ファイル `commands/run.py`
- 使用するモジュール `os`
- 使用する関数 `os.execvp(file: str, args: str[])`


#### 実装③ 〜子プロセスのコマンドが終了するまでwaitする〜
- ファイル `commands/run.py`
- 使用するモジュール `os`
- 使用する関数 `os.waitpid(pid: int, options: int)`

#### 確認 (VM)
```shell
cd /vagrant
./mini-docker run echo hello world
# ---> hello world
```

### 1-3. 子プロセスでpidを出力して、確認してみよう

#### 実装
- ファイル `commands/run.py`
- 使用するモジュール `os`
- 使用する関数 `os.getpid()`

#### 確認 (VM)
```shell
cd /vagrant
 
./mini-docker run
# ---> exec_runのpid: ??? ※ 親プロセスのpidも出力して比較すると理解が深まると思います
# ---> 子プロセスのpid: ???
```


## Lesson 2. プロセスを隔離してみよう

### 2-1. cgroupを利用してcpuを制限してみよう

#### 実装
- ファイル `commands/run.py`
- 使用するモジュール `commands.cgroup as cgroup`
- 使用するクラス `cgroup.CGroup`
  - 参照: https://github.com/francisbouvier/cgroups
- 使用する関数
    - `CGroup.set_cpu_limit(cpu: float)`
    - `CGroup.add(pid: int)`

### 2-2. コマンドラインのオプションからcpu上限を設定できるようにしてみよう

#### 実装
- ファイル 
  - `mini-docker`
  - `commands/run.py`
- 使用するモジュール `click`
- 使用する関数アノテーション `@click.option`


#### 確認
VMに2つのターミナルからsshする
- 1. 確認用のVM
- 2. プロセス立ち上げ用のVM

```shell
# 1. 確認用のVM
cd /vagrant

s-tui
```
参照: [amanusk/s-tui](https://github.com/amanusk/s-tui)
※ s-tuiが使えなそうだったら、vmstatを実行しCPUのid（アイドル状態）を確認するでもいいです
例） vmstat 5 100 ←5秒間の平均負荷を100回取得する

```shell
# 2. プロセス立ち上げ用のVM
cd /vagrant

./mini-docker run --cpu 0.5 bash -c 'yes > /dev/null'
# 1.確認用のVMでcpuの推移を見てみる
^C

./mini-docker run --cpu 0.1 bash -c 'yes > /dev/null'
# 1.確認用のVMでcpuの推移を見てみる
^C
```

### 2-3. UTS名前空間を分離させてみよう

#### 実装①
- ファイル `commands/run.py`
- 使用するモジュール `linux`
- 使用する関数 `linux.clone(callback: Callable[[], None], flags: int, *callback_args)`
- 使用するフラグ(UTS名前空間) `linux.CLONE_NEWUTS`

#### 実装② 〜子プロセスでhostnameを変更する〜
- ファイル `commands/run.py`
- 使用するモジュール `linux`
- 使用する関数 `linux.sethostname(hostname: str)`

#### 確認

```shell
cd /vagrant

hostname
# ---> vagrant

./mini-docker run
# ---> set hostname: "container"

hostname
# ---> vagrant
# プロセスでのhostname変更が、host側と分離されていることを確認
```

### 2-4. PID名前空間を分離させてみよう

#### 実装①
- ファイル `commands/run.py`
- 使用するモジュール `linux`
- 使用する関数 `linux.clone(callback: Callable[[], None], flags: int, *callback_args)`
- 使用するフラグ(PID名前空間) `linux.CLONE_NEWPID`

#### 実装② 〜子プロセスでpidを出力する〜
- ファイル `commands/run.py`
- 使用するモジュール `os`
- 使用する関数 `os.getpid()`


#### 確認

```shell
cd /vagrant

ps a
#    PID TTY      STAT   TIME COMMAND
#    701 tty1     Ss+    0:00 /sbin/agetty -o -p -- \u --noclear tty1 linux
#  50902 pts/0    Ss     0:00 -bash
#  50954 pts/0    R+     0:00 ps a


./mini-docker run
# ---> pid: 1
# 子プロセスのpidがhost側と分離されていることを確認
```


## Lesson 3. OverlayFs を使用してファイルをマウントしてみよう

### 3-1. pythonからイメージを扱ってみよう

#### 準備 コンテナに使用するイメージを取得しよう

- 使用するコマンド 
```shell
./mini-docker pull busybox
```
※m1macの人はイメージ名を `arm64v8/busybox` で実行する必要がありそう

- 確認 
```shell
ls /var/opt/app/images/library_busybox_latest/contents/
```

#### 実装 busybox イメージをpythonから取得してみよう

- ファイル `commands/run.py`
- 使用するモジュール `commands.local as local`
- 使用する関数 `local.find_images()`

### 3-2. イメージのファイル群をOverlayFsとしてマウントしてみよう

#### 実装① コンテナ用のディレクトリを用意しよう
- 使用するモジュール `commands.data`
- 使用するクラス 
  - `Image`
  - `Container`
- 使用する関数
  - `Container.init_from_image(image: Image)`
- ディレクトリ構成
```
/var/opt/app/container/{image_name}_{version}_{uuid}
├── rw
└── work
```

- mountがごちゃついたときのtips
```
mount -t overlay | cut -d ' ' -f 3 | xargs -I@@ umount -f @@
```

#### 実装② 準備したディレクトリ群をoverlayfsとしてマウントしてみよう

- 使用するモジュール 
  - `linux`
  - `commands.data as data`
- 使用するクラス
  - `data.Image`
  - `data.Container`
- 使用する関数
  ```python
  rootdir = '???'
  lowerdir = '???'
  upperdir = '???'
  workdir = '???'
  linux.mount(
    'overlay',
    root_dir,
    'overlay',
    linux.MS_NODEV,
    f"lowerdir={lowerdir},upperdir={upperdir},workdir={workdir}"
  )
  ```

### 3-3. 子プロセスのルートディレクトリを変更する

#### 実装 
- 使用するモジュール `os`
- 使用する関数 
  - `os.chroot(path: str)`
  - `os.chdir(path: str)`


### overlayfsの動作確認 (VM)

```shell
cd /vagrant

./mini-docker run busybox /bin/sh

# 〜〜〜 プロセス内の処理 〜〜〜

ls -la
# --->
# total 68
# drwxr-xr-x    1 root     root          4096 Jul 13 03:05 .
# drwxr-xr-x    1 root     root          4096 Jul 13 03:05 ..
# drwxr-xr-x    2 root     root          4096 Jun 15 14:34 bin
# drwxr-xr-x    2 root     root          4096 Jun 15 14:34 dev
# ...

echo 'this file is created from container' > tmp.txt 

ls -la
# --->
# drwxr-xr-x    1 root     root          4096 Jul 15 12:48 .
# drwxr-xr-x    1 root     root          4096 Jul 15 12:48 ..
# drwxr-xr-x    2 root     root         12288 Jun  7 17:34 bin
# drwxr-xr-x    2 root     root          4096 Jun  7 17:34 dev
# ...
# drwxrwxrwt    2 root     root          4096 Jun  7 17:34 tmp
# ...

exit

# 〜〜〜 host の処理 〜〜〜

# tmp.txtがないことを確認

ls -la  /var/opt/app/images/library_busybox_latest/contents/
# --->
# drwxr-xr-x 10 root   root     4096 Jul 15 10:31 .
# drwxr-xr-x  4 root   root     4096 Jul 15 10:31 ..
# drwxr-xr-x  2 root   root    12288 Jun  7 17:34 bin
# drwxr-xr-x  2 root   root     4096 Jun  7 17:34 dev
# drwxr-xr-x  3 root   root     4096 Jun  7 17:34 etc
# drwxr-xr-x  2 nobody nogroup  4096 Jun  7 17:34 home
# drwx------  2 root   root     4096 Jun  7 17:34 root
# drwxrwxrwt  2 root   root     4096 Jun  7 17:34 tmp
# drwxr-xr-x  3 root   root     4096 Jun  7 17:34 usr
# drwxr-xr-x  4 root   root     4096 Jun  7 17:34 var

# tmp.txtはどこへ？

ls -la /var/opt/app/container/library-busybox_latest_<container_id>/
# ---> 
# drwxr-xr-x 1 root   root     4096 Jul 15 12:56 .
# drwxr-xr-x 3 root   root     4096 Jul 15 12:56 ..
# drwxr-xr-x 2 root   root    12288 Jun  7 17:34 bin
# drwxr-xr-x 2 root   root     4096 Jun  7 17:34 dev
# ...
# -rw-r--r-- 1 root   root       36 Jul 15 12:56 tmp.txt
# ...
# drwxr-xr-x 3 root   root     4096 Jun  7 17:34 usr
# drwxr-xr-x 4 root   root     4096 Jun  7 17:34 var

```


## Lesson 4. dockerイメージを指定して動かしてみよう

### 4-1. コマンドラインからイメージ名を指定できるようにしてみよう

#### 動作確認
```shell
# alpineコンテナを実行する
./mini-docker pull alpine
./mini-docker run alpine ash

# hello-worldコンテナを実行する
./mini-docker pull hello-world
./mini-docker run hello-world /hello

```

### 4-2. manifest.jsonのCMDをデフォルトコマンドとして使用できるようにしてみよう

#### 動作確認
```shell
./mini-docker run alpine

./mini-docker run hello-world
```

---

今後の展望

- /dev/nullなどのデバイスをマウントしよう
- ポートフォワードでwebサーバーを起動してみよう
