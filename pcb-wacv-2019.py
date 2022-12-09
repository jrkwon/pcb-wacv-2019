# -----------------------------------------------------------------------------
# 12/08/2022: Created by Jaerock
# 
# Convert XML files of PCB_WACV_2019 dataset to 
# 1. remove "text" labels
# 2. remove names of components (ex. resistor R19 --> resistor)
#

import xml.etree.ElementTree as ET
import os
import shutil


class PcbWacv2019:
    component_names = [
        'resistor', 'capacitor', 'pins', 'connector', 'pads', 'ic', 
        'transistor', 'diode', 'jumper', 'led', 'button', 'switch',
        'inductor', 'switch', 'clock', 'potentiometer', 'transformer',
        'fuse', 'buzzer', 'display', 'heatsink', 'battery'
    ]

    remove_names = [ 
        'text', '"component text', 'unknown'
    ]

    replace_names = { 
        '"diode zener array"': 'diode_zener_array',
        '"resistor network"' : 'resistor_network',
        '"resistor jumper"'  : 'resistor_jumper',
        '"capacitor jumper"' : 'capacitor_jumper',
        '"emi filter"'       : 'emi_filter',
        '"test point"'       : 'test_point',
        '"ferrite bead"'     : 'ferrite_bead',
        '"zener diode"'      : 'zener_diode',
        '"electrolytic capacitor"' : 'electrolytic_capacitor'
    }

    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.xml_files = []


    def find_xml_files(self):

        for root, dirs, files in os.walk(self.root_folder):
            for file in files:
                 if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    self.xml_files.append(file_path)
        
        return self.xml_files


    def convert(self, xml_file):
        # Backup the original
        shutil.copy(xml_file, xml_file+'.org')

        tree = ET.parse(xml_file)
        root = tree.getroot()

        nodes = root.findall('.//object')
        for node in nodes:
            if not node.find('name').text:
                continue

            obj_name = node.find('name').text

            for component_name in self.component_names:
                if obj_name.startswith(component_name): 
                    node.find('name').text = node.find('name').text.split()[0]

            for text_name in self.remove_names:
                if obj_name.startswith(text_name):
                    root.remove(node)

            for key in self.replace_names:
                if obj_name.startswith(key):
                    node.find('name').text = self.replace_names[key]

        tree.write(xml_file)

    
    def convert_all(self):
        num_files = len(self.xml_files)
        if num_files == 0:
            print(f'[ERROR] No XML files found')
            return

        for i, file in enumerate(self.xml_files):
            self.convert(file)
            print(f'[INFO] Converting {file}... [{i+1}/{num_files}]')

    
if __name__ == '__main__':
    root_folder = 'data/pcb_wacv_2019-kwon'
    pcb_wacv_2019 = PcbWacv2019(root_folder)
    pcb_wacv_2019.find_xml_files()
    pcb_wacv_2019.convert_all()
