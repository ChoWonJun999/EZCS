import argparse
from func import recording
from stt import STTModel

parser = argparse.ArgumentParser()
parser.add_argument("--client_id", type=str, required=True)
parser.add_argument("--client_secret", type=str, required=True)

args = parser.parse_args()

stt = STTModel(args.client_id, args.client_secret)

audio_data = recording()

output = stt.request(audio_data)

print(output)