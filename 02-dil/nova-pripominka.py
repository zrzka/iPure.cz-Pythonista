#!python3

import datetime

import dialogs
import notification


# Vychozi polozky formulare
_FIELDS = (
    {
        'type': 'text',
        'key': 'message',
        'title': 'Připomínka'
    },
    {
        'type': 'datetime',
        'key': 'date',
        'title': 'Kdy',
    },
    {
        'type': 'url',
        'key': 'action',
        'title': 'Akce',
        'placeholder': 'URL, ...'
    }
)


def fields_with_previous_input(input):
    """Vraci polozky formulare.

    Arguments:
        input (dict): None nebo predchozi vstupni udaje z formulare.
    """

    if not input:
        # Prvni zobrazeni formulare, uzivatel zatim nic nezadal, vratime vychozi polozky
        return _FIELDS

    # Uzivatel uz neco zadal, vstupni udaje neprosli validaci, tak mu zobrazime
    # polozky formulare do kterych navic pridame to co uz zadal. Neboli vratime
    # _FIELDS, ale do kazdeho slovniku/mapy pridame klic `value` s tim co uz zadal.
    return [
        dict(**field, value=input[field['key']])
        for field in _FIELDS
    ]


def alert(message):
    """Zobrazi varovný dialog s textem a tlacitkem OK.

    Arguments:
        message (str): Varovna zprava.
    """

    dialogs.alert('Chybné údaje', message, button1='OK', hide_cancel_button=True)


def get_user_input():
    """Vraci slovnik se vstupnima udajema nebo None v pripade zavreni dialogu.

    Klice slovniku jsou primo pouzitelne ve funkci notification.schedule. Tj.
    slovnik obsahuje message, delay a action_url.
    """

    input = None

    # Opakujeme porad dokola dokud nebudou vstupni data validni
    while True:
        input = dialogs.form_dialog('Nová připomínka', fields=fields_with_previous_input(input))

        if input is None:
            # Dialog byl zavreny krizkem, vratime None
            return None

        # Validace pripominky
        message = input['message'].strip()
        if not message:
            alert('Připomínka nemůže být prázdná.')
            continue

        # Validace data & casu zobrazeni
        delta = input['date'] - datetime.datetime.now()
        delay = delta.seconds

        if delay < 60:
            alert('Čas upozornění musí nastat nejdříve za minutue.')
            continue

        # Pokud nezadal akci, zkonvertujeme na None
        action = input['action'].strip() or None

        return dict(message=message, delay=delay, action_url=action)


def main():
    # Ziskame vstup od uzivatele
    result = get_user_input()
    if result:
        # Pokud neco zadal, nastavime novou notifikaci
        notification.schedule(**result)


if __name__ == '__main__':
    main()
