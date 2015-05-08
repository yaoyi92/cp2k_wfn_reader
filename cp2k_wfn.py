##### cp2k wfn reader and writer
##### May 8th 2015
##### YY
##### yaoyi92@gmail.com

import struct
import numpy as np

class cp2k_wavefunction:
    """
    class of cp2k wavefunction. read and write cp2k wavefunction.
    """
    def __init__(self):
        self.fileContent = ''

        self.natom_read,self.nspin_read,self.nao_read,self.nset_max,self.nshell_max \
            = (0,0,0,0,0)
        self.nset_info = np.array([])
        self.nshell_info = np.array([])
        self.nso_info = np.array([])
        self.nmo_all = []
        self.homo_all = []
        self.lfomo_all = []
        self.nelectron_all = []
        self.evals_all = []
        self.occups_all = []
        self.vecs_all = []

    def __str__(self):
        return_string = ""
        return_string += "natom_read, nspin_read, nao_read, nset_max, nshell_max\n"
        return_string += str(self.natom_read) + " " +\
                         str(self.nspin_read) + " " +\
                         str(self.nao_read) + " " +\
                         str(self.nset_max) + " " +\
                         str(self.nshell_max) + "\n"
        return_string += "nset_info: " + str(self.nset_info) + "\n"
        return_string += "nshell_info: " + str(self.nshell_info) + "\n"
        return_string += "nso_info: " + str(self.nso_info) + "\n"
        return_string += "nmo_all: " + str(self.nmo_all) + "\n"
        return_string += "homo_all: " + str(self.homo_all) + "\n"
        return_string += "lfomo_all: " + str(self.lfomo_all) + "\n"
        return_string += "nelectron_all: " + str(self.nelectron_all) + "\n"
        return_string += "evals_all: " + str(self.evals_all) + "\n"
        return_string += "occups_all: " + str(self.occups_all) + "\n"
        return_string += "vecs_all: " + str(self.vecs_all) + "\n"

        return return_string

    def __repr__(self):
        return self.__str__()
    
    def readline(self):
        if len(self.fileContent) == 0:
            print "end of File"
            return False
        len_line, = struct.unpack("I", self.fileContent[0:4])
        line = self.fileContent[4:len_line+4]
        self.fileContent = self.fileContent[4+4+len_line:]
        return line

    def writeline(self,words):
        len_line = 0
        fmt = ""
        for word in words:
            if type(word) == int or type(word) == np.int64:
                len_line += 4
            if type(word) == float or type(word) == np.float64:
                len_line += 8
        self.fileContent += struct.pack("I",len_line)
        for word in words:
            if type(word) == int or type(word) == np.int64:
                fmt = "I"
            if type(word) == float or type(word) == np.float64: #double
                fmt = "d"
            self.fileContent += struct.pack(fmt,word)
        self.fileContent += struct.pack("I",len_line)
    
    def read_cp2k_wfn(self,filename):
        """
        read cp2k wfn file
        """
        with open(filename, mode='rb') as file:
            self.fileContent = file.read()
        line = self.readline()
        self.natom_read, \
        self.nspin_read, \
        self.nao_read, \
        self.nset_max, \
        self.nshell_max \
            = struct.unpack("IIIII",line)
        line = self.readline()
        self.nset_info = np.array(struct.unpack( \
          "I"*self.natom_read,line))
        line = self.readline()
        self.nshell_info = np.array(struct.unpack( \
          "I"*self.natom_read*self.nset_max,line))
        line = self.readline()
        self.nso_info = np.array(struct.unpack( \
          "I"*self.natom_read*self.nset_max*self.nshell_max,line))
        self.vecs_all = []
        self.nmo_all = []
        self.homo_all = []
        self.lfomo_all = []
        self.nelectron_all = []
        self.evals_all = []
        self.occups_all = []
        for i in range(self.nspin_read):
            vecs_spin = []
            line = self.readline()
            if not line:
                break
            nmo,homo,lfomo,nelectron = \
                struct.unpack("IIII",line)
            self.nmo_all.append(nmo)
            self.homo_all.append(homo)
            self.lfomo_all.append(lfomo)
            self.nelectron_all.append(nelectron)
            line = self.readline()
            evals = np.array(struct.unpack("d"*nmo,line[:8*nmo]))
            occups = np.array(struct.unpack("d"*nmo,line[8*nmo:]))
            self.evals_all.append(evals)
            self.occups_all.append(occups)
            for i in range(nmo):
                line = self.readline()
                vec = np.array(struct.unpack("d"*self.nao_read,line))
                vecs_spin.append(vec)
            self.vecs_all.append(vecs_spin)

    def write_cp2k_wfn(self,filename):
        """
        write cp2k wfn file. 
        """
        words = (self.natom_read,\
                 self.nspin_read,\
                 self.nao_read,\
                 self.nset_max,\
                 self.nshell_max)
        self.writeline(words)
        self.writeline(self.nset_info)
        self.writeline(self.nshell_info)
        self.writeline(self.nso_info)
        for i in range(self.nspin_read):
            if self.nmo_all[i] > 0:
                words = (self.nmo_all[i],\
                         self.homo_all[i],\
                         self.lfomo_all[i],\
                         self.nelectron_all[i])
                self.writeline(words)
                words = [word for word in self.evals_all[i]] +\
                        [word for word in self.occups_all[i]]
                self.writeline(words)
                for j in range(self.nmo_all[i]):
                    self.writeline(self.vecs_all[i][j])
        f = open(filename, 'wb')
        f.write(self.fileContent)
