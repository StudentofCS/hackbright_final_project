" Models for Wakfu character builder app"

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                   autoincrement = True,
                   primary_key = True)
    email = db.Column(db.String,
                      unique = True)
    password = db.Column(db.String)

    build = db.relationship('Build', back_populates='user')

    def __repr__(self):
        return f'<User id = {self.id}; email = {self.email}>'


class Build(db.Model):
    """A build"""

    __tablename__ = 'builds'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        default=0)
    equipment_set_id = db.Column(db.Integer,
                                 db.ForeignKey('equipment_sets.id'))
    characteristic_id = db.Column(db.Integer,
                                  db.ForeignKey('characteristics.id'))
    # base_stats_id = db.Column(db.Integer,
    #                          db.ForeignKy('base_stats.id'))
    character_class_id = db.Column(db.Integer,
                         db.ForeignKey('character_classes.id'))
    level = db.Column(db.Integer, default=20)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                           default=datetime.now(timezone.utc),
                           onupdate=datetime.now(timezone.utc))
    build_name = db.Column(db.String)
    public = db.Column(db.Boolean, default=True)
    main_role = db.Column(db.Integer)
    content_type = db.Column(db.Integer)

    user = db.relationship('User', 
                           back_populates='build')
    equipment_set = db.relationship('Equipment_set', 
                                    back_populates='build', 
                                    lazy='joined')
    characteristic = db.relationship('Characteristic', 
                                     back_populates='build', 
                                    lazy='joined')
    character_class = db.relationship('Character_class', 
                                      back_populates='build')
    # selected_mastery = db.relationship('Selected_mastery_element', 
    #                                    back_populates='build')
    # selected_resistance = db.relationship('Selected_resistance_element', 
    #                                       back_populates='build')
    selected_spell = db.relationship('Selected_spell', 
                                     back_populates='build')
    selected_passive = db.relationship('Selected_passive', 
                                       back_populates='build')
    selected_elements = db.relationship('Selected_element',
                                        back_populates='build',
                                        lazy='joined')


    def show(self):
        """Return a dict of non-empty attributes"""
        attributes = {}

        for key, value in self.__dict__.items():
            # Remove _sa_instance_state attr and values with None
            if value != None and not key.startswith('_'):
                attributes.update({key : value})

        return attributes


    def __repr__(self):
        return f"""
            <Build id = {self.id}; User id = {self.user_id};
            Class id = {self.character_class_id}; Level = {self.level}>
            """ 
    

class Characteristic(db.Model):
    """Selected characteristics"""

    __tablename__ = 'characteristics'

    test_dict = {'int' : 4}

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    intelligence = db.Column(db.Integer, default=0)
    hp_percentage = db.Column(db.Integer, default=0)
    elemental_res = db.Column(db.Integer, default=0)
    barrier = db.Column(db.Integer, default=0)
    heals_received = db.Column(db.Integer, default=0)
    armor = db.Column(db.Integer, default=0)
    strength = db.Column(db.Integer, default=0)
    elemental_mastery = db.Column(db.Integer, default=0)
    melee_mastery = db.Column(db.Integer, default=0)
    distance_mastery = db.Column(db.Integer, default=0)
    hp = db.Column(db.Integer, default=0)
    agility = db.Column(db.Integer, default=0)
    lock = db.Column(db.Integer, default=0)
    dodge = db.Column(db.Integer, default=0)
    initiative = db.Column(db.Integer, default=0)
    lock_dodge = db.Column(db.Integer, default=0)
    force_of_will = db.Column(db.Integer, default=0)
    fortune = db.Column(db.Integer, default=0)
    crit_hit = db.Column(db.Integer, default=0)
    block = db.Column(db.Integer, default=0)
    crit_mastery = db.Column(db.Integer, default=0)
    rear_mastery = db.Column(db.Integer, default=0)
    berserk_mastery = db.Column(db.Integer, default=0)
    healing_mastery = db.Column(db.Integer, default=0)
    rear_res = db.Column(db.Integer, default=0)
    crit_res = db.Column(db.Integer, default=0)
    major = db.Column(db.Integer, default=0)
    ap = db.Column(db.Integer, default=0)
    mp = db.Column(db.Integer, default=0)
    spell_range = db.Column(db.Integer, default=0)
    wp = db.Column(db.Integer, default=0)
    control = db.Column(db.Integer, default=0)
    dmg_inflicted = db.Column(db.Integer, default=0)
    resistance = db.Column(db.Integer, default=0)

    build = db.relationship('Build', back_populates='characteristic')


    def show(self):
        """Return a dict of non-empty attributes"""
        attributes = {}

        for key, value in self.__dict__.items():
            # Remove _sa_instance_state attr and values with None
            if value != None and not key.startswith('_'):
                attributes.update({key : value})

        return attributes


    def __repr__(self):
        return f"""
                <Characteristic id = {self.id}; 
                Intelligence = {self.intelligence};
                Strength = {self.strength};
                Agility = {self.agility};
                Fortune = {self.fortune};
                Major = {self.major}>
                """
    

