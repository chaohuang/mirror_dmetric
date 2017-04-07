#!/usr/bin/python
import os
import collections
import sys
import getopt
import ConfigParser

org = {}
norm = {}
pref = {}
log = {}
gRange = {}
cRange = {}
pjRange = {}
pPSNR = {}
seqSet = []
calc = '/data/tian/pc_psnr/pcc_quality/test/pc_error_0322'  # Specify the program of the distortion calculator


def tree():
  return collections.defaultdict(tree)


def getFloatValue( line, keyword ):
  flag = 0
  value = 0.0
  if keyword in line:
    for token in line.split():
      try:
        if float(token):
          flag = 1
          value = float(token)
      except ValueError:
        continue
  return flag, value


def getResults( keyword, logfile ):
  ret = 0.0
  with open( logfile ) as inf:
    for line in inf:
      line = line.strip()
      if keyword in line:
        flag, value = getFloatValue( line, keyword )
        if flag:
          ret = value
  return ret


def usage():
  print('./anchor -c config.ini <-r> <-h> <-d data>')


def getSetFromString( str, separator ):
  if separator == " ":
    ret = str.split()
  else:
    str = ''.join(str.split())
    ret = str.split( separator )
  return ret


def ConfigSectionMap( section ):
  options = Config.options( section )
  for option in options:
    if option == "org":
      org[section] = Config.get( section, option )
    elif option == "norm":
      norm[section] = Config.get( section, option )
    elif option == "pref":
      pref[section] = Config.get( section, option )
    elif option == "log":
      log[section] = Config.get( section, option )
    elif option == "grange":
      strtmp = Config.get( section, option )
      gRange[section] = map( int, getSetFromString( strtmp, ',' ) )
    elif option == "crange":
      strtmp = Config.get( section, option )
      cRange[section] = map(int, getSetFromString( strtmp, ',' ) )
    elif option == "pjrange":
      strtmp = Config.get( section, option )
      pjRange[section] = getSetFromString( strtmp, ',' )
    elif option == "ppsnr":
      pPSNR[section] = float( Config.get( section, option ) )


def main(argv):
  ##########################################
  # Tune this section on what you want to do
  ##########################################
  runCmd = 0                      # Set to 1 to run evaluation. Set to 0 to put the Excel sheet ready output and no evaluation would be actually called
  myIni = ""
  seqSetSpecial = ""

  # Update the variables from command line
  try:
    opts, args = getopt.getopt(argv, "hrd:c:", ["help", "run", "data=", "config="])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      usage()
      sys.exit()
    elif opt in ("-d", "--data"):
      seqSetSpecial = [arg]
    elif opt in ("-r", "--run"):
      runCmd = 1
    elif opt in ("-c", "--config"):
      myIni = [arg]

  if myIni == "":
    usage()
    sys.exit(2)

  # Load configurations
  Config.read(myIni)
  seqSet = Config.sections()
  # print("sections: %s" % seqSet)

  if seqSetSpecial != "":
    seqSet = seqSetSpecial

  for seq in seqSet:
    ConfigSectionMap( seq )

  # Do evaluations and reporting
  for seq in seqSet:
    data = tree()
    # Do evaluations
    for g in gRange[seq]:
      for c in cRange[seq]:
        for pj in pjRange[seq]:
          decoded = '%s_g%d_c%d_%s.ply' % ( pref[seq], g, c, pj )
          logfile = '%s_g%d_c%d_%s.txt' % ( log[seq], g, c, pj )
          bExist = os.path.isfile(decoded)
          if bExist:
            if norm[seq]:
              cmd = 'date; %s -a %s -b %s -n %s -c -r %f > %s; date' % (calc, org[seq], decoded, norm[seq], pPSNR[seq], logfile)
            # else:
            #   cmd = 'date; %s -a %s -b %s -c -r %f > %s; date' % (calc, org[seq], decoded, pPSNR[seq], logfile)
            if runCmd:
              print('%s' % (cmd) )
              os.system(cmd)
            c2c = getResults( 'rmsF,PSNR (p2point):', logfile )
            c2p = getResults( 'rmsF,PSNR (p2plane):', logfile )
            y   = getResults( 'c[0],PSNRF         :', logfile )
            u   = getResults( 'c[1],PSNRF         :', logfile )
            v   = getResults( 'c[2],PSNRF         :', logfile )
            if runCmd:
              print( '%s -> %f, %f' % (logfile, c2c, c2p) )
            data[g][c][pj]['c2c'] = c2c
            data[g][c][pj]['c2p'] = c2p
            data[g][c][pj]['y'  ] = y
            data[g][c][pj]['u'  ] = u
            data[g][c][pj]['v'  ] = v
          else:
            data[g][c][pj]['c2c'] = -99.12345
            data[g][c][pj]['c2p'] = -99.67890
            data[g][c][pj]['y'  ] = -99.99
            data[g][c][pj]['u'  ] = -99.99
            data[g][c][pj]['v'  ] = -99.99

    # Do reporting
    print('')
    print('%s point2point point2plane y u v' % (seq))

    for pj in pjRange[seq]:
      # print('pj = %s' % (pj) )
      for c in cRange[seq]:
        # print('c = %s' % (c) )
        for g in gRange[seq]:
          print( '%d  %f  %f  %f  %f  %f' % (g, data[g][c][pj]['c2c'], data[g][c][pj]['c2p'], data[g][c][pj]['y'], data[g][c][pj]['u'], data[g][c][pj]['v']) )
        print('')

# Init the config variable
Config = ConfigParser.ConfigParser()
if __name__ == "__main__":
  main(sys.argv[1:])
