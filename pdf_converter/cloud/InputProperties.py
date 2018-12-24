import os.path
import inspect
import xml.etree.ElementTree
from . import EasyPDFCloudAPIExceptions


class ImportProperties:
    def __init__(self):
        self.__data__ = []

    def load_properties(self):
        print("Loading data from Properties.xml...")
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        tree = xml.etree.ElementTree.parse(os.path.join(path, "Properties.xml"))
        root = tree.getroot()

        data1 = []
        for i in range(0, len(root)):
            data1.append(root[i].text)
        data2 = []
        for elem in tree.findall("entry"):
            data2.append(elem.get("key"))

        if not len(data1) == len(data2):
            raise EasyPDFCloudAPIExceptions.EasyPDFCloudArgException()

        for i in range(0, len(data2)):
            self.__data__.append([data2[i], data1[i]])
            if data1[i] == "" and data2[i] is not "WorkflowName":
                raise EasyPDFCloudAPIExceptions.EasyPDFCloudArgException(data2[i])

    def get_client_id(self):
        return self.__get_element__("ClientID")

    def get_client_secret(self):
        return self.__get_element__("ClientSecret")

    def get_workflow_id(self):
        return self.__get_element__("WorkflowID")

    def get_input_directory(self):
        return self.__get_element__("InputPath")

    def get_output_directory(self):
        return self.__get_element__("OutputPath")

    def get_file_name(self):
        return self.__get_element__("FileName")

    def __get_element__(self, key):
        for i in range(0, len(self.__data__)):
            if self.__data__[i][0] == key:
                return self.__data__[i][1]
        raise EasyPDFCloudAPIExceptions.EasyPDFCloudArgException(key)
