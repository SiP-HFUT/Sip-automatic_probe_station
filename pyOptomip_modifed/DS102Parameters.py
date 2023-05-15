# -*- coding: utf-8 -*-
import wx

import CorvusEco
import CorvusEcoFrame#这俩个import是否需要添加/更改对应的
# import visa
import pyvisa as visa

class DS102Parameters(wx.Panel):
    name = 'Stage: DS102'
    def __init__(self, parent, connectPanel, **kwargs):
        super(DS102Parameters, self).__init__(parent)
        self.connectPanel = connectPanel
        self.InitUI()
        
        
    def InitUI(self):
        sb = wx.StaticBox(self, label='DS102 Connection Parameters');
        vbox = wx.StaticBoxSizer(sb, wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        #First Parameter: Serial Port
        self.para1 = wx.BoxSizer(wx.HORIZONTAL)
        self.para1name = wx.StaticText(self,label='Serial Port')
        self.para1tc = wx.ComboBox(self, choices=visa.ResourceManager().list_resources())
        #self.para1tc = wx.TextCtrl(self,value='ASRL5::INSTR')
        self.para1.AddMany([(self.para1name,1,wx.EXPAND|wx.ALIGN_LEFT),(self.para1tc,1,wx.EXPAND|wx.ALIGN_RIGHT)])
        
        #Second Parameter: Number of Axis
        self.para2 = wx.BoxSizer(wx.HORIZONTAL)
        self.para2name = wx.StaticText(self,label='Number of Axis')
        self.para2tc = wx.TextCtrl(self,value='2')
        self.para2.AddMany([(self.para2name,1,wx.EXPAND|wx.ALIGN_LEFT),(self.para2tc,1,wx.EXPAND|wx.ALIGN_RIGHT)])
        
        self.disconnectBtn = wx.Button(self, label='Disconnect')
        self.disconnectBtn.Bind( wx.EVT_BUTTON, self.disconnect)
        self.disconnectBtn.Disable()
        
        self.connectBtn = wx.Button(self, label='Connect')
        self.connectBtn.Bind( wx.EVT_BUTTON, self.connect)
        
        hbox.AddMany([(self.disconnectBtn, 0, wx.ALIGN_RIGHT), (self.connectBtn, 0, wx.ALIGN_RIGHT)])
        vbox.AddMany([(self.para1,0,wx.EXPAND),(self.para2,0,wx.EXPAND), (hbox,0,wx.ALIGN_BOTTOM)])
        
        
        
        self.SetSizer(vbox)
        
        
    def connect(self, event):
        self.stage = CorvusEco.CorvusEcoClass()#这里用的CorvusEco.CorvusEcoClass
        self.stage.connect(str(self.para1tc.GetValue()),visa.ResourceManager(),5,500,int(self.para2tc.GetValue()))
        self.stage.panelClass = CorvusEcoFrame.topCorvusPanel
        self.connectPanel.instList.append(self.stage)  
        self.disconnectBtn.Enable()
        self.connectBtn.Disable()   

    def disconnect(self, event):
        self.stage.disconnect()
        if self.stage in self.connectPanel.instList:
            self.connectPanel.instList.remove(self.stage)
        self.disconnectBtn.Disable()
        self.connectBtn.Enable()        
