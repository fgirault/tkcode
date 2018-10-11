""" tkcode.model contains core abstract classes """
import os

# pylint: disable=too-few-public-methods


class FSEntryFactory:
    """A factory of model objects with a cache"""

    def __init__(self, cache_size=1024):
        self.__cache = {}
        self.cache_size = cache_size

    def get_entry(self, path, class_obj):
        """ build a FSEntry instance or use cache"""
        path = os.path.abspath(path)
        if path in self.__cache:
            file_obj = self.__cache[path]
        else:
            file_obj = class_obj(path)
            if len(self.__cache) > self.cache_size:
                self.clear_cache()
            self.__cache[file_obj.path] = file_obj
        file_obj.factory = self
        return file_obj

    def get_folder(self, path):
        """build a Folder instance using cache """
        return self.get_entry(path, Folder)

    def get_file(self, path):
        """build a FileEntry instance using cache """
        return self.get_entry(path, FileEntry)

    def clear_cache(self):
        """clear first elements of the cache. not good but no leaks :) """
        for index, (path, _) in enumerate(self.__cache.keys()):
            if index < self.cache_size:
                del self.__cache[path]
            else:
                break


class FSEntry:
    """Base class for the model """

    def __init__(self, path):
        assert isinstance(path, str)
        self.path = os.path.abspath(path)
        self.__basename = None
        self.parent = None
        self.factory = None

    def __get_basename(self):
        if self.__basename is None:
            self.__basename = os.path.basename(self.path)
        return self.__basename

    basename = property(__get_basename)

    dirname = property(lambda self: os.path.dirname(self.path))

    def __hash__(self):
        return self.path

    def __eq__(self, other):
        return self.path == other.path

    def __lt__(self, other):
        return self.path < other.path


class FileEntry(FSEntry):
    """File entry model class"""

    def __get_content(self):
        return open(self.path).read()

    content = property(__get_content)

    def is_image(self):
        _, ext = os.path.splitext(self.path)
        return ext.lower() in (".png", ".jpg", ".gif", ".bmp")


class Folder(FSEntry):
    """Folder model: contains other entries """

    def __get_entries(self):
        dir_entries = []
        file_entries = []
        for path in os.listdir(self.path):
            path = os.path.join(self.path, path)

            if os.path.isdir(path):
                dir_entries.append(self.factory.get_folder(path))
            else:
                file_entries.append(self.factory.get_file(path))
        dir_entries.sort()
        file_entries.sort()
        return dir_entries + file_entries

    entries = property(__get_entries)


class TkCodeModel:
    """A model that implements a simple observer pattern """

    def __init__(self):
        """ constructor """
        self.factory = FSEntryFactory()
        self.openfiles = []
        self.folders = []
        self.recent_folders = []
        self.recent_files = []
        self.initial_activity = None
        self.observers = []
        self.current_file = None
        self.preview = None

    def add_observer(self, obverser):
        """ add an observer to the model """
        self.observers.append(obverser)

    def update_observers(self, method_name, *args, originator=None, **kw):
        """
        execute method_name callback in observers, skipping originator.
        returns list of return value of all callbacks
        """
        return [
            getattr(observer, method_name)(*args, **kw)
            for observer in self.observers
            if hasattr(observer, method_name)
            and getattr(observer, method_name).__self__ is not originator
        ]

    def open_folder(self, path, originator=None):
        """open a folder """
        folder = self.factory.get_folder(path)
        if not folder in self.folders:
            self.folders.append(folder)

        self.update_observers("on_folder_open", folder, originator=originator)

    def open_file(self, path, originator=None):
        """open a single file"""
        file_obj = self.factory.get_file(path)

        if file_obj in self.recent_files:
            self.recent_files.remove(file_obj)

        self.recent_files.insert(0, file_obj)

        if file_obj in self.openfiles:
            self.set_current_file(file_obj, originator)
        else:
            self.openfiles.append(file_obj)
            self.update_observers("on_file_open", file_obj, originator=originator)

    def set_current_file(self, file_obj, originator=None):
        """ fire on_file_selected event to observers"""
        self.current_file = file_obj
        self.update_observers("on_file_selected", file_obj, originator=originator)

    def close_file(self, file_obj, originator=None):
        """remove a file entry from the model"""
        if file_obj not in self.openfiles:
            return
        i = self.openfiles.index(file_obj)
        self.openfiles.remove(file_obj)
        self.update_observers("on_file_closed", file_obj, originator=originator)
        if self.openfiles:
            if i == 0:
                self.set_current_file(self.openfiles[0])
            else:
                self.set_current_file(self.openfiles[i - 1])

    def get_file_obj(self, path_or_obj):
        """If path_or_obj is a string, build and return a FileEntry instance.
        If path_or_obj is a FileEntry instance, return it.
        Seems strange but sometime useful
            """
        if isinstance(path_or_obj, str):
            return self.factory.get_file(path_or_obj)
        elif isinstance(path_or_obj, FileEntry):
            return path_or_obj

    def set_preview(self, path_or_obj, originator=None):
        self.preview = self.get_file_obj(path_or_obj)
        self.update_observers("on_file_preview", self.preview, originator=originator)
