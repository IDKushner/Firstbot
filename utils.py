from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from telegram import ReplyKeyboardMarkup
from random import choice
from emoji import emojize
import Settings

def main_keyboard():
    return ReplyKeyboardMarkup([['Котик!']])

def get_smile(user_data): # функция присваивает пользователю случайный смайлик из списка и потом возвращает только его (до перезапуска бота)
    if 'emoji' not in user_data: # user_data это встроенный словарь с информацией о юзере, который обновляется при перезапуске бота
        smile = choice(Settings.USER_EMOJI)
        return emojize(smile, language='alias') # language='alias' позволяет называть смайлики по текстовому псевдониму с двоеточием
    return user_data['emoji']

def has_object_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {Settings.CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
		# 'rb': т.к. у нас картинка, открывать её для чтения надо в бинарном виде
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)
    
    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    return check_responce_for_object(response, object_name)

def check_responce_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.85:
                return True
    else:
        print(f"Ошибка распознавания: {response.outputs[0].status.details}")

    return False

# if __name__ == '__main__':
#     print(has_object_on_image('images/Cat1.jpg', 'cat'))
#     print(has_object_on_image('images/doge.jpg', 'dog'))