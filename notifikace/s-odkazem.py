import notification

#
# Za 5s od spusteni skriptu se zobrazi notifikace.
#
# Pokud bude Pythonista v popredi, notifikace se zobrazi jako dialog
# primo v Pythonistovi. Po tapnuti na tlacitko OK se otevre Safari
# s odkazem http://www.ipure.cz/
#
# Pokud bude Pythonista v pozadi, zobrazi se systemova notifikace. Po
# tapnuti na notifikaci se spusti Pythonista a hned pote se otevre
# Safari s odkazem http://www.ipure.cz/
#
notification.schedule('Mrkni co je nového na iPure.cz', delay=5, action_url='http://www.ipure.cz/')

