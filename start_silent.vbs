Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\ian_l\OneDrive\Desktop\polymarket-bot"
WshShell.Run "python server.py", 0, False
WScript.Sleep 3000
WshShell.Run "python auto_trader.py", 0, False
