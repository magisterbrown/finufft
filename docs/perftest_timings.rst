.. _perftest_timings:

Performance regression
========================

This page compares performance of every FINUFFT release version and latest commit on master.

The CPU used for all benchmarks below is: Intel(R) Xeon(R) CPU E5-2698 v4 @ 2.20GHz

AVX extensions present: avx, avx2.

FMA supported: yes.


1D Transforms
---------------------------------------------


Type 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:f N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:0.0001``

.. image:: pics/perftestci_0b33ac4a9176_type_3.png
   :alt: pics/perftestci_0b33ac4a9176_type_3.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_03275989fec8_type_3.png
   :alt: pics/perftestci_03275989fec8_type_3.png
   :width: 100%



Type 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:f N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:0.0001``

.. image:: pics/perftestci_0b33ac4a9176_type_2.png
   :alt: pics/perftestci_0b33ac4a9176_type_2.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_03275989fec8_type_2.png
   :alt: pics/perftestci_03275989fec8_type_2.png
   :width: 100%



Type 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:f N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:0.0001``

.. image:: pics/perftestci_0b33ac4a9176_type_1.png
   :alt: pics/perftestci_0b33ac4a9176_type_1.png
   :width: 100%


Parameters: ``prec:d N1:10000.0 N2:1 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_03275989fec8_type_1.png
   :alt: pics/perftestci_03275989fec8_type_1.png
   :width: 100%




2D Transforms
---------------------------------------------


Type 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_f74d476ec1c4_type_3.png
   :alt: pics/perftestci_f74d476ec1c4_type_3.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_6485d6e25595_type_3.png
   :alt: pics/perftestci_6485d6e25595_type_3.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_391ae776ff39_type_3.png
   :alt: pics/perftestci_391ae776ff39_type_3.png
   :width: 100%



Type 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_f74d476ec1c4_type_2.png
   :alt: pics/perftestci_f74d476ec1c4_type_2.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_6485d6e25595_type_2.png
   :alt: pics/perftestci_6485d6e25595_type_2.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_391ae776ff39_type_2.png
   :alt: pics/perftestci_391ae776ff39_type_2.png
   :width: 100%



Type 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_f74d476ec1c4_type_1.png
   :alt: pics/perftestci_f74d476ec1c4_type_1.png
   :width: 100%


Parameters: ``prec:d N1:320 N2:320 N3:1
ntransf:1 threads:1 M:10000000.0 tol:1e-09``

.. image:: pics/perftestci_6485d6e25595_type_1.png
   :alt: pics/perftestci_6485d6e25595_type_1.png
   :width: 100%


Parameters: ``prec:f N1:320 N2:320 N3:1
ntransf:1 threads:0 M:10000000.0 tol:1e-05``

.. image:: pics/perftestci_391ae776ff39_type_1.png
   :alt: pics/perftestci_391ae776ff39_type_1.png
   :width: 100%




3D Transforms
---------------------------------------------


Type 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_d0555deb358e_type_3.png
   :alt: pics/perftestci_d0555deb358e_type_3.png
   :width: 100%



Type 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_d0555deb358e_type_2.png
   :alt: pics/perftestci_d0555deb358e_type_2.png
   :width: 100%



Type 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parameters: ``prec:d N1:192 N2:192 N3:128
ntransf:1 threads:0 M:10000000.0 tol:1e-07``

.. image:: pics/perftestci_d0555deb358e_type_1.png
   :alt: pics/perftestci_d0555deb358e_type_1.png
   :width: 100%



