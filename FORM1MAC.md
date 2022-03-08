m1macのためにUTMを利用している際、ディレクトリをマウントすると普段お使いのエディターでハンズオンが進めていけると思うので軽く補足しておきます。

# UTMの shared directory を設定
# ここからはrootユーザーでやると色々と楽
sudo su -
# ubuntuでdirectory shareに必要なものをinstall
apt install spice-vdagent spice-webdavd
# fstabを設定
下記を /etc/fstab に追記
http://127.0.0.1:9843 /vagrant davfs rw,user,auto,exec 0 0
# /vagrant ディレクトリを作成
mkdir /vagrant
# マウント
mount -a
# /vagrant の中身を確認
ls /vagrant
