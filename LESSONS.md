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
このファイルが、コマンドを、各関数にマッピングシています。

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
- 使用する関数アノテーション `@click.argument`


#### 実装② ~子プロセスで任意のコマンドを実行する~
- ファイル `commands/run.py`
- 使用するモジュール `os`
- 使用する関数 `os.execvp(file: str, args: str[])`


#### 実装③ ~子プロセスのコマンドが終了するまでwaitする~
- ファイル `commands/run.py`
- 使用するモジュール `os`
- 使用する関数 `os.wait(pid: int)`


#### 確認 (VM)
```shell
cd /vagrant
./mini-docker echo hello world
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

ps
# --->
#    PID TTY      STAT   TIME COMMAND
#    701 tty1     Ss+    0:00 /sbin/agetty -o -p -- \u --noclear tty1 linux
#  50902 pts/0    Ss     0:00 -bash
#  50954 pts/0    R+     0:00 ps a
 
./mini-docker run
# ---> pid: ???
```


## Lesson 2. リソースを制御してみよう

### 2-1. cgroupを利用してcpuを制限してみよう

#### 実装
- ファイル `commands/run.py`
- 使用するモジュール `commands.cgroup as cgroup`
- 使用するクラス `cgroup.Cgroup`
- 使用する関数
    - `Cgroup.set_cpu_limit(cpu: float)`
    - `Cgroup.add(pid: int)`

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


```shell
# 2. プロセス立ち上げ用のVM
cd /vagrant

./mini-docker run --cpus 0.5 yes > /dev/null
# 1.確認用のVMでcpuの推移を見てみる
^C

./mini-docker run --cpus 0.1 yes > /dev/null
# 1.確認用のVMでcpuの推移を見てみる
^C
```


## Lesson 3. UTS名前空間を分離させてみよう

### UTS名前空間を分離させてプロセスを立ち上げてみよう

#### 実装①
- ファイル `commands/run.py`
- 使用するモジュール `linux`
- 使用する関数 `linux.clone(callback: Callable[[], None], flags: int, *callback_args)`
- 使用するフラグ(UTS名前空間) `linus.CLONE_NEWUTS`

#### 実装② ~子プロセスでhostnameを変更する~
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


## Lesson 4. PID名前空間を分離させてみよう

### PID名前空間を分離させてプロセスを立ち上げてみよう

#### 実装①
- ファイル `commands/run.py`
- 使用するモジュール `linux`
- 使用する関数 `linux.clone(callback: Callable[[], None], flags: int, *callback_args)`
- 使用するフラグ(PID名前空間) `linus.CLONE_NEWPID`

#### 実装② ~子プロセスでpidを出力する~
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

## Lesson 5. dockerイメージを触ってみよう

### dockerイメージをpullしてみよう

#### 実装
- ファイル `commands/pull.py`
- 使用するモジュール
    - `tarfile`
    - `commands.fetch`
- 使用する関数
    - tarfile
      - `tarfile.write`
      - `tarfile.open`
      - `tarfile.extractall`
    - commands.fetch
      - `fetch_auth_token`
      - `fetch_manifest`
      - `fetch_layer`

#### 確認
```shell
cd /vagrant

./mini-docker pull hello-world
./mini-docker pull alpine
./mini-docker pull busybox
```


### dockerイメージの一覧をいい感じに出力してみよう
- ファイル `commands/images.py`
- 使用するモジュール 
  - `terminaltables as tt`
  - `commands.local as local`
- 使用するクラス `tt.AsciiTable(data: str[][])`
- 使用する関数
  - `local.find_images()`
  - `tt.AsciiTable.table`

#### 確認
```shell
cd /vagrant

./mini-docker images

# ---> ？？？
```

## Lesson 6. dockerイメージを動かしてみよう

### dockerイメージのファイルを子プロセスで扱えるようにしてみよう

- ファイル `commands/run.py`

#### 実装① 子プロセス用のディレクトリ群を作成する
- 使用するモジュール `commands.data`
- 使用するクラス 
  - `Image`
  - `Container`
- 使用する関数
  - `Container.init_from_image(image: Image)`
- ディレクトリのアウトプットイメージ
```
/var/opt/app/container/<container identifier>/
├── cow_rw
│   └── root
└── cow_workdir
    └── work
```
- 実装イメージ
```python
# run.py

def _mount_overlay_fs(image: Image, container: Container):
    # todo implement here
    pass
```


#### 実装② 子プロセスのディレクトリ群をoverlayfsとしてマウントする
実装①で準備したディレクトリ群をマウントしてみよう

- 使用するモジュール `linux`
- 使用する関数
  ```python
  linux.mount(
    'overlay',
    root_dir,
    'overlay',
    linux.MS_NODEV,
    f"lowerdir={image.content_dir},upperdir={rw_dir},workdir={work_dir}"
  )
  ```

#### 実装③ 子プロセスのルートディレクトリを変更する
- 使用するモジュール `os`
- 使用する関数 `os.chroot(path: str)`

#### 確認 (VM)

```shell
cd /vagrant

./mini-docker run alpine ash

# ~~~ プロセス内の処理 ~~~

ls -la
# --->
# total 68
# drwxr-xr-x    1 root     root          4096 Jul 13 03:05 .
# drwxr-xr-x    1 root     root          4096 Jul 13 03:05 ..
# drwxr-xr-x    2 root     root          4096 Jun 15 14:34 bin
# drwxr-xr-x    2 root     root          4096 Jun 15 14:34 dev
# ...

```

## Lesson 7. 各種linuxシステムディレクトリをマウントしよう

### 実装
```python
# proc, sys, dev の linux システムディレクトリの作成
proc_dir = os.path.join(container.root_dir, 'proc')  # proc: PIDなどプロセスの情報
sys_dir = os.path.join(container.root_dir, 'sys')  # sys: ドライバ関連のプロセスの情報
dev_dir = os.path.join(container.root_dir, 'dev')  # dev: CPUやメモリなど基本デバイス
for d in (proc_dir, sys_dir):
    if not os.path.exists(d):
        os.makedirs(d)

# システムディレクトリのマウント
print('mounting /proc, /sys, /dev, /dev/pts')
linux.mount('proc', proc_dir, 'proc', 0, '')
linux.mount('sysfs', sys_dir, 'sysfs', 0, '')
```

---

今後の展望

- /dev/nullなどのデバイスをマウントしよう
- ポートフォワードでwebサーバーを起動してみよう
