import capnp
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from cereal import car
from selfdrive.car import dbc_dict
from selfdrive.car.docs_definitions import CarInfo, Harness
Ecu = car.CarParams.Ecu


class CAR:
  # Chrysler
  PACIFICA_2017_HYBRID = "CHRYSLER PACIFICA HYBRID 2017"
  PACIFICA_2018_HYBRID = "CHRYSLER PACIFICA HYBRID 2018"
  PACIFICA_2019_HYBRID = "CHRYSLER PACIFICA HYBRID 2019"
  PACIFICA_2018 = "CHRYSLER PACIFICA 2018"  # includes 2017 Pacifica
  PACIFICA_2020 = "CHRYSLER PACIFICA 2020"

  # Jeep
  JEEP_CHEROKEE = "JEEP GRAND CHEROKEE V6 2018"   # includes 2017 Trailhawk
  JEEP_CHEROKEE_2019 = "JEEP GRAND CHEROKEE 2019" # includes 2020 Trailhawk

  # Ram
  RAM_1500 = "RAM 1500 5TH GEN"


class CarControllerParams:
  def __init__(self, CP):
    self.STEER_MAX = 261  # higher than this faults the EPS on Chrysler/Jeep. Ram DT allows more
    self.STEER_ERROR_MAX = 80

    if CP.carFingerprint in RAM_CARS:
      self.STEER_DELTA_UP = 6
      self.STEER_DELTA_DOWN = 6
    else:
      self.STEER_DELTA_UP = 3
      self.STEER_DELTA_DOWN = 3

STEER_THRESHOLD = 120

RAM_CARS = {CAR.RAM_1500, }
PRE_2019 = {CAR.PACIFICA_2017_HYBRID, CAR.PACIFICA_2018_HYBRID, CAR.PACIFICA_2018, CAR.JEEP_CHEROKEE,}

@dataclass
class ChryslerCarInfo(CarInfo):
  package: str = "Adaptive Cruise"
  harness: Enum = Harness.fca

CAR_INFO: Dict[str, Optional[Union[ChryslerCarInfo, List[ChryslerCarInfo]]]] = {
  CAR.PACIFICA_2017_HYBRID: ChryslerCarInfo("Chrysler Pacifica Hybrid 2017-18"),
  CAR.PACIFICA_2018_HYBRID: None,  # same platforms
  CAR.PACIFICA_2019_HYBRID: ChryslerCarInfo("Chrysler Pacifica Hybrid 2019-22"),
  CAR.PACIFICA_2018: ChryslerCarInfo("Chrysler Pacifica 2017-18"),
  CAR.PACIFICA_2020: ChryslerCarInfo("Chrysler Pacifica 2019-20"),
  CAR.JEEP_CHEROKEE: ChryslerCarInfo("Jeep Grand Cherokee 2016-18", video_link="https://www.youtube.com/watch?v=eLR9o2JkuRk"),
  CAR.JEEP_CHEROKEE_2019: ChryslerCarInfo("Jeep Grand Cherokee 2019-21", video_link="https://www.youtube.com/watch?v=jBe4lWnRSu4"),
  CAR.RAM_1500: ChryslerCarInfo("Ram 1500 2019-22"),
}

# Unique CAN messages:
# Only the hybrids have 270: 8
# Only the gas have 55: 8, 416: 7
# For 564, All 2017 have length 4, whereas 2018-19 have length 8.
# For 924, Pacifica 2017 has length 3, whereas all 2018-19 have length 8.
# For 560, All 2019 have length 8, whereas all 2017-18 have length 4.

# Jeep Grand Cherokee unique messages:
# 2017 Trailhawk: 618: 8
# For 924, Trailhawk 2017 has length 3, whereas 2018 V6 has length 8.

