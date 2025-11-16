a = Analysis(['main.py'], pathex=['.'], binaries=[], datas=[('skins/*','skins'),('media/*','media'),('kv/*','kv'),('config/*','config')], hiddenimports=[], hookspath=[])
pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(pyz, a.scripts, exclude_binaries=True, name='KingOfKingsJukebox', debug=False, bootloader_ignore_signals=False, strip=False, upx=False, console=False)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=False, name='KingOfKingsJukebox')
