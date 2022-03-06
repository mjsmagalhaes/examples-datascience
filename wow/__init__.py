ENCOUNTER_DATA = {}

CLASS_DATA = {
    'Death Knight': '#C41E3A',
    'Demon Hunter': '#A330C9',
    'Druid': '#FF7C0A',
    'Hunter': '#AAD372',
    'Mage': '#3FC7EB',
    'Monk': '#00FF98',
    'Paladin': '#F48CBA',
    'Priest': '#FFFFFF',
    'Rogue': '#FFF468',
    'Shaman': '#0070DD',
    'Warlock': '#8788EE',
    'Warrior': '#C69B6D'
}

SPECIALIZATION_DATA = {
    250: ('Death Knight', 'Blood', 'Tank'),
    251: ('Death Knight', 'Frost', 'DPS'),
    252: ('Death Knight', 'Unholy', 'DPS'),

    577: ('Demon Hunter', 'Havoc', 'DPS'),
    581: ('Demon Hunter', 'Vengeance', 'Tank'),

    102: ('Druid', 'Balance', 'DPS'),
    103: ('Druid', 'Feral', 'DPS'),
    104: ('Druid', 'Guardian', 'Tank'),
    105: ('Druid', 'Restoration', 'Healer'),

    253: ('Hunter', 'Beast Mastery', 'DPS'),
    254: ('Hunter', 'Marksmanship', 'DPS'),
    255: ('Hunter', 'Survival', 'DPS'),

    62: ('Mage', 'Arcane', 'DPS'),
    63: ('Mage', 'Fire', 'DPS'),
    64: ('Mage', 'Frost', 'DPS'),

    268: ('Monk', 'Brewmaster', 'Tank'),
    269: ('Monk', 'Windwalker', 'DPS'),
    270: ('Monk', 'Mistweaver', 'Healer'),

    65: ('Paladin', 'Holy', 'Healer'),
    66: ('Paladin', 'Protection', 'Tank'),
    70: ('Paladin', 'Retribution', 'DPS'),

    256: ('Priest', 'Discipline', 'Healer'),
    257: ('Priest', 'Holy', 'Healer'),
    258: ('Priest', 'Shadow', 'DPS'),

    259: ('Rogue', 'Assassination', 'DPS'),
    260: ('Rogue', 'Outlaw', 'DPS'),
    261: ('Rogue', 'Subtlety', 'DPS'),

    262: ('Shaman', 'Elemental', 'DPS'),
    263: ('Shaman', 'Enhancement', 'DPS'),
    264: ('Shaman', 'Restoration', 'Healer'),

    265: ('Warlock', 'Affliction', 'DPS'),
    266: ('Warlock', 'Demonology', 'DPS'),
    267: ('Warlock', 'Destruction', 'DPS'),

    71: ('Warrior', 'Arms', 'DPS'),
    72: ('Warrior', 'Fury', 'DPS'),
    73: ('Warrior', 'Protection', 'Tank'),
}

# https://wowpedia.fandom.com/wiki/DifficultyID

cDifficulty = {
    '7': 'LFR',
    '14': 'Normal',
    '15': 'Heroic',
    '16': 'Mythic'
}
