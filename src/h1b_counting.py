# This code is originally written by Amin Ghiasi
# Email: amin.ghiasi@gmail.com
# Date: October 2018

import os
import sys


class FeatureNotFoundError(Exception):
    pass


class Feature:

    """This class represents the features in the input files header. For this exercise,
     we are only interested in occupations and states. However, it can be any feature we want"""

    def __init__(self, feature_type):
        self.feature_type = feature_type
        self.feature_instances = {}
        self.total_num_of_certified_applications = 0

    def call_add_application_method(self, featureinstance_name):
        """This method checks if the current FeatureInstance.name exists, and if not creates it before
         calling 'add_application' method"""
        if not featureinstance_name:
            return
        self.total_num_of_certified_applications += 1
        try:
            self.feature_instances[featureinstance_name].add_application()
        except Exception:
            self.feature_instances[featureinstance_name] = Feature.FeatureInstance(featureinstance_name)

    def write_output(self, number_of_top_instances_to_print):
        file_path = os.path.join(os.path.dirname(__file__), '../output/top_10_{}.txt'.
                                 format(self.feature_type.replace(' ', '_').lower()))
        try:
            with open(file_path, 'w') as output_file:
                output_file.write('TOP_{};NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'.
                                  format(self.feature_type.replace(' ', '_').upper()))
                line_number = 1
                for key, value in sorted(self.feature_instances.items(), key=lambda x: x[1]):
                    if line_number > number_of_top_instances_to_print:
                        break
                    ratio = -1
                    if self.total_num_of_certified_applications:
                        ratio = round(100 * float(value.num_of_certified_applications) /\
                                      float(self.total_num_of_certified_applications), 1)
                    output_file.write('{};{};{}%\n'.format(value.name, value.num_of_certified_applications, ratio))
                    line_number += 1
        except FileNotFoundError:
            sys.exit('Cannot open file {} for writing the output! Running the code is terminated.'.format(file_path))

    class FeatureInstance:
        """The inner class of the class 'Feature'. If Feature.type = 'STATES', FeatureInstance.name can be 'CA', 'FL',
         'NY', 'MD', 'TX', etc; Or if Feature.type = 'OCCUPATIONS', FeatureInstance.name can be 'software engineer',
          'accountant', 'doctor' and so on"""

        def __init__(self, name):
            self.num_of_certified_applications = 1
            self.name = name

        def add_application(self):
            self.num_of_certified_applications += 1

        def __gt__(self, other):
            """This method defines greater operator (>) to be used in sorting. Sorting is done according to
            'num_of_certified_applications' and 'name' respectively"""
            if other.num_of_certified_applications > self.num_of_certified_applications:
                return True
            elif other.num_of_certified_applications < self.num_of_certified_applications:
                return False
            elif other.name < self.name:
                return True
            else:
                return False


def find_feature_titles_in_file(feature_index, feature_names, file):

    """This function finds which feature titles (among the ones given by the user in dictionary feature_names)
    is used in a file. If any feature is not found, the run will be terminated.
    The function returns a dictionary with feature title (i.e. SOC_NAME) as key and feature name (e.g. OCCUPATIONS)
    as value"""

    dict_of_features_in_this_file = {}
    for feature_name, feature_titles in feature_names.items():
        try:
            features_found = [feature for feature in feature_titles if feature in feature_index]
            if len(features_found) == 1:
                dict_of_features_in_this_file[feature_name] = features_found[0]
            else:
                raise FeatureNotFoundError

        except FeatureNotFoundError:
                sys.exit(
                    'ERROR: Finding zero or more than one occurrence of feature {} in the header of input file'
                    'file {}! Please check variable feature_names in the function main().'
                    'Running the code is terminated.'.format(feature_titles, file))
    return dict_of_features_in_this_file


def read_inputs(file, features_dict, feature_names):

    """This function reads the input file and calls method call_add_application_method() to store total
    number of certified applicants and number of certified applicants in every featureinstance"""

    file_path = os.path.join(os.path.dirname(__file__), '../input/'+file)
    with open(file_path, 'r') as input_file:
        feature_index = {feature: index for index, feature in enumerate(input_file.readline().split(';'))}
        dict_of_features_in_this_file = find_feature_titles_in_file(feature_index, feature_names, file)
        # reading the file line by line
        try:
            for line in input_file:
                list_of_values = line.split(';')
                if list_of_values[feature_index[dict_of_features_in_this_file['STATUS']]].replace('"', '') != \
                        'CERTIFIED':
                    continue
                for feature_name, feature_title in dict_of_features_in_this_file.items():
                    if feature_name != 'STATUS':
                        feature_value = list_of_values[feature_index[feature_title]].replace('"', '')
                        features_dict[feature_name].call_add_application_method(feature_value)
        except IndexError:
            sys.exit('Input file {} is broken. Running the code is terminated.'.format(file))


def main():

    # Inputs that user can change
    TOP_K_TO_PRINT = 10

    feature_names = {'STATUS': {'STATUS', 'CASE_STATUS'}}
    # Features (fields) for which the top-k are to be computed.
    # Example: To have top-k for cities as well as State and Occupation name, add this line:
    # feature_names['CITIES'] = {'LCA_CASE_WORKLOC2_CITY', 'WORKSITE_CITY'}
    feature_names['OCCUPATIONS'] = {'LCA_CASE_SOC_NAME', 'SOC_NAME'}
    feature_names['STATES'] = {'LCA_CASE_EMPLOYER_STATE', 'WORKSITE_STATE'}
    # End of what user can change

    features_dict = {feature_name: Feature(feature_name) for feature_name in feature_names}
    try:
        if os.listdir(os.path.join(os.path.dirname(__file__), '../input')):
            # Running function read_inputs() on every input file in directory ../input
            for file in os.listdir(os.path.join(os.path.dirname(__file__), '../input')):
                print('Reading data from file {} ...'.format(file), end = '')
                read_inputs(file, features_dict, feature_names)
                print ('Done!')
            # Printing the output
            del features_dict['STATUS']
            for feature in features_dict.values():
                    feature.write_output(TOP_K_TO_PRINT)
        else:
            raise FileNotFoundError

    except FileNotFoundError:
        sys.exit('ERROR: No input file found! Running the code is terminated.')


if __name__ == '__main__':
    main()