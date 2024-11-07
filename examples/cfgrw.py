from cfgrw import CFGRW

cfgrw = CFGRW(conf_file='cfgrw.json')
values = cfgrw.read(['handlers', 'level', 'extras'])
print(values['handlers'], 'stream,file')
print(values['level'], 'info')
