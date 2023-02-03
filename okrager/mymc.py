import subprocess
from okrager.logger import Logger, Verbosity

class MyMC:
    """mymcplus interface class for interacting with the mymcplus command line application.

    python -m pip install mymcplus
    """
    BINARY = 'mymcplus'

    def __init__(self, file):
        """Initialize the MyMC instace with the filepath to the game save file.

        Args:
            file (str): The filepath to the target game save file.
        """
        self.file = file

    def __run(self, args):
        """Run a mymcplus command on the instances file and retrieve the output.

        Args:
            args (list(str)|str): A list of mymcplus arguments or a string argument.

        Returns:
            str: The mymcplus command output.
        """
        if type(args) == str:
            args = [args]
        args = [MyMC.BINARY, '-i', self.file] + args
        output = subprocess.check_output(args).decode('UTF-8')

        command = ' '.join(args)
        Logger.info(Verbosity.DEBUG, f'{command}\n' + output, '')
        return output

    def dir(self):
        """Retrieves the list of saves within the memory card.

Parses the output of the "dir" command which looks as shown:
BASCUS-97129                     Ｏｋａｇｅ　Ｓｈａｄｏｗ
 147KB Not Protected             　Ｋｉｎｇ

7,986 KB Free

        Returns:
            Object.free                (str):  The total file size remaining in the memory card. (Eg: 7,986 KB Free)
            Object.saves               (list): A list of file saves inside the memory card.
            Object.saves[i].id         (str):  The id of the save. (Eg: BASCUS-97129)
            Object.saves[i].size       (str):  The size of the save. (Eg: 147KB)
            Object.saves[i].protection (str):  The proection state of the save. (Eg: Not Protected)
            Object.saves[i].text       (str):  The text name of the save. (Eg: Ｏｋａｇｅ　Ｓｈａｄｏｗ　Ｋｉｎｇ)
        """
        output = self.__run('dir')
        parts = output.split('\n\n')

        # Get free size
        free = parts.pop().strip()

        # Parse saves
        saves = []
        for part in parts:
            lines = part.split('\n')

            # Eg: ['BASCUS-97129', '', '', '', '', '', '', '', '', '', ' Ｏｋａｇｅ\u3000Ｓｈａｄｏｗ']
            id = lines[0].split('  ')

            # Eg: [' 145KB Not Protected', '', '', '', '', '', ' \u3000Ｋｉｎｇ']
            sizeProtected = lines[1].split('  ')

            # Eg: Ｏｋａｇｅ　Ｓｈａｄｏｗ Ｋｉｎｇ
            text = id.pop().strip() + ' ' + sizeProtected.pop().strip()

            # Eg: BASCUS-97129
            id = id[0].strip()

            # Eg: ['145KB', 'Not', 'Protected']
            sizeProtected = sizeProtected[0].strip().split(' ')

            # Eg: 145KB
            size = sizeProtected[0]

            # Eg: Not Protected
            protected = ' '.join(sizeProtected[1:])

            saves.append({
                'id': id,
                'size': size,
                'protection': protected,
                'text': text
            })

        return {
            'saves': saves,
            'free': free,
        }

    def has(self, id):
        """Does the memory card contain a game save with the given id?

        Args:
            id (str): The id of the game save to search for.

        Returns:
            bool: True if a game save with the given id exists.
        """
        for save in self.dir()['saves']:
            if save['id'] == id:
                return True
        return False

    def export(self, id):
        """Export the game save with the given id to a file in the current directory named {id}.psu

        Args:
            id (str): The id of the game save to export.

        Returns:
            str: The command tool output. Eg: "Exporting BASCUS-97129 to BASCUS-97129.psu"
        """
        return self.__run(['export', id])

    def delete(self, id):
        """Delete the game save with the given id from the memory card.

        Args:
            id (str): The id of the game save to delete.

        Returns:
            str: The command tool output. Eg: "\\n"
        """
        return self.__run(['delete', id])

    def copy(self, file):
        """Import the given file into the game save. The id is the name of the file without the ".psu" extension.

        Args:
            file (str): The filepath of the game save to import.

        Returns:
            str: The command tool output. Eg: "Importing BASCUS-97129.psu to BASCUS-97129"
        """
        return self.__run(['import', file])