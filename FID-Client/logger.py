import logging
import logging.handlers

# syslogサーバーのホスト名またはIPアドレスとポート番号

def sendSyslog(text: str):

    SYSLOG_SERVER = '172.20.0.2'
    SYSLOG_PORT = 514

    # ロガーの設定
    logger = logging.getLogger('SyslogLogger')
    logger.setLevel(logging.INFO)

    #Syslogハンドラの設定（facilityを指定）
    syslog_handler = logging.handlers.SysLogHandler(
        address=(SYSLOG_SERVER, SYSLOG_PORT),
        facility=logging.handlers.SysLogHandler.LOG_LOCAL1)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    syslog_handler.setFormatter(formatter)

    # ロガーにハンドラを追加
    logger.addHandler(syslog_handler)

    # ログメッセージの送信
    logger.info(text)