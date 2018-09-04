import random
import hashlib

words = """
kyacks	19	19
wampum	15	19
jogger	15	19
jading	15	19
coxing	16	19
piquet	17	19
ghazis	19	19
jebels	15	19
plazas	17	19
colzas	17	19
pozole	17	19
fuzees	18	19
zocalo	17	19
xebecs	17	19
chabuk	17	19
jaygee	17	19
cojoin	15	19
boxing	16	19
except	17	19
shmuck	17	19
zirams	17	18
zamias	17	18
peroxy	18	18
hiccup	15	18
brazes	17	18
brazer	17	18
sheqel	18	18
matzas	17	18
sleazy	18	18
chuffs	17	18
flippy	16	18
baizas	17	18
chumps	15	18
squish	18	18
whelky	19	18
jargon	14	18
kecked	17	18
yutzes	18	18
chalky	18	18
chuppa	15	18
hexyls	19	18
dibbuk	15	18
prezes	17	18
djinns	14	18
matzos	17	18
pricky	17	18
jihads	17	18
keckle	16	18
lockup	14	18
kicked	17	18
exuvia	16	18
hexing	17	18
jugate	14	18
matzot	17	18
kibbeh	17	18
chocks	17	18
pompom	14	18
donjon	14	18
judder	15	18
chinky	18	18
zebras	17	18
scummy	15	18
zibets	17	18
mazier	17	18
pimply	15	18
squill	15	18
cupful	13	18
unjust	13	18
chicks	17	18
mazers	17	18
feijoa	16	18
prizer	17	18
zenith	18	18
muchly	16	18
cyclic	15	18
djinni	14	18
hazans	18	18
kimchi	17	18
hazard	19	18
bazars	17	18
bowwow	17	18
prizes	17	18
bazoos	17	18
jadish	17	18
feezes	18	18
jibers	15	18
taters	6	6
sitter	6	6
tastes	6	6
triter	6	6
tartar	6	6
sistra	6	6
sitars	6	6
triose	6	6
tarots	6	6
tarres	6	6
soiree	6	6
resort	6	6
triste	6	6
tarsia	6	6
resist	6	6
resite	6	6
resits	6	6
rarest	6	6
retort	6	6
rooses	6	6
rooser	6	6
riatas	6	6
roarer	6	6
setter	6	6
settee	6	6
roasts	6	6
terete	6	6
terras	6	6
terrae	6	6
isseis	6	6
ritter	6	6
setose	6	6
sestet	6	6
rioter	6	6
irises	6	6
iritis	6	6
ristra	6	6
terais	6	6
risers	6	6
terret	6	6
territ	6	6
tsores	6	6
tetter	6	6
tsetse	6	6
teases	6	6
tetris	6	6
tetras	6	6
testae	6	6
terser	6	6
terror	6	6
testee	6	6
tester	6	6
testis	6	6
teeter	6	6
"""

words = words.strip().split("\n")
words = [word.split()[0] for word in words]

passwords = []

# Length 4 words
random.shuffle(words)
for word in words[:20]:
    passwords.append(word[:4])

# Length 5 words
for word in words[20:40]:
    passwords.append(word[:5])

for word in words[40:60]:
    passwords.append(word[:4] + str(random.randint(0, 9)))

# Length 6 words
for word in words[60:80]:
    passwords.append(word[:6])

for word in words[80:100]:
    passwords.append(word[:5] + str(random.randint(0, 9)))

for word in words[100:120]:
    passwords.append(word[:4] + str(random.randint(10, 99)))

sha1_hashes = open("static/hashes/sha1_hashes.txt", "wt")
md5_hashes = open("static/hashes/md5_hashes.txt", "wt")
plain_passwords = open("static/hashes/plain_passwords.txt", "wt")

sha1 = hashlib.sha1
md5 = hashlib.md5

for psw in passwords:
    sha1_hashes.write(sha1(bytes(psw, 'utf-8')).hexdigest() + "\n")
    md5_hashes.write(md5(bytes(psw, 'utf-8')).hexdigest() + "\n")
    plain_passwords.write(psw + "\n")

sha1_hashes.close()
md5_hashes.close()
plain_passwords.close()
