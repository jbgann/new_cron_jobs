from subprocess import Popen, PIPE
import os
import struct
import datetime
import fcntl
from time import sleep

MAX_FILE_SIZE = 500

class Command(object):
    def __init__(self,command,timeout="10s"):
        self.command = command
        wrappedCommand = "timeout -k 20 "+timeout+" "+self.command
        process = Popen(wrappedCommand,shell=True,stdout=PIPE,stderr=PIPE)

        self.output,self.err = process.communicate()
        self.timedout = process.returncode == 124 or process.returncode == 137
        self.success = not process.returncode

class LogFile(file):
    def __init__(self,path,mode,*args):
        if not os.path.isfile(path):
            with open(path,"w") as f:
                print "writing metadata"
                f.write(struct.pack("I",12))
                f.write(struct.pack("I",12))
                f.write(struct.pack("I",args[0])) #args[0] is the max_size
                f.flush()
                self.max_size = args[0]
        else:
            with open(path,"r") as f:
                f.seek(8)
                self.max_size = struct.unpack("I",f.read(4))[0]
        file.__init__(self,path,mode)


    def read(self,bytes):
        if self.tell() + bytes > self.max_size:
            front_split_size = self.max_size - self.tell()
            back_split_size = (self.tell() + bytes) - self.max_size
            front_split = file.read(self,front_split_size)
            self.seek(12)
            back_split = file.read(self,back_split_size)
            return front_split + back_split
        else:
            return file.read(self,bytes)

    def write(self,string):
        print self.tell()
        if self.tell() + len(string) > self.max_size:
            front_split_size = self.max_size - self.tell()
            back_split_size = (self.tell() + len(string)) - self.max_size
            front_split = string[:front_split_size]
            back_split = string[-back_split_size:]
            print "Back split size: %d" % (back_split_size,)
            print "front split size: %d" % (front_split_size,)
            file.write(self,front_split)
            self.seek(12)
            file.write(self,back_split)
        else:
            file.write(self,string)

class Logger:
    def __init__(self, logpath, mode):
        if not os.path.isfile(logpath):
            LogFile(logpath,"r",MAX_FILE_SIZE).close()
        self.logpath = logpath

    def get_timestamp(self):
        fmt = "[%Y-%b-%d %H:%M:%S]"
        return datetime.datetime.now().strftime(fmt) #add formatting

    def register_write_pos(self,file):
        pos = file.tell()
        file.seek(0)
        file.write(struct.pack("I", pos))
        file.seek(pos)
        print "Registered write position:" + str(pos)

    def register_log_begin_pos(self,file,pos):
        cursor_pos = file.tell()
        file.seek(4)
        file.write(struct.pack("I",pos))
        file.seek(cursor_pos)
        print "Log begin position registered as %d" % (pos,)

    def get_log_begin_pos(self,file):
        cursor_pos = file.tell()
        file.seek(4)
        log_begin_pos = struct.unpack("I",file.read(4))[0]
        file.seek(cursor_pos)
        return log_begin_pos

    def write_entry(self, entry):
        with LogFile(self.logpath,"r+") as f:
            fcntl.flock(f,fcntl.LOCK_EX)
            entry = self.get_timestamp() + entry
            length = struct.pack("H",len(entry))
            entry = length + entry
            self.write_to_file(entry,f)
            fcntl.flock(f,fcntl.LOCK_UN)

    def get_write_pos(self,file):
        cursor = file.tell()
        file.seek(0)
        position = struct.unpack("I",file.read(4))[0]
        file.seek(cursor)
        return position

    def seek_to_write_pos(self,file):
        file.seek(0)
        pos = struct.unpack("I",file.read(4))[0]
        file.seek(pos)

    def get_log_as_string(self):
        lines = []
        with LogFile(self.logpath,"r") as f:
            write_pos = self.get_write_pos(f)
            log_begin_pos = self.get_log_begin_pos(f)
            f.seek(log_begin_pos)
            while f.tell() != write_pos:
                print "Tell: " + str(f.tell())
                sleep(.5)
                entry_length = struct.unpack("H", f.read(2))[0]
                lines.append(f.read(entry_length))
            return "\n\n".join(lines)

    def write_to_file(self,text, file):
        write_pos = self.get_write_pos(file)
        log_begin_pos = self.get_log_begin_pos(file)
        print "Write position: %d" % (write_pos,)
        print "Text length: %d" % (len(text),)
        print "Entering loop"
        while ((write_pos < log_begin_pos and
               write_pos + len(text) + 12 > log_begin_pos) or
               (write_pos + len(text) > file.max_size and
               write_pos > log_begin_pos and
               (((write_pos + len(text)) % file.max_size) + 12 > log_begin_pos))):
            file.seek(log_begin_pos)
            first_entry_length = struct.unpack("H",file.read(2))[0]
            file.read(first_entry_length)
            log_begin_pos = file.tell()
            self.register_log_begin_pos(file,log_begin_pos)
        file.seek(write_pos)
        file.write(text)
        self.register_write_pos(file)

def runCommandWithLogging(command, origin_process, timeout, logfile):
    process = Command(command, timeout)
    if not process.success:
        logger = Logger(logfile,"w")
        if process.timeout:
            entry = '%s : Command "%s" timed out.' % (origin_process, command)
        else:
            if process.err:
                entry = '%s : Command "%s" failed with error message : %s' % (origin_process, command, process.err)
            elif process.output:
                entry = '%s : Command "%s" failed with output : %s' % (origin_process, command, process.output)
            else:
                entry = '%s : Command "%s" failed with return code %d' % (origin_process, command, process.returncode)
        logger.write_entry(entry)
    return process.success

def getConfigAsDict():
    import config
    attrs = [attr for attr in dir(config) if "__" not in attr]
    return_dict = {}
    for attr in attrs:
        exec("tmp = config." + attr)
        return_dict[attr] = tmp
    return return_dict
