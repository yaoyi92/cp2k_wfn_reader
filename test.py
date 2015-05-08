import cp2k_wfn
wfn = cp2k_wfn.cp2k_wavefunction()
wfn.read_cp2k_wfn("H2O-RESTART.wfn")
print wfn
wfn.write_cp2k_wfn("H2O-RESTART-write.wfn")
