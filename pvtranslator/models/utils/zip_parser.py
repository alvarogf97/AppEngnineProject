import zipfile
from datetime import datetime
from pvtranslator.models.entities.module import Module
from pvtranslator.models.entity_managers.facade import create_campaign, create_curve


def allowed_file(filename):
    allowed_file_extension = {'zip'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_file_extension


def parse_xls(_file):
    done = False
    error_msg = ''
    campaign_name = None
    campaign_date = None
    curve_hour = None
    curve_v_values = None
    curve_i_values = None
    curve_p_values = None
    line_number = 0

    try:
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
        error_msg = str(e)

    return done, error_msg, campaign_name, campaign_date, curve_hour, curve_v_values, curve_i_values, curve_p_values


# return (code, errors):
#   code == 0 -> not complete
#   code == 1 -> complete
#   code == 2 -> complete with errors
def parse_zip(zip_file_storage, module_key):
    result_code = 1
    errors = []
    module = Module.get_by_key_name(key_names=module_key)
    campaign = None

    if not allowed_file(zip_file_storage.filename):
        return 0, ['file must be zip']

    z_files = zipfile.ZipFile(zip_file_storage.stream, 'r')

    for file_name in z_files.namelist():
        _file = z_files.open(file_name, 'rU')

        done, error_msg, campaign_name, campaign_date, curve_hour, curve_v_values, \
        curve_i_values, curve_p_values = parse_xls(_file)
        _file.close()

        if done:
            if not campaign:
                campaign = create_campaign(name=campaign_name, date=campaign_date, module=module)

            create_curve(hour=curve_hour, v_values=curve_v_values,
                         i_values=curve_i_values, p_values=curve_p_values, campaign=campaign)

        else:
            errors.append(error_msg)
            result_code = 2

    z_files.close()
    return result_code, errors
