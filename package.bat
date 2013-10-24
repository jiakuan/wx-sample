rmdir /s /q build
rmdir /s /q dist
del *.spec

pyinstaller test_windows.py --onefile --windowed