class Characteristic_cap(db.Model):
    """Max number of each characteristic by level"""

    __tablename__ = 'characteristic_caps'

    level = db.Column(db.Integer,
                      primary_key = True)
    intelligence = db.Column(db.Integer)
    hp_percentage = db.Column(db.Integer)
    elemental_res = db.Column(db.Integer)
    barrier = db.Column(db.Integer)
    heals_received = db.Column(db.Integer)
    armor = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    elemental_mastery = db.Column(db.Integer)
    melee_mastery = db.Column(db.Integer)
    distance_mastery = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    agility = db.Column(db.Integer)
    lock = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
    initiative = db.Column(db.Integer)
    lock_dodge = db.Column(db.Integer)
    force_of_will = db.Column(db.Integer)
    fortune = db.Column(db.Integer)
    crit_hit = db.Column(db.Integer)
    block = db.Column(db.Integer)
    crit_mastery = db.Column(db.Integer)
    rear_mastery = db.Column(db.Integer)
    berserk_mastery = db.Column(db.Integer)
    healing_mastery = db.Column(db.Integer)
    rear_res = db.Column(db.Integer)
    crit_res = db.Column(db.Integer)
    major = db.Column(db.Integer)
    ap = db.Column(db.Integer)
    mp = db.Column(db.Integer)
    spell_range = db.Column(db.Integer)
    wp = db.Column(db.Integer)
    control = db.Column(db.Integer)
    dmg_inflicted = db.Column(db.Integer)
    resistance = db.Column(db.Integer)

    def __repr__(self):
        return f"""
                <Characteristic_cap level = {self.level}; 
                Intelligence cap = {self.intelligence};
                Strength cap = {self.strength};
                Agility cap = {self.agility};
                Fortune cap = {self.fortune};
                Major cap = {self.major}>
                """
    

class Equipment_set(db.Model):
    """All the equippable pieces included in a set for the character"""

    __tablename__ = 'equipment_sets'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    helmet_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    amulet_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    breastplate_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    boots_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    ring1_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    ring2_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    cape_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    epaulettes_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    belt_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    off_hand_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    main_hand_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    two_hander_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    emblem_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    mount_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))

    build = db.relationship('Build',
                            back_populates='equipment_set')
    helmet = db.relationship('Equipment',
                             foreign_keys=[helmet_id], 
                             back_populates='equipment_set_helmet', 
                             lazy="joined")
    amulet = db.relationship('Equipment',
                             foreign_keys=[amulet_id],
                             back_populates='equipment_set_amulet',
                             lazy='joined')
    breastplate = db.relationship('Equipment', 
                                  foreign_keys=[breastplate_id],
                                  back_populates='equipment_set_breastplate',
                                  lazy='joined')
    boots = db.relationship('Equipment',
                            foreign_keys=[boots_id],
                            back_populates='equipment_set_boots',
                            lazy='joined')
    ring1 = db.relationship('Equipment',
                            foreign_keys=[ring1_id],
                            back_populates='equipment_set_ring1',
                            lazy='joined')
    ring2 = db.relationship('Equipment',
                            foreign_keys=[ring2_id],
                            back_populates='equipment_set_ring2',
                            lazy='joined')
    cape = db.relationship('Equipment',
                           foreign_keys=[cape_id],
                           back_populates='equipment_set_cape',
                           lazy='joined')
    epaulettes = db.relationship('Equipment',
                                 foreign_keys=[epaulettes_id],
                                 back_populates='equipment_set_epaulettes',
                                 lazy='joined')
    belt = db.relationship('Equipment',
                           foreign_keys=[belt_id],
                           back_populates='equipment_set_belt',
                           lazy='joined')
    pet = db.relationship('Equipment',
                          foreign_keys=[pet_id],
                          back_populates='equipment_set_pet',
                          lazy='joined')
    off_hand = db.relationship('Equipment',
                               foreign_keys=[off_hand_id],
                               back_populates='equipment_set_off_hand',
                               lazy='joined')
    main_hand = db.relationship('Equipment',
                                foreign_keys=[main_hand_id],
                                back_populates='equipment_set_main_hand',
                                lazy='joined')
    two_hand = db.relationship('Equipment',
                               foreign_keys=[two_hander_id],
                               back_populates='equipment_set_two_hand',
                               lazy='joined')
    emblem = db.relationship('Equipment',
                             foreign_keys=[emblem_id],
                             back_populates='equipment_set_emblem',
                             lazy='joined')
    mount = db.relationship('Equipment',
                            foreign_keys=[mount_id],
                            back_populates='equipment_set_mount',
                            lazy='joined')


    def show(self):
        """Return a dict of non-empty attributes"""
        attributes = {}

        for key, value in self.__dict__.items():
            # Remove _sa_instance_state attr and values with None
            if value != None and not key.startswith('_'):
                attributes.update({key : value})

        return attributes


    def __repr__(self):
        return f"""
                <Equipment_set id = {self.id};
                Helmet_id = {self.helmet_id};
                Amulet_id = {self.amulet_id};
                Breastplate_id = {self.breastplate_id};
                Boots_id = {self.boots_id};
                Ring1_id = {self.ring1_id};
                Ring2_id = {self.ring2_id};
                Cape_id = {self.cape_id};
                Epaulettes_id = {self.epaulettes_id};
                Belt_id = {self.belt_id};
                Pet_id = {self.pet_id};
                Off_hand_id = {self.off_hand_id};
                Main_hand_id = {self.main_hand_id};
                Two_hander_id = {self.two_hander_id};
                Emblem_id = {self.emblem_id};
                Mount_id = {self.mount_id}>
                """

