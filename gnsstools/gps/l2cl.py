# GPS L2CL code construction
#
# Copyright 2014 Peter Monta

import numpy as np

chip_rate = 511500
code_length = 767250

# initial-state table from pages 9--11 and pages 62--63 of IS-GPS-200H
# index is PRN

l2cl_init = {
    1: 0o624145772,    2: 0o506610362,    3: 0o220360016,    4: 0o710406104,
    5: 0o001143345,    6: 0o053023326,    7: 0o652521276,    8: 0o206124777,
    9: 0o015563374,   10: 0o561522076,   11: 0o023163525,   12: 0o117776450,
   13: 0o606516355,   14: 0o003037343,   15: 0o046515565,   16: 0o671511621,
   17: 0o605402220,   18: 0o002576207,   19: 0o525163451,   20: 0o266527765,
   21: 0o006760703,   22: 0o501474556,   23: 0o743747443,   24: 0o615534726,
   25: 0o763621420,   26: 0o720727474,   27: 0o700521043,   28: 0o222567263,
   29: 0o132765304,   30: 0o746332245,   31: 0o102300466,   32: 0o255231716,
   33: 0o437661701,   34: 0o717047302,   35: 0o222614207,   36: 0o561123307,
   37: 0o240713073,
   38: 0o101232630,   39: 0o132525726,   40: 0o315216367,   41: 0o377046065,
   42: 0o655351360,   43: 0o435776513,   44: 0o744242321,   45: 0o024346717,
   46: 0o562646415,   47: 0o731455342,   48: 0o723352536,   49: 0o000013134,
   50: 0o011566642,   51: 0o475432222,   52: 0o463506741,   53: 0o617127534,
   54: 0o026050332,   55: 0o733774235,   56: 0o751477772,   57: 0o417631550,
   58: 0o052247456,   59: 0o560404163,   60: 0o417751005,   61: 0o004302173,
   62: 0o715005045,   63: 0o001154457,
  159: 0o605253024,  160: 0o063314262,  161: 0o066073422,  162: 0o737276117,
  163: 0o737243704,  164: 0o067557532,  165: 0o227354537,  166: 0o704765502,
  167: 0o044746712,  168: 0o720535263,  169: 0o733541364,  170: 0o270060042,
  171: 0o737176640,  172: 0o133776704,  173: 0o005645427,  174: 0o704321074,
  175: 0o137740372,  176: 0o056375464,  177: 0o704374004,  178: 0o216320123,
  179: 0o011322115,  180: 0o761050112,  181: 0o725304036,  182: 0o721320336,
  183: 0o443462103,  184: 0o510466244,  185: 0o745522652,  186: 0o373417061,
  187: 0o225526762,  188: 0o047614504,  189: 0o034730440,  190: 0o453073141,
  191: 0o533654510,  192: 0o377016461,  193: 0o235525312,  194: 0o507056307,
  195: 0o221720061,  196: 0o520470122,  197: 0o603764120,  198: 0o145604016,
  199: 0o051237167,  200: 0o033326347,  201: 0o534627074,  202: 0o645230164,
  203: 0o000171400,  204: 0o022715417,  205: 0o135471311,  206: 0o137422057,
  207: 0o714426456,  208: 0o640724672,  209: 0o501254540,  210: 0o513322453
}

def l2cl_shift(x):
  return (x>>1) ^ (x&1)*0o445112474;

def make_l2cl(prn):
  x = l2cl_init[prn]
  n = code_length
  y = numpy.zeros(n)
  for i in range(n):
    y[i] = x&1
    x = l2cl_shift(x)
  return y

codes = {}

def l2cl_code(prn):
  if not codes.has_key(prn):
    codes[prn] = make_l2cl(prn)
  return codes[prn]

def code(prn,chips,frac,incr,n):
  c = l2cl_code(prn)
  idx = (chips%code_length) + frac + incr*np.arange(n)
  idx = np.floor(idx).astype('int')
  idx = np.mod(idx,code_length)
  x = c[idx]
  return 1.0 - 2.0*x

# test vectors in IS-GPS-200H

l2cl_end_state = {
    1: 0o267724236,    2: 0o167516066,    3: 0o771756405,    4: 0o047202624,
    5: 0o052770433,    6: 0o761743665,    7: 0o133015726,    8: 0o610611511,
    9: 0o352150323,   10: 0o051266046,   11: 0o305611373,   12: 0o504676773,
   13: 0o272572634,   14: 0o731320771,   15: 0o631326563,   16: 0o231516360,
   17: 0o030367366,   18: 0o713543613,   19: 0o232674654,   20: 0o641733155,
   21: 0o730125345,   22: 0o000316074,   23: 0o171313614,   24: 0o001523662,
   25: 0o023457250,   26: 0o330733254,   27: 0o625055726,   28: 0o476524061,
   29: 0o602066031,   30: 0o012412526,   31: 0o705144501,   32: 0o615373171,
   33: 0o041637664,   34: 0o100107264,   35: 0o634251723,   36: 0o257012032,
   37: 0o703702423,
   38: 0o463624741,   39: 0o673421367,   40: 0o703006075,   41: 0o746566507,
   42: 0o444022714,   43: 0o136645570,   44: 0o645752300,   45: 0o656113341,
   46: 0o015705106,   47: 0o002757466,   48: 0o100273370,   49: 0o304463615,
   50: 0o054341657,   51: 0o333276704,   52: 0o750231416,   53: 0o541445326,
   54: 0o316216573,   55: 0o007360406,   56: 0o112114774,   57: 0o042303316,
   58: 0o353150521,   59: 0o044511154,   60: 0o244410144,   61: 0o562324657,
   62: 0o027501534,   63: 0o521240373,
  159: 0o044547544,  160: 0o707116115,  161: 0o412264037,  162: 0o223755032,
  163: 0o403114174,  164: 0o671505575,  165: 0o606261015,  166: 0o223023120,
  167: 0o370035547,  168: 0o516101304,  169: 0o044115766,  170: 0o704125517,
  171: 0o406332330,  172: 0o506446631,  173: 0o743702511,  174: 0o022623276,
  175: 0o704221045,  176: 0o372577721,  177: 0o105175230,  178: 0o760701311,
  179: 0o737141001,  180: 0o227627616,  181: 0o245154134,  182: 0o040015760,
  183: 0o002154472,  184: 0o301767766,  185: 0o226475246,  186: 0o733673015,
  187: 0o602507667,  188: 0o753362551,  189: 0o746265601,  190: 0o036253206,
  191: 0o202512772,  192: 0o701234023,  193: 0o722043377,  194: 0o240751052,
  195: 0o375674043,  196: 0o166677056,  197: 0o123055362,  198: 0o707017665,
  199: 0o437503241,  200: 0o275605155,  201: 0o376333266,  202: 0o467523556,
  203: 0o144132537,  204: 0o451024205,  205: 0o722446427,  206: 0o412376261,
  207: 0o441570172,  208: 0o063217710,  209: 0o110320656,  210: 0o113765506
}

def test_end_state(prn):
  x = l2cl_init[prn]
  n = code_length
  for i in range(n-1):
    x = l2cl_shift(x)
  return x

if __name__=='__main__':
  for prn in l2cl_end_state.keys():
    s = test_end_state(prn)
    t = l2cl_end_state[prn]
    if s!=t:
      print "prn %d: ***mismatch*** %09o %09o" % (prn,s,t)
    else:
#      print "prn %d: %09o %09o" % (prn,s,t)
      pass