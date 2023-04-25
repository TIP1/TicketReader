import pytest
from job_task.utils import Utils

PATTERN_FILE = '../files/abstract_reference_file.pdf'


class TestFileQuality:

    #тест на корректную работу функции, получения расположения элементов
    def test_get_elements_positions_function(self):

        reference_file = Utils.get_elements_positions(PATTERN_FILE)
        testing_file = Utils.get_elements_positions('../files/abstract_reference_file.pdf')

        assert reference_file == testing_file, '\n\n!!! Something wrong with function or files !!!\n\n'
        print('\nPositions of elements was got correct! Function works well!')

    def test_file_elements_placements_wrong(self):
        reference_file = Utils.get_elements_positions(PATTERN_FILE)
        testing_file = Utils.get_elements_positions('../files/test_task_damaged.pdf')

        with pytest.raises(AssertionError):
            assert reference_file == testing_file, '\n\n!!! File accepted, but should not !!!\n\n'
        print('\nFile with wrong elements placements did\'t accepted!')

    def test_file_with_different_values(self):
        reference_file = Utils.get_elements_positions(PATTERN_FILE, include_fields=True)
        testing_file = Utils.get_elements_positions('../files/test_task_another_values.pdf', include_fields=True)

        assert reference_file == testing_file, '\n\n!!! File with different values in field must be accepted !!!\n\n'
        print('\nFile with different values in fields was accepted!')

    def test_file_with_wrong_fields(self):
        reference_file = Utils.get_elements_positions(PATTERN_FILE, include_fields=True)
        testing_file = Utils.get_elements_positions('../files/test_task_wrong_fields.pdf', include_fields=True)

        with pytest.raises(AssertionError):
            assert reference_file == testing_file, '\n\n!!! File accepted, but should not, due to incorrect fields name !!!\n\n'
        print('\nFile with wrong fields name did\'t accepted!')