import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import subprocess
import os
import configparser

cfg = configparser.ConfigParser()
cfg.read("bot.ini")

searx_instance = cfg.get("Main", "searx_instance")
group_id = cfg.getint("Main", "group_id")
group_token = cfg.get("Main", "group_token")
my_id = None
try:
    my_id = cfg.getint("Main", "my_id")
except Exception as e:
    print(str(e) + " - operating in public mode (NOT RECOMMENDED)")
    my_id = None

def save_webpage(url):
    if url.find(" ") > 0 or url.find(".") == -1:
        url = searx_instance + "/search?q=" + url.replace(" ", "+")
    if url.find("https://") == -1 and url.find("http://") == -1:
        url = "https://" + url
    print("Saving webpage at: " + url)
    file = "cache/" + url.replace("https://", "").replace("/", "-").replace(":", "-").replace(".", "-").replace("https---", "") + ".map"
    if os.path.exists(file):
        os.remove(file)
        print("Removed .map")
    if os.path.exists(file + ".gz"):
        os.remove(file + ".gz")
        print("Removed .map.gz")
    subprocess.run(["./single-file", url, file])
    print("Saved")
    subprocess.run(["gzip", file])
    if os.path.exists(file + ".gz"):
        return file + ".gz"
    return file

def main():
    

    
    vk_session = vk_api.VkApi(token=group_token)
    vk = vk_session.get_api()


    longpoll = VkBotLongPoll(vk_session, group_id)
    upload = vk_api.VkUpload(vk_session)
    while True:
        try:
            print("Waiting for requests")

            for event in longpoll.listen():

                if event.type == VkBotEventType.MESSAGE_NEW:
                    print(event)
                    print(event.obj)
                    print(event.obj.message)

                    print('Новое сообщение:')

                    print('Для меня от: ', end='')

                    print(event.obj.message["from_id"])
                    vk.messages.send(
                        peer_id = event.obj.message["peer_id"],
                        random_id = 0,
                        message="Downloading webpage..."
                    )

                    if my_id == None or event.obj.message["peer_id"] == my_id:

                        try:
                            print('Текст:', event.obj.message["text"])
                            document = upload.document_message(save_webpage(event.obj.message["text"]), title="Webpage", peer_id=event.obj.message["peer_id"])
                            print(document)
                            
                            vk.messages.send(
                                peer_id = event.obj.message["peer_id"],
                                random_id = 0,
                                attachment = "doc" + str(document["doc"]["owner_id"]) + "_" + str(document["doc"]["id"])
                            )
                        except Exception as e:
                            print(e)
                            vk.messages.send(
                                peer_id = event.obj.message["peer_id"],
                                random_id = 0,
                                message=str(e)
                            )
                    else:
                        print("Not the owner; ignoring")
                    

                """    
                elif event.type == VkBotEventType.MESSAGE_REPLY:
                    print('Новое сообщение:')

                    print('От меня для: ', end='')

                    print(event.obj.message["peer_id"])

                    print('Текст:', event.obj.message["text"])
                """

                print()
        except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
