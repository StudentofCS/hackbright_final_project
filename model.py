" Models for Wakfu character builder app"

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

    def __repr__(self):
        return f'<User id = {self.id}; email = {self.email}>'


class Build(db.Model):
    "A build"

    __tablename__ = 'builds'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    equipment_set_id = db.Column(db.Integer,
                                 db.ForeignKey('equipment_sets.id'))
    characteristics_id = db.Column(db.Integer,
                                  db.ForeignKey('characteristics.id'))
    # base_stats_id = db.Column(db.Integer,
    #                          db.ForeignKy('base_stats.id'))
    class_id = db.Column(db.Integer,
                         db.ForeignKey('classes.id'))
    level = db.Column(db.Integer, default = 1)

    def __repr__(self):
        return f"""
            <Build id = {self.id}; User id = {self.user_id};
            Class id = {self.class_id}; Level = {self.level}>
            """ 
    

class Characteristic(db.Model):
    "Selected characteristics"

    __tablename__ = 'characteristics'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    intelligence = db.Column(db.Integer)
    hp_percentage = db.Column(db.Integer)
    elem_res = db.Column(db.Integer)
    barrier = db.Column(db.Integer)
    heals_received = db.Column(db.Integer)
    armor_hp = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    elem_mastery = db.Column(db.Integer)
    melee = db.Column(db.Integer)
    distance = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    agility = db.Column(db.Integer)
    lock = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
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
    action_points = db.Column(db.Integer)
    movement_points = db.Column(db.Integer)
    spell_range = db.Column(db.Integer)
    wakfu_points = db.Column(db.Integer)
    control = db.Column(db.Integer)
    dmg_inflicted = db.Column(db.Integer)
    resistance = db.Column(db.Integer)

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
    elem_res = db.Column(db.Integer)
    barrier = db.Column(db.Integer)
    heals_received = db.Column(db.Integer)
    armor_hp = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    elem_mastery = db.Column(db.Integer)
    melee = db.Column(db.Integer)
    distance = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    agility = db.Column(db.Integer)
    lock = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
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
    action_points = db.Column(db.Integer)
    movement_points = db.Column(db.Integer)
    spell_range = db.Column(db.Integer)
    wakfu_points = db.Column(db.Integer)
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
                Mount_id = {self.mount_id};
                """