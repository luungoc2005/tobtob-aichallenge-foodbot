import socketio

socket = socketio.Client()
if __name__ == "__main__":
    @socket.event
    def message(data):
        print('I received a message!')

    pass