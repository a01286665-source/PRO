from os import environ

# El laboratorio facilita el servidor, PostgreSQL y secretos al desplegar.
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')
SECRET_KEY = environ.get('SECRET_KEY')

SESSION_CONFIGS = [
    dict(name='percepcion', display_name='Percepción de categorías raciales',
         app_sequence=['percepcion'], num_demo_participants=8),
    dict(name='piloto_negro', display_name='Piloto: negro(a)', app_sequence=['percepcion'],
         num_demo_participants=1, force_condition=1),
    dict(name='piloto_afromexicano', display_name='Piloto: afromexicano(a)', app_sequence=['percepcion'],
         num_demo_participants=1, force_condition=2),
    dict(name='piloto_afrodescendiente', display_name='Piloto: afrodescendiente', app_sequence=['percepcion'],
         num_demo_participants=1, force_condition=3),
    dict(name='piloto_inegi', display_name='Piloto: frase combinada INEGI',
         app_sequence=['percepcion'], num_demo_participants=1, force_condition=4),
]
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.00, participation_fee=0.00,
                               doc='Experimento anónimo de percepción; sin pagos.')
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
LANGUAGE_CODE = 'es'
REAL_WORLD_CURRENCY_CODE = 'MXN'
USE_POINTS = False
# No se necesitan Rooms: se distribuyen enlaces individuales de participación.
ROOMS = []
