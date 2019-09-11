from moviepy import editor
from utils import *
import numpy as np
from synchronization_path import *
import cv2


def get_fps(video):
    return cv2.VideoCapture(video).get(cv2.CAP_PROP_FPS)


def annotate(clip, txt, txt_color='white', fontsize=100, font='Xolonium-Bold', text_position=('center', 900)):
    """ Writes a text at the bottom of the clip. """
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=font, color=txt_color)
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(text_position)])
    return cvc.set_duration(clip.duration)


def set_subtitle(input_video_file, output_video_file, subs):
    video = editor.VideoFileClip(input_video_file)

    # save subtitle meta
    subtitle_meta_npy = get_joined_path(get_parent_directory(input_video_file),
                                        get_file_name_without_extension(input_video_file) + '_subtitle_meta' + '.npy')

    subtitle_meta_data = np.array(subs)
    np.save(subtitle_meta_npy, subtitle_meta_data)

    annotated_clips = [annotate(video.subclip(from_t, to_t), txt) for (from_t, to_t), txt in subs]

    # concatenate
    final_clip = editor.concatenate_videoclips(annotated_clips)
    final_clip.write_videofile(output_video_file)


def synchronize_subtitle(ref_video_subtitle_meta_npy, ref_video_fps, tgt_video_fps, cost_matrix_npy):
    ref_video_subtitle_meta = np.load(ref_video_subtitle_meta_npy, allow_pickle=True)
    cost_matrix = np.load(cost_matrix_npy)

    # compute synchronization path (Dynamic Programming)
    tar_path, ref_path, _, _ = dp(cost_matrix)
    smoothed_target_path, smoothed_ref_path = smoothing_curve(tar_path, ref_path)

    # tgt_subs
    tgt_subs = []

    # parse clip time stamps
    for ((ref_clip_start_time, ref_clip_end_time), text) in ref_video_subtitle_meta:
        # mapping (frame index): timestamp to frame index <- fps needed
        ref_clip_start_frame_idx = int(ref_video_fps * ref_clip_start_time)
        ref_clip_end_frame_idx = int(ref_video_fps * ref_clip_end_time)

        # frame mapping
        tgt_clip_start_frame_idx = np.where(smoothed_ref_path == ref_clip_start_frame_idx)[0][0]
        tgt_clip_end_frame_idx = np.where(smoothed_ref_path == ref_clip_end_frame_idx)[0][0]

        tgt_clip_start_time = smoothed_target_path[tgt_clip_start_frame_idx] / tgt_video_fps
        tgt_clip_end_time = smoothed_target_path[tgt_clip_end_frame_idx] / tgt_video_fps

        # tgt_subs append
        tgt_current_clip_sub = ((tgt_clip_start_time, tgt_clip_end_time), text)
        tgt_subs.append(tgt_current_clip_sub)

    return tgt_subs


if __name__ == '__main__':
    # # Todo: set subtitle of a video
    # # input, output video file name
    # input_video_file = '/home/dohyeong/Documents/Subtitle_Change/Video/DH_happy_slow_fast.mp4'
    # output_video_file = '/home/dohyeong/Documents/Subtitle_Change/Video/test_result/test.mp4'
    #
    # # subtitle clip setting
    # # empty subtitle: ' ' not ''
    # # basically, all clips are continuous. Start time of a clip corresponds to the end time of the previous clip.
    # subs = [((0, 1.3), ' '),
    #         ((1.3, 3.6), 'Whoever it was'),
    #         ((3.6, 4), ' '),
    #         ((4, 7.5), 'He or she would always say'),
    #         ((7.5, 8.3), ' '),
    #         ((8.3, 9.5), 'That is a hat')]
    #
    # set_subtitle(input_video_file, output_video_file, subs)

    # # Todo: synchronize subtitle (reference to target)
    ref_video = '/home/dohyeong/Documents/Subtitle_Change/Video/DH_happy_slow_fast.mp4'
    tgt_video = '/home/dohyeong/Documents/Subtitle_Change/Video/YJ_happy_2.mp4'

    ref_video_subtitle_meta_npy = '/home/dohyeong/Documents/Subtitle_Change/Video/DH_happy_slow_fast_subtitle_meta.npy'
    cost_matrix_npy = '/home/dohyeong/Documents/Subtitle_Change/Video/cost_matrix.mp4.npy'

    ref_video_fps = get_fps(ref_video)
    tgt_video_fps = get_fps(tgt_video)

    tgt_subs = synchronize_subtitle(ref_video_subtitle_meta_npy, ref_video_fps, tgt_video_fps, cost_matrix_npy)
    print(tgt_subs)
    # exit()
    # tgt video set subtitles
    tgt_input = tgt_video
    tgt_output = get_joined_path(get_parent_directory(tgt_input),
                                 get_file_name_without_extension(tgt_input) + '_with_synced_sub.mp4')
    set_subtitle(tgt_input, tgt_output, tgt_subs)
