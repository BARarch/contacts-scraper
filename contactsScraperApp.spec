# -*- mode: python -*-

block_cipher = None

addedFiles = [('phantomjs.exe','.'),
              ('client_secret.json','.')]

a = Analysis(['C:\\Users\\Anthony\\scripts\\Contacts-Scraper\\contactsScraperApp.py'],
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
          name='contactsScraperApp',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='contactsScraperApp')
