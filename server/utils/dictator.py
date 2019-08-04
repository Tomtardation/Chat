import asyncio
from concurrent.futures import TimeoutError, ThreadPoolExecutor


class Slave:
    def __init__(self, tasks, loop, id):
        self.tasks = tasks
        self.loop = loop
        self.id = id


    def execute(self):
        try:
            main_task = asyncio.gather(self.tasks, loop=self.loop,return_exceptions=True)
        except:
            print("Failed")
        else:
            return self.loop.create_task(main_task)


class Dictator:
    def __init__(self, loop):
        self.loop = loop
        self.count = 0
        self.queue = []
        self.slaves = {}
        self.threads = ThreadPoolExecutor(max_workers=5)

    
    async def main(self):
        while True:
            while len(queue) == 0:
                asyncio.sleep(1, loop=self.loop)
            
            while len(tasks) < 4 or len(queue) == 0:
                tasks = self.queue if len(self.queue) <= 5 else self.queue[:5]
                try:
                    loop = asyncio.new_event_loop()
                    # TODO: thread-safe this
                    self.count += 1
                    slave = Slave(tasks, loop, self.count)
                    slaves[self.count] = slave
                finally:
                    if loop is not None:
                        loop.close()
            
            with ThreadPoolExecutor() as executor:
                fn = partial(self.__run__, slave)
                executor.map(fn)
    
    
    async def __run__(self, slave):
        print("Executing slave #{}".format(slave.id))
        result = await slave.execute()
        del self.slaves[slave.id]
        return result

