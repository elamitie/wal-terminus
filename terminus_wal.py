import yaml
import json
import shutil
import os

colors_path = r'C:\Users\elami\.cache\wal\colors.yml'
terminus_path = r'C:\Users\elami\AppData\Roaming\terminus\config.yaml'

terminus_config = ""
wal_colors = ""

# Step 1, we need to open the color file normally and replace all instances of '\' to either '\\' or '/' 
# on the first line.
colors = open(colors_path, 'r')
i = 0
lines = []
for x in colors:
    if i == 0:
        line = x
        sp = line.split()
        newpath = sp[1].replace(os.sep, '/')
        line = sp[0] + " " + newpath + "\n"
        lines.append(line)
        i += 1
    else:
        lines.append(x)

colors.close()

colors = open(colors_path, 'w')
colors.writelines(lines)
colors.close()

with open(terminus_path) as file:
    terminus_config = yaml.load(file, Loader=yaml.FullLoader)

colors_hash = {}

with open(colors_path) as file:
    wal_colors = yaml.load(file, Loader=yaml.FullLoader)

for k, v in wal_colors['special'].items():
    colors_hash[k] = v

for k, v in wal_colors['colors'].items():
    colors_hash[k] = v

colorscheme = terminus_config['terminal']['colorScheme']
colorscheme['foreground'] = colors_hash['foreground']
colorscheme['background'] = colors_hash['background']
colorscheme['cursor']     = colors_hash['cursor']

for i in range(16):
    colorscheme['colors'][i] = colors_hash["color{}".format(i)]

terminus_config['terminal']['colorScheme'] = colorscheme


with open(terminus_path, 'w') as file:
    terminus_config = yaml.dump(terminus_config, file, sort_keys=False)