FINGERPRINTS = {
  CAR.PACIFICA_2017_HYBRID: [{
    168: 8, 257: 5, 258: 8, 264: 8, 268: 8, 270: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 291: 8, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 515: 7, 516: 7, 517: 7, 518: 7, 520: 8, 528: 8, 532: 8, 542: 8, 544: 8, 557: 8, 559: 8, 560: 4, 564: 4, 571: 3, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 653: 8, 654: 8, 655: 8, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 678: 8, 680: 8, 701: 8, 704: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 737: 8, 746: 5, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 782: 8, 784: 8, 788:3, 792: 8, 799: 8, 800: 8, 804: 8, 808: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 878: 8, 882: 8, 897: 8, 908: 8, 924: 3, 926: 3, 929: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 956: 8, 958: 8, 959: 8, 969: 4, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1082: 8, 1083: 8, 1098: 8, 1100: 8, 1216: 8, 1218: 8, 1220: 8, 1225: 8, 1235: 8, 1242: 8, 1246: 8, 1250: 8, 1284: 8, 1537: 8, 1538: 8, 1562: 8, 1568: 8, 1856: 8, 1858: 8, 1860: 8, 1865: 8, 1875: 8, 1882: 8, 1886: 8, 1890: 8, 1892: 8, 2016: 8, 2024: 8
  }],
  CAR.PACIFICA_2018: [{
    55: 8, 257: 5, 258: 8, 264: 8, 268: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 416: 7, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 516: 7, 517: 7, 520: 8, 524: 8, 526: 6, 528: 8, 532: 8, 542: 8, 544: 8, 557: 8, 559: 8, 560: 4, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 656: 4, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 678: 8, 680: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 746: 5, 752: 2, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 784: 8, 792: 8, 799: 8, 800: 8, 804: 8, 808: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 882: 8, 897: 8, 924: 8, 926: 3, 937: 8, 947: 8, 948: 8, 969: 4, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1098: 8, 1100: 8, 1537: 8, 1538: 8, 1562: 8
  },
  {
    55: 8, 257: 5, 258: 8, 264: 8, 268: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 416: 7, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 516: 7, 517: 7, 520: 8, 524: 8, 526: 6, 528: 8, 532: 8, 542: 8, 544: 8, 557: 8, 559: 8, 560: 4, 564: 4, 571: 3, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 656: 4, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 678: 8, 680: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 746: 5, 752: 2, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 784: 8, 792: 8, 799: 8, 800: 8, 804: 8, 808: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 882: 8, 897: 8, 924: 3, 926: 3, 937: 8, 947: 8, 948: 8, 969: 4, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1098: 8, 1100: 8, 1537: 8, 1538: 8, 1562: 8
  }],
  CAR.PACIFICA_2020: [{
    55: 8, 179: 8, 181: 8, 257: 5, 258: 8, 264: 8, 268: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 352: 8, 362: 8, 368: 8, 376: 3, 384: 8, 388: 4, 416: 7, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 516: 7, 517: 7, 520: 8, 524: 8, 526: 6, 528: 8, 532: 8, 536: 8, 542: 8, 544: 8, 557: 8, 559: 8, 560: 8, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 650: 8, 656: 4, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 676: 8, 678: 8, 680: 8, 683: 8, 703: 8, 705: 8, 706: 8, 709: 8, 710: 8, 711: 8, 719: 8, 720: 6, 729: 5, 736: 8, 746: 5, 752: 2, 754: 8, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 776: 8, 779: 8, 782: 8, 784: 8, 792: 8, 793: 8, 794: 8, 795: 8, 799: 8, 800: 8, 801: 8, 802: 8, 803: 8, 804: 8, 808: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 847: 1, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 882: 8, 886: 8, 897: 8, 906: 8, 924: 8, 926: 3, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 962: 8, 969: 4, 973: 8, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1098: 8, 1100: 8, 1216: 8, 1218: 8, 1220: 8, 1223: 7, 1225: 8, 1227: 8, 1235: 8, 1242: 8, 1246: 8, 1250: 8, 1251: 8, 1252: 8, 1284: 8, 1543: 8, 1568: 8, 1570: 8, 1856: 8, 1858: 8, 1860: 8, 1863: 8, 1865: 8, 1867: 8, 1875: 8, 1882: 8, 1886: 8, 1890: 8, 1891: 8, 1892: 8, 1898: 8, 2015: 8, 2016: 8, 2017:8, 2024: 8, 2025: 8
  }],
  CAR.PACIFICA_2018_HYBRID: [{
    68: 8, 168: 8, 257: 5, 258: 8, 264: 8, 268: 8, 270: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 291: 8, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 520: 8, 528: 8, 532: 8, 544: 8, 557: 8, 559: 8, 560: 4, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 653: 8, 654: 8, 655: 8, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 680: 8, 701: 8, 704: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 736: 8, 737: 8, 746: 5, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 782: 8, 784: 8, 792: 8, 799: 8, 800: 8, 804: 8, 808: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 878: 8, 882: 8, 897: 8, 908: 8, 924: 8, 926: 3, 929: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 958: 8, 959: 8, 969: 4, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1082: 8, 1083: 8, 1098: 8, 1100: 8
  },
    # based on 9ae7821dc4e92455|2019-07-01--16-42-55
  {
    168: 8, 257: 5, 258: 8, 264: 8, 268: 8, 270: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 291: 8, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 515: 7, 516: 7, 517: 7, 518: 7, 520: 8, 528: 8, 532: 8, 542: 8, 544: 8, 557: 8, 559: 8, 560: 4, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 653: 8, 654: 8, 655: 8, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 678: 8, 680: 8, 701: 8, 704: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 737: 8, 746: 5, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 782: 8, 784: 8, 792: 8, 799: 8, 800: 8, 804: 8, 808: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 878: 8, 882: 8, 897: 8, 908: 8, 924: 8, 926: 3, 929: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 958: 8, 959: 8, 969: 4, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1082: 8, 1083: 8, 1098: 8, 1100: 8, 1216: 8, 1218: 8, 1220: 8, 1225: 8, 1235: 8, 1242: 8, 1246: 8, 1250: 8, 1251: 8, 1252: 8, 1258: 8, 1259: 8, 1260: 8, 1262: 8, 1284: 8, 1537: 8, 1538: 8, 1562: 8, 1568: 8, 1856: 8, 1858: 8, 1860: 8, 1865: 8, 1875: 8, 1882: 8, 1886: 8, 1890: 8, 1891: 8, 1892: 8, 1898: 8, 1899: 8, 1900: 8, 1902: 8, 2016: 8, 2018: 8, 2019: 8, 2020: 8, 2023: 8, 2024: 8, 2026: 8, 2027: 8, 2028: 8, 2031: 8
  }],
  CAR.PACIFICA_2019_HYBRID: [{
    168: 8, 257: 5, 258: 8, 264: 8, 268: 8, 270: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 291: 8, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 515: 7, 516: 7, 517: 7, 518: 7, 520: 8, 528: 8, 532: 8, 542: 8, 544: 8, 557: 8, 559: 8, 560: 8, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 653: 8, 654: 8, 655: 8, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 680: 8, 701: 8, 703: 8, 704: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 736: 8, 737: 8, 746: 5, 752: 2, 754: 8, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 782: 8, 784: 8, 792: 8, 799: 8, 800: 8, 804: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 878: 8, 882: 8, 897: 8, 906: 8, 908: 8, 924: 8, 926: 3, 929: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 958: 8, 959: 8, 962: 8, 969: 4, 973: 8, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1082: 8, 1083: 8, 1098: 8, 1100: 8, 1538: 8
  },
    # Based on 0607d2516fc2148f|2019-02-13--23-03-16
  {
    168: 8, 257: 5, 258: 8, 264: 8, 268: 8, 270: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 291: 8, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 520: 8, 528: 8, 532: 8, 544: 8, 557: 8, 559: 8, 560: 8, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 653: 8, 654: 8, 655: 8, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 678: 8, 680: 8, 701: 8, 703: 8, 704: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 737: 8, 746: 5, 752: 2, 754: 8, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 782: 8, 784: 8, 792: 8, 799: 8, 800: 8, 804: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 878: 8, 882: 8, 897: 8, 906: 8, 908: 8, 924: 8, 926: 3, 929: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 958: 8, 959: 8, 962: 8, 969: 4, 973: 8, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1082: 8, 1083: 8, 1098: 8, 1100: 8, 1537: 8
  },
    # Based on 3c7ce223e3571b54|2019-05-11--20-16-14
  {
    168: 8, 257: 5, 258: 8, 264: 8, 268: 8, 270: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 291: 8, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 520: 8, 528: 8, 532: 8, 544: 8, 557: 8, 559: 8, 560: 8, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 653: 8, 654: 8, 655: 8, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 678: 8, 680: 8, 701: 8, 703: 8, 704: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 737: 8, 746: 5, 752: 2, 754: 8, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 782: 8, 784: 8, 792: 8, 799: 8, 800: 8, 804: 8, 808: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 878: 8, 882: 8, 897: 8, 906: 8, 908: 8, 924: 8, 926: 3, 929: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 958: 8, 959: 8, 962: 8, 969: 4, 973: 8, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1082: 8, 1083: 8, 1098: 8, 1100: 8, 1562: 8, 1570: 8
  },
    # Based on "8190c7275a24557b|2020-02-24--09-57-23"
  {
    168: 8, 257: 5, 258: 8, 264: 8, 268: 8, 270: 8, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 291: 8, 292: 8, 294: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 368: 8, 376: 3, 384: 8, 388: 4, 448: 6, 456: 4, 464: 8, 469: 8, 480: 8, 500: 8, 501: 8, 512: 8, 514: 8, 515: 7, 516: 7, 517: 7, 518: 7, 520: 8, 524: 8, 526: 6, 528: 8, 532: 8, 542: 8, 544: 8, 557: 8, 559: 8, 560: 8, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 624: 8, 625: 8, 632: 8, 639: 8, 640: 1, 650: 8, 653: 8, 654: 8, 655: 8, 656: 4, 658: 6, 660: 8, 669: 3, 671: 8, 672: 8, 678: 8, 680: 8, 683: 8, 701: 8, 703: 8, 704: 8, 705: 8, 706: 8, 709: 8, 710: 8, 711: 8, 719: 8, 720: 6, 729: 5, 736: 8, 737: 8, 738: 8, 746: 5, 752: 2, 754: 8, 760: 8, 764: 8, 766: 8, 770: 8, 773: 8, 779: 8, 782: 8, 784: 8, 792: 8, 793: 8, 794: 8, 795: 8, 796: 8, 797: 8, 798: 8, 799: 8, 800: 8, 801: 8, 802: 8, 803: 8, 804: 8, 805: 8, 807: 8, 808: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 847: 1, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 878: 8, 882: 8, 886: 8, 897: 8, 906: 8, 908: 8, 924: 8, 926: 3, 929: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 958: 8, 959: 8, 962: 8, 969: 4, 973: 8, 974: 5, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1082: 8, 1083: 8, 1098: 8, 1100: 8, 1216: 8, 1218: 8, 1220: 8, 1225: 8, 1235: 8, 1242: 8, 1246: 8, 1250: 8, 1251: 8, 1252: 8, 1258: 8, 1259: 8, 1260: 8, 1262: 8, 1284: 8, 1536: 8, 1568: 8, 1570: 8, 1856: 8, 1858: 8, 1860: 8, 1863: 8, 1865: 8, 1875: 8, 1882: 8, 1886: 8, 1890: 8, 1891: 8, 1892: 8, 1898: 8, 1899: 8, 1900: 8, 1902: 8, 2015: 8, 2016: 8, 2017: 8, 2018: 8, 2019: 8, 2020: 8, 2023: 8, 2024: 8, 2026: 8, 2027: 8, 2028: 8, 2031: 8
  }],
  CAR.JEEP_CHEROKEE: [{
    55: 8, 168: 8, 181: 8, 256: 4, 257: 5, 258: 8, 264: 8, 268: 8, 272: 6, 273: 6, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 292: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 352: 8, 362: 8, 368: 8, 376: 3, 384: 8, 388: 4, 416: 7, 448: 6, 456: 4, 464: 8, 500: 8, 501: 8, 512: 8, 514: 8, 520: 8, 532: 8, 544: 8, 557: 8, 559: 8, 560: 4, 564: 4, 571: 3, 579: 8, 584: 8, 608: 8, 618: 8, 624: 8, 625: 8, 632: 8, 639: 8, 656: 4, 658: 6, 660: 8, 671: 8, 672: 8, 676: 8, 678: 8, 680: 8, 683: 8, 684: 8, 703: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 737: 8, 738: 8, 746: 5, 752: 2, 754: 8, 760: 8, 761: 8, 764: 8, 766: 8, 773: 8, 776: 8, 779: 8, 782: 8, 783: 8, 784: 8, 785: 8, 788: 3, 792: 8, 799: 8, 800: 8, 804: 8, 806: 2, 808: 8, 810: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 831: 6, 832: 8, 838: 2, 840: 8, 844: 5, 847: 1, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 874: 2, 882: 8, 897: 8, 906: 8, 924: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 956: 8, 968: 8, 969: 4, 970: 8, 973: 8, 974: 5, 975: 8, 976: 8, 977: 4, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1062: 8, 1098: 8, 1100: 8, 1543: 8, 1562: 8, 2015: 8, 2016: 8, 2017: 8, 2024: 8, 2025: 8
  },
    # Jeep Grand Cherokee 2018 Trackhawk
  {
    55: 8, 168: 8, 256: 4, 257: 5, 258: 8, 264: 8, 268: 8, 272: 6, 273: 6, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 292: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 344: 8, 352: 8, 362: 8, 368: 8, 376: 3, 384: 8, 388: 4, 416: 7, 448: 6, 456: 4, 464: 8, 500: 8, 501: 8, 512: 8, 514: 8, 520: 8, 532: 8, 544: 8, 557: 8, 559: 8, 560: 4, 564: 4, 571: 3, 579: 8, 584: 8, 608: 8, 618: 8, 624: 8, 625: 8, 632: 8, 639: 8, 656: 4, 658: 6, 660: 8, 671: 8, 672: 8, 676: 8, 678: 8, 680: 8, 683: 8, 684: 8, 703: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 737: 8, 738: 8, 746: 5, 752: 2, 754: 8, 760: 8, 761: 8, 764: 8, 766: 8, 773: 8, 776: 8, 779: 8, 782: 8, 783: 8, 784: 8, 785: 8, 792: 8, 799: 8, 800: 8, 804: 8, 806: 2, 808: 8, 810: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 832: 8, 838: 2, 840: 8, 847: 1, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 874: 2, 882: 8, 897: 8, 906: 8, 924: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 968: 8, 969: 4, 970: 8, 973: 8, 974: 5, 976: 8, 977: 4, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1098: 8, 1100: 8, 1543: 8, 2015: 8, 2024: 8, 2025: 8
  }],
  CAR.JEEP_CHEROKEE_2019: [{
    # Jeep Grand Cherokee 2019, including most 2020 models
    55: 8, 168: 8, 179: 8, 181: 8, 256: 4, 257: 5, 258: 8, 264: 8, 268: 8, 272: 6, 273: 6, 274: 2, 280: 8, 284: 8, 288: 7, 290: 6, 292: 8, 300: 8, 308: 8, 320: 8, 324: 8, 331: 8, 332: 8, 341: 8, 344: 8, 352: 8, 362: 8, 368: 8, 376: 3, 384: 8, 388: 4, 416: 7, 448: 6, 456: 4, 464: 8, 500: 8, 501: 8, 512: 8, 514: 8, 520: 8, 530: 8, 532: 8, 544: 8, 557: 8, 559: 8, 560: 8, 564: 8, 571: 3, 579: 8, 584: 8, 608: 8, 618: 8, 624: 8, 625: 8, 632: 8, 639: 8, 640: 1, 656: 4, 658: 6, 660: 8, 671: 8, 672: 8, 676: 8, 678: 8, 680: 8, 683: 8, 684: 8, 703: 8, 705: 8, 706: 8, 709: 8, 710: 8, 719: 8, 720: 6, 729: 5, 736: 8, 737: 8, 738: 8, 746: 5, 752: 2, 754: 8, 760: 8, 761: 8, 764: 8, 766: 8, 773: 8, 776: 8, 779: 8, 782: 8, 783: 8, 784: 8, 785: 8, 792: 8, 799: 8, 800: 8, 804: 8, 806: 2, 808: 8, 810: 8, 816: 8, 817: 8, 820: 8, 825: 2, 826: 8, 831: 6, 832: 8, 838: 2, 840: 8, 844: 5, 847: 1, 848: 8, 853: 8, 856: 4, 860: 6, 863: 8, 882: 8, 897: 8, 906: 8, 924: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 960: 4, 968: 8, 969: 4, 970: 8, 973: 8, 974: 5, 976: 8, 977: 4, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1062: 8, 1098: 8, 1100: 8, 1216: 8, 1218: 8, 1220: 8, 1223: 8, 1225: 8, 1227: 8, 1235: 8, 1242: 8, 1250: 8, 1251: 8, 1252: 8, 1254: 8, 1264: 8, 1284: 8, 1536: 8, 1537: 8, 1543: 8, 1545: 8, 1562: 8, 1568: 8, 1570: 8, 1572: 8, 1593: 8, 1856: 8, 1858: 8, 1860: 8, 1863: 8, 1865: 8, 1867: 8, 1875: 8, 1882: 8, 1890: 8, 1891: 8, 1892: 8, 1894: 8, 1896: 8, 1904: 8, 2015: 8, 2016: 8, 2017: 8, 2024: 8, 2025: 8
  }],
  CAR.RAM_1500: [
    {35: 8, 37: 8, 39: 8, 41: 8, 43: 8, 47: 8, 49: 8, 53: 8, 55: 8, 113: 8, 119: 2, 121: 8, 123: 7, 125: 6, 127: 8,  129: 8, 131: 8, 133: 8, 135: 8, 137: 8, 139: 8, 141: 8, 145: 8, 147: 8, 149: 7, 153: 8, 155: 8, 157: 8, 163: 8,  164: 8, 166: 8, 167: 8, 169: 8, 171: 8, 173: 5, 177: 3, 179: 8, 181: 8, 213: 3, 221: 8, 232: 8, 250: 8, 278: 8, 289: 5, 293: 3, 295: 8, 296: 8, 297: 4, 298: 8, 299: 8, 305: 8, 307: 8, 311: 8, 315: 8, 317: 8, 319: 8, 323: 8, 333: 8, 334: 8, 341: 8, 343: 8, 345: 8, 347: 8, 409: 6, 421: 8, 448: 6, 456: 4, 464: 8, 489: 8, 491: 8, 502: 8, 503: 8, 505: 8, 507: 5, 516: 7, 517: 7, 524: 8, 526: 6, 557: 8, 560: 8, 584: 8, 601: 8, 605: 8, 607: 8, 609: 8, 611: 8, 613: 8, 623: 8, 631: 8, 633: 8, 634: 8, 635: 8, 637: 8, 641: 8, 643: 8, 645: 2, 649: 8, 650: 8, 651: 8, 656: 4, 657: 8, 659: 5, 663: 8, 664: 8, 673: 8, 676: 8, 679: 8, 685: 8, 687: 8, 689: 5, 706: 8, 709: 8, 710: 8, 711: 8, 720: 6, 752: 2, 754: 8, 773: 8, 788: 3, 792: 8, 808: 8, 818: 8, 819: 8, 822: 8, 823: 8, 825: 2, 838: 2, 840: 8, 848: 8, 856: 4, 860: 6, 862: 8, 875: 2, 897: 8, 906: 8, 910: 8, 926: 3, 929: 8, 930: 8, 931: 8, 932: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 956: 8, 961: 8, 962: 8, 969: 4, 971: 8, 972: 8, 973: 8, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1062: 8, 1098: 8, 1100: 8, 2015: 8, 2016: 8, 2017: 8, 2024: 8, 2025: 8},
    {35: 8, 37: 8, 39: 8, 43: 8, 47: 8, 49: 8, 53: 8, 55: 8, 113: 8, 119: 2, 121: 8, 123: 7, 125: 6, 127: 8, 129: 8, 131: 8, 133: 8, 135: 8, 137: 8, 139: 8, 141: 8, 145: 8, 147: 8, 149: 7, 153: 8, 155: 8, 157: 8, 163: 8, 164: 8, 166: 8, 167: 8, 169: 8, 171: 8, 173: 5, 177: 3, 179: 8, 181: 8, 213: 3, 221: 8, 232: 8, 250: 8, 276: 8, 277: 8, 278: 8, 289: 5, 293: 3, 295: 8, 296: 8, 297: 4, 299: 8, 301: 8, 302: 8, 305: 8, 307: 8, 311: 8, 317: 8, 319: 8, 323: 8, 327: 8, 333: 8, 334: 8, 341: 8, 343: 8, 345: 8, 347: 8, 421: 8, 448: 6, 456: 4, 457: 8, 464: 8, 489: 8, 491: 8, 502: 8, 503: 8, 507: 5, 516: 7, 517: 7, 524: 8, 526: 6, 557: 8, 560: 8, 584: 8, 601: 8, 605: 8, 607: 8, 609: 8, 613: 8, 623: 8, 631: 8, 633: 8, 634: 8, 635: 8, 637: 8, 641: 8, 643: 8, 645: 2, 649: 8, 650: 8, 651: 8, 656: 4, 657: 8, 663: 8, 673: 8, 676: 8, 679: 8, 685: 8, 687: 8, 689: 5, 706: 8, 709: 8, 710: 8, 711: 8, 720: 6, 738: 8, 752: 2, 754: 8, 773: 8, 792: 8, 808: 8, 812: 8, 813: 8, 814: 8, 818: 8, 819: 8, 821: 8, 822: 8, 823: 8, 825: 2, 838: 2, 840: 8, 847: 1, 848: 8, 856: 4, 860: 6, 862: 8, 874: 2, 876: 8, 897: 8, 906: 8, 910: 8, 926: 3, 929: 8, 930: 8, 931: 8, 932: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 961: 8, 962: 8, 969: 4, 971: 8, 972: 8, 973: 8, 975: 8, 976: 8, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1030: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1098: 8, 1100: 8},
    {35: 8, 37: 8, 39: 8, 43: 8, 47: 8, 49: 8, 53: 8, 55: 8, 113: 8, 119: 2, 121: 8, 123: 7, 125: 6, 127: 8, 129: 8, 131: 8, 133: 8, 135: 8, 137: 8, 139: 8, 141: 8, 145: 8, 147: 8, 149: 7, 153: 8, 155: 8, 157: 8, 163: 8, 164: 8, 166: 8, 167: 8, 169: 8, 171: 8, 173: 5, 177: 3, 179: 8, 181: 8, 213: 3, 221: 8, 232: 8, 250: 8, 289: 5, 293: 3, 295: 8, 296: 8, 297: 4, 299: 8, 301: 8, 302: 8, 305: 8, 307: 8, 311: 8, 317: 8, 319: 8, 323: 8, 334: 8, 337: 8, 343: 8, 347: 8, 409: 6, 421: 8, 448: 6, 456: 4, 464: 8, 489: 8, 491: 8, 502: 8, 503: 8, 507: 5, 516: 7, 517: 7, 524: 8, 526: 6, 557: 8, 560: 8, 584: 8, 601: 8, 605: 8, 607: 8, 609: 8, 613: 8, 623: 8, 631: 8, 633: 8, 634: 8, 635: 8, 637: 8, 641: 8, 643: 8, 645: 2, 649: 8, 650: 8, 651: 8, 656: 4, 657: 8, 659: 5, 663: 8, 664: 8, 673: 8, 676: 8, 679: 8, 685: 8, 687: 8, 689: 5, 706: 8, 709: 8, 710: 8, 711: 8, 720: 6, 752: 2, 754: 8, 773: 8, 788: 3, 792: 8, 808: 8, 812: 8, 813: 8, 814: 8, 818: 8, 819: 8, 821: 8, 822: 8, 825: 2, 838: 2, 840: 8, 847: 1, 848: 8, 856: 4, 860: 6, 862: 8, 876: 8, 897: 8, 906: 8, 910: 8, 926: 3, 929: 8, 930: 8, 931: 8, 932: 8, 937: 8, 938: 8, 939: 8, 940: 8, 941: 8, 942: 8, 943: 8, 947: 8, 948: 8, 956: 8, 961: 8, 962: 8, 969: 4, 971: 8, 972: 8, 973: 8, 979: 8, 980: 8, 981: 8, 982: 8, 983: 8, 984: 8, 992: 8, 993: 7, 995: 8, 996: 8, 1000: 8, 1001: 8, 1002: 8, 1003: 8, 1008: 8, 1009: 8, 1010: 8, 1011: 8, 1012: 8, 1013: 8, 1014: 8, 1015: 8, 1024: 8, 1025: 8, 1026: 8, 1030: 8, 1031: 8, 1033: 8, 1050: 8, 1059: 8, 1062: 8, 1098: 8, 1100: 8},
  ],
}

