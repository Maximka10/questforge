from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QROOT = ROOT / 'config' / 'ftbquests' / 'quests'
CHAPTERS = [
    ('welcome','Добро пожаловать','QuestForge: введение','minecraft:book',[
        ('Вход в QuestForge','Открой Quest Book и ознакомься с правилами сборки.','minecraft:book'),
        ('Первые ресурсы','Собери базовый набор для старта.','minecraft:oak_log'),
        ('Первое убежище','Подготовь место для постоянной базы.','minecraft:crafting_table'),
        ('Готов к пути','Сделай базовый инструмент и начни исследование.','minecraft:stone_pickaxe')]),
    ('exploration','Исследование','Мир, биомы и редкие места','minecraft:compass',[
        ('Компас','Создай компас для навигации.','minecraft:compass'),
        ('Карта','Создай карту и начни отмечать интересные места.','minecraft:map'),
        ('Глубокие пещеры','Добудь редкий ресурс из подземелья.','minecraft:diamond'),
        ('Редкие места','Найди одну из необычных структур мира.','minecraft:ender_eye')]),
    ('building','Строительство','База, декор и большие проекты','minecraft:bricks',[
        ('План базы','Подготовь площадку под основную базу.','minecraft:bricks'),
        ('Декор','Используй декоративные блоки для оформления базы.','chipped:oak_planks'),
        ('Инженерная мастерская','Создай отдельную зону для машин и автоматизации.','create:andesite_casing'),
        ('Большой проект','Начни крупную постройку, которая станет центром мира.','minecraft:beacon')]),
    ('storage','Хранение','От сундуков к организованному складу','minecraft:chest',[
        ('Организация','Собери базовую систему хранения.','minecraft:chest'),
        ('Рюкзак','Сделай Sophisticated Backpack.','sophisticatedbackpacks:backpack'),
        ('Ящики','Перейди к специализированному хранению ресурсов.','functionalstorage:oak_1_1'),
        ('Автоматизация склада','Свяжи производство с системой хранения.','storagedrawers:controller')]),
    ('technology','Технологии','Create и Mekanism','create:mechanical_press',[
        ('Сила Create','Собери механический пресс Create.','create:mechanical_press'),
        ('Базовая автоматизация','Автоматизируй одну производственную цепочку Create.','create:mechanical_crafter'),
        ('Металлургия','Создай Metallurgic Infuser Mekanism.','mekanism:metallurgic_infuser'),
        ('Энергия','Создай энергетический блок и подключи первую линию.','mekanism:basic_energy_cube')]),
    ('magic','Магия','Ars Nouveau и Iron\'s Spells','ars_nouveau:novice_spell_book',[
        ('Путь мага','Создай Novice Spell Book.','ars_nouveau:novice_spell_book'),
        ('Первое заклинание','Освой базовое заклинание Ars Nouveau.','ars_nouveau:novice_spell_book'),
        ('Боевые чары','Создай предмет из Iron\'s Spells.','irons_spellbooks:iron_spell_book'),
        ('Магическая база','Организуй отдельное место для магических исследований.','ars_nouveau:arcane_core')]),
    ('combat','Боевые испытания','Опасные территории, боссы и экипировка','minecraft:diamond_sword',[
        ('Подготовка','Собери полноценную алмазную экипировку.','minecraft:diamond_chestplate'),
        ('Опасная экспедиция','Подготовься к исследованию редких подземелий.','minecraft:golden_apple'),
        ('Редкая добыча','Добудь артефакт из опасной зоны.','artifacts:antidote_vessel'),
        ('Босс','Победи сильного противника и вернись с трофеем.','minecraft:nether_star')]),
    ('colonies','Колония','NPC, рабочие и автоматизация поселения','minecolonies:supplycamp',[
        ('Первый колонист','Размести стартовую колонию MineColonies.','minecolonies:supplycamp'),
        ('Рабочие','Создай первые рабочие места и обеспечь колонию ресурсами.','minecolonies:builder'),
        ('Развитие','Подними уровень ключевого здания колонии.','minecolonies:townhall'),
        ('Автономная база','Настрой цепочки снабжения между своей базой и колонией.','minecolonies:warehouse')]),
    ('advanced','Продвинутая автоматизация','Производство, логистика и большие цепочки','mekanism:elite_control_circuit',[
        ('Продвинутая энергия','Перейди на продвинутую энергетическую инфраструктуру.','mekanism:elite_energy_cube'),
        ('Автоматическая переработка','Построй полноценную линию переработки руд.','mekanism:purification_chamber'),
        ('Логистика','Автоматизируй перемещение материалов между машинами.','create:brass_funnel'),
        ('Производственный комплекс','Собери крупную автоматизированную производственную линию.','create:mechanical_crafter')]),
    ('endgame','Эндгейм','Редкие ресурсы, боссы и долгосрочные цели','minecraft:nether_star',[
        ('Эндгейм-ресурсы','Собери редкие материалы для финальных проектов.','minecraft:netherite_ingot'),
        ('Мастер автоматизации','Доведи одну производственную цепочку до почти полного автомата.','mekanism:ultimate_control_circuit'),
        ('Мегастроительство','Начни проект масштаба, который невозможно закончить за один игровой вечер.','minecraft:beacon'),
        ('Мир после финала','Создай долгосрочную цель: город, фабрика, колония или исследовательский комплекс.','minecraft:dragon_egg')])]