class Equipment(db.Model):
    """All equippable items in the game"""

    __tablename__ = 'equipments'

    id = db.Column(db.Integer,
                   primary_key = True)
    equip_type_id = db.Column(db.Integer)
    level = db.Column(db.Integer)
    rarity = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    hp_neg = db.Column(db.Integer)
    armor = db.Column(db.Integer)
    armor_neg = db.Column(db.Integer)
    ap = db.Column(db.Integer)
    ap_neg = db.Column(db.Integer)
    mp = db.Column(db.Integer)
    mp_neg = db.Column(db.Integer)
    wp = db.Column(db.Integer)
    wp_neg = db.Column(db.Integer)
    elemental_mastery = db.Column(db.Integer)
    elemental_mastery_neg = db.Column(db.Integer)
    water_mastery = db.Column(db.Integer)
    water_mastery_neg = db.Column(db.Integer)
    air_mastery = db.Column(db.Integer)
    air_mastery_neg = db.Column(db.Integer)
    earth_mastery = db.Column(db.Integer)
    earth_mastery_neg = db.Column(db.Integer)
    fire_mastery = db.Column(db.Integer)
    fire_mastery_neg = db.Column(db.Integer)
    elemental_res = db.Column(db.Integer)
    elemental_res_neg = db.Column(db.Integer)
    water_res  = db.Column(db.Integer)
    water_res_neg = db.Column(db.Integer)
    air_res = db.Column(db.Integer)
    air_res_neg = db.Column(db.Integer)
    earth_res = db.Column(db.Integer)
    earth_res_neg = db.Column(db.Integer)
    fire_res = db.Column(db.Integer)
    fire_res_neg = db.Column(db.Integer)
    dmg_inflicted = db.Column(db.Integer)
    dmg_inflicted_neg = db.Column(db.Integer)
    crit_hit = db.Column(db.Integer)
    crit_hit_neg = db.Column(db.Integer)
    initiative = db.Column(db.Integer)
    initiative_neg = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
    dodge_neg = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    wisdom_neg = db.Column(db.Integer)
    control = db.Column(db.Integer)
    control_neg = db.Column(db.Integer)
    heals_performed = db.Column(db.Integer)
    heals_performed_neg = db.Column(db.Integer)
    heals_received = db.Column(db.Integer)
    heals_received_neg = db.Column(db.Integer)
    block = db.Column(db.Integer)
    block_neg = db.Column(db.Integer)
    spell_range = db.Column(db.Integer)
    spell_range_neg = db.Column(db.Integer)
    lock = db.Column(db.Integer)
    lock_neg = db.Column(db.Integer)
    prospecting = db.Column(db.Integer)
    prospecting_neg = db.Column(db.Integer)
    force_of_will = db.Column(db.Integer)
    force_of_will_neg = db.Column(db.Integer)
    crit_mastery = db.Column(db.Integer)
    crit_mastery_neg = db.Column(db.Integer)
    rear_mastery = db.Column(db.Integer)
    rear_mastery_neg = db.Column(db.Integer)
    melee_mastery = db.Column(db.Integer)
    melee_mastery_neg = db.Column(db.Integer)
    distance_mastery = db.Column(db.Integer)
    distance_mastery_neg = db.Column(db.Integer)
    healing_mastery = db.Column(db.Integer)
    healing_mastery_neg = db.Column(db.Integer)
    berserk_mastery = db.Column(db.Integer)
    berserk_mastery_neg = db.Column(db.Integer)
    crit_res = db.Column(db.Integer)
    crit_res_neg = db.Column(db.Integer)
    rear_res = db.Column(db.Integer)
    rear_res_neg = db.Column(db.Integer)
    armor_given = db.Column(db.Integer)
    armor_given_neg = db.Column(db.Integer)
    armor_received = db.Column(db.Integer)
    armor_received_neg = db.Column(db.Integer)
    indirect_dmg = db.Column(db.Integer)
    indirect_dmg_neg = db.Column(db.Integer)
    random_masteries = db.Column(db.Integer) 
    num_random_masteries = db.Column(db.Integer) #num of random masteries allowed
    random_resistances = db.Column(db.Integer)
    num_random_resistances = db.Column(db.Integer)
    state = db.Column(db.String)
    farmer = db.Column(db.Integer)
    lumberjack = db.Column(db.Integer)
    herbalist = db.Column(db.Integer)
    miner = db.Column(db.Integer)
    trapper = db.Column(db.Integer)
    fisherman = db.Column(db.Integer)

    equipment_set_helmet = db.relationship('Equipment_set', 
                                           foreign_keys=[Equipment_set.helmet_id],
                                           back_populates='helmet')
    equipment_set_amulet = db.relationship('Equipment_set', 
                                           foreign_keys=[Equipment_set.amulet_id],
                                           back_populates='amulet')
    equipment_set_breastplate = db.relationship('Equipment_set', 
                                                foreign_keys=[Equipment_set.breastplate_id],
                                                back_populates='breastplate')
    equipment_set_boots = db.relationship('Equipment_set', 
                                          foreign_keys=[Equipment_set.boots_id],
                                          back_populates='boots')
    equipment_set_ring1 = db.relationship('Equipment_set', 
                                          foreign_keys=[Equipment_set.ring1_id],
                                          back_populates='ring1')
    equipment_set_ring2 = db.relationship('Equipment_set', 
                                          foreign_keys=[Equipment_set.ring2_id],
                                          back_populates='ring2')
    equipment_set_cape = db.relationship('Equipment_set', 
                                         foreign_keys=[Equipment_set.cape_id],
                                         back_populates='cape')
    equipment_set_epaulettes = db.relationship('Equipment_set', 
                                               foreign_keys=[Equipment_set.epaulettes_id],
                                               back_populates='epaulettes')
    equipment_set_belt = db.relationship('Equipment_set', 
                                         foreign_keys=[Equipment_set.belt_id],
                                         back_populates='belt')
    equipment_set_pet = db.relationship('Equipment_set', 
                                        foreign_keys=[Equipment_set.pet_id],
                                        back_populates='pet')
    equipment_set_off_hand = db.relationship('Equipment_set', 
                                             foreign_keys=[Equipment_set.off_hand_id],
                                             back_populates='off_hand')
    equipment_set_main_hand = db.relationship('Equipment_set', 
                                              foreign_keys=[Equipment_set.main_hand_id],
                                              back_populates='main_hand')
    equipment_set_two_hand = db.relationship('Equipment_set', 
                                              foreign_keys=[Equipment_set.two_hander_id],
                                              back_populates='two_hand')
    equipment_set_emblem = db.relationship('Equipment_set', 
                                           foreign_keys=[Equipment_set.emblem_id],
                                           back_populates='emblem')
    equipment_set_mount = db.relationship('Equipment_set', 
                                          foreign_keys=[Equipment_set.mount_id],
                                          back_populates='mount')
    # random_mastery = db.relationship('Equipment_random_mastery_element',
    #                                  back_populates='equipment')
    # random_resistance = db.relationship('Equipment_random_resistance_element',
    #                                     back_populates='equipment')

    def show(self):
        """Return a dict of non-empty attributes"""
        attributes = {}

        for key, value in self.__dict__.items():
            # Remove _sa_instance_state attr and values with None
            if value != None and not key.startswith('_'):
                attributes.update({key : value})

        return attributes


    def __repr__(self):
        return f"""
                <id = {self.id};
                equip_type_id = {self.equip_type_id};
                level = {self.level};
                rarity = {self.rarity}
                hp = {self.hp};
                hp_neg = {self.hp_neg};
                armor = {self.armor};
                armor_neg = {self.armor_neg};
                ap = {self.ap};
                ap_neg = {self.ap_neg};
                mp = {self.mp};
                mp_neg = {self.mp_neg};
                wp = {self.wp};
                wp_neg = {self.wp_neg};
                elemental_mastery = {self.elemental_mastery};
                elemental_mastery_neg = {self.elemental_mastery_neg};
                water_mastery = {self.water_mastery};
                water_mastery_neg = {self.water_mastery_neg};
                air_mastery = {self.air_mastery};
                air_mastery_neg = {self.air_mastery_neg};
                earth_mastery = {self.earth_mastery};
                earth_mastery_neg = {self.earth_mastery_neg};
                fire_mastery = {self.fire_mastery};
                fire_mastery_neg = {self.fire_mastery_neg};
                elemental_res = {self.elemental_res};
                elemental_res_neg = {self.elemental_res_neg};
                water_res  = {self.water_res };
                water_res_neg = {self.water_res_neg};
                air_res = {self.air_res};
                air_res_neg = {self.air_res_neg};
                earth_res = {self.earth_res};
                earth_res_neg = {self.earth_res_neg};
                fire_res = {self.fire_res};
                fire_res_neg = {self.fire_res_neg};
                dmg_inflicted = {self.dmg_inflicted};
                dmg_inflicted_neg = {self.dmg_inflicted_neg};
                crit_hit = {self.crit_hit};
                crit_hit_neg = {self.crit_hit_neg};
                initiative = {self.initiative};
                initiative_neg = {self.initiative_neg};
                dodge = {self.dodge};
                dodge_neg = {self.dodge_neg};
                wisdom = {self.wisdom};
                wisdom_neg = {self.wisdom_neg};
                control = {self.control};
                control_neg = {self.control_neg};
                heals_performed = {self.heals_performed};
                heals_performed_neg = {self.heals_performed_neg};
                block = {self.block};
                block_neg = {self.block_neg};
                spell_range = {self.spell_range};
                spell_range_neg = {self.spell_range_neg};
                lock = {self.lock};
                lock_neg = {self.lock_neg};
                prospecting = {self.prospecting};
                prospecting_neg = {self.prospecting_neg};
                force_of_will = {self.force_of_will};
                force_of_will_neg = {self.force_of_will_neg};
                crit_mastery = {self.crit_mastery};
                crit_mastery_neg = {self.crit_mastery_neg};
                rear_mastery = {self.rear_mastery};
                rear_mastery_neg = {self.rear_mastery_neg};
                melee_mastery = {self.melee_mastery};
                melee_mastery_neg = {self.melee_mastery_neg};
                distance_mastery = {self.distance_mastery};
                distance_mastery_neg = {self.distance_mastery_neg};
                healing_mastery = {self.healing_mastery};
                healing_mastery_neg = {self.healing_mastery_neg};
                berserk_mastery = {self.berserk_mastery};
                berserk_mastery_neg = {self.berserk_mastery_neg};
                crit_res = {self.crit_res};
                crit_res_neg = {self.crit_res_neg};
                rear_res = {self.rear_res};
                rear_res_neg = {self.rear_res_neg};
                armor_given = {self.armor_given};
                armor_given_neg = {self.armor_given_neg};
                armor_received = {self.armor_received};
                armor_received_neg = {self.armor_received_neg};
                indirect_dmg = {self.indirect_dmg};
                indirect_dmg_neg = {self.indirect_dmg_neg};
                random_masteries = {self.random_masteries};
                num_random_masteries = {self.num_random_masteries};
                random_resistances = {self.random_resistances};
                num_random_resistances = {self.num_random_resistances};
                state = {self.state};
                farmer = {self.farmer};
                lumberjack = {self.lumberjack};
                herbalist = {self.herbalist};
                miner = {self.miner};
                trapper = {self.trapper};
                fisherman = {self.fisherman}>
                """
    

