from cfgrw import CFGRW

cfgrw = CFGRW(conf_file="cfgrw.yaml")
values = cfgrw.read(["handlers", "level", "extras"])
print(values["handlers"], "stream,file")
print(values["level"], "info")

cfgrw = CFGRW(conf_file="cfgrw.json")
values = cfgrw.read(["handlers", "level", "extras"])
print(values["handlers"], "stream,file")
print(values["level"], "info")

cfgrw = CFGRW(conf_file="cfgrw.xml")
values = cfgrw.read(["handlers", "level", "extras"])
print(values["handlers"], "stream,file")
print(values["level"], "info")

cfgrw = CFGRW(conf_file="cfgrw.ini")
values = cfgrw.read(["handlers", "level", "extras"], {"section": "cfgrw"})
print(values["handlers"], "stream,file")
print(values["level"], "info")

cfgrw = CFGRW()
values = cfgrw.read(["handlers", "filemode", "level"], {"prefix": "CFGRW_"})
print(values["handlers"], "stream,file")
print(values["level"], "info")

cfgrw = CFGRW(conf_file="cfgrw.json.j2")
values = cfgrw.read(["handlers", "filemode", "level"], {"prefix": "CFGRW_"})
print(values["handlers"], "stream,file")
print(values["level"], "info")
