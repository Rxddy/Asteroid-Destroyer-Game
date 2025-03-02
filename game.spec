# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['spacewars.py'],
             pathex=['/spacewars.py'],
             binaries=[],
             datas=[('Images/*', 'Images'), ('Sounds/*', 'Sounds')],
             hiddenimports=['pygame'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='AsteroidDestroyer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='AsteroidDestroyer')

app = BUNDLE(coll,
             name='AsteroidDestroyer.app',
             icon=None,
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': 'True',
                'CFBundleShortVersionString': '1.0.0',
                'CFBundleVersion': '1.0.0'
             })