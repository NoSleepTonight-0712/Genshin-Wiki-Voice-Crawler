import os

def getDestByFileName(fn, base_dir='voice'):
    if 'Character_Voice' in fn:
        character_name = fn.split('_')[2]

        return os.path.join(base_dir, 'character_voice', character_name), os.path.join(base_dir, 'character_voice', character_name, fn)

    quest_name = fn.split('__')[0]
    return os.path.join(base_dir, quest_name), os.path.join(base_dir, quest_name, fn)