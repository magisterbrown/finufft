DUCC
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

.. image:: pics/perftestci_9cb19b1f-9968-421a-b521-7a3f471c35dc.png
   :alt: pics/perftestci_9cb19b1f-9968-421a-b521-7a3f471c35dc.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_843561bf-7949-4970-a98f-1311fd47618e.png
   :alt: pics/perftestci_843561bf-7949-4970-a98f-1311fd47618e.png
   :width: 100%



Type 2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:0.0001``

.. image:: pics/perftestci_d960d9f6-0bae-44b1-8214-0a9a001645c6.png
   :alt: pics/perftestci_d960d9f6-0bae-44b1-8214-0a9a001645c6.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_71470254-9212-48cd-a7dd-571d1c83f7e0.png
   :alt: pics/perftestci_71470254-9212-48cd-a7dd-571d1c83f7e0.png
   :width: 100%



Type 3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:0.0001``

.. image:: pics/perftestci_e6ea9edb-f93d-455a-86e3-5d5d20a8acb5.png
   :alt: pics/perftestci_e6ea9edb-f93d-455a-86e3-5d5d20a8acb5.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_82668286-452f-4995-a571-15dcec6effc0.png
   :alt: pics/perftestci_82668286-452f-4995-a571-15dcec6effc0.png
   :width: 100%




2D Transforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Type 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_a79afb3d-50df-4ec3-a394-5adcc82428ba.png
   :alt: pics/perftestci_a79afb3d-50df-4ec3-a394-5adcc82428ba.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_567979c7-41df-4b3f-a033-1c476b3193fb.png
   :alt: pics/perftestci_567979c7-41df-4b3f-a033-1c476b3193fb.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_ba0b2b4c-1471-4f70-b2a5-9562bf72a888.png
   :alt: pics/perftestci_ba0b2b4c-1471-4f70-b2a5-9562bf72a888.png
   :width: 100%



Type 2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_9adbed5a-af6d-4b55-bc49-5af830b801d0.png
   :alt: pics/perftestci_9adbed5a-af6d-4b55-bc49-5af830b801d0.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_f3d87268-d497-4772-b7d5-4a555ca5d53c.png
   :alt: pics/perftestci_f3d87268-d497-4772-b7d5-4a555ca5d53c.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_4e1d03ac-fc00-4329-ab26-77e83845dc6a.png
   :alt: pics/perftestci_4e1d03ac-fc00-4329-ab26-77e83845dc6a.png
   :width: 100%



Type 3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_892bd4cd-efcf-4781-91e7-4ee4910db642.png
   :alt: pics/perftestci_892bd4cd-efcf-4781-91e7-4ee4910db642.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_ef1b6fff-a7d2-4571-875a-411b6db2e75c.png
   :alt: pics/perftestci_ef1b6fff-a7d2-4571-875a-411b6db2e75c.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_43d8cd2f-0b3c-4236-bd21-505a478493bb.png
   :alt: pics/perftestci_43d8cd2f-0b3c-4236-bd21-505a478493bb.png
   :width: 100%




3D Transforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Type 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_aefc7127-6e01-4ec6-9d2d-3fdd80861316.png
   :alt: pics/perftestci_aefc7127-6e01-4ec6-9d2d-3fdd80861316.png
   :width: 100%



Type 2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_f10a6838-41d0-405a-94dc-035dbe2d3512.png
   :alt: pics/perftestci_f10a6838-41d0-405a-94dc-035dbe2d3512.png
   :width: 100%



Type 3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_a9f12303-9a05-45ab-bf13-3311de910e1b.png
   :alt: pics/perftestci_a9f12303-9a05-45ab-bf13-3311de910e1b.png
   :width: 100%