GROUP_ID = 'A1B2C3D4E5F60708'

def hid(value: int) -> str:
    return f'{value:016X}'

chapter_ids = {slug: hid(0x1000000000000000 + i + 1) for i,(slug,*_) in enumerate(CHAPTERS)}
quest_ids = {}
task_ids = {}
reward_ids = {}
n = 1
for slug,*_ in CHAPTERS:
    for qi in range(4):
        quest_ids[(slug,qi)] = hid(0x2000000000000000 + n); n += 1
        task_ids[(slug,qi)] = hid(0x3000000000000000 + n); n += 1
        reward_ids[(slug,qi)] = hid(0x4000000000000000 + n); n += 1

QROOT.mkdir(parents=True, exist_ok=True)
(QROOT / 'lang').mkdir(parents=True, exist_ok=True)
(QROOT / 'chapters').mkdir(parents=True, exist_ok=True)

(QROOT / 'data.snbt').write_text('''{\n\tdefault_autoclaim_rewards: "disabled"\n\tdefault_consume_items: false\n\tdefault_quest_disable_jei: false\n\tdefault_quest_shape: "circle"\n\tdefault_reward_team: false\n\tdetection_delay: 10\n\tdisable_gui: false\n\tdrop_book_on_death: false\n\tdrop_loot_crates: false\n\temergency_items: []\n\temergency_items_cooldown: 300\n\tfallback_locale: "en_us"\n\tgrid_scale: 0.5d\n\thide_excluded_quests: false\n\ticon: { id: "minecraft:book" }\n\tlock_message: ""\n\tloot_crate_no_drop: { boss: 0, monster: 0, passive: 0 }\n\tpause_game: false\n\tprogression_mode: "flexible"\n\tshow_lock_icons: true\n\tverify_on_load: false\n\tversion: 13\n}\n''', encoding='utf-8')
(QROOT / 'chapter_groups.snbt').write_text(f'{{\n\tchapter_groups: [{{ id: "{GROUP_ID}" }}]\n}}\n', encoding='utf-8')

for ci,(slug,title,desc,icon,quests) in enumerate(CHAPTERS):
    lines = ['{', '\tdefault_hide_dependency_lines: false', '\tdefault_min_width: 250', '\tdefault_quest_shape: ""', f'\tfilename: "{slug}"', f'\tgroup: "{GROUP_ID}"', f'\ticon: {{ id: "{icon}" }}', f'\tid: "{chapter_ids[slug]}"', '\timages: []', f'\torder_index: {ci}', '\tquest_links: []', '\tquests: [']
    for qi,(_,_,item) in enumerate(quests):
        qid,tid,rid = quest_ids[(slug,qi)], task_ids[(slug,qi)], reward_ids[(slug,qi)]
        deps = []
        if qi: deps.append(quest_ids[(slug,qi-1)])
        elif ci: deps.append(quest_ids[(CHAPTERS[ci-1][0],3)])
        lines += ['\t\t{', f'\t\t\tid: "{qid}"', f'\t\t\ticon: {{ id: "{item}" }}']
        if deps: lines.append('\t\t\tdependencies: [' + ' '.join(f'"{x}"' for x in deps) + ']')
        lines += ['\t\t\trewards: [', '\t\t\t\t{', f'\t\t\t\t\tid: "{rid}"', '\t\t\t\t\ttype: "xp"', f'\t\t\t\t\txp: {10 + ci*5}', '\t\t\t\t}', '\t\t\t]', '\t\t\tshape: "square"', '\t\t\tsize: 1.0d', '\t\t\ttasks: [', '\t\t\t\t{', f'\t\t\t\t\tid: "{tid}"', f'\t\t\t\t\titem: {{ count: 1, id: "{item}" }}', '\t\t\t\t\ttype: "item"', '\t\t\t\t}', '\t\t\t]', f'\t\t\tx: {qi*4.0}d', '\t\t\ty: 0.0d', '\t\t}']
    lines += ['\t]', '}']
    (QROOT / 'chapters' / f'{slug}.snbt').write_text('\n'.join(lines)+'\n', encoding='utf-8')

for locale in ('en_us','ru_ru'):
    out = ['{']
    for slug,title,desc,icon,quests in CHAPTERS:
        cid = chapter_ids[slug]
        out += [f'\tchapter.{cid}.title: "{title}"', f'\tchapter.{cid}.description: ["{desc}"]']
        for qi,(qt,qdesc,_) in enumerate(quests):
            qid = quest_ids[(slug,qi)]
            out += [f'\tquest.{qid}.title: "{qt}"', f'\tquest.{qid}.quest_desc: ["{qdesc}"]']
    out.append('}\n')
    (QROOT / 'lang' / f'{locale}.snbt').write_text('\n'.join(out), encoding='utf-8')

print(f'Generated {len(CHAPTERS)} chapters and {len(CHAPTERS)*4} quests in {QROOT}')
