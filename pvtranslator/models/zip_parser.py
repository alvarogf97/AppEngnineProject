import warnings
import zipfile
from datetime import datetime
from os import listdir
from os.path import isfile, join

temporary_dir = '/temp'


def parse_xls(filepath):

    done = False
    campaign_name = None
    campaign_date = None
    curve_hour = None
    curve_v_values = None
    curve_i_values = None
    curve_p_values = None
    line_number = 0

    try:
        with open(filepath, "r") as _file:
            curve_v_values = []
            curve_i_values = []
            curve_p_values = []
            _buffer = _file.readline()
            while _buffer:
                if line_number == 1:
                    buffer_split = _buffer.split(':')
                    campaign_name = buffer_split[1].replace('\t', '').replace('\n', '')
                if line_number == 2:
                    buffer_split = _buffer.split(':')
                    campaign_date = buffer_split[1].replace('\t', '').replace('\n', '')
                    campaign_date = datetime.strptime(campaign_date, '%d/%m/%Y').date()
                if line_number == 3:
                    buffer_split = _buffer.split(':')
                    curve_hour = (":".join(buffer_split[1:])).replace('\t', '').replace('\n', '')
                if line_number > 35:
                    buffer_split = _buffer.replace(',', '.').split()
                    curve_v_values.append(float(buffer_split[1]))
                    curve_i_values.append(float(buffer_split[2]))
                    curve_p_values.append(float(buffer_split[3]))
                line_number += 1
                _buffer = _file.readline()
            done = True
    except Exception as e:
        warnings.warn(str(e))

    return done, campaign_name, campaign_date, curve_hour, curve_v_values, curve_i_values, curve_p_values


def parse_zip(file_path):
    z_files = zipfile.ZipFile(file_path)
    z_files.extractall(temporary_dir)
    files = [f for f in listdir(temporary_dir) if isfile(join(temporary_dir, f))]

    for _file in files:

        done, campaign_name, campaign_date, curve_hour, curve_v_values, \
            curve_i_values, curve_p_values = parse_xls(temporary_dir+"/"+_file)

        if done:
            # create elements
            pass