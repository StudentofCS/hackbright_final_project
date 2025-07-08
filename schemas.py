from model import (db, connect_to_db, User, Build,
                   Characteristic, Characteristic_cap,
                   Equipment_set, Equipment,
                   Element, Selected_element, 
                   Base_stat, Character_class, Spell,
                   Selected_spell, Spell_slot_cap, Passive,
                   Selected_passive, Passive_slot_cap,
                   Name_translation
                   )
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        include_relationships = True
        load_instance = True
    

class CharacteristicSchema(BaseSchema):
    class Meta:
        model = Characteristic


class CharacteristicCapSchema(BaseSchema):
    class Meta:
        model = Characteristic_cap


class EquipmentSchema(BaseSchema):
    class Meta:
        model = Equipment


class EquipmentSetSchema(BaseSchema):
    class Meta:
        model = Equipment_set

    helmet = Nested(EquipmentSchema)
    amulet = Nested(EquipmentSchema)
    breastplate = Nested(EquipmentSchema)
    boots = Nested(EquipmentSchema)
    ring1 = Nested(EquipmentSchema)
    ring2 = Nested(EquipmentSchema)
    cape = Nested(EquipmentSchema)
    epaulettes = Nested(EquipmentSchema)
    belt = Nested(EquipmentSchema)
    pet = Nested(EquipmentSchema)
    off_hand = Nested(EquipmentSchema)
    main_hand = Nested(EquipmentSchema)
    two_hand = Nested(EquipmentSchema)
    emblem = Nested(EquipmentSchema)
    mount = Nested(EquipmentSchema)


class ElementSchema(BaseSchema):
    class Meta:
        model = Element


class SelectedElementSchema(BaseSchema):
    class Meta:
        model = Selected_element
    
    element = Nested(ElementSchema)


class BaseStatSchema(BaseSchema):
    class Meta:
        model = Base_stat

    
class CharacterClassSchema(BaseSchema):
    class Meta:
        model = Character_class
    

class NameTranslationSchema(BaseSchema):
    class Meta:
        model = Name_translation



class BuildSchema(BaseSchema):
    class Meta:
        model = Build

    equipment_set = Nested(EquipmentSetSchema)
    characteristic = Nested(CharacteristicSchema)
    character_class = Nested(CharacterClassSchema)
    selected_elements = Nested(SelectedElementSchema, many=True)


class UserSchema(BaseSchema):
    class Meta:
        model = User
    
    build = Nested(BuildSchema, many=True)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)