FW_VERSIONS: Dict[str, Dict[Tuple[capnp.lib.capnp._EnumModule, int, Optional[int]], List[str]]] = {
  CAR.RAM_1500: {
    (Ecu.combinationMeter, 0x742, None): [],
    (Ecu.srs, 0x744, None): [],
    (Ecu.esp, 0x747, None): [],
    (Ecu.fwdCamera, 0x753, None): [],
    (Ecu.fwdCamera, 0x764, None): [],
    (Ecu.eps, 0x761, None): [],
    (Ecu.fwdRadar, 0x757, None): [],
    (Ecu.eps, 0x75A, None): [],
    (Ecu.engine, 0x7e0, None): [],
    (Ecu.transmission, 0x7e1, None): [],
    (Ecu.gateway, 0x18DACBF1, None): [],
  }
}

DBC = {
  CAR.PACIFICA_2017_HYBRID: dbc_dict('chrysler_pacifica_2017_hybrid_generated', 'chrysler_jvepilot', 'chrysler_pacifica_2017_hybrid_private_fusion'),
  CAR.PACIFICA_2018: dbc_dict('chrysler_pacifica_2017_hybrid_generated', 'chrysler_jvepilot', 'chrysler_pacifica_2017_hybrid_private_fusion'),
  CAR.PACIFICA_2020: dbc_dict('chrysler_pacifica_2017_hybrid_generated', 'chrysler_jvepilot', 'chrysler_pacifica_2017_hybrid_private_fusion'),
  CAR.PACIFICA_2018_HYBRID: dbc_dict('chrysler_pacifica_2017_hybrid_generated', 'chrysler_jvepilot', 'chrysler_pacifica_2017_hybrid_private_fusion'),
  CAR.PACIFICA_2019_HYBRID: dbc_dict('chrysler_pacifica_2017_hybrid_generated', 'chrysler_jvepilot', 'chrysler_pacifica_2017_hybrid_private_fusion'),
  CAR.JEEP_CHEROKEE: dbc_dict('chrysler_pacifica_2017_hybrid_generated', 'chrysler_jvepilot', 'chrysler_pacifica_2017_hybrid_private_fusion'),
  CAR.JEEP_CHEROKEE_2019: dbc_dict('chrysler_pacifica_2017_hybrid_generated', 'chrysler_jvepilot', 'chrysler_pacifica_2017_hybrid_private_fusion'),
  CAR.RAM_1500: dbc_dict('chrysler_ram_dt_generated', None),
}
