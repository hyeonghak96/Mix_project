import paho.mqtt.client as mqtt

def subscribe(host, topic, on_message, forever=True):
    # print(topic)
    def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        if rc == 0:
            client.subscribe(topic) # 연결 선공시 토픽 구독 신청
        else:
            print('연결 실패: ', rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host)
    if forever:
        client.loop_forever()   # 현재 스레드에서 무한 루프를 돌며 메세지 처리
    else:
        client.loop_start()     # 새로운 스레드를 기동하고, 스레드가 무한 루프에서 메세지 처리