class Element(db.Model):
    """The four elements used in masteries and resistances"""

    __tablename__ = 'elements'

    id = db.Column(db.Integer,
                #    autoincrement = True,
                   primary_key = True)
    name = db.Column(db.String,
                     nullable = False)
    resistance_id = db.Column(db.Integer)
    mastery_id = db.Column(db.Integer)

    # selected_mastery = db.relationship('Selected_mastery_element', 
    #                                    back_populates='element')
    # selected_resistance = db.relationship('Selected_resistance_element', 
    #                                       back_populates='element')
    # random_mastery = db.relationship('Equipment_random_mastery_element', 
    #                                  back_populates='element')
    # random_resistance = db.relationship('Equipment_random_resistance_element', 
    #                                  back_populates='element')
    selected_elements = db.relationship('Selected_element', 
                                          back_populates='element')
    
    def __repr__(self):
        return f"""
                <Element id = {self.id}; name = {self.name}
                Resistance id = {self.resistance_id};
                Mastery id = {self.mastery_id}>
                """
    

class Selected_element(db.Model):
    """The elements selected for random mastery and resistance 
    for the build"""

    __tablename__ = 'selected_elements'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    build_id = db.Column(db.Integer,
                          db.ForeignKey('builds.id'))
    element_id = db.Column(db.Integer,
                           db.ForeignKey('elements.id'))
    # Positions 0-3 mastery, 4-7 resistance
    position = db.Column(db.Integer)

    build = db.relationship('Build', back_populates='selected_elements')
    element = db.relationship('Element', 
                              back_populates='selected_elements',
                              lazy="joined")
    
    def __repr__(self):
        return f"""
                <Selected_mastery_element id = {self.id};
                Build id = {self.build_id};
                Element id = {self.element_id};
                Position = {self.position}>
                """



