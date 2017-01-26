__author__ = 'namatra'
import time
import datetime
import random, uuid
from time import sleep
import socket
import argparse
import multiprocessing
from argparse import ArgumentParser

ips=["123.221.14.56","16.180.70.237","10.182.189.79","218.193.16.244","198.122.118.164","114.214.178.92","233.192.62.103","244.157.45.12","81.73.150.239","237.43.24.118"]
referers=["-","http://www.casualcyclist.com","http://bestcyclingreviews.com/top_online_shops","http://bleater.com","http://searchengine.com"]
resources=["/handle-bars","/stems","/wheelsets","/forks","/seatposts","/saddles","/shifters","/Store/cart.jsp?productID="]
useragents=["Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36","Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1","Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25","Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201","Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0","Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))"]

#Number of messages per second
#number = 2500
#sleep_thread = 0.000223

# 10 Thread
number = 500
sleep_thread = 0.0015

def worker(process, duration):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    thread_name = socket.gethostname()+"_"+str(process)
    #unique_message_1 = thread_name+"_uni"+str(uuid.uuid4())[:6]
    f = open('/data/logs/access_log_'+timestr+'_'+str(process)+'_'+'.log','w')
    initial_time = datetime.datetime.now()

    # Execute 60 second * total cycle provided in input
    print duration
    for cycle in range(duration):
        t_end = time.time() + 60
        count = 0
        final_time = 0
        while time.time() < t_end:
            for i in xrange(0,number):
                increment = datetime.timedelta(seconds=random.randint(30,300))
                #otime += increment
                uri = random.choice(resources)
                if uri.find("Store")>0:
                    uri += `random.randint(1000,1500)`
                ip = random.choice(ips)
                useragent = random.choice(useragents)
                referer = random.choice(referers)
                sleep(sleep_thread)
                f.write('%s - %s - [%s] "GET %s HTTP/1.0" 200 %s "%s" "%s"\n' % (datetime.datetime.now(), thread_name, random.choice(ips),uri,random.randint(2000,5000),referer,useragent))
            unique_message_1 = thread_name+"_uni"+str(uuid.uuid4())[:6]
            message_time = datetime.datetime.now()
            f.write('%s - %s - [%s_%d] "GET %s HTTP/1.0" 200 %s "%s" "%s"\n' % (message_time, thread_name, unique_message_1,count, uri,random.randint(2000,5000),referer,useragent))
            count = count + 1
            final_time = datetime.datetime.now()
        print ("Source %s took  %.2f seconds and generated messgage with string %s : %d times"  % (thread_name, (final_time - initial_time).total_seconds(), thread_name+"_uni", count))

def execute_main():
    jobs = []
    for process in range(options.processes):
        p = multiprocessing.Process(target=worker, args=(process, options.time))
        jobs.append(p)
        p.start()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-p", "--processes", type=int,default=1,choices=[1,2,3,4,5,6,7,8,9,10],help="Number of processes to execute in parallell")
    parser.add_argument("-t", "--time", type=int,default=1,help="Total minutes to execute in parallell")
    options = parser.parse_args()
    execute_main()
