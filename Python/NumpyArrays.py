import os
import sys
import numpy
import numpy.matlib
import astropy
import astropy.io
import astropy.io.fits
import urllib
import matplotlib.pyplot as plt

class NumpyArrays(object):

    MAIN_MIN_ID = 100000
    COLUMN_NUMBER = 8

    def Run(self, filenameCorot, filenameAsu, filenamefits, directoryLightCurves):
        self._GetNumpyArray(filenameCorot)
        self._RemoveUnwantedCorotLines()
        self._ReadLightCurves(filenameAsu)
        self._AddLightCurvesPathToInitialArray()
        self._WriteArrayToFitsFile(filenamefits)
        self._DownloadLightCurves(directoryLightCurves)
        self._ReadLightCurvesFiles()
        self._PlotLightCurves()

    def _GetNumpyArray(self, filename):
        print("Read corot result file")
        self.myarray = numpy.genfromtxt(fname=filename, dtype=[('c1', 'a64'), ('c2', 'a64'), ('c3', 'a64'), ('c4', 'a64'), ('c5', 'a64'), ('c6', 'a64'), ('c7', 'a64')], delimiter=";", names=True, converters= { "Main_ID": lambda x: x[len("CoRoT-"):]}) 

    def _RemoveUnwantedCorotLines(self):
        print("Remove unwanted corot lines")
        self.myarray = [x for x in self.myarray if int(x[3]) >= NumpyArrays.MAIN_MIN_ID]

    def _ReadLightCurves(self, filename):
        print("Read light curves file")
        self.lightcurves = numpy.genfromtxt(filename, dtype=[('c1', 'a64'), ('c2', 'a256')], delimiter="|", skip_header=40).flatten()

    def _AddLightCurvesPathToInitialArray(self):
        mylen = len(self.myarray)
        print("Add light curves to array")
        newarray = []
        for i in range(mylen):
            sys.stdout.write("\r%d%% (%d/%d)" % ((100 * i) / mylen, i, mylen))
            sys.stdout.flush()
            newarray.append([])
            for j in range(self.COLUMN_NUMBER):
                if (j == 7):
                    myindex = numpy.where(self.lightcurves['c1'] == self.myarray[i][3])                    
                    if len(myindex[0]) > 0:
                        newarray[i].append(self.lightcurves[myindex[0][0]][1])
                else:
                    newarray[i].append(self.myarray[i][j])
        newarray = sorted(newarray, key=lambda x: int(x[6]), reverse=True)
        self.myarray = numpy.array(newarray)

    def _WriteArrayToFitsFile(self, filenamefits):
        print("Write array to fits file")
        try:
            os.remove(filenamefits)
        except OSError:
            pass
        cols = astropy.io.fits.ColDefs([
        astropy.io.fits.Column(name="Ra", format="F", array=self.myarray[:, 0]),
        astropy.io.fits.Column(name="Dec", format="F", array=self.myarray[:, 1]),
        astropy.io.fits.Column(name="ID", format="64A", array=self.myarray[:, 2]),
        astropy.io.fits.Column(name="Main_ID", format="64A", array=self.myarray[:, 3]),
        astropy.io.fits.Column(name="coo_bibcode", format="64A", array=self.myarray[:, 4]),
        astropy.io.fits.Column(name="Sp_Type", format="64A", array=self.myarray[:, 5]),
        astropy.io.fits.Column(name="nbref", format="I", array=self.myarray[:, 6]),
        astropy.io.fits.Column(name="LightCurves", format="256A", array=self.myarray[:, 7])])
        cols = astropy.io.fits.ColDefs(cols)
        fittable = astropy.io.fits.TableHDU.from_columns(columns=cols)
        fittable.writeto(filenamefits)

    def _DownloadLightCurves(self, directoryLightCurves):
        print("Download light curves")
        self.PathComputerLightCurves = []
        for i in range(5):
            pathLightCurves = self.myarray[i][7].decode('ascii').replace(",", "")
            filenameLightCurves = pathLightCurves.split('/')[-1]
            self.myarray[i][7] = pathLightCurves.encode('ascii')
            self.PathComputerLightCurves.append(directoryLightCurves + filenameLightCurves)
            print("Download file %s", filenameLightCurves)
            if os.path.isfile(directoryLightCurves + filenameLightCurves) == False:
                urllib.urlretrieve('ftp://cdsarc.u-strasbg.fr/pub/cats/B/corot/files/' + pathLightCurves, directoryLightCurves + filenameLightCurves)

    def _ReadLightCurvesFiles(self):
        print("Read light curves files")
        self.arrayLightCurves = []
        self.validityLightCurves = []
        
        for i in range(5):
            self.arrayLightCurves.append(numpy.empty([0, 5], dtype=float))
            self.validityLightCurves.append([0, 0, 0, 0]);
            fit = astropy.io.fits.open(self.PathComputerLightCurves[i])
            data = fit[1].data
            columns = fit[1].columns
            for col in columns:
                if col.name == "REDFLUX":
                    self.validityLightCurves[i][0] = 1;
                elif col.name == "BLUEFLUX":
                    self.validityLightCurves[i][1] = 1;                
                elif col.name == "GREENFLUX":
                    self.validityLightCurves[i][2] = 1;                
                elif col.name == "WHITEFLUX":
                    self.validityLightCurves[i][3] = 1; 
            mylen = len(data)
            for j in range(mylen):
                sys.stdout.write("\r%d%% (%d/%d)" % ((100 * j) / mylen, j, mylen))
                sys.stdout.flush()
                row = data[j]
                if row.field("STATUS") == 0:
                    self.arrayLightCurves[i] = numpy.append(self.arrayLightCurves[i], 
                                                            [[
                                                                row.field("DATEJD"),
                                                                row.field("REDFLUX") if self.validityLightCurves[i][0] == 1 else 0,
                                                                row.field("BLUEFLUX") if self.validityLightCurves[i][1] == 1 else 0,
                                                                row.field("GREENFLUX") if self.validityLightCurves[i][2] == 1 else 0,
                                                                row.field("WHITEFLUX") if self.validityLightCurves[i][3] == 1 else 0,                                                            
                                                            ]], axis = 0)

    def _PlotLightCurves(self):
        print("\n" "Plot light curves")
        for i in range(5):
            if self.validityLightCurves[i][0] == 0 and self.validityLightCurves[i][1] == 0 and self.validityLightCurves[i][2] == 0:
                plt.figure(i)
                plt.plot(self.arrayLightCurves[i][:,0], self.arrayLightCurves[i][:,4],'k')
                plt.xlabel("DATEJD")
                plt.ylabel("WHITEFLUX")
                plt.title("COROT " + self.myarray[i][3].decode('ascii'))
            else:
                plt.figure(i)
                if self.validityLightCurves[i][0] == 1:
                    plt.subplot(1,3,1)
                    plt.plot(self.arrayLightCurves[i][:,0], self.arrayLightCurves[i][:,1],'r')
                    plt.xlabel("DATEJD")
                    plt.ylabel("REDFLUX")
                    plt.title("COROT " + self.myarray[i][3].decode('ascii'))
                if self.validityLightCurves[i][1] == 1:
                    plt.subplot(1,3,2)
                    plt.plot(self.arrayLightCurves[i][:,0], self.arrayLightCurves[i][:,2],'b')
                    plt.xlabel("DATEJD")
                    plt.ylabel("BLUEFLUX")
                    plt.title("COROT " + self.myarray[i][3].decode('ascii'))
                if self.validityLightCurves[i][2] == 1:
                    plt.subplot(1,3,3)
                    plt.plot(self.arrayLightCurves[i][:,0], self.arrayLightCurves[i][:,3],'g')
                    plt.xlabel("DATEJD")
                    plt.ylabel("GREENFLUX")
                    plt.title("COROT " + self.myarray[i][3].decode('ascii'))
        plt.show()
