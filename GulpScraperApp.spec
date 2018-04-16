# -*- mode: python -*-

block_cipher = None

addedFiles = [('phantomjs.exe','.'),
              ('client_secret.json','.'),
              ('iconGulpPng.png','.')]

a = Analysis(['C:\\Users\\Anthony\\scripts\\Contacts-Scraper\\GulpScraperApp.py'],
             pathex=['C:\\Users\\Anthony\\scripts\\Contacts-Scraper'],
             binaries=[],
             datas=addedFiles,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='GulpScraperApp',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='C:\\Users\\Anthony\\scripts\\Contacts-Scraper\\icongulppng_Qlo_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='GulpScraperApp')
