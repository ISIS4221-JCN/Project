from utils import Utils

utils = Utils('/media/juan/Juan/NLP/', num_workers=10)
print('Starting...')
datos = utils.data_loader('en', 'tweets', 1000)

print(len(datos))
