import json

level_list = [[80, 400, 'map3.tmx', 'castle_level.png', True],
              [80, 400, 'map3.tmx', 'castle_level_pes.png', False],
              [80, 400, 'map3.tmx', 'castel_level_more.png', False]]

# writing to json
with open('list_levels_j.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(level_list))
