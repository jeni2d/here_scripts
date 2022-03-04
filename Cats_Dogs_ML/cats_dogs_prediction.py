from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

def run_example():
    # load the image
    img = load_image('I_qCpW4Vonw.jpg')
    # load model
    model = load_model('final_model.h5')
    # predict the class
    result = model.predict(img)
    print(result[0])
    
# run_example()

for folders, subfolder, files in os.walk('some_dir'):
    for file in files:
        img = load_image(folders+'/'+file)
        result = model.predict(img)
        print(result[0])
        print(file)
