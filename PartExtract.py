# -*- coding: utf-8 -*-

import argparse
import configparser
import os
import shutil
import sys
import time
import winreg
from subprocess import *
import wx
import wx.xrc



# 判断NX目录是否正确
def ugpcfile(ugpath):
    if ugpath[-1] == "\\":
        ugpath = ugpath[:-1]
    if os.path.exists(f"{ugpath}\\UGII\\ugpc.exe"):
        ugpcpath = f"{ugpath}\\UGII\\ugpc.exe"
    elif os.path.exists(f"{ugpath}\\NXBIN\\ugpc.exe"):
        ugpcpath = f"{ugpath}\\NXBIN\\ugpc.exe"
    else:
        ugpcpath = ""
    return ugpcpath


# 读取配置文件
def readconf():
    ugpath = os.getenv('UGII_BASE_DIR')  # 读取NX目录
    ugpcpath = ugpcfile(ugpath)
    ispack = False
    isdel = False
    isfolder = False
    sufnum = 1
    zippath = f'{os.getcwd()}\\7z.exe'
    cf = configparser.ConfigParser()
    if os.path.exists("C:/ProgramData/unpack_conf.ini"):
        cf.read("C:/ProgramData/unpack_conf.ini")
        if cf.has_option("DEFAULT", "ugpath") and cf.get("DEFAULT", "ugpath") != "":
            ugpath = cf.get("DEFAULT", "ugpath")
            ugpcpath = ugpcfile(ugpath)
        if cf.has_option("DEFAULT", "ispack") and cf.get("DEFAULT", "ispack") != "":
            ispack = cf.get("DEFAULT", "ispack") == "True"
        if cf.has_option("DEFAULT", "isdel") and cf.get("DEFAULT", "isdel") != "":
            isdel = cf.get("DEFAULT", "isdel") == "True"
        if cf.has_option("DEFAULT", "sufnum") and cf.get("DEFAULT", "sufnum") != "":
            sufnum = int(cf.get("DEFAULT", "sufnum"))
        if cf.has_option("DEFAULT", "isfolder") and cf.get("DEFAULT", "isfolder") != "":
            isfolder = cf.get("DEFAULT", "isfolder") == "True"
        if cf.has_option("DEFAULT", "zippath") and cf.get("DEFAULT", "zippath") != "":
            zippath = cf.get("DEFAULT", "zippath")
    else:
        saveconf(ugpath, ispack, isdel, isfolder, sufnum)
    return ugpcpath, ugpath, ispack, isdel, isfolder, sufnum,zippath


# 保存配置信息
def saveconf(ugpath, ispack, isdel, isfolder, sufnum):
    ispack = str(ispack)
    isdel = str(isdel)
    isfolder = str(isfolder)
    sufnum = str(sufnum)
    zippath = f'{os.getcwd()}\\7z.exe'
    cf = configparser.ConfigParser()
    cf.read("C:/ProgramData/unpack_conf.ini")
    if ugpcfile(ugpath) != "":
        cf.set("DEFAULT", 'ugpath', ugpath)
    else:
        print("设置的目录不正确，请重新设置")
        wx.MessageBox(u'NX目录设置不正确，请重新设置', u'错误', wx.OK | wx.ICON_ERROR)
    if ispack != "":
        cf.set("DEFAULT", 'ispack', ispack)
    if isdel != "":
        cf.set("DEFAULT", 'isdel', isdel)
    if isfolder != "":
        cf.set("DEFAULT", 'isfolder', isfolder)
    if sufnum != "":
        cf.set("DEFAULT", 'sufnum', sufnum)
    cf.set("DEFAULT", 'zippath', zippath)
    try:
        with open("C:/ProgramData/unpack_conf.ini", 'w') as f:
            cf.write(f)
    except:
        wx.MessageBox(u'配置信息保存失败', u'提示', wx.OK | wx.ICON_INFORMATION)
    else:
        wx.MessageBox(u'配置信息保存成功', u'提示', wx.OK | wx.ICON_INFORMATION)


# 复制文件
def copyfiles(folderpath, fileslist):
    n = 0
    e = 0
    errfile = []
    progressMax = len(fileslist)
    dialog = wx.ProgressDialog("状态", "开始提取文件", progressMax)  # , style=wx.PD_CAN_ABORT)
    for file in fileslist:
        try:
            shutil.copy(file, folderpath)
            keepGoing = dialog.Update(n, newmsg=f"正在复制文件{file}")
            if keepGoing == False:
                sys.exit()
        except:
            e = e + 1
            errfile.append(file)
            print(f"文件:{file}复制失败")
        else:
            n = n + 1
    if errfile == []:
        print(f"所有{n}个文件成功复制。")
    else:
        print(f"成功复制了{n}个文件,{e}个文件复制失败:\n{'、'.join(errfile)}")
    dialog.Destroy()
    return errfile


