from ncc import NCC
from box import Box

fileNameTension = "6.5/6.5 Curves and Images/Tension.crv"

fileNameCompression = "6.5/6.5 Curves and Images/Compression.crv"

fileNameFlexion = "6.5/6.5 Curves and Images/MomentAngleFlexion.crv"

fileNameExtension = "6.5/6.5 Curves and Images/MomentAngleExtension.crv"

fileNameFlexionAngle = "6.5/6.5 Curves and Images/HeadAngleFlexion.crv"

fileNameExtensionAngle = "6.5/6.5 Curves and Images/HeadAngleExtension.crv"

fileNameNBDLx = "6.5/6.5 Curves and Images/NBDLHeadxCoord.crv"

fileNameNBDLz = "6.5/6.5 Curves and Images/NBDLHeadzCoord.crv"

# This is the wrong EXPERIMENT file
fileNameNBDLHeadLag = "corridors/HeadLag+Corr.csv"
fileNameNBDLHeadLagCorridor = "corridors/HeadLag+Corr.csv"

fileNameCHOPEAMx = "6.5/6.5 Curves and Images/CHOP_EAMX_model.crv"
fileNameCHOPEAMxCorridor = "corridors/CHOP_EAMX.crv"

fileNameCHOPEAMz = "6.5/6.5 Curves and Images/CHOP_EAMZ_model.crv"
fileNameCHOPEAMzCorridor = "corridors/CHOP_EAMZ.crv"

fileNameCHOPNASx = "6.5/6.5 Curves and Images/CHOP_NASX_model.crv"
fileNameCHOPNASxCorridor = "corridors/CHOP_NASX.crv"

fileNameCHOPNASz = "6.5/6.5 Curves and Images/CHOP_NASZ_model.crv"
fileNameCHOPNASzCorridor = "corridors/CHOP_NASZ.crv"

# Do not run rotation velocity

# # This is the wrong CORRIDOR file
# fileNameRV = "6.5/6.5 Curves and Images/CHOP_ROTVELY_model.crv"
# fileNameRVCorridor = "corridors/CHOP_NASZ.crv"




print("\nNOW RUNNING TENSION TEST")
tensionTest = NCC(29.8, 98.5, 167.1, fileNameTension)
tensionTest.runTest(0.2, "tension")

print("\nNOW RUNNING COMPRESSION TEST")
compressionTest = NCC(0, 116.4, 235, fileNameCompression)
compressionTest.runTest(0.2, "compression")

print("\nNOW RUNNING FLEXION (MOMENT VS ANGLE) TEST")
flexionTest = NCC(0, 0, 0, fileNameFlexion)
flexionTest.runTest(0.2, "flexion")

print("\nNOW RUNNING EXTENSION (MOMENT VS ANGLE) TEST")
extensionTest = NCC(0, 0, 0, fileNameExtension)
extensionTest.runTest(0.2, "extension")

print("\nNOW RUNNING FLEXION (TIME VS ANGLE) TEST")
flexionAngleTest = Box([82.75, 85], [98.25, 105], fileNameFlexionAngle, type="max")
flexionAngleTest.runTest("Flexion Angle Test", "Time (ms)", "Angle (degrees)")

print("\nNOW RUNNING EXTENSION (TIME VS ANGLE) TEST")
extensionAngleTest = Box([80, -120], [140, -20], fileNameExtensionAngle, type="min")
extensionAngleTest.runTest("Extension Angle Test", "Time (ms)", "Angle (degrees)")

print("\nNOW RUNNING NBDL X TEST")
NBDLxTest = Box([100, 100], [160, 180], fileNameNBDLx, type="max")
NBDLxTest.runTest("NBDLx Test", "Time (ms)", "Angle (degrees)")

print("\nNOW RUNNING NBDL Z TEST")
NBDLzTest = Box([100, 0], [180, 60], fileNameNBDLz, type="min")
NBDLzTest.runTest("NBDLz Test", "Time (ms)", "Angle (degrees)")

print("\nNOW RUNNING HEAD LAG TEST")
NBDLHeadLagTest = NCC(0, 0, 0, fileNameNBDLHeadLag, corridor = fileNameNBDLHeadLagCorridor)
NBDLHeadLagTest.runTest(0, "headlag", title="Head Lag Test")

print("\nNOW RUNNING CHOP EAM X TEST")
CHOPEAMxTest = NCC(0, 0, 0, fileNameCHOPEAMx, corridor=fileNameCHOPEAMxCorridor)
CHOPEAMxTest.runTest(0, "eam", title="EAMX Test")

print("\nNOW RUNNING CHOP EAM Z TEST")
CHOPEAMzTest = NCC(0, 0, 0, fileNameCHOPEAMz, corridor=fileNameCHOPEAMzCorridor)
CHOPEAMzTest.runTest(0, "eam", title="EAMZ Test")

print("\nNOW RUNNING CHOP NAS X TEST")
CHOPNASxTest = NCC(0, 0, 0, fileNameCHOPNASx, corridor=fileNameCHOPNASxCorridor)
CHOPNASxTest.runTest(0, "eam", title="NASX Test")

print("\nNOW RUNNING CHOP NASZ TEST")
CHOPNASzTest = NCC(0, 0, 0, fileNameCHOPNASz, corridor=fileNameCHOPNASzCorridor)
CHOPNASzTest.runTest(0, "eam", title="NASZ Test")

# Do not run rotation velocity
# NBDLHeadLagTest = NCC(0, 0, 0, fileNameRV, corridor = fileNameRVCorridor)
# NBDLHeadLagTest.runTest(0, "rvel", title="Head Angular Velocity Test")

print("\nALL TESTS COMPLETED")