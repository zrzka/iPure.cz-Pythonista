import notification

#
# Za 5s od spusteni skriptu se zobrazi notifikace.
#
# Pokud bude Pythonista v popredi, notifikace se zobrazi jako dialog
# primo v Pythonistovi. Po tapnuti na tlacitko OK se pouze zavre
# dialog s notifikaci.
#
# Pokud bude Pythonista v pozadi, zobrazi se systemova notifikace. Po
# tapnuti na notifikaci se spusti Pythonista.
#
notification.schedule('Mrkni co je nového na iPure.cz', delay=5)

