import glob
from os.path import isfile, join as path_join, isdir, sep as path_separator, basename
from importlib import import_module
from typing import List

import_separator = '.'


class AutoClassDiscoveryUtil:

    _INIT_FILE = 'auto_discovery/__init__.py'
    _PYCACHE_FILE = '__pycache__.py'

    @staticmethod
    def get_child_classes(parent_class, children_class_location) -> List:
        """
        Returns child classes (single level) of 'parent_class' which are part of package 'children_class_location'
        @param parent_class: Parent class reference
        @param children_class_location: Child class package location
        @return: List of child classes
        @rtype: list
        """
        import_location = AutoClassDiscoveryUtil.__get_import_location(children_class_location)
        AutoClassDiscoveryUtil.__import_child_classes(import_location)
        child_classes = parent_class.__subclasses__()
        return child_classes

    @staticmethod
    def get_common_child_classes(parent_class_list: List, children_class_location) -> List:
        """
        Return common child classes among multiple parent classes
        @param parent_class_list:
        @param children_class_location:
        @return:
        """
        import_location = AutoClassDiscoveryUtil.__get_import_location(children_class_location)
        AutoClassDiscoveryUtil.__import_child_classes(import_location)
        child_classes_union = set()
        for parent_class in parent_class_list:
            if not child_classes_union:
                child_classes_union = set(parent_class.__subclasses__())
            else:
                child_classes_union.intersection_update(parent_class.__subclasses__())

        return list(child_classes_union)

    @staticmethod
    def __search_all_paths_at_location(module_location: str, pattern_search="*"):
        return glob.glob(path_join(module_location, pattern_search))

    @staticmethod
    def __import_child_classes(import_location):
        for item in AutoClassDiscoveryUtil.__search_all_paths_at_location(import_location):
            if isdir(item):
                AutoClassDiscoveryUtil.__import_child_classes(item)
            else:
                AutoClassDiscoveryUtil.__import_modules_for_auto_discovery(item)

    @staticmethod
    def __import_modules_for_auto_discovery(sub_module_file):
        """
        If sub_module_file is a .py file and not an package file, import the module
        @param sub_module_file:
        @return:
        """
        if isfile(sub_module_file) and AutoClassDiscoveryUtil.__is_importable_file(sub_module_file):
            item_without_file_extension = sub_module_file[:-3]
            importer_path = item_without_file_extension.replace(path_separator, import_separator)
            import_module(importer_path)

    @staticmethod
    def __get_import_location(packages_to_import_from) -> str:
        """
        Returns import string for package
        @param packages_to_import_from: module
        @return: string to import module
        """
        import_path: str = packages_to_import_from.__package__
        import_location = import_path.replace(import_separator, path_separator) + path_separator
        return import_location

    @staticmethod
    def __is_importable_file(sub_module_file):
        return sub_module_file.endswith('.py') and \
               not basename(sub_module_file) in [AutoClassDiscoveryUtil._PYCACHE_FILE,
                                                 AutoClassDiscoveryUtil._INIT_FILE]