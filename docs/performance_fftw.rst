FFTW
---------------------------------------------

CPU name: ``Intel(R) Xeon(R) CPU E5-2698 v4 @ 2.20GHz``.

Arch: ``X86_64``.

Core count: ``20``.

ISA extensions present: ``3dnowprefetch, abm, acpi, adx, aes, aperfmperf, apic, arat, arch_perfmon, avx, avx2, bmi1, bmi2, bts, cat_l3, cdp_l3, clflush, cmov, constant_tsc, cpuid, cpuid_fault, cqm, cqm_llc, cqm_mbm_local, cqm_mbm_total, cqm_occup_llc, cx16, cx8, dca, de, ds_cpl, dtes64, dtherm, dts, epb, ept, ept_ad, erms, est, f16c, flexpriority, flush_l1d, fma, fpu, fsgsbase, fxsr, hle, ht, ibpb, ibpb_exit_to_user, ibrs, ida, intel_ppin, intel_pt, invpcid, lahf_lm, lm, mca, mce, md_clear, mmx, monitor, movbe, msr, mtrr, nonstop_tsc, nopl, nx, osxsave, pae, pat, pbe, pcid, pclmulqdq, pdcm, pdpe1gb, pebs, pge, pln, pni, popcnt, pqe, pqm, pse, pse36, pti, pts, rdrand, rdrnd, rdseed, rdt_a, rdtscp, rep_good, rtm, sdbg, sep, smap, smep, smx, ss, ssbd, sse, sse2, sse4_1, sse4_2, ssse3, stibp, syscall, tm, tm2, tpr_shadow, tsc, tsc_adjust, tsc_deadline_timer, tscdeadline, vme, vmx, vnmi, vpid, x2apic, xsave, xsaveopt, xtopology, xtpr``.

Compiler version: ``c++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0``.

Compiler flags: ``-march=native``.



1D Transforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Type 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:0.0001``

.. image:: pics/perftestci_09aa995d-b201-4851-81ad-7cb130986c1e.png
   :alt: pics/perftestci_09aa995d-b201-4851-81ad-7cb130986c1e.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_8a067a51-30c9-482e-baf3-b4a40c6b710e.png
   :alt: pics/perftestci_8a067a51-30c9-482e-baf3-b4a40c6b710e.png
   :width: 100%



Type 2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:0.0001``

.. image:: pics/perftestci_63113157-788e-4c05-a478-f1292b6cd393.png
   :alt: pics/perftestci_63113157-788e-4c05-a478-f1292b6cd393.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_2171908a-23fd-48bc-9687-2a8f70470514.png
   :alt: pics/perftestci_2171908a-23fd-48bc-9687-2a8f70470514.png
   :width: 100%



Type 3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:0.0001``

.. image:: pics/perftestci_949a92ce-a458-4844-a184-ab061407d1d9.png
   :alt: pics/perftestci_949a92ce-a458-4844-a184-ab061407d1d9.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_da59833e-726f-492f-9c96-a7046779ccc7.png
   :alt: pics/perftestci_da59833e-726f-492f-9c96-a7046779ccc7.png
   :width: 100%




2D Transforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Type 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_2e8dcf3b-d04f-4904-9db3-5d94b4a7425d.png
   :alt: pics/perftestci_2e8dcf3b-d04f-4904-9db3-5d94b4a7425d.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_7f5ddb80-d5a1-45c0-87ef-9a5ac8dafe4b.png
   :alt: pics/perftestci_7f5ddb80-d5a1-45c0-87ef-9a5ac8dafe4b.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_54f0b1da-f625-4c0a-aff3-1195d321bb78.png
   :alt: pics/perftestci_54f0b1da-f625-4c0a-aff3-1195d321bb78.png
   :width: 100%



Type 2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_862872f9-34b2-476e-91e1-2706bf4fef46.png
   :alt: pics/perftestci_862872f9-34b2-476e-91e1-2706bf4fef46.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_2b9aa7eb-272d-4911-8bd4-3ad3e89d2c88.png
   :alt: pics/perftestci_2b9aa7eb-272d-4911-8bd4-3ad3e89d2c88.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_d9ea47a7-e65f-4b26-b799-29d684fdf93c.png
   :alt: pics/perftestci_d9ea47a7-e65f-4b26-b799-29d684fdf93c.png
   :width: 100%



Type 3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_092cb482-f6ac-481e-b0e7-db7e3ade9211.png
   :alt: pics/perftestci_092cb482-f6ac-481e-b0e7-db7e3ade9211.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_9b653f79-08a2-4330-83b5-4fc57563e603.png
   :alt: pics/perftestci_9b653f79-08a2-4330-83b5-4fc57563e603.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_e8623004-a680-4b86-b80a-b8f476e6279a.png
   :alt: pics/perftestci_e8623004-a680-4b86-b80a-b8f476e6279a.png
   :width: 100%




3D Transforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Type 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_afd37061-b457-4af5-a3e6-969d87de9ccd.png
   :alt: pics/perftestci_afd37061-b457-4af5-a3e6-969d87de9ccd.png
   :width: 100%



Type 2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_59e6ee39-fe38-4af9-88f4-9af4b4e36890.png
   :alt: pics/perftestci_59e6ee39-fe38-4af9-88f4-9af4b4e36890.png
   :width: 100%



Type 3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_24f90176-12e0-435f-9ce8-19e3f6c48f49.png
   :alt: pics/perftestci_24f90176-12e0-435f-9ce8-19e3f6c48f49.png
   :width: 100%



