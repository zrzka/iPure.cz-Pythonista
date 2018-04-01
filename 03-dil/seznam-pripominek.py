#!python3

import console
import notification
import datetime
import dialogs
import time


def cancel_removed_reminders(initial, final):
    """Zrusi vsechny pripominky z `initial` pokud nejsou ve `final`.

    Arguments:
        initial: Puvodni pripominky (pred zobrazenim / editaci).
        final: Pripominky, ktere maji zustat.

    Note:
        Tento zpusob nefunguje, protoze Pythonista obsahuje chybu znemoznujici
        odstranit notifikaci obsahujici action_url. Vice viz. funkce
        cancel_removed_reminders_workaround.
    """
    to_be_removed = [x for x in initial if x not in final]

    for x in to_be_removed:
        notification.cancel(x['note'])


def cancel_removed_reminders_workaround(initial, final):
    """Zrusi vsechny pripominky z `initial` pokud nejsou ve `final`.

    Arguments:
        initial: Puvodni pripominky (pred zobrazenim / editaci).
        final: Pripominky, ktere maji zustat.
    """

    if len(initial) == len(final):
        # Nic nechceme odstranit, koncime
        return

    # Musime zrusit vsechny notifikace
    notification.cancel_all()

    # Zjistime si aktualni cas
    now = time.time()

    def calculate_delay(note):
        # Funkce vypocita hodnotu delay a vlozi ji do notifikace.
        # fire_date je totiz cas kdy se ma notifikace zobrazit, ale my ji musime
        # znovu nastavit a tam se vyuziva delay, tj. za jak dlouho se ma zobrazit.
        note['delay'] = note.pop('fire_date') - now
        return note

    # Vypocitame delay pro vsechny notifikace
    notes = [calculate_delay(x['note']) for x in final]

    # Znovu je nastavime
    for note in notes:
        notification.schedule(**note)

    count = len(initial) - len(final)
    console.hud_alert(f'Odstraněno {count} připomínek')


def main():
    # Nacteme notifikace
    notes = notification.get_scheduled()

    # Pokud zadne nejsou, zobrazime alert
    if not notes:
        console.hud_alert('Žádné připomínky k zobrazení')
        return

    # Setridime notifikace podle data
    notes = sorted(notes, key=lambda x: x['fire_date'])

    # Prevedeme do vlastniho slovniku, neboli celou notifikaci ulozime
    # do klice note a pridame vlastni titulek (klic title) skladajici se z data & casu
    # a textu notifikace. Hodnotu klice title pouziva dialogs.edit_list_dialog.

    def title(note):
        dt = datetime.datetime.fromtimestamp(note['fire_date'])
        return f"{dt:%Y-%m-%d %H:%M} {note['message']}"

    reminders = [
        {
            'title': title(note),
            'note': note
        }
        for note in notes
    ]

    final = dialogs.edit_list_dialog('Připomínky', reminders, move=False, delete=True)
    if final is None:
        return

    cancel_removed_reminders_workaround(reminders, final)


if __name__ == '__main__':
    main()
