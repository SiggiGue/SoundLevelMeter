import tornado.ioloop
import tornado.web
import tornado.websocket
import webbrowser

from tornado.options import define, options, parse_command_line

from pysoundcard import Stream, continue_flag
import numpy as np


sample_rate = 44100
block_length = 2048
tau = 0.1

global level, psc_stream
level = -120
alpha = np.exp(-1.0/(tau*(sample_rate/block_length)))
b0 = 1 - alpha
a1 = -alpha

define("port", default=8888, help='run on the given port', type=int)

def callback(in_data, frame_count, time_info, status):
    global level, send_message
    new_value = b0*np.mean(in_data**2)  - a1*10**(level*0.1)
    level = 10*np.log10(new_value)
    send_message('{:.1f}'.format(level))
    return in_data, continue_flag

psc_stream = Stream(callback=callback,
                    sample_rate=sample_rate,
                    block_length=block_length,
                    output_device=False)

class SlmWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        self.start_stream()

    def on_message(self, message):

        if '#start#' in message:
            print('start')
            self.start_stream()

        if '#stop#' in message:
            print('stop')
            self.stop_stream()

    def on_close(self):
        print("Websocket is closed")

    def start_stream(self):
        global psc_stream, send_message
        send_message = self.write_message
        if not psc_stream.is_active():
            print('Start stream')
            psc_stream.start()

    def stop_stream(self):
        global psc_stream
        if psc_stream.is_active():
            print('Stop stream')
            psc_stream.stop()

app = tornado.web.Application([(r'/', SlmWebSocket),])

if __name__=='__main__':
    parse_command_line()
    app.listen(options.port)
    webbrowser.open_new_tab('slm.html')
    tornado.ioloop.IOLoop.instance().start()
