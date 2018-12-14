import logging
import zipfile
from datetime import datetime
from pvtranslator.models.entities.campaign import Campaign
from pvtranslator.models.entities.module import Module


def allowed_file(filename):
    allowed_file_extension = {'zip'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_file_extension


def parse_xls(_file):

    done = False
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
        logging.error(str(e))

    return done, campaign_name, campaign_date, curve_hour, curve_v_values, curve_i_values, curve_p_values


def parse_zip(zip_file_storage, module_key):

    module = Module.get_by_key_name(key_names=module_key)
    logging.info(module.name)

    if not allowed_file(zip_file_storage.filename):
        return False

    z_files = zipfile.ZipFile(zip_file_storage.stream, 'r')

    for file_name in z_files.namelist():
        _file = z_files.open(file_name, 'rU')

        done, campaign_name, campaign_date, curve_hour, curve_v_values, \
            curve_i_values, curve_p_values = parse_xls(_file)
        _file.close()

        if done:
            logging.info(campaign_name)
            campaign = Campaign.create_campaign(name=campaign_name, date=campaign_date, module=module)
            # TODO create curve

    z_files.close()
    return True
