import queue
from flask import Flask, Response, request, jsonify, render_template
from queue import Queue
import time
import datetime
import json

app = Flask(__name__)

# 進捗パーセンテージ用キュー
queue = Queue()

# プログレスバーストリーム


@app.route('/stream')
def stream():
    return Response(event_stream(queue), mimetype='text/event-stream')

# Queueの値を取り出してEventSourceの'progress-item'に出力（100だったら'last-item'イベントに出力）


def event_stream(queue):
    while True:
        persent = queue.get(True)
        print("progress：{}%".format(persent))
        sse_event = 'progress-item'
        if persent == 100:
            sse_event = 'last-item'
        yield "event:{event}\ndata:{data}\n\n".format(event=sse_event, data=persent)


# トップページ
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/ajax", methods=['POST'])
def ajax():
    if request.method == 'POST':
        start = str(datetime.datetime.now())
        print("-------------- {} --------------".format(request.form['data']))
        """
        処理runner_01が終わったら10％まで進行としてキューに追加
        runner_01()
        queue.put(10)
 
        処理runner_02が終わったら20％まで進行としてキューに追加
        runner_02()
        queue.put(20)
        ・・・
        """

        # サンプル用ループ処理（2秒ごとに10パーセントづつ進行）
        for i in range(10, 110, 10):
            queue.put(i)
            time.sleep(3)

        end = str(datetime.datetime.now())
        result = {"start": start, "end": end}
        return jsonify(json.dumps(result))


if __name__ == '__main__':
    app.run(port=5000)
