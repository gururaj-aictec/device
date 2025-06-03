import logging
from logging import handlers
import datetime
from enum import Enum
import os
from Helpers.log_conf import Logger
class LogHelper:

    @staticmethod
    def Send(message, sn=""):
        print("Send:>>>>>>>>>>>>>>>>>>>>")
        datetimestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sn_=""
        if sn is None or len(sn) == 0:
            sn_=""
        else:
            sn_ = "[" + sn + "]"
        msg=f"{datetimestr}[Info]{sn_}{message}"
        print(msg)
        LogHelper._FlowLog(FlowType.SEND, msg, sn)

    @staticmethod
    def Receive(message, sn=""):
        print("Recv:<<<<<<<<<<<<<<<<<<<<")
        datetimestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sn_ = ""
        if sn is None or len(sn) == 0:
            sn_ = ""
        else:
            sn_ = "[" + sn + "]"
        msg = f"{datetimestr}[Info]{sn_}{message}"
        LogHelper._FlowLog(FlowType.RECIVE, msg, sn)

    # / <summary>
    # / 流程日志
    # / </summary>
    # / <param name="folowType"></param>
    # / <param name="msg"></param>
    # / <param name="sn"></param>
    @staticmethod
    def _FlowLog(folowType, msg, sn=""):

        try:
            currentPath = os.getcwd()
            if sn is None or len(sn) == 0 == False:
                currentPath = currentPath+'/'+sn+'/'
            if not os.path.exists(currentPath):
                os.mkdir(currentPath)

            if folowType == FlowType.SEND:
                content = "Send:>>>>>>>>>>>>>>>>>>> \r\n" +  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + msg
            else:
                content = "Recv:<<<<<<<<<<<<<<<<<<< \r\n" +  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + msg

            fileName=currentPath + "/Flow_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".Log"
            LogHelper.logger(fileName,content)

        except:
            import traceback
            traceback.print_exc()

        finally:
            # sw.Close()
            pass

    @staticmethod
    def Error_(message, sn=""):

        datetimestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if sn is None or len(sn) == 0:
            sn_ = ""
        else:
            sn_ = "[" + sn + "]"
        msg = f"{datetimestr}[Info]{sn_}{message}"
        #print(msg)
        LogHelper._WriteLog(msg, sn)

    @staticmethod
    def Info_(message, sn=""):

        datetimestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if sn is None or len(sn) == 0:
            sn_ = ""
        else:
            sn_ = "[" + sn + "]"
        msg = f"{datetimestr}[Info]{sn_}{message}"
        #print(msg)
        LogHelper._WriteLog(msg, sn)

    # / <summary>
    # / 写日志
    # / <param name="msg">日志内容</param>
    # / <param name="logType">日志类型</param>
    # / </summary>
    @staticmethod
    def _WriteLog(msg, sn=""):

        try:
            currentPath = os.getcwd()
            if sn is None or len(sn) == 0 == False:
                currentPath = currentPath + '/' + sn + '/'
            if not os.path.exists(currentPath):
                os.mkdir(currentPath)

            fileName = currentPath + "/Flow_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".Log"
            LogHelper.logger(fileName, msg)
        except:
            import traceback
            traceback.print_exc()
        finally:
            pass


class FlowType(Enum):

    SEND=0,
    RECIVE=1



