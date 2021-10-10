import json
import os
import asyncio
import websockets
import concurrent.futures
import logging

from libs.ukr.init_model import get_ukr_model


def process_chunk(rec, message):
    if message == '{"eof" : 1}':
        return rec.FinalResult(), True
    elif rec.AcceptWaveform(message):
        return rec.Result(), False
    else:
        return rec.PartialResult(), False


async def recognize(websocket, path):
    global args
    global loop
    global pool
    global recognizer

    logging.info('Connection from %s', websocket.remote_address)

    while True:

        message = await websocket.recv()

        # Load configuration if provided
        if isinstance(message, str) and 'config' in message:
            jobj = json.loads(message)['config']
            logging.info("Config %s", jobj)
            if 'sample_rate' in jobj:
                sample_rate = float(jobj['sample_rate'])
            continue

        response, stop = await loop.run_in_executor(pool, process_chunk, recognizer, message)

        await websocket.send(response)

        if stop:
            break


def start():
    global args
    global loop
    global pool
    global recognizer

    # Enable logging if needed
    #
    # logger = logging.getLogger('websockets')
    # logger.setLevel(logging.INFO)
    # logger.addHandler(logging.StreamHandler())
    logging.basicConfig(level=logging.INFO)

    args = type('', (), {})()

    args.interface = os.environ.get('VOSK_SERVER_INTERFACE', '0.0.0.0')
    args.port = int(os.environ.get('VOSK_SERVER_PORT', 2700))
    args.sample_rate = float(os.environ.get('VOSK_SAMPLE_RATE', 8000))

    # Gpu part, uncomment if vosk-api has gpu support
    #
    # from vosk import GpuInit, GpuInstantiate
    # GpuInit()
    # def thread_init():
    #     GpuInstantiate()
    # pool = concurrent.futures.ThreadPoolExecutor(initializer=thread_init)

    # Create the recognizer
    recognizer = get_ukr_model(args.sample_rate)
    recognizer.SetWords(True)

    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))
    loop = asyncio.get_event_loop()

    start_server = websockets.serve(recognize, args.interface, args.port)

    logging.info("Listening on %s:%d", args.interface, args.port)
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == '__main__':
    start()
