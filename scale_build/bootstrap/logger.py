from scale_build.utils.logger import get_logger as _get_logger


def get_log_file_name(bootstrap_dir_type, logger_file):
    if logger_file:
        return logger_file
    elif bootstrap_dir_type == 'cdrom':
        return 'cdrom-bootstrap.log'
    else:
        return 'bootstrap_chroot.log'


def get_logger(bootstrap_dir_type, mode='a+', logger_file=None):
    return _get_logger(f'bootstrap_dir_{bootstrap_dir_type}', get_log_file_name(bootstrap_dir_type, logger_file), mode)