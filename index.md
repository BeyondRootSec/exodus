## Exodus - Version 1.0.0

### ☑️ Currently Supported Protocols

* SMB
* SSH
* FTP

### 📌 To Do

* TELNET
* LDAP
* KERBEOS
* HTTP


### 🛠 Installation

```sh
git clone https://github.com/spicesouls/exodus
cd exodus && pip install -r requirements.txt
chmod +x exodus.py
```

### 📃 Usage

```sh
./exodus.py [ IP / CIDR ] [ PROTOCOL ] -u [ USERNAME ] -p [ PASSWORD ] -t [ THREADS ]
```

### 📖 Examples

#### Finding weak SSH Logins

```sh
./exodus.py 192.168.1.0/24 ssh -u admin -p admin
```

#### Finding Services Accepting Anonymous FTP

```sh
./exodus.py 192.168.1.0/24 ftp -u anonymous
```

![](https://raw.githubusercontent.com/spicesouls/exodus/main/exodus.png)

My Blog: https://beyondrootsec.wordpress.com

BTC Donations: 1CQvmpRCDasK7YKyjsQTZPUobRygqt86t7

**🚧! THIS IS FOR STRICTLY EDUCATIONAL PURPOSES, I AM NOT RESPONSIBLE FOR YOUR USE OF THIS !🚧**
