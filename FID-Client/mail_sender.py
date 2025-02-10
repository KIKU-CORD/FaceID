import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

def sender(username: str, to_address: str, passwd: str):

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.set_debuglevel(True) # enable debug output
    connection.starttls()
    connection.login('Email', '???')

    # メッセージコンテナの作成
    msg = MIMEMultipart("alternative") # MIME type は multipart/alternative
    msg["Subject"] = "【FaceID】メール認証（" + username + "様）" # メール表題
    msg["From"] = formataddr(("FaceID System", "Email"))
    msg["To"] = to_address # 送信先のメールアドレスの設定

    # 平文でのメッセージ本体の作成
    text = """
        Text Line
        """

    # HTMLでのメッセージ本体の作成
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Python HTML メールサンプル</title>
            <style>
                body {
                    background-color: #f6f9fc;
                }
                .container {
                    margin: auto;
                    width: 60%;
                    padding: 10px;
                    border-radius: 20px;
                    background-color: white;
                }
                .container span {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <p>
                    ご利用いただきありがとうございます。<br/>
                    以下のパスワードを入力して認証をお願いします。<br/><br/>
                    <span>""" + passwd + """</span> <br/><br/>
                    ※ ５分経過すると顔認証がリセットされます。

                </p>
            </div>
        </body>
        </html>
        """

    # メッセージコンテナにメッセージ本体を設定
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    
    connection.sendmail("Email", to_address, msg.as_string())

    connection.quit()

def senderRadius(uuidstr: str, username: str, to_address: str):

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.set_debuglevel(True) # enable debug output
    connection.starttls()
    connection.login('Email', '???')

    # メッセージコンテナの作成
    msg = MIMEMultipart("alternative") # MIME type は multipart/alternative
    msg["Subject"] = "【FaceID】RADIUS 認証（" + username + "様）" # メール表題
    msg["From"] = formataddr(("FaceID System", "Email")) # 送信元の名前とメールアドレスの設定。メールアドレス直接指定でも可。
    msg["To"] = to_address # 送信先のメールアドレスの設定

    url = 'https://172.20.0.1/in/' + uuidstr

    # 平文でのメッセージ本体の作成
    text = """
        Text Line
        """

    # HTMLでのメッセージ本体の作成
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Python HTML メールサンプル</title>
            <style>
                body {
                    background-color: #f6f9fc;
                }
                .container {
                    margin: auto;
                    width: 60%;
                    padding: 10px;
                    border-radius: 20px;
                    background-color: white;
                }
                .link {
				    background-color: #007fff;
				    width: fit-content;
				    margin: 5px;
				    padding: 10px 20px;
				    border-radius: 5px;
			    }
			    .link a{
				    color: aliceblue;
				    text-decoration: none;
			    }
                .container span {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <p>
                    ご利用いただきありがとうございます。<br/>
                    ご登録いただいたユーザー名とパスワードを入力してください。<br/><br/>
                    <span>下のリンクから認証をお願いいたします。</span> <br/><br/>
                </p>
                <div class="link"><a href=""" + url + """>クリックで認証</a></div>
            </div>
        </body>
        </html>
        """

    # メッセージコンテナにメッセージ本体を設定
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    
    connection.sendmail("Email", to_address, msg.as_string())

    connection.quit()

def senderRadiusHarry(uuidstr: str, username: str, to_address: str):

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.set_debuglevel(True) # enable debug output
    connection.starttls()
    connection.login('Email', '???')

    # メッセージコンテナの作成
    msg = MIMEMultipart("alternative") # MIME type は multipart/alternative
    msg["Subject"] = "【FaceID】* 早急 * RADIUS 認証（" + username + "様）" # メール表題
    msg["From"] = formataddr(("FaceID System", "Email")) # 送信元の名前とメールアドレスの設定。メールアドレス直接指定でも可。
    msg["To"] = to_address # 送信先のメールアドレスの設定

    url = 'https://172.20.0.1/in/' + uuidstr

    # 平文でのメッセージ本体の作成
    text = """
        Text Line
        """

    # HTMLでのメッセージ本体の作成
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Python HTML メールサンプル</title>
            <style>
                body {
                    background-color: #f6f9fc;
                }
                .container {
                    margin: auto;
                    width: 60%;
                    padding: 10px;
                    border-radius: 20px;
                    background-color: white;
                }
                .link {
				    background-color: #007fff;
				    width: fit-content;
				    margin: 5px;
				    padding: 10px 20px;
				    border-radius: 5px;
			    }
			    .link a{
				    color: aliceblue;
				    text-decoration: none;
			    }
                .container span {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <p>
                    ご利用いただきありがとうございます。<br/><br/>
                    <span>ユーザー様は複数人での入室扱いとなっております。</span> <br/>
                    <span>この認証を必ず２分以内に完了させてください。</span> <br/><br/>
                    ご登録いただいたユーザー名とパスワードを入力してください。<br/><br/>
                    <span>下のリンクから認証をお願いいたします。</span> <br/><br/>
                </p>
                <div class="link"><a href=""" + url + """>クリックで認証</a></div>
            </div>
        </body>
        </html>
        """

    # メッセージコンテナにメッセージ本体を設定
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    
    connection.sendmail("Email", to_address, msg.as_string())

    connection.quit()

def senderResult(username: str, to_address: str):

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.set_debuglevel(True) # enable debug output
    connection.starttls()
    connection.login('Email', '???')

    # メッセージコンテナの作成
    msg = MIMEMultipart("alternative") # MIME type は multipart/alternative
    msg["Subject"] = "【FaceID】すべての認証完了（" + username + "様）" # メール表題
    msg["From"] = formataddr(("FaceID System", "Email")) # 送信元の名前とメールアドレスの設定。メールアドレス直接指定でも可。
    msg["To"] = to_address # 送信先のメールアドレスの設定

    # 平文でのメッセージ本体の作成
    text = """
        Text Line
        """

    # HTMLでのメッセージ本体の作成
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Python HTML メールサンプル</title>
            <style>
                body {
                    background-color: #f6f9fc;
                }
                .container {
                    margin: auto;
                    width: 60%;
                    padding: 10px;
                    border-radius: 20px;
                    background-color: white;
                }
                .container span {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <p>
                    ご利用いただきありがとうございます。<br/>
                    すべての認証が完了しました。<br/>
                    前方のドアが開きますのでご注意ください。<br/><br/>
                    <span>""途中入退出用のメールもご確認ください。""</span> <br/><br/>
                </p>
            </div>
        </body>
        </html>
        """

    # メッセージコンテナにメッセージ本体を設定
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    
    connection.sendmail("Email", to_address, msg.as_string())

    connection.quit()

def senderOut(uuidstr: str, username: str, to_address: str):

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.set_debuglevel(True) # enable debug output
    connection.starttls()
    connection.login('Email', '???')

    # メッセージコンテナの作成
    msg = MIMEMultipart("alternative") # MIME type は multipart/alternative
    msg["Subject"] = "【FaceID】途中入退出・退出について（" + username + "様）" # メール表題
    msg["From"] = formataddr(("FaceID System", "Email")) # 送信元の名前とメールアドレスの設定。メールアドレス直接指定でも可。
    msg["To"] = to_address # 送信先のメールアドレスの設定

    mid_in_url = 'https://172.20.0.1/mid-in/' + uuidstr
    out_url = 'https://172.20.0.1/out/' + uuidstr

    # 平文でのメッセージ本体の作成
    text = """
        Text Line
        """

    # HTMLでのメッセージ本体の作成
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Python HTML メールサンプル</title>
            <style>
                body {
                    background-color: #f6f9fc;
                }
                .container {
                    margin: auto;
                    width: 60%;
                    padding: 10px;
                    border-radius: 20px;
                    background-color: white;
                }
                .link1 {
				    background-color: #007fff;
				    width: fit-content;
				    margin: 5px;
				    padding: 10px 20px;
				    border-radius: 5px;
			    }
                .link2 {
				    background-color: #ff6347;
				    width: fit-content;
				    margin: 5px;
				    padding: 10px 20px;
				    border-radius: 5px;
			    }
			    .link1 a{
				    color: aliceblue;
				    text-decoration: none;
			    }
                .link2 a{
				    color: aliceblue;
				    text-decoration: none;
			    }
                .container span {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <p>
                    ご利用いただきありがとうございます。<br/>
                    お部屋からの途中入退出・退出についてお伝えします。<br/>
                    以下のボタンを押すことで鍵の解錠操作が行えます。<br/><br/>
                    <span>途中退出については手動でドアの鍵を解錠いただけます。</span><br/>
                    <span>退出をすると再入室できなくなるのでご注意ください。</span><br/><br/>
                </p>
                <div class="link1"><a href=""" + mid_in_url + """>再入室</a></div>
                <div class="link2"><a href=""" + out_url + """>退出</a></div>
            </div>
        </body>
        </html>
        """

    # メッセージコンテナにメッセージ本体を設定
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    
    connection.sendmail("Email", to_address, msg.as_string())

    connection.quit()
