import wmi

c = wmi.WMI()
for p in c.Win32_Process(name="explorer.exe"):
    print(p.ProcessId, p.Name)
