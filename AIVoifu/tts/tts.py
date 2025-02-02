import os
import json
from scipy.io import wavfile
import numpy as np

# write your own tts class and place it in this folder
# model weight will be downloaded and save at tts_base_model
class khanomtal11:
    def __init__(self) -> None:
        from TTS.api import TTS
        root = os.path.dirname(os.path.abspath(__file__))            
        # change config.json to match your model
        json_path = os.path.join(root, 'config.json')
        configs = json.load(open(json_path, 'r'))
        configs['speakers_file'] = os.path.join(root, 'speakers.pth')
        configs['language_ids_file'] = os.path.join(root, 'language_ids.json')
        configs['model_args']['speakers_file'] = os.path.join(root, 'speakers.pth')
        configs['model_args']['speaker_ids_file'] = os.path.join(root, 'speaker_ids.json')
        configs['model_args']['speaker_encoder_config_path'] = os.path.join(root, 'config_se.json')
        configs['model_args']['speaker_encoder_model_path'] = os.path.join(root, 'model_se.pth')
        self.sr = configs['audio']["sample_rate"]
        # save the new config
        json.dump(configs, open(json_path.replace('config', 'nconfig'), 'w'), indent=4)

        self.model = TTS(model_path=os.path.join(root, 'best_model.pth'), config_path=os.path.join(root, 'nconfig.json'), progress_bar=False, gpu=False)
        self.model.model_name = 'khanomtal11'

    def tts(self, text, out_path, speaker=0, language=3):
        self.model.tts_to_file(text=text, file_path=out_path, speaker=self.model.speakers[speaker], language=self.model.languages[language])

class OpenJtalk:
    def __init__(self) -> None:
        import pyopenjtalk
        self.model_name = 'openjtalk'
        self.sr = 48000
        self.model = pyopenjtalk
    def tts(self, text, out_path):

        wav, sr = self.model.tts(text)
        wavfile.write(out_path, sr, wav.astype(np.int16))