# class Selected_mastery_element(db.Model):
#     """The mastery elements selected for the build"""

#     __tablename__ = 'selected_mastery_elements'

#     id = db.Column(db.Integer,
#                    autoincrement = True,
#                    primary_key = True)
#     build_id = db.Column(db.Integer,
#                           db.ForeignKey('builds.id'))
#     element_id = db.Column(db.Integer,
#                            db.ForeignKey('elements.id'))
#     position = db.Column(db.Integer)

#     build = db.relationship('Build', back_populates='selected_mastery')
#     element = db.relationship('Element', back_populates='selected_mastery')
    
#     def __repr__(self):
#         return f"""
#                 <Selected_mastery_element id = {self.id};
#                 Build id = {self.build_id};
#                 Element id = {self.element_id}>
#                 """
    

# class Equipment_random_mastery_element(db.Model):
#     """The elements assigned to the random mastery slots of an item"""

#     __tablename__ = 'equipment_random_mastery_elements'

#     id = db.Column(db.Integer,
#                    autoincrement = True,
#                    primary_key = True)
#     equipment_id = db.Column(db.Integer,
#                              db.ForeignKey('equipments.id'))
#     element_id = db.Column(db.Integer,
#                              db.ForeignKey('elements.id'))

#     equipment = db.relationship('Equipment', back_populates='random_mastery')
#     element = db.relationship('Element', back_populates='random_mastery')
    
