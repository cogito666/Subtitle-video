import os
from collections import OrderedDict


# Todo:
# 1) os.path.join
# 2) file or directory ? only text parse? or real type check? if not exist, how to check it's meta?
# 3) file exist check

def mkdir_if_not_exist(directory):
    """
    mkdir directory
    :param directory: path/to/dir

    Usage:
    dir = './Dohyeong/face_director_with_dl'
    mkdir_if_not_exist(dir)frame_extraction
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def mkdir_multiple_directories(directories):
    """
    make multiple directories

    :param directories: a dictionary whose elements are "directory alias (key)" and "path/to/dir (value)"
    """
    for directory in directories.values():
        if directory.split('.').__len__() is 1:
            mkdir_if_not_exist(directory)


def get_parent_directory(path):
    """
    get parent directory of a given path

    :param path: path/to/file-or-dir
    :return: path/to/dir of given file's parent directory
    """
    file_directory = os.path.dirname(path)

    return file_directory


def get_joined_path(dir, add):
    return os.path.join(dir, add)


def get_file_name(file):
    """

    :param file: path/to/file
    :return: path/to/file without extension
    """

    filename = os.path.basename(file)

    return filename


def get_file_name_without_extension(file):
    """

    :param file: path/to/file
    :return: path/to/file without extension
    """
    file_name = os.path.basename(file)
    file_name_without_extension = file_name.split('.')[0]

    return file_name_without_extension


def get_same_parent_directory_same_name_directory_of_file(file):
    """
    Get path/to/parent-directory-of-a-file/file-name

    :param file: path/to/file
    :return: path/to/directory
    """
    parent_directory = get_parent_directory(file)
    file_name = os.path.basename(file)
    file_name_without_extension = file_name.split('.')[0]

    same_parent_directory_same_name_directory = os.path.join(parent_directory, file_name_without_extension)

    return same_parent_directory_same_name_directory


def get_number_of_files_in_directory(directory):
    """

    :param directory: path/to/dir
    :return: number of files in a given directory
    """
    file_list = [os.path.join(directory, f) for f in os.listdir(directory)]
    number_of_files = len(file_list)

    return number_of_files


def get_directory_path_from_file_name(file, parent_directory=None):
    """
    Get path/to/directory from path/to/file

    # Data structure:
    # -- video_name.mp4
    # -- video_name -- original -- frame -- %05d.png
    #                           -- face -- %05d.png
    #                           -- mouth -- %05d.png
    #                           -- landmark -- %05d.npy
    #                           -- audio -- %05d.wav
    #                           -- mfcc -- %05d.npy
    #                           -- merged_audio.wav

    :param file: path/to/file
    :param parent_directory: path/to/directory
    :return: path/to/directory
    """
    # if data root-directory is not given, use parent-dir as root
    if parent_directory is None:
        parent_directory = get_parent_directory(file)

    # root
    root_directory = os.path.join(parent_directory, get_file_name_without_extension(file))

    # original
    original_data_directory = os.path.join(root_directory, 'original')

    # visual
    frame_directory = os.path.join(original_data_directory, 'frame')
    face_directory = os.path.join(original_data_directory, 'face')
    mouth_directory = os.path.join(original_data_directory, 'mouth')
    openface_directory = os.path.join(original_data_directory, 'openface')
    landmark_directory = os.path.join(original_data_directory, 'landmark')

    # audio
    audio_directory = os.path.join(original_data_directory, 'audio')
    mfcc_directory = os.path.join(original_data_directory, 'mfcc')
    audio_file = os.path.join(original_data_directory, 'merged_audio.wav')

    directory_dict = OrderedDict([
        ('root', root_directory),

        ('original', original_data_directory),

        ('frame', frame_directory),
        ('face', face_directory),
        ('mouth', mouth_directory),
        ('openface', openface_directory),
        ('landmark', landmark_directory),

        ('audio', audio_directory),
        ('mfcc', mfcc_directory),
        ('audio_file', audio_file),
    ])

    return directory_dict
