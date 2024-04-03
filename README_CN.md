# OneClickEH
一款简单却便利的工具，适用于希望通过上传种子到E-Hentai画廊来赚取GPs的用户。

## 如果您...
- 在PC上浏览E-Hentai，并且**拥有一台安装了qbittorrent的Linux服务器**。
- 想要赚取一些GPs，但由于某些原因无法使用H@H。
- 只是想帮助那些缺少GPs的人。

## 这款工具能做什么？（流程）
1. 向服务器发送信号下载画廊
2. 创建一个种子文件，上传至EH
3. 种子做种

## 使用方法
1. 右键点击画廊，选择"通过OneClickEH做种"。
2. 检查"Torrent Download (x)"。你已经添加了一个种子到画廊。你将通过你上传的种子下载赚取GPs。

## 安装
您需要安装OneClickEH扩展和OneClickEH服务器。

### OneClickEH扩展（在您的本地PC上）
1. 安装[OneClickEH扩展](https://github.com/Tofudry233/OneClickEH_ext)。

### OneClickEH服务器（在您的远程服务器上）
1. 先决条件：[Qbittorrent-nox](https://github.com/userdocs/qbittorrent-nox-static)、Python、Conda
2. [下载OneClickEH](https://github.com/Tofudry233/OneClickEH_ext/archive/refs/heads/master.zip)
3. 安装依赖项：pip install -r requirements.txt
4. 配置configs.json
5. 开放端口（假设您将其设置为9999）：sudo ufw allow 9999
6. 运行服务器：python main.py
7. 建议使用screen在后台运行（以Ubuntu为例）：
   1. 安装screen：sudo apt-get install screen
   2. 创建一个新会话：screen -S OneClickEH
   3. cd到目录：cd /path/to/OneClickEH
   4. 运行python main.py
   5. 分离screen，这样即使关闭终端也会继续运行：Ctrl+A+D
   6. 恢复screen：screen -r OneClickEH

## Configs.json
- "eh"：e-hentai和ex-hentai的cookies。从浏览器获取这些，并在此处输入。
- "qb"：您的qbittorrent WebUI的设置。
  - "host"：您的VPS的IP地址
  - "port"：您的qbittorrent WebUI的端口。
  - "username" 和 "password"：您登录qbittorrent WebUI的信息
- "server"：这款OneClickEH连接的设置
  - "host"：保持为"0.0.0.0"。
  - "port"：服务器监听的端口。这应该设置为与OneClickEH扩展中的相同
  - "passwd"：验证入站连接的密码。这应该设置为与OneClickEH扩展中的相同
- "path"：保存文件的路径。
  - "archive"：下载的存档将被存储的位置。
  - "temp"：一些临时文件将被存储的地方，包括创建的种子文件。
  - "torrent"：下载的种子文件将被存储的位置。
- "qb_api"：qbittorrent的一些高级设置。
  - "ratio_limit"：达到此比例时，种子将停止上传。这是为了节省您的带宽。如果您不想限制上传比例，设置为0。
  - "is_paused"：如果您想手动启动种子，设置为1。否则保持为0，这样做种将自动开始。