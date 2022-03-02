import asyncio
from scrollerbase import Scroller
from threading import Thread
from async_finance import Finance

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        scroller.interrupt(str(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '0.0.0.0', 8888)
    async with server:
        await server.serve_forever()

def run_socket_server():
    asyncio.run(main())


print("Starting finance data service")
finance = Finance()

print("Starting scroller")
scroller = Scroller()

print("Starting socket server")
thread = Thread(target=run_socket_server)
thread.daemon = True
thread.start()
if (not scroller.process()):
    scroller.print_help()