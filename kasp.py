import json
import hashlib


def comp(key):
	return key['l']

if __name__ == "__main__":
	msg = r'[{"l":20,"s":"r, nashi sociologi o"},{"l":33,"s":"t krasnuyu planetu..............."},{"l":5,"s":"osado"},{"l":16,"s":" podhodyashchih,"},{"l":27,"s":"a-ehlektrika, 5 specialisto"},{"l":15,"s":"vybrat 40 samyh"},{"l":25,"s":"ii specialisty: 1 rukovod"},{"l":14,"s":"a. Vam nuzhno "},{"l":3,"s":"try"},{"l":18,"s":"zaselenie Marsa. C"},{"l":28,"s":"v po kompyuternym sistemam, "},{"l":10,"s":"din - vse "},{"l":21,"s":"predelili tri kriteri"},{"l":30,"s":"uchyonyh.\n\nZnaya ehtu informac"},{"l":26,"s":"itel, 3 povara, 4 inzhener"},{"l":2,"s":"z "},{"l":13,"s":"e pomestyatsy"},{"l":1,"s":"I"},{"l":4,"s":"oh p"},{"l":8,"s":" isprave"},{"l":9,"s":"n tolko o"},{"l":31,"s":"iyu, vyberete 40 uchastnikov, k"},{"l":22,"s":"ya.\n\nNa bort modulya d"},{"l":12,"s":"tov v nego n"},{"l":11,"s":"120 kolonis"},{"l":32,"s":"otorye otpravyatsya kolonizirova"},{"l":6,"s":"chnyh "},{"l":17,"s":" kotorye nachnut "},{"l":29,"s":"5 vrachej, 8 mekhanikov i 14 "},{"l":24,"s":"odimye dlya zhizni kolon"},{"l":7,"s":"modulej"},{"l":23,"s":"olzhny popast vse neobh"},{"l":19,"s":"Htoby uprostit otbo"}]'

	data = json.loads(msg)

	res = ''
	for i in sorted(data, key=comp):
		print(i['s'], end='')
		res += i['s']

	m = hashlib.md5()
	m.update(res.encode('utf-8'))
	print(m.hexdigest())
		# msg_part = i['s']
		# print(i['l'])
		# print(len(msg_part), end='\n\n')