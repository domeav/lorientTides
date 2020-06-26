#!/usr/bin/env python3

from datetime import datetime
import subprocess
import json
from io import StringIO
import Adafruit_CharLCD as LCD

day = str(datetime.now().date())

command = f'''curl "https://services.data.shom.fr/b2q8lrcdl4s04cbabsj4nhcb/hdm/spm/hlt?harborName=LORIENT&duration=1&date={day}&utc=standard&correlation=1" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' -H 'Accept: */*' -H 'Accept-L\
anguage: en-US,en;q=0.7,fr;q=0.3' --compressed -H 'Origin: https://maree.shom.fr' -H 'Connection: keep-alive' -H "Referer: https://maree.shom.fr/harbor/LORIENT/wl/0?date={day}&utc=standard"'''

output = subprocess.run(command, shell=True, check=True, capture_output=True)

data = json.loads(output.stdout)

highTimes = StringIO()
lowTimes = StringIO()
coef = None
diff = None

for tide in data[day]:
	if tide[0] == 'tide.high':
		if not coef:
			coef = int(tide[3])
		else:
			diff = int(tide[3]) - coef
			if diff >= 0:
				diff = f'+{diff}'
		highTimes.write(f' {tide[1]}')
	else:
		lowTimes.write(f' {tide[1]}')


lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_color(0, 0, 0)
lcd.clear()

tides = f'{coef} {highTimes.getvalue()}\n{diff} {lowTimes.getvalue()}'
print(tides)

lcd.message(tides)