#     def __repr__(self):
#         return f"""
#                 <Equipment_random_mastery_element id = {self.id};
#                 Equipment id = {self.equipment_id};
#                 Element id = {self.element_id}>
#                 """
    

# class Selected_resistance_element(db.Model):
#     """The resistance elements selected for the build"""

#     __tablename__ = 'selected_resistance_elements'

#     id = db.Column(db.Integer,
#                    autoincrement = True,
#                    primary_key = True)
#     build_id = db.Column(db.Integer,
#                           db.ForeignKey('builds.id'))
#     element_id = db.Column(db.Integer,
#                            db.ForeignKey('elements.id'))
#     position = db.Column(db.Integer)
    
#     build =  db.relationship('Build', back_populates='selected_resistance')
#     element = db.relationship('Element', back_populates='selected_resistance')
    
#     def __repr__(self):
#         return f"""
#                 <Selected_resistance_element id = {self.id};
#                 Build id = {self.build_id};
#                 Element id = {self.element_id}>
#                 """
    

# class Equipment_random_resistance_element(db.Model):
#     """The elements assigned to the random resistance slots of an item"""

#     __tablename__ = 'equipment_random_resistance_elements'

#     id = db.Column(db.Integer,
#                    autoincrement = True,
#                    primary_key = True)
#     equipment_id = db.Column(db.Integer,
#                              db.ForeignKey('equipments.id'))
#     element_id = db.Column(db.Integer,
#                              db.ForeignKey('elements.id'))
    
#     equipment = db.relationship('Equipment', back_populates='random_resistance')
#     element = db.relationship('Element', back_populates='random_resistance')
    
#     def __repr__(self):
#         return f"""
#                 <Equipment_random_resistance_element id = {self.id};
#                 Equipment id = {self.equipment_id};
#                 Element id = {self.element_id}>
#                 """


