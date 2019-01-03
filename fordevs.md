# English
## DEPENDENCIES:
* Python3
* Pony.ORM

### Installing Python
#### Windows

Download Python3 from [here](https://python.org/downloads/)

#### Linux / Mac OS X

Python should be preinstalled. If not, install it with your package manager.


### Installing Pony.ORM
#### With PIP

	reader@workstation:~$ pip install --user pony
	...
	reader@workstation:~$ # check if it was installed successfully
	reader@workstation:~$ python3 -c "import pony.orm"
	reader@workstation:~$ # If there was an error, use the fucking google


Since the bot stores the data in a sqlite3 database, you do not  need to install anything else.
## Can I make a different version for my region?


Sure, just make a branch of this project and modify the configuration of the message in the code.

Here are the commands that the users of the bot can run:
|command| action | lines |
|--|--|--|
| /configura | The bot asks the user the required data like where he lives |49, 60, 75, 77, 143|
| /cancella | The bot deletes the configuration of the user |50, 62|
| /aiuto | Show all commands to the user | 47, 52 |
| /dona | Make a donation | 41, 51 |


**LICENSE: [WTFPL](http://www.wtfpl.net/)**


# Italiano
## DIPENDENZE:
* Python3
* Pony.ORM

### Installazione di Python
#### Windows

Scarica Python3 da [qui](https://python.org/downloads/)

#### Linux / Mac OS X

Python dovrebbe essere preinstallato. In caso contrario, va installato col proprio gestore dei pacchetti.


### Installazione di Pony.ORM
#### Con PIP

	lettore@workstation:~$ pip install --user pony
	...
	lettore@workstation:~$ # verifica se è stato installato correttamente
	lettore@workstation:~$ python3 -c "import pony.orm"
	lettore@workstation:~$ # se si è risconrato un errore, usa il cazzo di google


Dato che il bot memorizza i dati in un database sqlite3, non si deve installare altro.

## Posso fare una versione differente per la mia città?

Certamente, ti chiedo solo di fare un branch del progetto e e di modificare la configurazione del messaggio nel codice!

Ecco i comandi che gli utenti possono dare al bot:
| comando | azione | riga di codice |
|--|--|--|
| /configura | Il bot chiede all'utente i dati richiesti come dove vive | 49, 60, 75, 77, 143 |
| /cancella  | Il bot elimina la configurazione dell'utente  | 50, 62 |
| /aiuto     | Mostra all'utente tutti i comandi             | 47, 52 |
| /dona      | Fai una donazione | 41, 51 |

**LICENZA: [WTFPL](http://wtfpl.net/)**

