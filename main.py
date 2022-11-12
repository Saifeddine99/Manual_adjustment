import streamlit as st

import wx

app = wx.App()

st.title('Folder Picker using wxPython')

clicked = st.button('Click to select the folder', key="FolderSelectionButton")

if clicked:
    dlg_obj = wx.DirDialog(None, "Choose input directory", "",
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

    if dlg_obj.ShowModal() == wx.ID_OK:
        folder_path = dlg_obj.GetPath()

    st.header('Selected Folder')
    st.write(folder_path)
