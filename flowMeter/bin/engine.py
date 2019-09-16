from flowMeter.bin.func import *

class engines():
    def __init__(self, flow_work = 0, cumulate_work = 0, pressure=101.325 , temperature=20.00):
        self.flow_work = flow_work
        self.flow_standard = 0

        self.cumulate_work = cumulate_work
        self.cumulate_standard = self.cumulate_work

        self.pressure = pressure
        self.temperature = temperature
        self.modulus = self.modulus_temp_pressure()

    def run(self):
        while True:
            t_init = time.time()
            self.creat_temp_pressure()
            self.creat_flow()
            time.sleep(0.1)
            self.creat_cumulate(time.time()-t_init)

    def get_data(self, lock = None):
        if lock:
            with lock:
                return {
                    'flow_work' : round(self.flow_work,5),
                    'flow_standard': round(self.flow_standard,5),

                    'cumulate_work': round(self.cumulate_work,5),
                    'cumulate_standard': round(self.cumulate_standard,5),

                    'pressure': round(self.pressure,5),
                    'temperature': round(self.temperature,5),
                }
        else:
            return {
                    'flow_work' : round(self.flow_work,5),
                    'flow_standard': round(self.flow_standard,5),

                    'cumulate_work': round(self.cumulate_work,5),
                    'cumulate_standard': round(self.cumulate_standard,5),

                    'pressure': round(self.pressure,5),
                    'temperature': round(self.temperature,5),
                }

    def creat_temp_pressure(self):
        self.pressure += self.fluctuation(n=2)
        self.temperature += self.fluctuation(n=2)
        self.modulus = self.modulus_temp_pressure()

    def creat_flow(self):
        self.flow_work += self.fluctuation(ranges=(0., 1, 6))
        self.flow_standard = self.flow_work * self.modulus

    def creat_cumulate(self, t):
        t = round(float(t/3600),10)
        self.cumulate_work += self.flow_work * t
        self.cumulate_standard = self.flow_work * t * self.modulus

    def modulus_temp_pressure(self):
        stemp = 29315/(27315 + self.temperature * 100)
        spres = self.pressure*1000/101325
        res = stemp * spres
        return res

    def fluctuation(self, n=1, ranges=None):
        #流量波动 ranges = (0.00001,1,5)
        s = 1
        if random.randint(1,100) < 50:
            s = -1
        if ranges:
            return s * self.ranges(ranges)
        tn = 10**n
        res = s * round(float(random.randint(1,tn)/tn),n)
        return res

    def ranges(self, data):
        #data = (0.00001,1,5)
        if isinstance(data, tuple) and len(data) == 3:
            n = data[-1]
            n1 = int(round(data[0], n) * 10 ** n)
            n2 = int(round(data[1], n) * 10 ** n)
            if n1 > n2:
                n1,n2=n2,n1
            x = random.choice(range(n1,n2))
            return round(float(x/(10**n)), n)
        else:
            return False

    def set_cumulate_work(self,cumulate):
        self.cumulate_work = cumulate

    def set_cumulate_standard(self, standard):
        self.cumulate_standard = standard

    def set_flow_work(self, flow):
        self.flow_work = flow

    def set_flow_standard(self, flow):
        self.flow_standard = flow

    def set_pressure(self, pressure):
        #压力设置，压力范围30-120
        if pressure > 120:
            pressure = 120
        elif pressure < 30:
            pressure = 30
        self.pressure = pressure
        return True

    def set_temperature(self, temperature):
        #温度设置，温度范围-40 — 80
        if temperature > 80:
            temperature = 80
        elif temperature < -40:
            temperature = -40
        self.pressure = temperature
        return True



if __name__ =='__main__':
    locks = threading.Lock()
    a = engines(flow_work=10,cumulate_work=10,)
    p = threading.Thread(target=a.run,args=())
    p.start()
    for i in range(10):
        print(a.get_data(locks))
        time.sleep(random.randint(1,30)/10)


