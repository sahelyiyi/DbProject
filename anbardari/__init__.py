from anbardari.database_communication import create_table

entities = {
    'goods': [
        ('group_title', 'text'),
        ('base_price', 'real'),
        ('maintenance', 'text'),
        ('barcode', 'integer'),
        ('code', 'integer'),
        ('exit_date', 'numeric'),
        ('entry_date', 'numeric'),
        ('production_date', 'numeric'),
        ('producer', 'text'),
        ('price', 'real'),
        ('name', 'text'),
    ],
    'team': [
        ('title', 'text'),
        ('maintenance', 'text'),
        ('base_price', 'real'),
    ],
    'person': [
        ('name', 'text'),
        ('national_code', 'integer'),
        ('membership_code', 'integer'),
        ('birth_date', 'numeric'),
    ],
    'member': [
        ('name', 'text'),
        ('code', 'integer'),
    ],
    'company': [
        ('name', 'text'),
        ('membership_code', 'integer'),
        ('registration_code', 'integer'),
    ],
    'staff': [
        ('national_code', 'integer'),
        ('name', 'text'),
        ('personnel_code', 'text'),
        ('phone_number', 'integer'),
    ],
    'transferee': [
        ('national_code', 'integer'),
        ('name', 'text'),
        ('personnel_code', 'text'),
        ('phone_number', 'integer'),
        ('work_hours', 'real'),
    ],
    'dischargerer': [
        ('national_code', 'integer'),
        ('name', 'text'),
        ('personnel_code', 'text'),
        ('phone_number', 'integer'),
        ('work_hours', 'real'),
    ],
    'transferer': [
        ('national_code', 'integer'),
        ('name', 'text'),
        ('personnel_code', 'text'),
        ('phone_number', 'integer'),
        ('work_hours', 'real'),
    ],
    'keeper': [
        ('national_code', 'integer'),
        ('name', 'text'),
        ('personnel_code', 'text'),
        ('phone_number', 'integer'),
        ('work_hours', 'real'),
    ],
    'not_being_adjacent': [
        ('title1', 'text'),
        ('title2', 'text'),
    ],
    'receive': [
        ('good_code', 'integer'),
        ('member_code', 'integer'),
        ('dischargerer_personal_code', 'integer'),
        ('code', 'integer'),
        ('date', 'numeric'),
    ],
    'surrender': [
        ('good_code', 'integer'),
        ('member_code', 'integer'),
        ('transferee_personal_code', 'integer'),
        ('code', 'integer'),
        ('date', 'numeric'),
    ],
    'instruction': [
        ('good_code', 'integer'),
        ('member_code', 'integer'),
        ('transferer_personal_code', 'integer'),
            ('code', 'integer'),
        ('date', 'numeric'),
        ('cost', 'real'),
    ],
    'caring': [
        ('good_code', 'integer'),
        ('keeper_personal_code', 'integer'),
    ],
}


for entity_name, entity_info in entities.iteritems():
    create_table(entity_name, entity_info)