class Base_stat(db.Model):
    """Base stats without any equippable items, spells, or passives"""

    __tablename__ = 'base_stats'

    level = db.Column(db.Integer,
                      primary_key = True)
    hp = db.Column(db.Integer,
                   nullable = False)
    ap = db.Column(db.Integer, default=6)
    mp = db.Column(db.Integer, default=3)
    wp = db.Column(db.Integer, default=6)

    
    def show(self):
        """Return a dict of non-empty attributes"""
        attributes = {}

        for key, value in self.__dict__.items():
            # Remove _sa_instance_state attr and values with None
            if value != None and not key.startswith('_'):
                attributes.update({key : value})

        return attributes

    def __repr__(self):
        return f'<Base_stat level = {self.level}; HP = {self.hp}>'


class Character_class(db.Model):
    """Selected character class"""

    __tablename__ = 'character_classes'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    name = db.Column(db.String,
                     nullable = False)
    
    build = db.relationship('Build', back_populates='character_class')
    spell = db.relationship('Spell', back_populates='character_class')
    passive = db.relationship('Passive', back_populates='character_class')
    
    def __repr__(self):
        return f"""
                <Character_class id = {self.id}; Name = {self.name}>
                """
    

class Spell(db.Model):
    """Spells available in the game"""

    __tablename__ = 'spells'

    id = db.Column(db.Integer,
                   primary_key = True)
    character_class_id = db.Column(db.Integer,
                                   db.ForeignKey('character_classes.id'))
    spell_level = db.Column(db.Integer,
                            nullable = False)
    # Move to separate table with all names/descriptions in diff languages
    # spell_name = db.Column(db.String)
    # spell_description = db.Column(db.String)
    ap_cost = db.Column(db.Integer)
    mp_cost = db.Column(db.Integer)
    wp_cost = db.Column(db.Integer)
    sp_cost = db.Column(db.Integer)
    cooldown = db.Column(db.Integer)
    dmg = db.Column(db.Integer)
    crit_dmg = db.Column(db.Integer)
    conditional_dmg = db.Column(db.Integer)
    crit_conditional_dmg = db.Column(db.Integer)

    character_class = db.relationship('Character_class', back_populates='spell')
    selected_spell = db.relationship('Selected_spell', back_populates='spell')

    def __repr__(self):
        return f"""
                <Spell id = {self.id};
                Spell level = {self.spell_level};
                Character_class_id = {self.character_class_id}>
                """


class Selected_spell(db.Model):
    """Spell selected for build"""

    __tablename_ = 'selected_spells'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    build_id = db.Column(db.Integer,
                         db.ForeignKey('builds.id'))
    spell_id = db.Column(db.Integer,
                         db.ForeignKey('spells.id'))
    
    build = db.relationship('Build', back_populates='selected_spell')
    spell = db.relationship('Spell', back_populates='selected_spell')
    
    def __repr__(self):
        return f"""
                <Selected_spell id {self.id}; 
                Build id = {self.build_id};
                Spell id = {self.spell_id}>
                """


class Spell_slot_cap(db.Model):
    """Number of spells allowed at each level"""

    __tablename__ = 'spell_slot_caps'

    level = db.Column(db.Integer,
                      primary_key = True)
    num_of_slots = db.Column(db.Integer,
                             nullable = False)
    
    def __repr__(self):
        return f"""
                <Spell_slot_cap level = {self.level};
                <Num_of_slots = {self.num_of_slots}>
                """


