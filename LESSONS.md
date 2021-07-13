# Lessons

## 子プロセスを立ち上げてみよう

### clone システムコールとはなにか確認してみよう

- ドキュメント https://linuxjm.osdn.jp/html/LDP_man-pages/man2/clone.2.html

### clone システムコールを呼び出してみよう

#### 実装
- ファイル `commands/run.py`
- 使用するモジュール `linux`
- 使用する関数 `linux.clone(callback: Callable[[], None], flags: int, *callback_args)`

#### 確認 (VM)
```shell
cd /vagrant

./mini-docker run~~~~
```

### 子プロセスでコマンドを受け取れるようにしてみよう

#### 実装①
- ファイル `mini-docker`
- 使用するモジュール `click`
- 使用する関数アノテーション `@click.argument`


#### 実装② ~子プロセスで任意のコマンドを実行する~
- ファイル `commands/run.py`
- 使用するモジュール `os`
- 使用する関数 `os.execvp(file: str, args: str[])`



#### 確認 (VM)
```shell
cd /vagrant
./mini-docker echo hello world
# ---> hello world
```


### 子プロセスでpidを出力して、確認してみよう

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


## リソースを制御してみよう

### cgroupを利用してcpuを制限してみよう

#### 実装
- ファイル `commands/run.py`
- 使用するモジュール `cgroups`
- 使用するクラス/関数
    - cgroups.Cgroup
    - Cgroup.set_cpu_limit(cpus: int)
    - Cgroup.add(pid: int)

### コマンドラインのオプションからcpu上限を設定できるようにしてみよう

#### 実装①
- ファイル `mini-docker`
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


## UTS名前空間を分離させてみよう

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


## PID名前空間を分離させてみよう

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

## dockerイメージを触ってみよう

### dockerイメージをpullしてみよう

#### 実装
- ファイル `commands/pull.py`
- 使用する関数
    - `_fetch_auth_token`
    - `_fetch_manifest`
    - `_fetch_layer`

#### 確認
```shell
cd /vagrant

./mini-docker pull hello-world
./mini-docker pull alpine
./mini-docker pull busybox
```

### dockerイメージの一覧をいい感じに出力してみよう
- ファイル `commands/images.py`
- 使用するモジュール `terminaltables`
- 使用するクラス `AsciiTable(data: str[][])`
- 使用する関数 `AsciiTable.table`

#### 確認
```shell
cd /vagrant

./mini-docker images
```

## dockerイメージのファイルシステムを子プロセスで扱えるようにしてみよう
- ファイル `commands/run.py`

### 実装① 子プロセス用のディレクトリ群を作成する
```
/var/opt/app/container/<container identifier>/
├── cow_rw
│   └── root
└── cow_workdir
    └── work
```

### 実装② 子プロセスのディレクトリ群をoverlayfsとしてマウントする
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

### 実装③ 子プロセスのルートディレクトリを変更する
- 使用するモジュール `os`
- 使用する関数 `os.chroot(path: str)`

### 確認 (VM)

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

## 各種linuxシステムディレクトリをマウントしよう

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

todo write

- /dev/nullなどのデバイスをマウントしよう
- ポートフォワードでwebサーバーを起動してみよう