# 通过ugpc.exe提取part文件的装配树相关文件列表
def getparts(checkpart, folder=""):
    ugpcpath, ugpath, ispack, isdel, isfolder, sufnum,zippath = readconf()
    if ugpcpath == "":
        wx.MessageBox(u'NX目录设置不正确，请重新设置', u'错误', wx.OK | wx.ICON_ERROR)
        sys.exit()
    dialog = wx.ProgressDialog("状态", "正在读取装配树信息", 0)
    p = Popen([ugpcpath, checkpart], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    dialog.Destroy()
    stdout, stderr = p.communicate()
    stdout = stdout.decode()
    stderr = stderr.decode()
    stdnote = ""
    lostlist = []
    suffolder = ["%y%m%d", "%Y%m%d", "%y%m%d%H%M%S", "%Y%m%d%H%M%S"]
    #判断文件是否正确
    if stdout == "":
        if "File " + checkpart + " not found" in stderr:
            stdnote = "选择的文件不是NX文件"
        elif "Error:" in stderr:
            stdnote = "选择的文件不正确，可能文件版本过高"
        else:
            stdnote = "选择的文件不正确，请检查。"
    elif stdout != "" and "has no assembly structure" in stderr:
        stdnote = "选择的文件不是装配文件，请选择装配文件"
    else:
        # 读取装配树信息
        partlist = stdout.splitlines()

        if " not found" in stderr:
            errlist = [i[5:-10] for i in stderr.splitlines()]
            lostlist = [i.split("\\")[-1] for i in errlist]
        if lostlist == []:
            print(f"找到{len(partlist)}个文件，没有丢失文件")
        else:
            print(f"部分文件未找到:{'、'.join(lostlist)}")

        # 获取文件当前目录及上一级目录
        if isfolder == False and folder == "":
            pathlist = checkpart.replace('/', '\\').split('\\')
            if ":" in pathlist[-2]:
                parentpath = "/".join(pathlist[:-1])
                newfolder = pathlist[-1][:-4]
            else:
                parentpath = "/".join(pathlist[:-2])
                newfolder = pathlist[-2]
            nowtime = time.strftime(suffolder[sufnum], time.localtime())
            newfolder = newfolder + "-" + nowtime
            newpath = parentpath + "/" + newfolder
            if os.path.exists(newpath):
                print(f"目录<{newpath}>已经存在，文件夹增加时间后缀")
                newpath = newpath + time.strftime("%H%M%S", time.localtime())
            os.mkdir(newpath)
            print(f"新目录<{newpath}>创建成功")
        else:
            if folder == "":
                dlg = wx.DirDialog(None, u'请选择提取文件夹', style=wx.DD_DEFAULT_STYLE)
                dlg.ShowModal()
                newpath = dlg.GetPath()
                dlg.Destroy()
            else:
                newpath = folder
            pathlist = newpath.replace('/', '\\').split('\\')

            if ":" in pathlist[0]:
                parentpath = pathlist[0]
                newfolder = checkpart.replace('/', '\\').split('\\')[-1][:-4]
                nowtime = time.strftime(suffolder[sufnum], time.localtime())
                newfolder = newfolder + "-" + nowtime
                newpath = parentpath + "/" + newfolder
                if os.path.exists(newpath):
                    print(f"目录<{newpath}>已经存在，文件夹增加时间后缀")
                    newpath = newpath + time.strftime("%H%M%S", time.localtime())
                os.mkdir(newpath)
            else:
                parentpath = "/".join(pathlist[:-1])

        errfile = copyfiles(newpath, partlist)  # 复制文件

        lostlist = lostlist + errfile  # 合并缺失文件
        lostnote = f"部分文件未找到，缺失{len(lostlist)}个文件:\n{'、'.join(lostlist)} \n\n是否继续打包"

        # 打包压缩文件
        if ispack == False:
            dlg = wx.MessageDialog(None, u'是否需要打包提取的文件夹', u'请选择', wx.YES_NO | wx.ICON_INFORMATION)
            if dlg.ShowModal() == wx.ID_YES:
                if lostlist != []:
                    dlg = wx.MessageDialog(None, lostnote, u'请选择是否继续', wx.YES_NO | wx.ICON_ERROR)
                    if dlg.ShowModal() == wx.ID_YES:
                        ispack = True
                else:
                    ispack = True
            dlg.Destroy()
        if isdel == False and ispack == True:
            dlg = wx.MessageDialog(None, u'打包后，是否删除提取的文件夹', u'请选择', wx.YES_NO | wx.ICON_INFORMATION)
            if dlg.ShowModal() == wx.ID_YES:
                isdel = True
            dlg.Destroy()

        if ispack == True:
            if os.path.exists(zippath):
                dialog = wx.ProgressDialog("状态", f"正在打包压缩{newpath}.7z", 1)  # , style=wx.PD_CAN_ABORT)
                try:
                    p=Popen([zippath, 'a', newpath + ".7z", newpath])
                    p.communicate()
                except:
                    print("打包失败")
                else:
                    print("打包成功")

            else:
                try:
                    dialog = wx.ProgressDialog("状态", f"正在打包压缩{newpath}.zip", 1)  # , style=wx.PD_CAN_ABORT)
                    shutil.make_archive(newpath, format="zip", root_dir=parentpath+"\\", base_dir=newfolder)
                except:
                    print("打包失败")
                else:
                    print("打包成功")


            if isdel == True and  os.path.exists(newpath):
                keepGoing = dialog.Update(1, newmsg=f"正在删除文件夹{newpath}")

                try:
                    if keepGoing == False:
                        sys.exit()
                    shutil.rmtree(newpath)
                except:
                    print("文件夹删除失败")
                else:
                    print("已经成功删除文件夹")
            dialog.Destroy()

    if stdnote != "":
        print(stdnote)
        wx.MessageBox(stdnote, u'错误', wx.OK | wx.ICON_ERROR)
    return stdnote, lostlist


# 注册表
def addreg(path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\")
        winreg.SetValue(key, "ExtractPart", winreg.REG_SZ, "NX装配树提取打包")
        newKey = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\ExtractPart")
        value = path + " -p \"%1\""
        winreg.SetValue(newKey, "command", winreg.REG_SZ, value)
    except:
        wx.MessageBox(u'右键菜单添加失败', u'提示', wx.OK | wx.ICON_ERROR)
    else:
        wx.MessageBox(u'成功添加右键菜单', u'提示', wx.OK | wx.ICON_INFORMATION)


def delreg():
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\ExtractPart")
        winreg.DeleteKey(key, "command")
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\\shell")
        winreg.DeleteKey(key, "ExtractPart")
    except:
        wx.MessageBox(u'右键菜单不存在', u'提示', wx.OK | wx.ICON_ERROR)
    else:
        wx.MessageBox(u'成功删除右键菜单', u'提示', wx.OK | wx.ICON_INFORMATION)


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"NX装配树提取 by dxl", pos=wx.DefaultPosition, size=wx.Size(680, 408),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.ugpcpath, self.ugpath, self.ispack, self.isdel, self.isfolder, self.sufnum,self.zippath= readconf()
        self.SetSizeHints(wx.Size(680, 400), wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"选择Part文件：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        gbSizer1.Add(self.m_staticText1, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"选择Part文件", u"*.prt",
                                               wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE | wx.FLP_SMALL)
        self.m_filePicker1.SetMinSize(wx.Size(300, -1))
        gbSizer1.Add(self.m_filePicker1, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer1, 1, wx.EXPAND, 5)

        gbSizer2 = wx.GridBagSizer(0, 0)
        gbSizer2.SetFlexibleDirection(wx.BOTH)
        gbSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"提到到：        ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)

        gbSizer2.Add(self.m_staticText2, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_dirPicker1 = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"选择提取目录", wx.DefaultPosition,
                                             wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        self.m_dirPicker1.SetMinSize(wx.Size(300, -1))
        gbSizer2.Add(self.m_dirPicker1, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer2, 1, wx.EXPAND, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"开始提取", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button1, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer1.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"默认设置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        bSizer1.Add(self.m_staticText3, 0, wx.ALL, 5)

        gbSizer3 = wx.GridBagSizer(0, 0)
        gbSizer3.SetFlexibleDirection(wx.BOTH)
        gbSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"NX安装目录： ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        gbSizer3.Add(self.m_staticText4, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_dirPicker2 = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"选择NX安装目录", wx.DefaultPosition,
                                             wx.DefaultSize, wx.DIRP_DEFAULT_STYLE| wx.FLP_SMALL)
        self.m_dirPicker2.SetMinSize(wx.Size(300, -1))
        gbSizer3.Add(self.m_dirPicker2, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer3, 1, wx.EXPAND, 5)

        gbSizer4 = wx.GridBagSizer(0, 0)
        gbSizer4.SetFlexibleDirection(wx.BOTH)
        gbSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"提取目录后缀格式", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)

        gbSizer4.Add(self.m_staticText5, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_choice1Choices = [u"-年月日，-200101", u"-年月日，-20200101", u"-年月日时分秒，200101083000", u"-年月日时分秒，20200101083000"]
        self.m_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(1)
        gbSizer4.Add(self.m_choice1, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"（未指定提取目录，程序自动提取到上级目录时有效）", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText6.Wrap(-1)

        gbSizer4.Add(self.m_staticText6, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(gbSizer4, 1, wx.EXPAND, 5)

        gbSizer5 = wx.GridBagSizer(0, 0)
        gbSizer5.SetFlexibleDirection(wx.BOTH)
        gbSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_checkBox1 = wx.CheckBox(self, wx.ID_ANY, u"默认打包（不提示选择）", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer5.Add(self.m_checkBox1, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_checkBox2 = wx.CheckBox(self, wx.ID_ANY, u"默认打包后删除提取文件夹（不提示选择）", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer5.Add(self.m_checkBox2, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_checkBox3 = wx.CheckBox(self, wx.ID_ANY, u"指定提取目录（否则提取到上级目录）", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer5.Add(self.m_checkBox3, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer5, 1, wx.EXPAND, 5)

        gbSizer6 = wx.GridBagSizer(0, 0)
        gbSizer6.SetFlexibleDirection(wx.BOTH)
        gbSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"保存设置", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer6.Add(self.m_button2, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"注册到右键菜单", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer6.Add(self.m_button3, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"删除右键菜单", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer6.Add(self.m_button4, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer6, 1, wx.EXPAND, 5)

        # self.m_gauge1 = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        # self.m_gauge1.SetValue(0)
        # bSizer1.Add(self.m_gauge1, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # 读取配置文件
        self.m_dirPicker2.SetPath(self.ugpath)
        self.m_choice1.SetSelection(self.sufnum)
        self.m_checkBox1.SetValue(self.ispack)
        self.m_checkBox2.SetValue(self.isdel)
        self.m_checkBox3.SetValue(self.isfolder)

        # Connect Events
        self.m_filePicker1.Bind(wx.EVT_FILEPICKER_CHANGED, self.m_filePicker1OnFileChanged)
        self.m_dirPicker1.Bind(wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker1OnDirChanged)
        self.m_button1.Bind(wx.EVT_BUTTON, self.m_button1OnButtonClick)
        self.m_dirPicker2.Bind(wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker2OnDirChanged)
        self.m_choice1.Bind(wx.EVT_CHOICE, self.m_choice1OnChoice)
        self.m_checkBox1.Bind(wx.EVT_CHECKBOX, self.m_checkBox1OnCheckBox)
        self.m_checkBox2.Bind(wx.EVT_CHECKBOX, self.m_checkBox2OnCheckBox)
        self.m_checkBox3.Bind(wx.EVT_CHECKBOX, self.m_checkBox3OnCheckBox)
        self.m_button2.Bind(wx.EVT_BUTTON, self.m_button2OnButtonClick)
        self.m_button3.Bind(wx.EVT_BUTTON, self.m_button3OnButtonClick)
        self.m_button4.Bind(wx.EVT_BUTTON, self.m_button4OnButtonClick)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    # 选择Part文件
    def m_filePicker1OnFileChanged(self, event):
        print(self.m_filePicker1.GetPath())
        event.Skip()

    # 提取目录
    def m_dirPicker1OnDirChanged(self, event):
        event.Skip()

    # 开始提取
    def m_button1OnButtonClick(self, event):
        part = self.m_filePicker1.GetPath()
        folder = self.m_dirPicker1.GetPath()
        if part == '':
            wx.MessageBox(u'操作不正确，请重新选择', u'提示', wx.OK | wx.ICON_ERROR)
        else:
            getparts(part, folder)

    # NX安装目录
    def m_dirPicker2OnDirChanged(self, event):
        self.ugpath = self.m_dirPicker2.GetPath()

    # 文件夹后缀
    def m_choice1OnChoice(self, event):
        self.sufnum = self.m_choice1.GetSelection()

    # 默认打包
    def m_checkBox1OnCheckBox(self, event):
        self.ispack = self.m_checkBox1.GetValue()

    # 默认删除
    def m_checkBox2OnCheckBox(self, event):
        self.isdel = self.m_checkBox2.GetValue()

    # 指定提取目录
    def m_checkBox3OnCheckBox(self, event):
        self.isfolder = self.m_checkBox3.GetValue()

    # 保存设置
    def m_button2OnButtonClick(self, event):
        saveconf(self.ugpath, self.ispack, self.isdel, self.isfolder, self.sufnum)

    # 注册右键菜单
    def m_button3OnButtonClick(self, event):
        addreg(sys.argv[0])

    # 删除右键菜单
    def m_button4OnButtonClick(self, event):
        delreg()


if __name__ == '__main__':
    app = wx.App(False)

    # 命令行参数
    parser = argparse.ArgumentParser()
    parser.description = "UG装配结构树文件提取"
    parser.add_argument("-p", "--Part", help="输入UG总装配PART文件，提取结构树文件到新目录，并打包压缩", type=str)
    args = parser.parse_args()
    if args.Part:
        getparts(args.Part)

    else:
        frame = MyFrame1(None)
        frame.Show()
        app.MainLoop()
