import re

# TODO: Define an interface for specifing what is the shape of PVS filenames

# EXAMPLE FROM DROPBOX
dropboxExample = 'AutumnMountains_A-phon-1mp_123.jpg'

splitted = re.split('_', dropboxExample)
src = splitted[0]
hrc = splitted[1]
pvs = re.findall(r'[0-9]+', splitted[2])[0]
print('-' * 40)
print('DROPBOX EXAMPLE AFTER ANALISIS: \n')
print('SRC: ' + src)
print('HRC: ' + hrc)
print('PVS: ' + pvs)
print('\n' + '-' * 40)

# CCRIQ2 EXAMPLE
CCRIQ = 'BouquetPastel_C_compct_5mp.jpg'

splitted = re.split('_', CCRIQ, 1)
src = splitted[0]
hrc = re.findall(r'[A-Za-z0-9_]*', splitted[1])[0]
pvs = CCRIQ
print('CCRIQ AFTER ANALISIS: \n')
print('SRC: ' + src)
print('HRC: ' + hrc)
print('PVS: ' + pvs)
print('\n' + '-' * 40)

# VIME1 EXAMPLE
vime = 'vime1_alley_camB-ver1.jpg'

splitted = re.split('_', vime)
src = splitted[1]
anotherSplit = re.split('\.', splitted[2])
hrc = anotherSplit[0]
pvs = vime
print('VIME1 EXAMPLE AFTER ANALISIS: \n')
print('SRC: ' + src)
print('HRC: ' + hrc)
print('PVS: ' + pvs)
