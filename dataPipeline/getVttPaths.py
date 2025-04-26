from pathlib import Path

def getVttPaths():
    data_path = 'data/rawData'
    data_folder = Path(data_path)
    vtt_paths_objs = list(data_folder.rglob('*.en.vtt'))
    vtt_paths_strs = [str(path) for path in vtt_paths_objs]
    return vtt_paths_strs
