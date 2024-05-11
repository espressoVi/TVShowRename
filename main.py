import os
import sys
import re
import shutil

class Rename:
    """ 
    Class that takes in a show name and appropriately renames all
    episodes in all seasons. The show name must match the name of the 
    directory in which the episodes are stored.

    We assume the directory is organized as follows:
        Show Name
          - Season x
            - ep 1
            - ep 2
            ...
          - Season y
            - ep 1
            ...

          ...
    The episodes will be renamed in the format - 'Show Name SxxExx.extension'
    """
    allowed_chars = {"(", ")", "-", " "}
    supported_extensions = {'srt', 'mp4', 'mkv', 'avi', 'flv'}

    def __init__(self, top_directory, name = None):
        if not os.path.exists(top_directory):
            raise FileNotFoundError(f"{top_directory} no such file or directory")
        self.top_directory = top_directory
        if name is None:
            tt = self.top_directory.split("/")
            name = tt[-1] if tt[-1] else tt[-2]
        name = "".join(
                [i for i in name if (i.isalnum() or i in self.allowed_chars)]
                )
        if not name:
            raise ValueError("Name is empty or contains non-allowed characters")
        self.name = name
        seasons = self._get_seasons()
        for num, path in seasons.items():
            self._rename_season(num, path)

    def _get_seasons(self):
        """ Explores the top directory and creates a dict with the key season
        number and value as the corresponding season path
        Args:
            None
        Returns:
            res (dict): {season number : path to season}
        """
        res = {}
        folders = os.listdir(self.top_directory)
        if any([True for i in folders if "Season" not in i]):
            raise ValueError("Erroneous file structure detected")
        for folder in folders:
            match = re.search(r"(.+)(\d{1,2})", folder)
            if not match:
                raise ValueError("Erroneous file structure detected")
            try:
                season_number = int(match.group(2))
            except:
                raise ValueError("Erroneous file structure detected")
            res[season_number] = os.path.join(self.top_directory, folder)
        return res

    def _rename_season(self, number, path):
        files = [f for f in os.listdir(path)\
                if os.path.splitext(f)[1][1:] in self.supported_extensions]
        if not files:
            return
        translation = {}
        for file in files:
            match = re.search(r"(.*)[sS](\d{1,2})[eE](\d{1,2})(.*?)\.(.+)", file)
            if not match:
                continue
            season_num = int(match.group(2))
            if season_num != number:
                raise ValueError(f"Potentially misnamed {file} in {path}")
            episode_num = int(match.group(3))
            extension = os.path.splitext(file)[1][1:]
            # Construct the new filename and path
            new_filename = f"{self.name} S{season_num:02d}E{episode_num:02d}.{extension}"
            new_path = os.path.join(path, new_filename)
            translation[file] = new_path
        if not len(translation.values()) == len(set(translation.values())):
            raise ValueError("File rename collision detected: ABORT")
        for key, value in translation.items():
            old_path = os.path.join(path, key)
            shutil.move(old_path, value)

def main():
    Rename("./Reservation Dogs")

if __name__ == "__main__":
    main()
