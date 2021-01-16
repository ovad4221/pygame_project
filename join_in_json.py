import json

level_list = [[80, 400, 'map1.tmx', 'castle_level.png', 'замок земля.wav', True],
              [80, 400, 'map2.tmx', 'castle_level_pes.png', 'пустынный город.wav', True],
              [80, 400, 'map3.tmx', 'castel_level_more.png', 'крепость на море.wav', True]]

# writing to json
with open('list_levels_j.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(level_list))
