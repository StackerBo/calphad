from tc_python import *

class SystemManager:
    """
    This class is used to manage the Thermo-calc system.
    """
    
    def __init__(self, database, elements):
        self.database = database
        self.elements = elements
        
    def create_system(self):
        """
        This function creates a new system in Thermo-calc.
        """
        with TCPython() as session:
            system = (session
                      .select_database_and_elements(self.database, self.elements)
                      .get_system())
        return system