class Passive(db.Model):
    """All spell passives in the game"""

    __tablename__ = 'passives'

    id = db.Column(db.Integer,
                   primary_key = True)
    character_class_id = db.Column(db.Integer,
                                   db.ForeignKey('character_classes.id'))
    passive_level = db.Column(db.Integer,
                              nullable = False)
    equip_type_id = db.Column(db.Integer)
    level = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    hp_neg = db.Column(db.Integer)
    armor = db.Column(db.Integer)
    armor_neg = db.Column(db.Integer)
    ap = db.Column(db.Integer)
    ap_neg = db.Column(db.Integer)
    mp = db.Column(db.Integer)
    mp_neg = db.Column(db.Integer)
    wp = db.Column(db.Integer)
    wp_neg = db.Column(db.Integer)
    water_mastery = db.Column(db.Integer)
    water_mastery_neg = db.Column(db.Integer)
    air_mastery = db.Column(db.Integer)
    air_mastery_neg = db.Column(db.Integer)
    earth_mastery = db.Column(db.Integer)
    earth_mastery_neg = db.Column(db.Integer)
    fire_mastery = db.Column(db.Integer)
    fire_mastery_neg = db.Column(db.Integer)
    water_res  = db.Column(db.Integer)
    water_res_neg = db.Column(db.Integer)
    air_res = db.Column(db.Integer)
    air_res_neg = db.Column(db.Integer)
    earth_res = db.Column(db.Integer)
    earth_res_neg = db.Column(db.Integer)
    fire_res = db.Column(db.Integer)
    fire_res_neg = db.Column(db.Integer)
    dmg_inflicted = db.Column(db.Integer)
    dmg_inflicted_neg = db.Column(db.Integer)
    crit_hit = db.Column(db.Integer)
    crit_hit_neg = db.Column(db.Integer)
    initiative = db.Column(db.Integer)
    initiative_neg = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
    dodge_neg = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    wisdom_neg = db.Column(db.Integer)
    control = db.Column(db.Integer)
    control_neg = db.Column(db.Integer)
    heals_performed = db.Column(db.Integer)
    heals_performed_neg = db.Column(db.Integer)
    heals_received = db.Column(db.Integer)
    heals_received_neg = db.Column(db.Integer)
    block = db.Column(db.Integer)
    block_neg = db.Column(db.Integer)
    spell_range = db.Column(db.Integer)
    range__neg = db.Column(db.Integer)
    lock = db.Column(db.Integer)
    lock_neg = db.Column(db.Integer)
    prospecting = db.Column(db.Integer)
    prospecting_neg = db.Column(db.Integer)
    force_of_will = db.Column(db.Integer)
    force_of_will_neg = db.Column(db.Integer)
    crit_mastery = db.Column(db.Integer)
    crit_mastery_neg = db.Column(db.Integer)
    rear_mastery = db.Column(db.Integer)
    rear_mastery_neg = db.Column(db.Integer)
    melee_mastery = db.Column(db.Integer)
    melee_mastery_neg = db.Column(db.Integer)
    distance_mastery = db.Column(db.Integer)
    distance_mastery_neg = db.Column(db.Integer)
    healing_mastery = db.Column(db.Integer)
    healing_mastery_neg = db.Column(db.Integer)
    berserk_mastery = db.Column(db.Integer)
    berserk_mastery_neg = db.Column(db.Integer)
    crit_res = db.Column(db.Integer)
    crit_res_neg = db.Column(db.Integer)
    rear_res = db.Column(db.Integer)
    rear_res_neg = db.Column(db.Integer)
    armor_given = db.Column(db.Integer)
    armor_given_neg = db.Column(db.Integer)
    armor_received = db.Column(db.Integer)
    armor_received_neg = db.Column(db.Integer)
    indirect_dmg = db.Column(db.Integer)
    indirect_dmg_neg = db.Column(db.Integer)
    sp = db.Column(db.Integer) #specific to fogger
    sp_neg = db.Column(db.Integer)

    character_class = db.relationship('Character_class', back_populates='passive')
    selected_passive = db.relationship('Selected_passive', back_populates='passive')

    def __repr__(self):
        return f"""
                <Passive id = {self.id};
                Passive level = {self.spell_level};
                Character_class_id = {self.character_class_id}>
                """


class Selected_passive(db.Model):
    """Passive selected for build"""

    __tablename__ = 'selected_passives'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    build_id = db.Column(db.Integer,
                         db.ForeignKey('builds.id'))
    passive_id = db.Column(db.Integer,
                         db.ForeignKey('passives.id'))

    build = db.relationship('Build', back_populates='selected_passive')
    passive = db.relationship('Passive', back_populates='selected_passive')
    
    def __repr__(self):
        return f"""
                <Selected_passive id {self.id}; 
                Build id = {self.build_id};
                Passive id = {self.passive_id}>
                """


class Passive_slot_cap(db.Model):
    """Number of passives allowed at each level"""

    __tablename__ = 'passive_slot_caps'

    level = db.Column(db.Integer,
                      primary_key = True)
    num_of_slots = db.Column(db.Integer,
                             nullable = False)
    
    def __repr__(self):
        return f"""
                <Passive_slot_cap level = {self.level};
                <Num_of_slots = {self.num_of_slots}>
                """


class Name_translation(db.Model):
    """All the names translated in English, French, Spanish, Portuguese"""

    __tablename__ = 'name_translations'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    name_id = db.Column(db.Integer) # ID of item
    name_type = db.Column(db.String(20)) # State, equipment, etc
    en = db.Column(db.String)
    fr = db.Column(db.String)
    es = db.Column(db.String)
    pt = db.Column(db.String)
    # Search localization libraries

    def __repr__(self):
        return f"""
                <Name_translation id = {self.id};
                Name_id = {self.name_id};
                Name_type = {self.name_type};
                English = {self.en};
                French = {self.fr};
                Spanish = {self.es};
                Portuguese = {self.pt}>
                """



# Connect the db to flask server
def connect_to_db(flask_app, db_uri="postgresql:///wakfuData", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)